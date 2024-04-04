import sys, os
sys.path.insert(0, r'C:\Users\yasha\Visual Studio Workspaces\OpenVisuals\OpenVisuals')
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
import copy
import json
import urllib.parse

#AUTOMATION MODULES
from Automations.Redfin.interface import *
from Automations.Redfin.redfind_errors import *

AUTOMATIONS_ERROR_CODES = []
class AutomationsHandler():
    def __init__(self):
        #Handles the automations.json and updates it 
        pass


class AvailableServices():
    def __init__(self):
        #Dynamically import modules of new automation folders/systems
        pass

    pass


class AutomationService():

    def __init__(self):
        self.path = ""
        self.responses = []
        self.data = None

    def __decode(self, path):
        self.path = path
        if(("/query=" in self.path) == False):
            print("\x1b[34m/QUERY=NOT FOUND\x1b[0m")
            return False
        
        print("\x1b[34m/QUERY=FOUND!!\x1b[0m")
        string = copy.copy(self.path).replace("/query=","")
        decoded_data = urllib.parse.unquote(string)
        decoded_data = decoded_data.replace("'", '"')
        print("Decoded DATA:", decoded_data)
        parsed_data = json.loads(decoded_data)
        print("After parsing:", parsed_data)


        try:
            parsed_data = json.loads(decoded_data)
            return parsed_data
        except Exception as error:
            print("Error coverting from json to python dict", error)
            try:
                decoded_data += ']'
                parsed_data = json.loads(decoded_data)
                print("Success on retrying the decoding tho...")
            except Exception as error:
                print("Failure on retrying to decode as well.....")
                pass


    def get_response(self):
        return self.responses

    def _handle(self, path):
        self.path = path
        response = self.__decode(path)
        print(response)

    def __POST(self):
        response = self.__decode(self.path)
        if(response == False):
            return False
        #Check Service Type
        if(response["service_type"] == "image_collection"):

            if(response["service_name"] == "redfin"):
                listing_requested = response["client_request_data"]["listing_requested"]
                type = listing_requested["type"]

                if(type == "housings"):
                    addresses = listing_requested["addresses"]
                    storage = listing_requested["storage"]
                
                    for address in addresses:
                        RedfinInterface.create_bot()
                        RedfinInterface.activate()
                        RedfinInterface.type("specific")
                        self.responses.append(RedfinInterface.search_images(address))
                        RedfinInterface.close_bot()
                    return self.responses

                elif(type == "city&state"):
                    filters = response["client_request_data"]["filters"]
                    areas = listing_requested["area"]
                    error_count = None
                    for area in areas:
                        RedfinInterface.create_bot()
                        RedfinInterface.activate()
                        RedfinInterface.type("general")
                        RedfinInterface.apply_filters(filters)
                        self.responses.append(RedfinInterface.search_images(area))
                        RedfinInterface.close_bot()
                    
                    for response in self.responses:
                        if(response in REDFIN_ERROR_CODES):
                            if(error_count == None):
                                error_count = 0
                            error_count += 1
                    
                    if(error_count != None):
                        if(error_count > 0):
                            return self.responses
                    
                    self.responses = True
                    return self.responses
            
            elif(response["service_name"] == "zillow"):
                self.responses = "No Automation Service Available For Zillow"
                return self.responses

            elif(response["service_name"] == "compass"):
                self.responses = "No Automation Service Available For Compass"
                return self.responses
        pass
    
    def __POST2(self):
        response = self.data
        if(response == None):
            return False
        
        #Check Service Type
        if(response["service_type"] == "image_collection"):

            if(response["service_name"] == "redfin"):
                listing_requested = response["client_request_data"]["listing_requested"]
                type = listing_requested["type"]

                if(type == "housings"):
                    addresses = listing_requested["addresses"]
                    storage = listing_requested["storage"]
                    self.responses = []
                    for address in addresses:
                        print("/x1b[31mProcessing address....\x1b[0m", address)
                        RedfinInterface.create_bot()
                        RedfinInterface.activate()
                        RedfinInterface.type("specific")
                        self.responses.append(RedfinInterface.search_images(address))
                        RedfinInterface.close_bot()
                    return self.responses

                elif(type == "city&state"):
                    filters = response["client_request_data"]["filters"]
                    areas = listing_requested["area"]
                    error_count = None
                    for area in areas:
                        RedfinInterface.create_bot()
                        RedfinInterface.activate()
                        RedfinInterface.type("general")
                        RedfinInterface.apply_filters(filters)
                        self.responses.append(RedfinInterface.search_images(area))
                        RedfinInterface.close_bot()

                    for response in self.responses:
                        if(response in REDFIN_ERROR_CODES):
                            if(error_count == None):
                                error_count = 0
                            error_count += 1
                    
                    if(error_count != None):
                        if(error_count > 0):
                            return self.responses
                    
                    #self.responses = True
                    return True
            
            elif(response["service_name"] == "zillow"):
                self.responses = "No Automation Service Available For Zillow"
                return self.responses

            elif(response["service_name"] == "compass"):
                self.responses = "No Automation Service Available For Compass"
                return self.responses
        pass
    
    def __PUT(self):
        pass

    def __GET(self):
        pass

    def __DELETE(self):
        pass
    
    def handle(self, path, TYPE):
        #DECODE THE JSON DATA RECIEVED
        self.path = path
        if(TYPE == 'POST'):
            value = self.__POST()
            if(value == False):
             print("POST ERROR:", "error")
        
        elif(TYPE == 'GET'):
            self.__GET()
        
        elif(TYPE == 'PUT'):
            self.__PUT()
        
        elif(TYPE == 'DELETE'):
            self.__DELETE()

    def handle2(self, data, TYPE):
        #DECODE THE JSON DATA RECIEVED
        if(TYPE == 'POST'):
            self.data = data
            try:
                value = self.__POST2()
                if(value == False):
                    print("POST ERROR:", "error")
            except Exception as error:
                print("POST ERROR EXCEPTION:", error)
        
        elif(TYPE == 'GET'):
            self.__GET()
        
        elif(TYPE == 'PUT'):
            self.__PUT()
        
        elif(TYPE == 'DELETE'):
            self.__DELETE()
        return self
    
#NOTE SPECIFIC SEARCH THROUGH IMAGERY.PY NOT WORKING THROWS AN ERRO, ALSO HAVE TO TEST SPECIFIC SEARCH FUNCTION IF IT PUTS THINGS IN FILE