import requests
import copy
import json


class Response():

    def __init__(self):
        pass


class AutomationAction():

    def __init__(self):
        self.host = ""
        #Represents a single Automation Action that automations supporclsts
        self.endpoint = ""

    def request(self):
        pass    


class Payload():

    def __init__(self, payload):
        self.payload = payload
    
    def export(self):
        pass

class STOP():

    def __init__(self, service):
        self.service = service
    

class START():

    def __init__(self, service):
        self.service = service
        pass


class Services():
    
    def __init__(self):
        self.server_address = None
        self.current_service = None
        self.stop_service = STOP()
        self.start_service = START()

    def select(self, service):
        self.current_service = service

    def post_payload(self):
        value = self._use_server_address()
        #combine value + payload and send them thru the http request 

    def _use_server_address(self):
        pass

    def stop(self):
        self.stop_service

    def start(self):
        self.start_service



#ADMIN API
class ImagingAPI():

    def __init__(self):
        self.proto = "http://"
        self.server_ip = ""
        self.server_port = ""
        self.housing_list = []
        self.area_list = []

        self.housing_payload = {
            "service_type":"image_collection",
            "service_name":"redfin",
            "client_request_data":{
                "listing_requested":{
                    "type":"housings",
                    "addresses":[],
                    "storage":"cache"
                    }
               }
            }
        
        #"5210 Rain Creek Pkwy, Austin, TX", "7122 Wood Hollow Dr 13, Austin, TX", "2914 Sorin St, Austin, TX", "6303 Dorchester Dr, Austin, TX 78723"
        self.area_payload = {
            "service_type":"image_collection",
            "service_name":"redfin",
            "client_request_data":{
                "filters":[""],
                "listing_requested":{
                    "type":"city&state",
                    "area":[],
                    "storage":"cache"
                    }
                }
            }
    
        #"san diego, CA", "Austin, TX", "Sacramento, CA"
    def initialize(self, ip, port):
        self.server_ip = ip
        self.server_port = port

    def add_general_search_filter(self, filter):
        self.area_payload["client_request_data"]["filters"].append(filter)

    def remove_general_search_filter(self, filter):
        index = 0
        for _filter in self.area_payload["client_request_data"]["filters"]:
            if(_filter == filter):
                self.area_payload["client_request_data"]["filters"].pop(index)
            index += 1

    def add_housings(self, address):
        self.housing_payload["client_request_data"]["listing_requested"]["addresses"].append(address)
        return self
    
    def search_housings(self):
        url = self.proto + self.server_ip + ":"+str(self.server_port) + "/automations/query="
        string = str(self.housing_payload)
        url += string
        headers = {'Content-Type': 'application/json'}
        req = requests.post(url, headers=headers)
        print(req)
        return self 
    
    def add_areas(self, area):
        self.area_payload["client_request_data"]["listing_requested"]["area"].append(area)
        return self

    def search_area(self):
        url = self.proto + self.server_ip + ":"+str(self.server_port) + "/automations/query="
        string = str(self.area_payload)
        url += string
        headers = {'Content-Type': 'application/json'}
        req = ""
        try:
            req = requests.post(url, headers=headers)
            print(req, "  status=", req.status_code)
        except Exception as error:
            print(error)
            if('403' in str(error)):
                string = str(error)
                string = string[string.find('{'):string.find('}')]
                return 403
            
            for i in range(200, 399):
                if(str(i) in str(error)):
                    return i
                
            else: return False
      
        return req.status_code

    def delete_area(self, area):
        areas = self.area_payload["client_request_data"]["listing_requested"]["area"]

        if(area == 'all'):
            alen = len(areas)
            for i in range(0, alen):
                areas.pop(i)
                alen = len(areas)
            return True
        else:
            for i in range(0, len(areas)):
                if(areas[i] == area):
                    self.area_payload["client_request_data"]["listing_requested"]["area"].pop(i)
                    return True
        
        return False
    
    def print_areas(self):
        print("Added areas....")
        filters = self.area_payload["client_request_data"]["filters"]
        for area in self.area_payload["client_request_data"]["listing_requested"]["area"]:
            print("area:", area, " filters:", filters)



#API requests have to be asynchronous, not blocking code. 
#API has to be able to send 'STOP' commands to automations running

"""
AutomationsAPI:
    - Controlling Hosted Automations
      - STOP
      - LAUNCH
            - Parameters

"""
#   AutomationAPI ->  Server -> /AutomationService -> AutomationHandlerProcess -> Launching Bots with parameters
        #65% DONE
        #Needs:
"""          - 
            
            """

#   ListingsImageAPI -> Server -> /ListingImages -> LibaryHandlerProcess -> Fetch and find the data using regex
