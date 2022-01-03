Readme

Test cases:

Script 1: python calcTotalsPL.py

Script 2: python calcTotalsPL.py -> China

Script 3: python calcMaterialCost.py 100 0.5 0.5 0.5 0.5 10853674 1462167 599540

Script 4: python calcLaborCost.py 0.01 0.1 0.5 0.5 10072908 89.4 1825299 77487708 599540 1462167

Script 5: python calcWorkstations.py 1500000 0 0 1500000 4000 5 188.91 3 1


Web Service - Test cases:

End Point: '/calcTotalsPL'

{
    "totRevenue": 77487708
}

End Point: '/calcMaterialCost'

{
    "matBomValue": 100.0,
    "matScrap": 0.5,
    "matCostOfMoney": 0.5,
    "matFgaMarkup": 0.5,
    "matFacUseMarkup": 0.5,
    "gl_directlabor_logistics": 1574010.0,
    "gl_indirectlabor_logistics": 2376541.0,
    "totMaterial": 85236479.0,
    "totFGA": 2007831.0,
    "totCostOfOccupancy": 1608384.0,
    "totRevenue": 77487708.0        
}

End Point: '/calcWorkstations'

{
"wrkInvestment": 1500000,
"wrkConsumables": 0,
"wrkUtilities": 0
}


End Point: '/calcLaborCost'

{
"labAbsenteismCost": 0.01,
"labProductivity": 0.1,
"labFacUseMarkup": 0.5,
"labFgaMarkup": 0.5
}