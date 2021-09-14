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

## Usage
```python
from burgissApi import burgissApiSession

# Initiate a session and get profile id for subsequent calls (obtains auth token)
burgissSession = burgissApiSession()

# Basic Request Syntax (Defaults to get)
orgs = burgissSession.request('orgs')

# Specifying profile as a header (instead of the request url)
lookUpValues = burgissSession.request('LookupValues', profileIdAsHeader=True)

# Optional Parameters
investments = burgissSession.request('investments', optionalParameters='&includeInvestmentNotes=false&includeCommitmentHistory=false&includeInvestmentLiquidationNotes=false')

# Analytics Endpoint (currently very few of these endpoints)
burgissSession.request('analyticsGroupingFields', analyticsApi=True, profileIdAsHeader=True)
```

## References

- [Burgiss API Documentation](https://api.burgiss.com/v2/docs/index.html)
- [Burgiss Analytics API Documentation](https://api-analytics.burgiss.com/swagger/index.html)
- [Burgiss API Token Auth Documentation](https://burgiss.docsend.com/view/fcqygcx)
- [Wikipedia: Markdown](http://wikipedia.org/wiki/Markdown)