# Burgiss API

## Description
This package simplifies the connection to the Burgiss API and is built on top of the requests package

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
```

## Usage
Data can be updated via the api, to enable this you must change the scope in the config file and specify the request type.

```python
from burgissApi import burgissApiSession

# Initiate a session and get profile id for subsequent calls (obtains auth token)
burgissSession = burgissApiSession()

# Basic Request Syntax (Defaults to get)
orgs = burgissSession.request('orgs')

# Specifying profile as a header (instead of the request url), this occurs for a few of the requests
lookUpValues = burgissSession.request('LookupValues', profileIdAsHeader=True)

# Optional Parameters
investments = burgissSession.request('investments', optionalParameters='&includeInvestmentNotes=false&includeCommitmentHistory=false&includeInvestmentLiquidationNotes=false')
```

## Transformed Data Requests
Some endpoints are supported for transformation to a flattened dataframe instead of a raw json

```python
from burgissApi import burgissApi

# Very similar syntax to above
apiSession = burgissApi()
orgs = apiSession.getData('orgs')
```

<details>
<summary>Supported Endpoints</summary>

|Field|
| -------|
|investments|
|orgs|
|portfolios|
|LookupData|
|LookupValues|
</details>


## Analytics API
```python
from burgissApi import burgissApiSession

# Initiate a session and get profile id for subsequent calls (obtains auth token)
burgissSession = burgissApiSession()

burgissSession.request('analyticsGroupingFields', analyticsApi=True, profileIdAsHeader=True)
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