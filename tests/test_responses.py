import pytest
from burgissApiWrapper.burgissApi import (ApiConnectionError,
                                          responseCodeHandling,
                                          testApiResponses, tokenErrorHandling)
from requests.models import Response

testApiResponses = testApiResponses()


def testTokenGen():
    testApiResponses.testGetBurgissApiToken()

def testTokenExpiration():
    testApiResponses.testTokenReset()

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

# Test token response handling
validTokenExample = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'

exampleTokenResponse = [
    {'error': 'invalid_scope'},
    {'status_code': 500},
    {'some_other_key': 'data'}
]

def testTokenResponse():
    assert tokenErrorHandling({'access_token': validTokenExample}) == validTokenExample

@pytest.mark.parametrize('tokenResponseJson', exampleTokenResponse)
def testTokenExceptions(tokenResponseJson):
    with pytest.raises(ApiConnectionError):
        tokenErrorHandling(tokenResponseJson)

responseCodes = [400, 401, 404, 500, 503]

@pytest.mark.parametrize('responseCode', responseCodes)
def testResponseErrorHandling(responseCode):
    response = Response()
    response.status_code = responseCode
    with pytest.raises(ApiConnectionError):
        responseCodeHandling(response)
