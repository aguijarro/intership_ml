import pandas as pd
import re
from pathlib import Path


class Directory:
    def __init__(self, source_folder, target_folder, gl_file):
        self.source_folder = source_folder
        self.target_folder = target_folder
        self.gl_file = gl_file
        self.output_file = None


    def __transform_data(self, amount):
	    if amount == '-':
	    	return 0
	    else:
	    	return int(amount.replace(",",""))


    def read_file(self):
        df_gl = pd.read_csv(self.source_folder / self.gl_file, sep=',')
        df_gl['amount'] = df_gl.apply(lambda row: self.__transform_data(row['amount']), axis=1)   
        return df_gl


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

	return totRevenue, totMaterial, totDirectLabor, totIndirectLabor, totFga, \
		totCostOfOccupancy, totCostOfEquipment, totDepreciation, totNreRepair, \
		totStockResale, totResaleOfMerch, totSga



def main():
	#Define directories
	source_folder = Path("../data")
	target_folder = Path("./output")
	gl_file = 'gl.csv'

	# Read files
	d = Directory(source_folder, target_folder, gl_file)
	gl = d.read_file()


	totRevenue, totMaterial, totDirectLabor, totIndirectLabor, totFga, totCostOfOccupancy, \
	totCostOfEquipment, totDepreciation, totNreRepair, totStockResale, totResaleOfMerch, totSga = calcTotasPL(gl)


	print("Values")
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


if __name__ == '__main__':
	main()