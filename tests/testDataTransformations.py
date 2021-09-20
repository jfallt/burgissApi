
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


def testLookupValuesTransformation():
    response = burgissApiSession.getData(
        'LookupValues', profileIdAsHeader=True)
    assert isinstance(response, pd.DataFrame) == True
    assert len(response) > 0
    print(response)
    #assert len(response.columns) == 3


def testLookupDataTransformation():
    response = burgissApiSession.getData(
        'LookupData')
    assert isinstance(response, pd.DataFrame) == True
    assert len(response) > 0
