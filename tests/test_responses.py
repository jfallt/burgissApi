import pytest
from burgissApiWrapper.burgissApi import (ApiConnectionError,
                                          responseCodeHandling,
                                          tokenErrorHandling,
                                          )
from requests.models import Response


def testTokenGen(testApiResponsesFixture):
    testApiResponsesFixture.testGetBurgissApiToken()


def testTokenExpiration(testApiResponsesFixture):
    testApiResponsesFixture.testTokenReset()


def testGetProfile(testApiResponsesFixture):
    testApiResponsesFixture.testProfileRequest()


def testOptionalParameters(testApiResponsesFixture):
    testApiResponsesFixture.testOptionalParametersRequestResponseCode('investments', '&includeInvestmentNotes=false&includeCommitmentHistory=false&includeInvestmentLiquidationNotes=false')


def testProfileIdAsHeader(testApiResponsesFixture):
    testApiResponsesFixture.testProfileIdAsHeaderResponse('LookupValues')


endpoints = ['orgs', 'investments', 'portfolios', 'assets', 'LookupData']


@pytest.mark.parametrize('endpoint', endpoints)
def testEndpoints(endpoint, testApiResponsesFixture):
    """
    Test if endpoint returns a 200 status code
    """
    testApiResponsesFixture.testRequestResponseCode(endpoint)


@pytest.mark.parametrize('endpoint', endpoints)
def testDataTransformation(endpoint, testApiResponsesFixture):
    "Test if endpoint returns a flattened dataframe with length > 0"
    testApiResponsesFixture.testDataTransformation(endpoint)


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
