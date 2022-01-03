import pandas as pd
import re
from pathlib import Path


class Directory:
    def __init__(self, source_folder, target_folder, employees_file):
        self.source_folder = source_folder
        self.target_folder = target_folder
        self.employees_file = employees_file   
        self.output_file = None


    def __transform_data(self, amount):
	    if amount == '-':
	    	return 0
	    else:
	    	return int(amount.replace(",",""))


    def read_file(self):
        df_employees = pd.read_csv(self.source_folder / self.employees_file, sep=',')
        return df_employees


    def write_file(self, output_text, output_file):
        self.output_file = output_file
        target = Path(self.target_folder / output_text)
        self.output_file.to_csv(target)
        print("Create output file:" + output_text)



def calcTotals(employees):
	total = sum(employees['rateAvg'])
	employess_group = employees.groupby('country', as_index=False).agg({"lastName": "count"})
	employess_group.rename(columns={"lastName" : "Count"}, inplace=True)
	employess_group['totLaborRate_location'] = total / employess_group['Count']
	return employess_group



def main():
	#Define directories
	source_folder = Path("../data")
	target_folder = Path("./output")
	gl_file = 'gl.csv'
	employees_file = 'employees.csv'
	equipment_file = 'equipment.csv'	


	# Read files
	d = Directory(source_folder, target_folder, employees_file)
	employees = d.read_file()
	totLaborRate_location_df = calcTotals(employees)


	count = 0

	while count == 0:
		country = str(input("Input a country name: ")) 
		result = totLaborRate_location_df[(totLaborRate_location_df['country'] == country.upper())]['totLaborRate_location']

		if not result.empty:
			totLaborRate_location = float(totLaborRate_location_df[(totLaborRate_location_df['country'] == country.upper())]['totLaborRate_location'])
			print("Labor Rate")
			print(totLaborRate_location)
			count = 1

	
if __name__ == '__main__':
	main()