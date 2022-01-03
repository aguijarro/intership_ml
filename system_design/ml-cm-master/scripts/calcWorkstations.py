import pandas as pd
import re
import sys
from pathlib import Path


class Directory:
    def __init__(self, source_folder, target_folder, equipment_file):
        self.source_folder = source_folder
        self.target_folder = target_folder
        self.equipment_file = equipment_file     
        self.output_file = None


    def __transform_data(self, amount):
	    if amount == '-':
	    	return 0
	    else:
	    	return int(amount.replace(",",""))


    def read_file(self):
        df_equipment = pd.read_csv(self.source_folder / self.equipment_file, sep=',')    
        return df_equipment


    def write_file(self, output_text, output_file):
        self.output_file = output_file
        target = Path(self.target_folder / output_text)
        self.output_file.to_csv(target)
        print("Create output file:" + output_text)



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

    arguments = sys.argv[1:]
    count = len(arguments)

    if count == 0:
        print("Add required inputs: wrkInvestment, wrkConsumables, wrkUtilities, equipment_investment,\
            equipment_useHours, equipment_useYears, labTotManuShopRate, equipment_reqStaffCnt, equipment_maintenance")
    else:
        if count != 9:
            print("Add required inputs: wrkInvestment, wrkConsumables, wrkUtilities, equipment_investment,\
            equipment_useHours, equipment_useYears, labTotManuShopRate, equipment_reqStaffCnt, equipment_maintenance")
        else:
            #Define directories

            source_folder = Path("../data")
            target_folder = Path("./output")
            equipment_file = 'equipment.csv'    


            # Read files
            d = Directory(source_folder, target_folder, equipment_file)
            equipment = d.read_file()


            wrkInvestment = float(arguments[0])
            wrkConsumables = float(arguments[1])
            wrkUtilities = float(arguments[2])
            equipment_investment = float(arguments[3])
            equipment_useHours = float(arguments[4])
            equipment_useYears = float(arguments[5])
            labTotManuShopRate = float(arguments[6])
            equipment_reqStaffCnt = float(arguments[7])
            equipment_maintenance = float(arguments[8])            


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




