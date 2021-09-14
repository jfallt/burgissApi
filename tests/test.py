
from burgissApi import burgissApiSession, burgissApiInit, burgissApiAuth, ApiConnectionError
import pytest


#=======================#
# Test token gen        #
#=======================#
def testGetBurgissApiToken():
    tokenInit = burgissApiAuth()
    token = tokenInit.getBurgissApiToken()
    assert len(token) != 0

#=======================#
# Test requests         #
#=======================#


def testProfileRequest():
    session = burgissApiInit()
    profileResponse = session.request('profiles')
    assert profileResponse.status_code == 200


# Initialize session for subsequent tests
burgissSession = burgissApiSession()


def testOrgRequest():
    response = burgissSession.request('orgs')
    assert response.status_code == 200


def testInvestmentsRequest():
    response = burgissSession.request('investments')
    assert response.status_code == 200


def testOptionalParameters():
    response = burgissSession.request(
        'investments', optionalParameters='&includeInvestmentNotes=false&includeCommitmentHistory=false&includeInvestmentLiquidationNotes=false')
    assert response.status_code == 200


def testPortfolioRequest():
    response = burgissSession.request('portfolios')
    assert response.status_code == 200


def testLookupData():
    response = burgissSession.request('LookupData')
    assert response.status_code == 200


def testLookupValues():
    response = burgissSession.request('LookupValues', profileIdAsHeader=True)
    assert response.status_code == 200


def testInvalidUrl():
    with pytest.raises(ApiConnectionError):
        burgissSession.request('fakeUrl')


#===========================#
# BurgissAnalytics requests #
#===========================#
def testAnalyticsGroupingFields():
    response = burgissSession.request(
        'analyticsGroupingFields', analyticsApi=True, profileIdAsHeader=True)
    assert response.status_code == 200
