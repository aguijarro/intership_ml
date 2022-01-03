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


def calcMaterialCost(matBomValue, matScrap, matCostOfMoney, matFgaMarkup, 
                      matFacUseMarkup, gl_directlabor_logistics, 
                      gl_indirectlabor_logistics, totMaterial, totFGA,
                      totCostOfOccupancy, totRevenue):


    print("Material Cost Inputs")
    print("-----------------------")       
    print("matBomValue", matBomValue)
    print("matScrap",matScrap )
    print("matCostOfMoney",matCostOfMoney) 
    print("matFgaMarkup", matFgaMarkup)
    print("matFacUseMarkup",matFacUseMarkup) 
    print("gl_directlabor_logistics",gl_directlabor_logistics) 
   # print("gl_material_logistics", gl_material_logistics)
    print("gl_indirectlabor_logistics", gl_indirectlabor_logistics)
    print("totMaterial", totMaterial)
    print("totFGA",totFGA)
    print("totCostOfOccupancy",totCostOfOccupancy) 
    print("totRevenue",totRevenue)


    matBomValue = matBomValue
    matScrap = matScrap
    matCostOfMoney = matCostOfMoney
    #matHandling = (gl_directlabor_logistics/totRevenue) + (gl_material_logistics/totRevenue) / (totMaterial/totRevenue) #(gl_directlabor_logistics + gl_material_logistics)/totMaterial

    print("gl_directlabor_logistics: ", gl_directlabor_logistics, "totRevenue:", totRevenue, "gl_indirectlabor_logistics: ",gl_indirectlabor_logistics, "totMaterial: ", totMaterial )
    matHandling = (gl_indirectlabor_logistics/totRevenue) + (gl_directlabor_logistics/totRevenue) / (totMaterial/totRevenue) #(gl_directlabor_logistics + gl_material_logistics)/totMaterial
    matFgaMarkup = matFgaMarkup
    matFga = (totFGA/totRevenue) * (totFGA/totRevenue)  #matFgaMarkup * totFGA 
    #matFga = (matFgaMarkup/totRevenue) * totFGA #matFgaMarkup * totFGA 
    matFacUseMarkup = matFacUseMarkup
    matFacUse = matFacUseMarkup * (totCostOfOccupancy/totRevenue)
    #matFacUse = matFacUseMarkup * totCostOfOccupancy    
    matTotalCost = (matBomValue*matScrap)+(matBomValue*matCostOfMoney)+(matBomValue*matHandling)+(matBomValue*matFacUse)
    matTotalRate = (matTotalCost-matBomValue)/matBomValue

    return matBomValue, matScrap, matCostOfMoney, matHandling, matFgaMarkup, matFga,\
    matFacUseMarkup, matFacUse, matTotalCost, matTotalRate


def main():
    arguments = sys.argv[1:]
    count = len(arguments)

    if count == 0:
        print("Add required inputs: matBomValue, matScrap, matCostOfMoney, matFgaMarkup, matFacUseMarkup, totMaterial, totFGA, totCostOfOccupancy, totRevenue")
    else:
        if count != 9:
            print("Add required inputs: matBomValue, matScrap, matCostOfMoney, matFgaMarkup, matFacUseMarkup, totMaterial, totFGA, totCostOfOccupancy, , totRevenue")
        else:
            #Define directories
            source_folder = Path("../data")
            target_folder = Path("./output")
            gl_file = 'v1_gl.csv'
          
            # Read files
            d = Directory(source_folder, target_folder, gl_file)
            gl = d.read_file()


            gl_directlabor_logistics = float(gl[(gl['type'] == 'DIRECT LABOR') & (gl['description'] =='Logistics')]['amount'])
            #gl_material_logistics = float(gl[(gl['type'] == 'MATERIAL') & (gl['description'] =='Logistics')]['amount'])
            gl_indirectlabor_logistics = float(gl[(gl['type'] == 'INDIRECT LABOR') & (gl['description'] =='Logistics')]['amount'])

            matBomValue = float(arguments[0])
            matScrap = float(arguments[1])
            matCostOfMoney = float(arguments[2])
            matFgaMarkup = float(arguments[3])
            matFacUseMarkup = float(arguments[4])
            totMaterial = float(arguments[5])
            totFga = float(arguments[6])
            totCostOfOccupancy = float(arguments[7])
            totRevenue = float(arguments[8])

            matBomValue, matScrap, matCostOfMoney, matHandling, matFgaMarkup, matFga, \
            matFacUseMarkup, matFacUse, matTotalCost, matTotalRate = calcMaterialCost(matBomValue=matBomValue, 
                                                                                        matScrap=matScrap, 
                                                                                        matCostOfMoney=matCostOfMoney, 
                                                                                        matFgaMarkup=matFgaMarkup, 
                                                                                        matFacUseMarkup=matFacUseMarkup, 
                                                                                        gl_directlabor_logistics = gl_directlabor_logistics,
                                                                                        #gl_material_logistics=gl_material_logistics,
                                                                                        gl_indirectlabor_logistics = gl_indirectlabor_logistics,
                                                                                        totMaterial = totMaterial,
                                                                                        totFGA = totFga,
                                                                                        totCostOfOccupancy = totCostOfOccupancy,
                                                                                        totRevenue = totRevenue 
                                                                                        )




            print("Values calcMaterialCost")
            print("-----------------------")            
            #print("matBomValue",matBomValue)
            #print("matScrap",matScrap)
            #print("matCostOfMoney",matCostOfMoney)
            print("matHandling", round(matHandling,4))
            #print("matFgaMarkup",matFgaMarkup)
            print("matFga", round(matFga*100,2))
            #print("matFacUseMarkup",matFacUseMarkup)
            print("matFacUse", round(matFacUse,3))
            print("matTotalCost", round(matTotalCost,2))
            print("matTotalRate", round(matTotalRate,3)) 



if __name__ == '__main__':
    main()


