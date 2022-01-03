from flask_restful import Resource
from flask import request
from flask import jsonify
from flask import abort
from werkzeug.exceptions import BadRequest


class CalcMarkup(Resource):
    def post(self):
    	#if not request.json or not 'wrkInvestment' in request.json:
    	if not request.json:
    		abort(400)
    	elif not 'revForecast' in request.json:
    		raise BadRequest('The parameter revForecast was not defined')
    	elif not 'matComponents' in request.json:
    		raise BadRequest('The parameter matComponents was not defined')
    	elif not 'matContractors' in request.json:
    		raise BadRequest('The parameter matContractors was not defined')    
    	elif not 'matFreightIn' in request.json:
    		raise BadRequest('The parameter matFreightIn was not defined')

    	else:
    		matComponentsData = 2500
    		matContractorsData = 1500
    		matFreightInData = 1500
    		dlProduction = 10000
    		dlLogistics = 1500


    		revForecast = request.json['revForecast']
    		matComponents = request.json['matComponents'] * matComponentsData * revForecast
    		matContractors = request.json['matContractors'] * matContractorsData * revForecast
    		matFreightIn = request.json['matFreightIn'] * matFreightInData * revForecast
    		matMuTotal = matComponents + matContractors + matFreightIn

    		dlProduction = request.json['dlProduction'] * dlProduction * revForecast
    		dlLogistics = request.json['dlLogistics'] * dlLogistics * revForecast
    		dlMuTotal = dlProduction + dlLogistics

    		idlEngineering = request.json['idlEngineering'] * (0.5 * revForecast) + (0.5 * revForecast)
    		idlProducts = request.json['idlProducts'] * (0.5 * revForecast) + (0.5 * revForecast)
    		idlLogistics = request.json['idlLogistics'] * (0.5 * revForecast) + (0.5 * revForecast)
    		idlProduction = request.json['idlProduction'] * (0.5 * revForecast) + (0.5 * revForecast)
    		idlProgramManagement = request.json['idlProgramManagement'] * (0.5 * revForecast) + (0.5 * revForecast)
    		idlQuality = request.json['idlQuality'] * (0.5 * revForecast) + (0.5 * revForecast)
    		idlFacility = request.json['idlFacility'] * (0.5 * revForecast) + (0.5 * revForecast)
    		idlRD = request.json['idlRD'] * (0.5 * revForecast) + (0.5 * revForecast)
    		idlLean = request.json['idlLean'] * (0.5 * revForecast) + (0.5 * revForecast)
    		idlFactoryGa = request.json['idlFactoryGa'] * (0.5 * revForecast) + (0.5 * revForecast)

    		idlMuTotals =  idlEngineering + idlProducts + idlLogistics + idlProduction + idlProgramManagement + idlQuality +  idlFacility + idlRD + idlLean + idlFactoryGa

    		fgaChangeInventory = request.json['fgaChangeInventory'] * revForecast
    		fgaFreightOut = request.json['fgaFreightOut'] * revForecast
    		fgaProductionSupplies = request.json['fgaProductionSupplies'] * 1 * revForecast
    		fgaUtilities = request.json['fgaUtilities'] * 0.5 * revForecast
    		fgaFuel = request.json['fgaFuel'] * 0 * revForecast
    		fgaSmallEquipment = request.json['fgaSmallEquipment'] * 1 * revForecast
    		fgaOfficeSupplies = request.json['fgaOfficeSupplies'] * 1 * revForecast
    		fgaPurchasingRebates = request.json['fgaPurchasingRebates'] * revForecast
    		fgaOutsourcing = request.json['fgaOutsourcing'] * revForecast
    		fgaLeaseTangibleAssets = request.json['fgaLeaseTangibleAssets'] * revForecast
    		fgaLeaseIntangibleAssests = request.json['fgaLeaseIntangibleAssests'] * revForecast
    		fgaBuildingRent = request.json['fgaBuildingRent'] * revForecast
    		fgaOtherRent = request.json['fgaOtherRent'] * revForecast
    		fgaEquipmentRent = request.json['fgaEquipmentRent'] * revForecast
    		fgaCarTruckRent = request.json['fgaCarTruckRent'] * revForecast
    		fgaOfficeEquipment = request.json['fgaOfficeEquipment'] * revForecast
    		fgaMaintBuilding = request.json['fgaMaintBuilding'] * revForecast
    		fgaProductionEquipment = request.json['fgaProductionEquipment'] * revForecast
    		fgaInsurance = request.json['fgaInsurance'] * 1 * revForecast
    		fgaResearchDev = request.json['fgaResearchDev'] * revForecast
    		fgaCapitalPropTax = request.json['fgaCapitalPropTax'] * revForecast
    		fgaRealEstateTax = request.json['fgaRealEstateTax'] * revForecast
    		fgaOtherProfessionalFees = request.json['fgaOtherProfessionalFees'] * 0 * revForecast
    		fgaRoyalties = request.json['fgaRoyalties']  * revForecast
    		fgaTrainingFee = request.json['fgaTrainingFee']  * revForecast
    		fgaDonations = request.json['fgaDonations']  * revForecast
    		fgaEmployeeTrans = request.json['fgaEmployeeTrans']  * revForecast
    		fgaTravelMeetings = request.json['fgaTravelMeetings'] * 0 * revForecast
    		fgaAccomodation = request.json['fgaAccomodation'] * 0 * revForecast
    		fgaCarAllowance = request.json['fgaCarAllowance'] * 0 * revForecast
    		fgaHousingAllowance = request.json['fgaHousingAllowance'] * revForecast
    		fgaMovingExpense = request.json['fgaMovingExpense'] * revForecast
    		fgaTelePost = request.json['fgaTelePost'] * 0 * revForecast
    		fgaSubscriptions = request.json['fgaSubscriptions'] * 0 * revForecast
    		fgaMuTotals = (fgaChangeInventory + fgaFreightOut + fgaProductionSupplies + fgaUtilities + fgaFuel + fgaSmallEquipment + fgaOfficeSupplies  + fgaPurchasingRebates + fgaOutsourcing  + fgaLeaseTangibleAssets + fgaLeaseIntangibleAssests + fgaBuildingRent  + fgaOtherRent  + fgaEquipmentRent + fgaCarTruckRent  +fgaOfficeEquipment  +fgaMaintBuilding +fgaProductionEquipment + fgaInsurance  +fgaResearchDev  +fgaCapitalPropTax  +fgaRealEstateTax  +fgaOtherProfessionalFees + fgaRoyalties +fgaTrainingFee +fgaDonations +fgaEmployeeTrans + fgaTravelMeetings +fgaAccomodation +fgaCarAllowance +fgaMovingExpense +fgaTelePost +fgaSubscriptions +fgaHousingAllowance)

    		cooOutsourcing = request.json['cooOutsourcing'] * revForecast
    		cooLeaseTangibleAssets = request.json['cooLeaseTangibleAssets'] * revForecast
    		cooLeaseInTangibleAssets = request.json['cooLeaseInTangibleAssets'] * revForecast
    		cooBuildingRent = request.json['cooBuildingRent'] * revForecast
    		cooOtherRentals = request.json['cooOtherRentals'] * revForecast
    		cooMaintBuilding = request.json['cooMaintBuilding'] * revForecast
    		cooCapitalPropTax = request.json['cooCapitalPropTax'] * revForecast
    		cooRealestateTax = request.json['cooRealestateTax'] * revForecast

    		cooMuTotals = cooOutsourcing + cooLeaseTangibleAssets + cooLeaseInTangibleAssets + cooBuildingRent + cooOtherRentals + cooMaintBuilding + cooCapitalPropTax + cooRealestateTax

    		coeEquipmentRent = request.json['coeEquipmentRent'] * revForecast
    		coeCarTruckRent = request.json['coeCarTruckRent'] * revForecast
    		coeOfficeEquipRent = request.json['coeOfficeEquipRent'] * revForecast
    		coeMaintProdEquip = request.json['coeMaintProdEquip'] * revForecast

    		coeMuTotals = coeEquipmentRent + coeCarTruckRent + coeOfficeEquipRent + coeMaintProdEquip

    		depAmortIntangibleAssets = request.json['depAmortIntangibleAssets'] * revForecast
    		depDepreciationTangibleAssets = request.json['depDepreciationTangibleAssets'] * revForecast
    		depCapitalLease = request.json['depCapitalLease'] * revForecast
    		depRevAmortInTangibleAsset = request.json['depRevAmortInTangibleAsset'] * revForecast
    		depRevAmortTangibleAsset = request.json['depRevAmortTangibleAsset'] * revForecast

    		depMuTotal = depAmortIntangibleAssets + depDepreciationTangibleAssets + depCapitalLease + depRevAmortInTangibleAsset + depRevAmortTangibleAsset
    		uoaMuTotal = matMuTotal + dlMuTotal	+ idlMuTotals + fgaMuTotals + cooMuTotals + coeMuTotals + depMuTotal



	    	calcMarkup = {
			 	"revForecast" : revForecast,
				"matComponents" : matComponents,
				"matContractors" : matContractors,
				"matFreightIn" : matFreightIn,
				"matMuTotal" : matMuTotal,
				"dlMuTotal" : dlMuTotal,
				"idlMuTotals" : idlMuTotals,
				"fgaMuTotals" : fgaMuTotals,
				"cooMuTotals" : cooMuTotals,
				"coeMuTotals" : coeMuTotals,
				"depMuTotal" : 	depMuTotal	
	    	}


    	return {"calcMarkup" : calcMarkup}, 201

