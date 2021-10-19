import pytest
from burgissApiWrapper.burgissApi import testApiResponses

testApiResponses = testApiResponses()
def testTokenGen():
    testApiResponses.testGetBurgissApiToken()
def testGetProfile():
    testApiResponses.testProfileRequest()
def testOptionalParameters():
    testApiResponses.testOptionalParametersRequestResponseCode('investments',
    '&includeInvestmentNotes=false&includeCommitmentHistory=false&includeInvestmentLiquidationNotes=false')
def testProfileIdAsHeader():
    testApiResponses.testProfileIdAsHeaderResponse('LookupValues')

@pytest.mark.parametrize('endpoint', testApiResponses.endpoints)
def testEndpoints(endpoint):
    """
    Test if endpoint returns a 200 status code
    """
    testApiResponses.testRequestResponseCode(endpoint)

@pytest.mark.parametrize('endpoint', testApiResponses.endpoints)
def testDataTransformation(endpoint):
    "Test if endpoint returns a flattened dataframe with length > 0"
    testApiResponses.testDataTransformation(endpoint)