from flask_restful import Resource
from flask import request
from flask import abort
from flask import jsonify

from werkzeug.exceptions import BadRequest

from Model import GL


class CalcTotalsPL(Resource):
	def post(self):
		if not request.json:
			abort(400)

		if not 'totRevenue' in request.json:
			# get all the data from dataset
			print("if")
			glObj = GL()
			gl = glObj.get_data()

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


		else:
			# get data from dataset execept totRevenue
			print("else")
			glObj = GL()
			gl = glObj.get_data()
			
			totRevenue = request.json['totRevenue']
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


		CalcTotalsPL = {
            "totRevenue" : totRevenue,
            "totMaterial" : str(totMaterial),
            "totDirectLabor" : str(totDirectLabor),
            "totIndirectLabor" : str(totIndirectLabor),
            "totFga" : str(totFga),
            "totCostOfOccupancy" : str(totCostOfOccupancy),
            "totCostOfEquipment" : str(totCostOfEquipment),
            "totDepreciation" : str(totDepreciation),
            "totNreRepair" : str(totNreRepair),
            "totStockResale" : str(totStockResale),
            "totResaleOfMerch" : str(totResaleOfMerch),
            "totSga" : str(totSga)      
            }

		return {"CalcTotalsPL" : CalcTotalsPL},201




