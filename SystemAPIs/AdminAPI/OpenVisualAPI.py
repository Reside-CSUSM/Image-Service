import requests
import copy
import json
import socket




class AutomationLauncher():

    def __init__(self):
        self.automation_settings = None
    
    def LaunchAutomation(self):
        return self
    
    def ConfigureSettings(self, settings):
        pass

class OperationCRUD():

    def __init__(self):
        self.server_endpoint = "https://vercel-open-visuals-app/OpenVisualDatabase"
        self.api_request = {
            'Operation':'None',
            'Country':'None',
            'State':'None',
            'City':'None',
            'Listing':'None',
            'AutomationForLaunch':'None'
        }
        self.response = None

    def Country(self, name):
        self.api_request['Country'] = name
        return self
    
    def State(self, name):
        self.api_request['State'] = name
        return self
    
    def City(self, name):
        self.api_request['City'] = name
        return self
    
    def Listing(self, name):
        self.api_request['Listing'] = name
        return self
    
    def SpecifyAutomation(self, name):
        self.api_request['AutomationForLaunch'] = name
        return self
    
    def perform(self):
        return self.response

    def ExportPayload(self):
        return self.api_request

    def perform(self):
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(self.api_request, json=self.server_endpoint, headers=headers)
            return response.text
        except Exception as error:
            print("Error:", error)
            return response.status_code
    

class OperationUpdate(OperationCRUD):

    def __init__(self):
        self.api_request = {
            'Operation':'UPDATE',
            'Country':'None',
            'State':'None',
            'City':'None',
            'Listing':'None'
        }


class OperationDelete(OperationCRUD):

    def __init__(self):
        self.api_request = {
            'Operation':'DELETE',
            'Country':'None',
            'State':'None',
            'City':'None',
            'Listing':'None'
        }
    

class OperationAdd(OperationCRUD):

    def __init__(self):
        self.api_request = {
            'Operation':'ADD',
            'Country':'None',
            'State':'None',
            'City':'None',
            'Listing':'None'
        }
        
class OperationSearch(OperationCRUD):

    def __init__(self):
        self.api_request = {
            'Operation':'SEARCH',
            'Country':'None',
            'State':'None',
            'City':'None',
            'Listing':'None'
        }


class OpenVisualCRUD():

    def __init__(self):
        self.available_operations = {
            'UPDATE':OperationUpdate(),
            'DELETE':OperationDelete(),
            'SEARCH':OperationSearch(),
            'ADD':OperationAdd()
        }
    
    def Update(self):
        return self.available_operations['UPDATE']

    def Add(self):
        return self.available_operations['ADD']
    
    def Delete(self):
        return self.available_operations['DELETE']

    def Search(self):
        return self.available_operations['SEARCH']


#Server needs to send complete logs of what's happending during each process when deleting, updating or adding areas.
class OpenVisualAPI():

    def __init__(self):
        self.database_crud_controller = OpenVisualCRUD()
    
    def CRUD(self):
        return self.database_crud_controller
    
    def Launcher(self):
        pass


"""
[IDEA]:  #PURPOSE:
        #1) Launch individual automations on a remote server with 'save data' mode disabled
        #2) Configure Automation setting to be parsed onto the server

[UPDATE]#Server will first delete the entire cache for specific area first in mongoDB
        #Server then will launch bots with 'collection' mode enabled for to add the same area again
        #Will update country, state or city depending on what's provided

[DELETE]#Requires Country, State and City to be listed
        #Sends command to server to delete a specific collection in database

[ADD] #Simply sends command to server create a new collection in database

"""