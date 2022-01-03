from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
from resources.CalcMaterialCost import CalcMaterialCost
from resources.CalcWorkstations import CalcWorkstations
from resources.CalcTotalsPL import CalcTotalsPL
from resources.CalcLaborCost import CalcLaborCost
from resources.CalcMarkup import CalcMarkup


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Hello, '/Hello')
api.add_resource(CalcMaterialCost, '/calcMaterialCost')
api.add_resource(CalcWorkstations, '/calcWorkstations')
api.add_resource(CalcTotalsPL, '/calcTotalsPL')
api.add_resource(CalcLaborCost, '/calcLaborCost')
api.add_resource(CalcMarkup, '/calcMarkup')
