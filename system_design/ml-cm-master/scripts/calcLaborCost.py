import pandas as pd
import re
import sys
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


def main():
    arguments = sys.argv[1:]
    count = len(arguments)

    if count == 0:
        print("Add required inputs: labAbsenteismCost, labProductivity, labFacUseMarkup, labFgaMarkup, totDirectLabor, totLaborRate_location, totIndirectLabor, totRevenue, totCostOfOccupancy, totFga ")
    else:
        if count != 10:
            print("Add required inputs: labAbsenteismCost, labProductivity, labFacUseMarkup, labFgaMarkup, totDirectLabor, totLaborRate_location, totIndirectLabor, totRevenue, totCostOfOccupancy, totFga ")
        else:
            #Define directories
            source_folder = Path("../data")
            target_folder = Path("./output")
            gl_file = 'gl.csv'

            # Read files
            d = Directory(source_folder, target_folder, gl_file)
            gl = d.read_file()

            gl_directlabor_logistics = float(gl[(gl['type'] == 'DIRECT LABOR') & (gl['description'] =='Logistics')]['amount'])



            labAbsenteismCost = float(arguments[0])
            labProductivity = float(arguments[1])
            labFacUseMarkup = float(arguments[2])
            labFgaMarkup = float(arguments[3])
            totDirectLabor = float(arguments[4])
            totLaborRateLocation = float(arguments[5])
            totIndirectLabor = float(arguments[6])
            totRevenue = float(arguments[7])
            totCostOfOccupancy = float(arguments[8])            
            totFga = float(arguments[9])



            labDirLabor, labAbsenteismCost, labProductivity, labDLrate, labFullLoadrate, labIndirectLabor,\
            labFacUseMarkup, labFacUse, labFgaMarkup, labFga, labTotalIDL, labTotManuShopRate = calcLaborCost(labAbsenteismCost = labAbsenteismCost, 
                                                                                       labProductivity=labProductivity, 
                                                                                       labFacUseMarkup=labFacUseMarkup, 
                                                                                       labFgaMarkup=labFgaMarkup, 
                                                                                       totDirectLabor=totDirectLabor, 
                                                                                       totLaborRateLocation=totLaborRateLocation, 
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


if __name__ == '__main__':
    main()




