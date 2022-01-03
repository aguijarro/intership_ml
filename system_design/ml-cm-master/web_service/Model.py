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


class GL:
	def __init__(self):
		#define data
		source_folder = Path("./data")
		target_folder = Path("./output")
		gl_file = 'v1_gl.csv'
		d = Directory(source_folder, target_folder, gl_file)
		self.gl = d.read_file()

	def get_data(self):
		return self.gl