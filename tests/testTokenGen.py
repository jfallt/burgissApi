
from burgissApi.burgissApi import burgissApiAuth
import pytest

import os
os.chdir("..")

#=======================#
# Test token gen        #
#=======================#
def testGetBurgissApiToken():
    tokenInit = burgissApiAuth()
    token = tokenInit.getBurgissApiToken()
    assert len(token) != 0
