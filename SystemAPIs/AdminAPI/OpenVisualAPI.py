import requests
import copy
import json
import socket


class OperationCRUD():

    def __init__(self):
        self.server_endpoint = "http://192.168.1.222:80/OpenVisualDatabase"
        self.server_endpoint = "https://https://open-visuals.vercel.app/OpenVisualDatabase"
        self.operation_name = "$None"
        self.api_request = {
            'Operation':self.operation_name,
            'Country':'$None',
            'State':'$None',
            'City':'$None',
            'Listing':'$None',
            'AdditionalListingData':'$None'
        }
        self.response = None

    def __reset_api_request(self):
        self.api_request = {
            'Operation':self.operation_name,
            'Country':'$None',
            'State':'$None',
            'City':'$None',
            'Listing':'$None',
            'AdditionalListingData':'$None'
        }
    
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
    
    def AdditionalListingData(self, data):
        self.api_request['AdditionalListingData'] = data
        return self
    
    def SpecifyAutomation(self, name):
        self.api_request['AutomationForLaunch'] = name
        return self
    
    def ExportPayload(self):
        return self.api_request

    def Perform(self):
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(self.server_endpoint, json=self.api_request, headers=headers)
            self.__reset_api_request()
            return response.text
        except Exception as error:
            print("Error:", error)
            #return response.status_code
            self.__reset_api_request()
            return False
        
    

class OperationUpdate(OperationCRUD):

    def __init__(self):
        super().__init__()
        self.operation_name = "UPDATE"
        self.api_request = {
            'Operation':self.operation_name,
            'Country':'$None',
            'State':'$None',
            'City':'$None',
            'Listing':'$None'
        }


class OperationDelete(OperationCRUD):

    def __init__(self):
        super().__init__()
        self.operation_name = "DELETE"
        self.api_request = {
            'Operation':self.operation_name,
            'Country':'$None',
            'State':'$None',
            'City':'$None',
            'Listing':'$None'
        }
    

class OperationAdd(OperationCRUD):

    def __init__(self):
        super().__init__()
        self.operation_name = "ADD"
        self.api_request = {
            'Operation':self.operation_name,
            'Country':'$None',
            'State':'$None',
            'City':'$None',
            'Listing':'$None'
        }
        
class OperationSearch(OperationCRUD):

    def __init__(self):
        super().__init__()
        self.operation_name = "SEARCH"
        self.api_request = {
            'Operation':self.operation_name,
            'Country':'$None',
            'State':'$None',
            'City':'$None',
            'Listing':'$None'
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



open_visual_api = OpenVisualAPI()
#value = open_visual_api.CRUD().Add().Country("USA").State("California").City("Otay Ranchers").Perform()
data = {
    'Images':[]
}
value = open_visual_api.CRUD().Update().Country("USA").State("California").City("La Mesa").Perform()
#value = open_visual_api.CRUD().Add().Country("USA").State("California").City("")
print(value)

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