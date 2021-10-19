import configparser
import logging
import uuid
from datetime import datetime, timedelta

import jwt
import pandas as pd
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from OpenSSL import crypto

# Create logging file for debugging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    logging.basicConfig(filename='burgissApi.log',
                        encoding='utf-8', level=logging.DEBUG,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger('burgissApi')
filehandler_dbg = logging.FileHandler(logger.name + '.log', mode='w')


class ApiConnectionError(Exception):
    """Base class for exceptions in this module."""
    pass


def responseCodeHandling(response):
    """
    Handle request responses and log if there are errors
    """
    if response.status_code == 200:
        return response
    elif response.status_code == 404:
        logger.error(
            "Url not found")
        raise ApiConnectionError(
            'Url not found, check the logs for the specific url!')
    else:
        logger.error(
            f"API Connection Failure: Error Code {response.status_code}")
        raise ApiConnectionError(
            'No recognized reponse from Burgiss API, Check BurgissApi.log for details')


def lowerDictKeys(d):
    newDict = dict((k.lower(), v) for k, v in d.items())
    return newDict


class tokenAuth(object):
    """
    Create and send a signed client token to receive a bearer token from the burgiss api endpoint
    """

    def __init__(self):
        logger.info("Import client details from config file")
        config = configparser.ConfigParser()
        config.read_file(open('config.cfg'))
        self.clientId = config.get('API', 'clientId')
        self.username = config.get('API', 'user')
        self.password = config.get('API', 'pw')
        self.urlToken = config.get('API', 'tokenUrl')
        self.urlApi = config.get('API', 'apiUrl')
        self.analyticsUrlApi = config.get('API', 'apiUrlAnalytics')
        self.assertionType = config.get('API', 'assertionType')
        self.scope = config.get('API', 'scope')
        logger.info("Client details import complete!")

    def getBurgissApiToken(self):
        """
        Sends a post request to burgiss api and returns a bearer token
        """
        logger.info("Begin Burgiss Token Authentication")

        # Read private key from file, used to encode jwt
        logger.info("Read private key from current directory")
        with open('private.pem', 'rb') as privateKey:
            secret = privateKey.read()
            secret_key = serialization.load_pem_private_key(
                secret, password=None, backend=default_backend())

        now = datetime.utcnow()
        exp = now + timedelta(minutes=1)

        headers = {
            'alg': 'RS256',
            'kid': crypto.X509().digest('sha1').decode('utf-8').replace(':', ''),
            'typ': 'JWT'
        }
        payload = {
            'jti': str(uuid.uuid4()),  # unique identifier, must be string
            'sub': self.clientId,
            'iat': now,
            'nbf': now,
            'exp': exp,
            'iss': self.clientId,
            'aud': self.urlToken
        }

        logger.info("Encode client assertion with jwt")
        clientToken = jwt.encode(
            payload, secret_key, headers=headers, algorithm='RS256')

        payload = {
            'grant_type': 'password',
            'clientId': self.clientId,
            'username': self.username,
            'password': self.password,
            'scope': self.scope,
            'client_assertion_type': self.assertionType,
            'client_assertion': clientToken
        }

        logger.info("Sending post request to obtain client token")
        tokenResponse = requests.request(
            'POST', self.urlToken, data=payload
        )
        tokenResponseJson = tokenResponse.json()

        # Error Handling
        if 'access_token' in tokenResponseJson.keys():
            logger.info("Token request successful!")
            return tokenResponseJson['access_token']
        elif 'error' in tokenResponseJson.keys():
            logging.error(
                f"API Connection Error: {tokenResponseJson['error']}")
            raise ApiConnectionError(
                'Check BurgissApi.log for details')
        elif 'status_code' in tokenResponseJson.keys():
            logging.error(
                f"API Connection Error: Error Code {tokenResponseJson ['status_code']}")
            raise ApiConnectionError(
                'Check BurgissApi.log for details')
        else:
            logging.error("Cannot connect to endpoint")
            raise ApiConnectionError(
                'No recognized reponse from Burgiss API, Check BurgissApi.log for details')


class init(tokenAuth):
    """
    Initializes a session for all subsequent calls using the tokenAuth class
    """

    def __init__(self):
        self.auth = tokenAuth()
        self.token = self.auth.getBurgissApiToken()
        self.tokenExpiration = datetime.utcnow() + timedelta(seconds=3600)
        self.urlApi = self.auth.urlApi
        self.analyticsUrlApi = self.auth.analyticsUrlApi

    def requestWrapper(self, url: str, analyticsApi: bool = False, requestType: str = 'GET', profileIdHeader: bool = False, data=''):
        """
        Burgiss api request call, handling bearer token auth in the header with token received when class initializes

        Args:
            url (str): api url for request
            analyticsApi (bool): if analytics api endpoint is used
            requestType (str, optional): Defaults to 'GET'.

        Returns:
            Response [json]: Data from url input
        """

        # Check if token is expired, if it is get a new token
        logger.info('Check if token has expired')
        if self.tokenExpiration < datetime.utcnow():
            logger.info('Token has expired, getting new token')
            self.token = self.auth.getBurgissApiToken()
            self.tokenExpiration = datetime.utcnow() + timedelta(seconds=3600)
        else:
            logger.info('Token is still valid')

        # Default to regular api but allow for analytics url
        if analyticsApi is False:
            baseUrl = self.urlApi
        else:
            baseUrl = self.analyticsUrlApi

        if profileIdHeader is False:
            headers = {
                'Authorization': 'Bearer ' + self.token
            }
        else:
            headers = {
                'ProfileID': profileIdHeader,
                'Authorization': 'Bearer ' + self.token,
            }

        if len(data) > 0:
            response = requests.request(
                requestType, baseUrl + url, headers=headers, data=data)
        else:
            response = requests.request(
                requestType, baseUrl + url, headers=headers)

        return responseCodeHandling(response)


class session(init):
    """
    Simplifies request calls by getting auth token and profile id from parent classes
    """

    def __init__(self):
        """
        Initializes a request session, authorizing with the api and gets the profile ID associated with the logged in account
        """
        config = configparser.ConfigParser()
        config.read_file(open('config.cfg'))
        self.profileIdType = config.get('API', 'profileIdType')
        self.session = init()
        self.profileResponse = self.session.requestWrapper(
            'profiles').json()
        self.profileId = self.profileResponse[0][self.profileIdType]

    def request(self, url: str, analyticsApi: bool = False, profileIdAsHeader: bool = False, optionalParameters: str = '',  requestType: str = 'GET', data=''):
        """
        Basic request, built on top of init.requestWrapper, which handles urls and token auth

        Args:
            url (str): Each burgiss endpoint has different key words e.g. 'investments' -> Gets list of investments
                Refer to API docs for specifics
            analyticsApi (bool, optional): Set to true if using the analytics api
            profileIdAsHeader (bool, optional): Set to true if profileId should be used in the header
            optionalParameters (str, optional): Certain endpoints have additional settings (i.e. Investments has the following:
                &includeInvestmentNotes=false
                &includeCommitmentHistory=false
                &includeInvestmentLiquidationNotes=false)
            requestType (str, optional): Determines the type of request. Defaults to 'GET'.

        Returns:
            response [object]: Request object, refer to the requests package documenation for details
        """

        if profileIdAsHeader is False:
            profileUrl = f'?profileID={self.profileId}'
            profileIdHeader = False
        else:
            profileUrl = ''
            profileIdHeader = self.profileId

        endpoint = url + profileUrl + optionalParameters

        response = self.session.requestWrapper(
            endpoint, analyticsApi, requestType, profileIdHeader, data)

        return responseCodeHandling(response)


class transformResponse(session):
    def __init__(self):
        """
        Initializes a request session, authorizing with the api and gets the profile ID associated with the logged in account
        """
        self.apiSession = session()
        # storing exceptions here for now until we can determine a better way to handle them
        self.nestedExceptions = {'LookupData':
                                 {'method': 'json_normalize',
                                  'data': 'fields',
                                  'recordPath': 'lookup',
                                  'meta': 'field'},
                                 'LookupValues':
                                 {'method': 'nestedJson'}
                                 }

    def parseNestedJson(self, responseJson):
        """
        Custom nested json parser

        Args:
            responseJson (dict)

        Returns:
            Pandas DataFrame [object]

        """
        dfTransformed = pd.json_normalize(responseJson).T.reset_index()
        dfTransformed[['field', 'id']] = dfTransformed['index'].str.split(
            '.', expand=True)
        dfTransformed = dfTransformed.rename(columns={0: 'value'})

        return dfTransformed

    def flattenResponse(self, resp, field):
        """
        The api sends a variety of responses, this function determines which parsing method to use based on the response
        """
        if isinstance(resp, list):
            flatDf = pd.json_normalize(resp)
        elif isinstance(resp, dict):
            respLower = lowerDictKeys(resp)

            if list(respLower)[0] == field.lower():
                respLower = respLower[field.lower()]

            # Exception handling
            if field in self.nestedExceptions.keys():
                parameters = self.nestedExceptions[field]
                if parameters['method'] == 'json_normalize':
                    flatDf = pd.json_normalize(
                        respLower[parameters['data']], record_path=parameters['recordPath'], meta=parameters['meta'])
                elif parameters['method'] == 'nestedJson':
                    flatDf = self.parseNestedJson(respLower)
            else:
                flatDf = pd.json_normalize(respLower)
        return flatDf

    def columnNameClean(self, df):
        """
        Removes column name prefix from unnested columns
        """
        columnList = []

        for column in df.columns:
            if '.' in column:
                column = column.split('.', 1)[1]
            columnList.append(column)
        df.columns = columnList
        return df

    def getData(self, field: str, profileIdAsHeader: bool = False, OptionalParameters: str = ''):
        """
        Basic api request and tabular transformation

        Args:
            field (str): Each burgiss endpoint has different key words e.g. 'investments' -> Gets list of investments
                - Refer to API docs for specifics
            useOptionalParameters (str, optional): Certain endpoints have additional settings (i.e. Investments has the following:
                &includeInvestmentNotes=false
                &includeCommitmentHistory=false
                &includeInvestmentLiquidationNotes=false)

        Returns:
            Pandas DataFrame [object]: Data from 'get' request transformed into relational dataframe

        """
        resp = self.apiSession.request(
            field, profileIdAsHeader=profileIdAsHeader, optionalParameters=OptionalParameters).json()

        # Flatten and clean response
        flatDf = self.flattenResponse(resp, field)
        cleanFlatDf = self.columnNameClean(flatDf)

        return cleanFlatDf

    def getTransactions(self, id: int, field: str):
        """
        Basic api request for values in 'transaction' model

        Args:
            id (int): refers to investmentID
            field (str): 'transaction' model has different key words (e.g. 'valuation', 'cash', 'stock', 'fee', 'funding')
                -> Gets list of values for indicated investmentID

        Returns:
            json [object]: dictionary of specified field's values for investmentID

        """
        url = f'investments/{id}/transactions/{field}'
        resp = self.apiSession.request(url=url)
        return resp.json()


def pointInTimeAnalyisInput(analysisParameters, globalMeasureParameters, measures, measureStartDateReference, measureEndDateReference, dataCriteria, groupBy):
    """
    Simplify nested json input for point in time analysis
    """
    # Add start and end date references to global measure and measure params
    globalMeasureParameters['measureStartDateReference'] = measureStartDateReference
    globalMeasureParameters['measureEndDateReference'] = measureEndDateReference
    measures['measureStartDateReference'] = measureStartDateReference
    measures['measureEndDateReference'] = measureEndDateReference

    # Nest global measure parameters and measures
    analysisParameters['globalMeasureParameters'] = globalMeasureParameters
    analysisParameters['measures'] = [measures]

    # Create final json
    pointInTimeAnalyis = {"pointInTimeAnalysis": [analysisParameters]}
    pointInTimeAnalyis['dataCriteria'] = [dataCriteria]
    pointInTimeAnalyis['groupBy'] = groupBy

    print(pointInTimeAnalyis)
    # Remove any none or null values
    # pointInTimeAnalyisProcessed = {x:y for x,y in pointInTimeAnalyis.items() if (y is not None and y!='null') }
    print(pointInTimeAnalyis)

    return pointInTimeAnalyis
    # return json.dumps(pointInTimeAnalyis)


class testApiResponses():
    def __init__(self) -> None:
        self.initSession = init()
        self.burgissSession = session()
        self.transformResponse = transformResponse()

        self.endpoints = ['orgs', 'investments', 'portfolios', 'assets', 'LookupData']

    def testGetBurgissApiToken(self):
        tokenInit = tokenAuth()
        token = tokenInit.getBurgissApiToken()
        assert len(token) != 0

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
        assert isinstance(response, pd.DataFrame) == True
        assert len(response) > 0