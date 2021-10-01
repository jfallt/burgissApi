
import os

import pandas as pd
import pytest
from burgissApi.burgissApi import burgissApi, burgissApiSession

os.chdir("..")

#=======================#
# Test requests         #
#=======================#
burgissApiSession = burgissApi()


def testOrgsTransformation():
    response = burgissApiSession.getData('orgs')
    assert isinstance(response, pd.DataFrame) == True
    assert len(response) > 0


def testInvestmentsTransformation():
    response = burgissApiSession.getData('investments')
    assert isinstance(response, pd.DataFrame) == True
    assert len(response) > 0


def testPortfoliosTransformation():
    response = burgissApiSession.getData('portfolios')
    assert isinstance(response, pd.DataFrame) == True
    assert len(response) > 0


def testLookupValuesTransformation():
    response = burgissApiSession.getData(
        'LookupValues', profileIdAsHeader=True)
    assert isinstance(response, pd.DataFrame) == True
    assert len(response) > 0
    assert len(response.columns) == 4


def testLookupDataTransformation():
    response = burgissApiSession.getData(
        'LookupData')
    assert isinstance(response, pd.DataFrame) == True
    assert len(response) > 0
