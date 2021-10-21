import configparser
from datetime import datetime, timedelta


import pytest
from burgissApiWrapper.burgissApi import (init, session, tokenAuth,
                                          transformResponse)
from pandas import DataFrame


class testApiResponses():
    def __init__(self, clientId=None, username=None, password=None, urlToken=None, urlApi=None, analyticsUrlApi=None, assertionType=None, scope=None, profileIdType=None) -> None:
        self.tokenInit = tokenAuth(clientId, username, password, urlToken, urlApi, analyticsUrlApi, assertionType, scope)
        self.initSession = init(clientId, username, password, urlToken, urlApi, analyticsUrlApi, assertionType, scope)
        self.burgissSession = session(clientId, username, password, urlToken, urlApi, analyticsUrlApi, assertionType, scope, profileIdType)
        self.transformResponse = transformResponse(clientId, username, password, urlToken, urlApi, analyticsUrlApi, assertionType, scope, profileIdType)

        self.endpoints = ['orgs', 'investments', 'portfolios', 'assets', 'LookupData']

    def testGetBurgissApiToken(self):
        token = self.tokenInit.getBurgissApiToken()
        assert len(token) != 0

    def testTokenReset(self):
        tokenExpiration = self.initSession.tokenExpiration
        self.initSession.tokenExpiration = datetime.now() + timedelta(seconds=3600)
        self.initSession.checkTokenExpiration()
        assert tokenExpiration != self.initSession.tokenExpiration

    def testProfileRequest(self):
        profileResponse = self.initSession.requestWrapper('profiles')
        assert profileResponse.status_code == 200

    def testRequestResponseCode(self, endpoint):
        response = self.burgissSession.request(endpoint)
        assert response.status_code == 200

    def testOptionalParametersRequestResponseCode(self, endpoint, optionalParameters):
        response = self.burgissSession.request(
            endpoint, optionalParameters=optionalParameters)
        assert response.status_code == 200

    def testProfileIdAsHeaderResponse(self, endpoint):
        response = self.burgissSession.request(endpoint, profileIdAsHeader=True)
        assert response.status_code == 200

    def testDataTransformation(self, endpoint):
        response = self.transformResponse.getData(endpoint)
        assert isinstance(response, DataFrame) is True
        assert len(response) > 0


def pytest_addoption(parser):
    config = configparser.ConfigParser()
    try:
        config.read_file(open('config.cfg'))
    except Exception as e:
        print(e)
        config.read_file(open('configTemplate.cfg'))
    parser.addoption("--user", action="store", default=config.get('API', 'user'))
    parser.addoption("--pw", action="store", default=config.get('API', 'pw'))
    parser.addoption("--clientId", action="store", default=config.get('API', 'clientId'))
    parser.addoption("--tokenUrl", action="store", default=config.get('API', 'tokenUrl'))
    parser.addoption("--apiUrl", action="store", default=config.get('API', 'apiUrl'))
    parser.addoption("--apiUrlAnalytics", action="store", default=config.get('API', 'apiUrlAnalytics'))
    parser.addoption("--assertionType", action="store", default=config.get('API', 'assertionType'))
    parser.addoption("--scope", action="store", default=config.get('API', 'scope'))
    parser.addoption("--profileIdType", action="store", default=config.get('API', 'profileIdType'))


@pytest.fixture(scope='session')
def testApiResponsesFixture(pytestconfig):
    """

    """
    clientId = pytestconfig.getoption("clientId")
    user = pytestconfig.getoption("user")
    pw = pytestconfig.getoption("pw")
    tokenUrl = pytestconfig.getoption("tokenUrl")
    apiUrl = pytestconfig.getoption("apiUrl")
    apiUrlAnalytics = pytestconfig.getoption("apiUrlAnalytics")
    assertionType = pytestconfig.getoption("assertionType")
    scope = pytestconfig.getoption("scope")
    profileIdType = pytestconfig.getoption("profileIdType")
    test = testApiResponses(clientId, user, pw, tokenUrl, apiUrl, apiUrlAnalytics, assertionType, scope, profileIdType)

    # Session
    test.burgissSession.profileIdType = pytestconfig.getoption("profileIdType")

    return test
