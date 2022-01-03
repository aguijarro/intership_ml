import pandas as pd
import re
from pathlib import Path


class Directory:
    def __init__(self, source_folder, target_folder, gl_file, employees_file, equipment_file):
        self.source_folder = source_folder
        self.target_folder = target_folder
        self.gl_file = gl_file
        self.employees_file = employees_file   
        self.equipment_file = equipment_file     
        self.output_file = None


    def __transform_data(self, amount):
	    if amount == '-':
	    	return 0
	    else:
	    	return int(amount.replace(",",""))


    def read_file(self):
        df_gl = pd.read_csv(self.source_folder / self.gl_file, sep=',')
        df_gl['amount'] = df_gl.apply(lambda row: self.__transform_data(row['amount']), axis=1)   
        df_employees = pd.read_csv(self.source_folder / self.employees_file, sep=',')
        df_equipment = pd.read_csv(self.source_folder / self.equipment_file, sep=',')    
        return df_gl, df_employees, df_equipment


    def write_file(self, output_text, output_file):
        self.output_file = output_file
        target = Path(self.target_folder / output_text)
        self.output_file.to_csv(target)
        print("Create output file:" + output_text)


def calcTotasPL(gl):
	totRevenue = gl['amount'][gl['type'] == 'REVENUE'].sum()
	totMaterial = gl['amount'][gl['type'] == 'MATERIAL'].sum() 
	totDirectLabor = gl['amount'][gl['type'] == 'DIRECT LABOR'].sum() 
	totIndirectLabor = gl['amount'][gl['type'] == 'INDIRECT LABOR'].sum() 
	totFga = gl['amount'][gl['type'] == 'FGA'].sum() 
	totCostOfOccupancy = gl['amount'][gl['type'] == 'COST OF OCCUPANCY'].sum() 
	totCostOfEquipment = gl['amount'][gl['type'] == 'COST OF EQUIPMENT'].sum() 
	totDepreciation = gl['amount'][gl['type'] == 'DEPRECIATION'].sum() 
	totNreRepair = gl['amount'][gl['type'] == 'NRE REPAIR'].sum() 
	totStockResale = gl['amount'][gl['type'] == 'STOCK RESALE'].sum() 
	totResaleOfMerch = gl['amount'][gl['type'] == 'RESALE OF MERCHANDISE'].sum() 
	totSga = gl['amount'][gl['type'] == 'SGA'].sum() 

	#tot = gl[gl["type"] == 'REVENUE'].groupby("type", as_index=False).agg({"amount": "sum"})

	return totRevenue, totMaterial, totDirectLabor, totIndirectLabor, totFga, \
		totCostOfOccupancy, totCostOfEquipment, totDepreciation, totNreRepair, \
		totStockResale, totResaleOfMerch, totSga


def calcTotals(employees):
	total = sum(employees['rateAvg'])
	employess_group = employees.groupby('country', as_index=False).agg({"lastName": "count"})
	employess_group.rename(columns={"lastName" : "Count"}, inplace=True)
	employess_group['totLaborRate_location'] = total / employess_group['Count']
	return employess_group
	

def calcMaterialCost(matBomValue, matScrap, matCostOfMoney, matFgaMarkup, 
					  matFacUseMarkup, gl_directlabor_logistics, 
					  gl_material_logistics, totMaterial, totFGA,
					  totCostOfOccupancy):
	matBomValue = matBomValue
	matScrap = matScrap
	matCostOfMoney = matCostOfMoney
	matHandling = (gl_directlabor_logistics + gl_material_logistics)/totMaterial
	matFgaMarkup = matFgaMarkup
	matFga = matFgaMarkup * totFGA 
	matFacUseMarkup = matFacUseMarkup
	matFacUse = matFacUseMarkup * totCostOfOccupancy
	matTotalCost = (matBomValue*matScrap)+(matBomValue*matCostOfMoney)+(matBomValue*matHandling)+(matBomValue*matFacUse)
	matTotalRate = (matTotalCost-matBomValue/matBomValue)

	return matBomValue, matScrap, matCostOfMoney, matHandling, matFgaMarkup, matFga,\
	matFacUseMarkup, matFacUse, matTotalCost, matTotalRate

def calcLaborCost(labAbsenteismCost, labProductivity, labFacUseMarkup, 
				   labFgaMarkup, totDirectLabor, totLaborRateLocation, 
				   totIndirectLabor, totRevenue, gl_directlabor_logistics, 
				   totCostOfOccupancy, totFga):
	labDirLabor = totDirectLabor / totRevenue
	labAbsenteismCost = labAbsenteismCost
	labProductivity = labProductivity
	labDLrate = totLaborRateLocation * (1 + 0.03)
	labFullLoadrate = (labDLrate * (1+labAbsenteismCost))*(1+(1-labProductivity))
	labIndirectLabor = (totIndirectLabor / totRevenue)-(gl_directlabor_logistics/totRevenue)
	labFacUseMarkup = labFacUseMarkup
	labFacUse = labFacUseMarkup * (totCostOfOccupancy / totRevenue)
	labFgaMarkup = labFgaMarkup
	labFga = labFgaMarkup * totFga / totRevenue 
	labTotalIDL = labFga+labFacUse+labIndirectLabor
	labTotManuShopRate = (labTotalIDL / labDirLabor+1)*labFullLoadrate

	return labDirLabor, labAbsenteismCost, labProductivity, labDLrate, labFullLoadrate, \
		   labIndirectLabor, labFacUseMarkup, labFacUse, labFgaMarkup, labFga, labTotalIDL, labTotManuShopRate
 

def calcWorkstations(wrkInvestment, wrkConsumables, wrkUtilities, 
	equipment_investment, equipment_useHours, equipment_useYears,
	labTotManuShopRate, equipment_reqStaffCnt,equipment_maintenance):
	wrkInvestment = wrkInvestment
	wrkDepreciation = equipment_investment/equipment_useHours/equipment_useYears
	wrkShpRate = labTotManuShopRate * 1 * equipment_reqStaffCnt
	wrkConsumables = wrkConsumables
	wrkUtilities = wrkUtilities
	wrkMaintenance = wrkDepreciation * equipment_maintenance #revisar
	wrkTotRate = wrkDepreciation + wrkShpRate + wrkConsumables + wrkUtilities + wrkMaintenance
	return wrkInvestment, wrkDepreciation, wrkShpRate, wrkConsumables, wrkUtilities, wrkMaintenance, wrkTotRate


def main():
	#Define directories
	source_folder = Path("./data")
	target_folder = Path("./output")
	gl_file = 'gl.csv'
	employees_file = 'employees.csv'
	equipment_file = 'equipment.csv'	


	# Read files
	d = Directory(source_folder, target_folder, gl_file, employees_file, equipment_file)
	gl, employees, equipment = d.read_file()



	totRevenue, totMaterial, totDirectLabor, totIndirectLabor, totFga, totCostOfOccupancy, \
	totCostOfEquipment, totDepreciation, totNreRepair, totStockResale, totResaleOfMerch, totSga = calcTotasPL(gl)



	print("Values calcTotasPL")
	print("totRevenue", totRevenue)
	print("totMaterial", totMaterial)
	print("totDirectLabor", totDirectLabor)
	print("totIndirectLabor", totIndirectLabor)
	print("totFga", totFga)
	print("totCostOfOccupancy", totCostOfOccupancy)
	print("totCostOfEquipment", totCostOfEquipment)
	print("totDepreciation", totDepreciation)
	print("totNreRepair", totNreRepair)
	print("totStockResale", totStockResale) 	
	print("totResaleOfMerch", totResaleOfMerch)
	print("totSga", totSga)


	totLaborRate_location_df = calcTotals(employees)
	totLaborRate_location = float(totLaborRate_location_df[(totLaborRate_location_df['country'] == 'CHINA')]['totLaborRate_location'])
	print("Labor Rate")
	print(totLaborRate_location)


	gl_directlabor_logistics = float(gl[(gl['type'] == 'DIRECT LABOR') & (gl['description'] =='Logistics')]['amount'])
	gl_material_logistics = float(gl[(gl['type'] == 'MATERIAL') & (gl['description'] =='Logistics')]['amount'])

	matBomValue, matScrap, matCostOfMoney, matHandling, matFgaMarkup, matFga, \
	matFacUseMarkup, matFacUse, matTotalCost, matTotalRate = calcMaterialCost(matBomValue=100, 
																				matScrap=0.5, 
																				matCostOfMoney=0.5, 
																				matFgaMarkup=0.5, 
																				matFacUseMarkup=0.5, 
																				gl_directlabor_logistics = gl_directlabor_logistics,
																				gl_material_logistics=gl_material_logistics,
																				totMaterial = totMaterial,
																				totFGA = totFga,
																				totCostOfOccupancy = totCostOfOccupancy 
																				)

	print("Values calcMaterialCost")
	print("matBomValue",matBomValue)
	print("matScrap",matScrap)
	print("matCostOfMoney",matCostOfMoney)
	print("matHandling",matHandling)
	print("matFgaMarkup",matFgaMarkup)
	print("matFga",matFga)
	print("matFacUseMarkup",matFacUseMarkup)
	print("matFacUse",matFacUse)
	print("matTotalCost",matTotalCost)
	print("matTotalRate",matTotalRate) 


	labDirLabor, labAbsenteismCost, labProductivity, labDLrate, labFullLoadrate, labIndirectLabor,\
	labFacUseMarkup, labFacUse, labFgaMarkup, labFga, labTotalIDL, labTotManuShopRate = calcLaborCost(labAbsenteismCost = 0.01, 
																			   labProductivity=0.1, 
																			   labFacUseMarkup=0.5, 
																			   labFgaMarkup=0.5, 
																			   totDirectLabor=totDirectLabor, 
																			   totLaborRateLocation=totLaborRate_location, 
																			   totIndirectLabor=totIndirectLabor, 
																			   totRevenue=totRevenue, 
																			   gl_directlabor_logistics=gl_directlabor_logistics, 
																			   totCostOfOccupancy=totCostOfOccupancy, 
																			   totFga=totFga 
																			)

	print("Values calcLaborCost")

	print("labDirLabor",labDirLabor)
	print("labAbsenteismCost",labAbsenteismCost)
	print("labProductivity",labProductivity)
	print("labDLrate",labDLrate)
	print("labFullLoadrate",labFullLoadrate)
	print("labIndirectLabor",labIndirectLabor)
	print("labFacUseMarkup",labFacUseMarkup)
	print("labFacUse",labFacUse)
	print("labFgaMarkups",labFgaMarkup)
	print("labFga",labFga) 
	print("labTotalIDL",labTotalIDL)
	print("labTotManuShopRate",labTotManuShopRate)




	gl_directlabor_logistics = float(gl[(gl['type'] == 'DIRECT LABOR') & (gl['description'] =='Logistics')]['amount'])
	gl_material_logistics = float(gl[(gl['type'] == 'MATERIAL') & (gl['description'] =='Logistics')]['amount'])

	wrkInvestment, wrkDepreciation, wrkShpRate, \
	wrkConsumables, wrkUtilities, wrkMaintenance, wrkTotRate = calcWorkstations(wrkInvestment = 1500000,
																				wrkConsumables = 0,
																				wrkUtilities = 0,
																				equipment_investment = 1500000, 
																				equipment_useHours = 4000,
																				equipment_useYears = 5,
																				labTotManuShopRate = labTotManuShopRate,
																			    equipment_reqStaffCnt = 3,
																				equipment_maintenance = 1
																				)


	print("Values calcWorkstations")

	print("wrkInvestment",wrkInvestment)
	print("wrkDepreciation",wrkDepreciation)
	print("wrkShpRate",wrkShpRate)
	print("wrkConsumables",wrkConsumables)
	print("wrkUtilities",wrkUtilities)
	print("wrkMaintenance",wrkMaintenance)
	print("wrkTotRate",wrkTotRate)



if __name__ == '__main__':
	main()




