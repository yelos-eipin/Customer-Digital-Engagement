from requests_oauthlib import OAuth2Session
import requests
import urllib.parse
import json
import logging
from auth import OAuth

apiUrl = 'https://sandboxapi.deere.com/platform'

deere = OAuth()

# attempt connect and get/refresh token if necessary.
deere.checkStatus()


def call_the_api():
    try:
        res = api_get(deere.accessToken, apiUrl)
        response = json.dumps(res.json(), indent=4)
        return index()
    except Exception as e:
        logging.exception(e)
        print('error' + e.msg)

def api_get(access_token, resource_url):
    headers = {
        'authorization': 'Bearer ' + deere.accessToken,
        'Accept': 'application/vnd.deere.axiom.v3+json'
    }
    
    return requests.get(resource_url, headers=headers)

def needsToDefineOrganization():
    api_response = api_get(deere.accessToken, apiUrl + '/organizations').json()
    for org in api_response['values']:
        for link in org['links']:
            if link['rel'] == 'connections':
                connectionsUri = link['uri']
                query = urllib.parse.urlencode({'redirect_uri': deere.redirectUri })
                return f"{connectionsUri}?{query}"
                 
    return None

def getOrganizationIDs():
    """
    returns all organizationIDs only 
    """
    api_response = api_get(deere.accessToken, apiUrl + '/organizations').json()

    orgIDs = []
    for org in api_response['values']:
        orgIDs.append(org["id"])

    return orgIDs

def getOrganizations():
    """
    returns all data items regarding an organization, such as Name, Type, ID and links
    """    
    api_response = api_get(deere.accessToken, apiUrl + '/organizations').json()

    return api_response['values'] 

def getMachinesByOrgID(orgID):
    try:
        api_response = api_get(deere.accessToken, apiUrl + '/organizations/' + orgID + '/machines' )

        if(api_response.status_code != '200'):
            print(api_response.status_code)
        else:
            return api_response['values']
    except Exception as e:
        logging.exception(e)     
        return None

def getUsers():
    api_response = api_get(deere.accessToken, apiUrl + '/organizations').json()

    return api_response 
   

Orgs = getOrganizations()   
for org in Orgs:
    print('Org Name: \t' + org["name"])
    print('OrgID:    \t' + org["id"])
    print()
    print('\t Machines listed under this org:')
    Machines = getMachinesByOrgID(org["id"])
    if(Machines is None):
        print('No machines to list')
    else:
        for machine in Machines:
            print('Make: ' + machine["make"])
        