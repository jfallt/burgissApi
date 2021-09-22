
from burgissApi.burgissApi import burgissApiSession,  pointInTimeAnalyisInput
import pytest

import os
os.chdir("..")

# Initialize session for subsequent tests
burgissSession = burgissApiSession()

#===========================#
# BurgissAnalytics requests #
#===========================#
def testAnalyticsGroupingFields():
    response = burgissSession.request(
        'analyticsGroupingFields', analyticsApi=True, profileIdAsHeader=True)
    assert response.status_code == 200


analysisParameters = {
    'userDefinedAnalysisName': 'Adjusted Ending Value',
    'userDefinedAnalysisID': '1',
    'analysisResultType': 'Pooled',
    'calculationContext': 'default_value3',
    'analysisCurrency': 'local',
    'analysisStartDate': 'default_value3',
    'analysisEndDate': 'default_value3'
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

measures = {"rollForward": False,
            "userDefinedMeasureAlias": "string",
            "measureName": "IRR",
            "measureStartDate": "2021-09-15T15:29:57.352Z",
            "measureEndDate": "2021-09-15T15:29:57.352Z",
            "indexID": "string",
            "indexPremium": 0,
            "decimalPrecision": 0
            }


dataCriteria = {"recordID": "string",
                "RecordGUID": "string",
                "recordContext": "investment",
                "selectionSet": "string",
                "excludeLiquidatedInvestments": False}

groupBy = ['Investment.Name']

analysisJson = pointInTimeAnalyisInput(analysisParameters, globalMeasureParameters,
                                      measures, measureStartDateReference, measureEndDateReference, dataCriteria, groupBy)

burgissSession = burgissApiSession()
burgissSession.request('analyticsGroupingFields',
                       analyticsApi=True, profileIdAsHeader=True)
burgissSession.request('pointinTimeAnalysis', analyticsApi=True,
                       profileIdAsHeader=True, requestType='POST', data=analysisJson)
