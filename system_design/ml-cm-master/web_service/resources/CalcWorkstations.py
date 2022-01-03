from flask_restful import Resource
from flask import request
from flask import jsonify
from flask import abort
from werkzeug.exceptions import BadRequest



class CalcWorkstations(Resource):
    def get(self):
        return {"message": "Hello, World!"}

    def post(self):
    	#if not request.json or not 'wrkInvestment' in request.json:
    	if not request.json:
    		abort(400)
    	elif not 'wrkInvestment' in request.json:
    		raise BadRequest('The parameter wrkInvestment was not defined')
    	elif not 'wrkConsumables' in request.json:
    		raise BadRequest('The parameter wrkConsumables was not defined')
    	elif not 'wrkUtilities' in request.json:
    		raise BadRequest('The parameter wrkUtilities was not defined')    		    		

    	equipment_investment = 1500000
    	equipment_useHours = 4000
    	equipment_useYears = 5
    	equipment_reqStaffCnt = 3
    	labTotManuShopRate = 188.91
    	equipment_maintenance = 1

    	wrkInvestment = request.json['wrkInvestment']
    	wrkDepreciation = equipment_investment/equipment_useHours/equipment_useYears
    	wrkShpRate = labTotManuShopRate * 1 * equipment_reqStaffCnt
    	wrkConsumables = request.json['wrkConsumables']
    	wrkUtilities = request.json['wrkUtilities']
    	wrkMaintenance = wrkDepreciation * equipment_maintenance #revisar
    	wrkTotRate = wrkDepreciation + wrkShpRate + wrkConsumables + wrkUtilities + wrkMaintenance    		

    	calcWorkstations = {
		 	"wrkInvestment" : wrkInvestment,
			"wrkDepreciation" : wrkDepreciation,
			"wrkShpRate" : wrkShpRate,
			"wrkConsumables" : wrkConsumables,
			"wrkUtilities" : wrkUtilities,
			"wrkMaintenance" : wrkMaintenance,
			"wrkTotRate" : wrkTotRate
    	}

    	print(calcWorkstations)

    	return {"calcWorkstations" : calcWorkstations}, 201

