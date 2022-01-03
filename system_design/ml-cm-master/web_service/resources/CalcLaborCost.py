from flask_restful import Resource
from flask import request
from flask import jsonify
from flask import abort
from werkzeug.exceptions import BadRequest

class CalcLaborCost(Resource):
    def get(self):
        return {"message": "Hello, World!"}

    def post(self):
    	#if not request.json or not 'wrkInvestment' in request.json:
    	if not request.json:
    		abort(400)
    	elif not 'labAbsenteismCost' in request.json:
    		raise BadRequest('The parameter labAbsenteismCost was not defined')
    	elif not 'labProductivity' in request.json:
    		raise BadRequest('The parameter labProductivity was not defined')
    	elif not 'labFacUseMarkup' in request.json:
    		raise BadRequest('The parameter labFacUseMarkup was not defined')    
    	elif not 'labFgaMarkup' in request.json:
    		raise BadRequest('The parameter labFgaMarkup was not defined')    				    		

    	totDirectLabor = 1500000
    	totRevenue = 4000
    	totLaborRateLocation = 5
    	totIndirectLabor = 3
    	gl_directlabor_logistics = 188.91
    	totCostOfOccupancy = 1
    	totFga = 8

    	labDirLabor = totDirectLabor / totRevenue
    	labAbsenteismCost = request.json['labAbsenteismCost']
    	labProductivity = request.json['labProductivity']
    	labDLrate = totLaborRateLocation * (1 + 0.03)
    	labFullLoadrate = (labDLrate * (1+labAbsenteismCost))*(1+(1-labProductivity))
    	labIndirectLabor = (totIndirectLabor / totRevenue)-(gl_directlabor_logistics/totRevenue)
    	labFacUseMarkup = request.json['labFacUseMarkup']
    	labFacUse = labFacUseMarkup * (totCostOfOccupancy / totRevenue)
    	labFgaMarkup = request.json['labFgaMarkup']
    	labFga = labFgaMarkup * totFga / totRevenue
    	labTotalIDL = labFga+labFacUse+labIndirectLabor
    	labTotManuShopRate = (labTotalIDL / labDirLabor+1)*labFullLoadrate    	

 		

    	calcLaborCost = {
		 	"labDirLabor" : labDirLabor,
			"labAbsenteismCost" : labAbsenteismCost,
			"labProductivity" : labProductivity,
			"labDLrate" : labDLrate,
			"labFullLoadrate" : labFullLoadrate,
			"labIndirectLabor" : labIndirectLabor,
			"labFacUseMarkup" : labFacUseMarkup,
			"labFacUse" : labFacUse,
			"labFgaMarkup" : labFgaMarkup,
			"labFga" : labFga,
			"labTotalIDL" : labTotalIDL,	
			"labTotManuShopRate" : labTotManuShopRate					
    	}


    	return {"calcLaborCost" : calcLaborCost}, 201

