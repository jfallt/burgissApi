# Burgiss API

## Description
This package simplifies the connection to the Burgiss API and flattens API responses to dataframes.

![Tests](https://github.com/jfallt/burgissApi/actions/workflows/tests.yml/badge.svg)

## Authentication Setup
The class burgissApiAuth handles all the JWT token authentication but there are a few prerequesite requirements for the authentication.
1. Create a private x.509 base 64 format public key and an associated private key
1. Send the public key to support@burgiss.com
1. Once they receive the public key, they will set up a client ID for api usage
1. Download the configTemplate.cfg and rename to config.cfg and place in the working directory
1. Add your clientID, user/email and password
1. Put your private key in the working directory, name it private.pem

## Installation
1. Creating a virtual environment is suggested
1. Download requirements.txt
```
pip install -r requirements.txt 
pip install burgiss-api

## Project Structure
```
├── config.cfg              <- Config file to run api calls (not included in repo)
├── configTemplate.cfg      <- Config template file to run api calls
├── pyproject.toml          
├── ReadMe.md          
├── requirements.txt        <- The requirements file for reproducing the package environment
├── requirementsDev.txt     <- The requirements file for reproducing the testing environment
├── setup.cfg
├── setup.py
├── tox.ini
│
├── tests
│   ├── conftest.py         <- Intermediate data that has been 
|   ├── test_burgissAnalytics.py
│   └── test_responses.py   <- tests for JWT auth, responses and response transformation
│
└── src                     <- Source code for use in this project.
    │
    └── burgissApiWrapper   <- Scripts to download or generate data
        └── burgissApi.py   <- Classes for JWT auth, request package wrapping and response trans

```

## Usage
### Get requests
Request method defaults to get

```python
from burgissApiWrapper.burgissApi import session

# Initiate a session and get profile id for subsequent calls (obtains auth token)
burgissSession = session()

# Basic Request Syntax (Defaults to get)
orgs = burgissSession.request('orgs')

# Specifying profile as a header (instead of the request url), this occurs for a few of the requests
lookUpValues = burgissSession.request('LookupValues', profileIdAsHeader=True)

# Optional Parameters
investments = burgissSession.request('investments', optionalParameters='&includeInvestmentNotes=false&includeCommitmentHistory=false&includeInvestmentLiquidationNotes=false')
```
### Put requests
Must add optional parameters for requestType and data

```python
from burgissApiWrapper.burgissApi import session

# Initiate a session and get profile id for subsequent calls (obtains auth token)
burgissSession = session()

# When creating a put request, all fields must be present
data = {'someJsonObject':'data'}

# Specify the request type
orgs = burgissSession.request('some endpoint', requestType='PUT', data=data)
```

## Transformed Data Requests
Receive a flattened dataframe instead of a raw json from api

```python
from burgissApiWrapper.burgissApi import transformResponse

# Very similar syntax to above
apiSession = transformResponse()
orgs = apiSession.getData('orgs')
```

## Analytics API
:x: Current package does not support this feature but it is a planned addition

```python
from burgissApi import burgissApiSession

# Initiate a session and get profile id for subsequent calls (obtains auth token)
burgissSession = burgissApiSession()

# Get grouping fields
burgissSession.request('analyticsGroupingFields', analyticsApi=True, profileIdAsHeader=True)

# Specify inputs for point in time analyis
analysisJson = pointInTimeAnalyisInput(analysisParameters, globalMeasureParameters,
                                      measures, measureStartDateReference, measureEndDateReference, dataCriteria, groupBy)

# Send post request to receive data
burgissSession.request('pointinTimeAnalysis', analyticsApi=True,
                       profileIdAsHeader=True, requestType='POST', data=analysisJson)
```

<details>
<summary>Supported Calcs</summary>

|Measure Name| Is Supported for Pooled calculations|
| --------  | ------------------- |
|IRR|Yes|
|TWRR|Yes|
|Commitment|Yes|
|AdjustedCommitment|Yes|
|Unfunded|Yes|
|NetCapitalContributed|Yes|
|FundSize|No|
|DPI|Yes|
|RVPI|Yes|
|TVPI|Yes|
|LN_ICMIRR|Yes|
|LN_ICMIRRSpread|Yes|
|LN_ICMValuation|Yes|
|KS_PME|Yes|
|GGS_DirectAlpha|Yes|
|PaidIn|Yes|
|Funding|Yes|
|Fees|Yes|
|Distributions|Yes|
|Distributions.CapitalGains| 	Yes|
|Distributions.Income|Yes|
|Distributions.Other|Yes|
|Distributions.RecallableCapital| 	Yes|
|Distributions.ReturnOfCapital|Yes|
|Valuation|Yes|
|Cash|Yes|
|Cash.CapitalGains|Yes|
|Cash.Income|Yes|
|Cash.Other|Yes|
|Cash.RecallableCapital|Yes|
|Cash.ReturnOfCapital|Yes|
|Stock|Yes|
|Stock.CapitalGains|Yes|
|Stock.Cost|Yes|
|Stock.RecallableCapital|Yes|
|Stock.ReturnOfCapital|Yes|
</details>

## References

- [Burgiss API Documentation](https://api.burgiss.com/v2/docs/index.html)
- [Burgiss Analytics API Documentation](https://api-analytics.burgiss.com/swagger/index.html)
- [Burgiss API Token Auth Documentation](https://burgiss.docsend.com/view/fcqygcx)
- [Pypi Package](https://pypi.org/project/burgiss-api/)
