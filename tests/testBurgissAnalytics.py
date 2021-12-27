
from burgissApiWrapper.burgissApi import session
import json

# Initialize session for subsequent tests
burgissSession = session()

# ==========================#
# BurgissAnalytics requests #
# ==========================#


def testAnalyticsGroupingFields():
    response = burgissSession.request(
        'analyticsGroupingFields', analyticsApi=True, profileIdAsHeader=True)
    assert response.status_code == 200


analysisParameters = {
    'userDefinedAnalysisName': 'Dingus',
    'userDefinedAnalysisID': '1',
    'calculationContext': 'Investment',
    'analysisResultType': 'individual',
    'analysisCurrency': 'Base',  # 'analysisStartDate': '2021-09-15T15:29:57.352Z',
    # 'analysisEndDate': '2021-09-15T15:29:57.352Z'
}

globalMeasureParameters = {
    "rollForward": False,
    "indexID": "string",
    "indexPremium": 0,
    "decimalPrecision": 0
}

measureStartDateReference = {
    "offset": "Years",
    "offsetPeriod": 0,
    "referenceDate": "Inception"
}

measureEndDateReference = {
    "offset": "Years",
    "offsetPeriod": 0,
    "referenceDate": "Inception"
}

# measureStartDateReference = None
# measureEndDateReference = None

measures = {  # "rollForward": False,
    # "userDefinedMeasureAlias": "string",
    "measureName": "Valuation"
    # "measureStartDate": "2021-09-15T15:29:57.352Z",
    # "measureEndDate": "2021-09-15T15:29:57.352Z",
    # "indexID": "string",
    # "indexPremium": 0,
    # "decimalPrecision": 0
}


dataCriteria = {"recordID": "9991",
                # "RecordGUID": "string",
                "recordContext": "Portfolio",
                # "selectionSet": "string",
                "excludeLiquidatedInvestments": False}

# groupBy = ['Investment.Name']
groupBy = None

# analysisJson, analysisJson2 = pointInTimeAnalyisInput(
# analysisParameters,
# globalMeasureParameters,
# measures,
# measureStartDateReference,
# measureEndDateReference,
# dataCriteria,
# groupBy
# )

analysisJson = {
    "pointInTimeAnalysis": [
        {
            "userDefinedAnalysisName": "NAVreport",
            "userDefinedAnalysisID": "NAVreport-001",
            "calculationContext": "Investment",
            "analysisResultType": "individual",
            "analysisCurrency": "Base",
            "globalMeasureProperties": {
                "rollForward": True
            },
            "measures": [
                {
                    "measureName": "Valuation"

                }

            ]
        }
    ],
    "dataCriteria": [
        {
            "recordID": "9991",
            "recordContext": "portfolio"

        }
    ]
}
print(json.dumps(analysisJson))

burgissSession = session()
burgissSession.request('analyticsGroupingFields',
                       analyticsApi=True, profileIdAsHeader=True)
boi = burgissSession.request('pointinTimeAnalysis', analyticsApi=True,
                             profileIdAsHeader=True, requestType='POST', data=json.dumps(analysisJson))

print(boi)
