from flask_restful import Resource
from flask import request
from flask import jsonify
from flask import abort
from werkzeug.exceptions import BadRequest

class CalcMaterialCost(Resource):
    def get(self):
        return {"message": "Hello, World!"}

    def post(self):
        print(request.json)
        if not request.json:
            abort(400)
        elif not "matBomValue" in request.json:
            raise BadRequest("The parameter matBomValue was not defined")
        elif not 'matScrap' in request.json:
            raise BadRequest('The parameter matScrap was not defined')
        elif not 'matCostOfMoney' in request.json:
            raise BadRequest('The parameter matCostOfMoney was not defined')
        elif not 'matFgaMarkup' in request.json:
            raise BadRequest('The parameter matFgaMarkup was not defined')
        elif not 'matFacUseMarkup' in request.json:
            raise BadRequest('The parameter matFacUseMarkup was not defined')


        gl_directlabor_logistics = 1574010.0
        gl_indirectlabor_logistics = 2376541.0
        totMaterial = 85236479.0
        totFGA = 2007831.0
        totCostOfOccupancy = 1608384.0
        totRevenue = 77487708.0                

        matBomValue = request.json['matBomValue']
        matScrap = request.json['matScrap']
        matCostOfMoney = request.json['matCostOfMoney']
        matHandling = (gl_indirectlabor_logistics/totRevenue) + (gl_directlabor_logistics/totRevenue) / (totMaterial/totRevenue)
        matFgaMarkup =request.json['matFgaMarkup']
        matFga = (totFGA/totRevenue) * (totFGA/totRevenue)
        matFacUseMarkup = request.json['matFacUseMarkup']
        matFacUse = matFacUseMarkup * (totCostOfOccupancy/totRevenue)
        matTotalCost = (matBomValue*matScrap)+(matBomValue*matCostOfMoney)+(matBomValue*matHandling)+(matBomValue*matFacUse)
        matTotalRate = (matTotalCost-matBomValue)/matBomValue           

        calcMaterialCosts = {
            "matBomValue" : matBomValue,
            "matScrapn" : matScrap,
            "matCostOfMoney" : matCostOfMoney,
            "matHandling" : matHandling,
            "matFgaMarkup" : matFgaMarkup,
            "matFga" : matFga,
            "matFacUseMarkup" : matFacUseMarkup,
            "matFacUse" : matFacUse,
            "matTotalCost" : matTotalCost,
            "matTotalRate" : matTotalRate          
        }
        return {"calcWorkstations" : calcMaterialCosts}, 201
