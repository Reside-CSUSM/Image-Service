import requests
import copy
import json
import socket


class SpecificSearchPayload():
    #GETS THE IMAGES OF THE LISTINGS PROVIDED
    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url
        self.payload = {
                "Listings":[]
            }
    
    def set_url(self, url):
        self.endpoint_url = url

    def add_housing(self, housing):
        if(isinstance(housing, str) == False):
            return None
        self.payload["Listings"].append(housing)
        return self

    def delete_housing(self, housing):
        if(isinstance(housing, str) == False):
            return None
        self.payload["Listings"].remove(housing)
        return self

    def delete_all(self):
        housing_list = self.payload["Listings"]
        for housing in housing_list:
            housing_list.pop()
        return self

    def get_housing(self, housing):
        list = self.payload["Listings"]

        if(housing == 'all'):
            return list
        
        for addr in list:
            if(addr == housing):
                return addr

    def print_housings(self):
        housing_list = self.payload["Listings"]

        for housing in housing_list:
            print("Housing:", housing)
        return self

    def send_calls(self):
        response = None
        try:
            headers =  {'Content-Type': 'application/json'}
            response = requests.get(self.endpoint_url, json=self.payload, headers=headers)
            #var = json.loads(response.text)
            #print(" json?", response.json())
            return response.text
        except Exception as error:
            #print("Error:", error, response.status_code)
            return response.status_code
        
        #headers =  {'Content-Type': 'application/json'}
        #response = requests.get(self.endpoint_url, json=self.payload, headers=headers)
        #return response.text
        pass


class GeneralSearchPayload():
    #LAUNCHES THE BOT ON SERVER TO CACHE THE IMAGES
    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url
        self.payload = {
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
    
    def set_url(self, url):
        self.endpoint_url = url

    def add_area(self, area):
        if(isinstance(area, str) == False):
            return None
        
        area_list = self.payload["client_request_data"]["listing_requested"]["area"]
        area_list.append(area)
        return self

    def add_filters(self, filter):
        self.payload["client_request_data"]["filters"].append(filter)
        return self
    
    def remove_filter(self, filter):
        list = self.payload["client_request_data"]["filters"]
        try:
            for i in range(len(list), 0, -1):
                if(list[i] == filter):
                    self.payload["client_request_data"]["filters"].pop(i)
        except Exception as error:
            print("\x1b[31mError: remove_filter() ResideImageryAPI\x1b[0m")
        return self
    
    def delete_area(self, area):
        if(isinstance(area, str) == False):
            return None
        
        area_list = self.payload["client_request_data"]["listing_requested"]["area"]
        
        try:area_list.remove(area)
        except Exception as error: print(error)
        return self
    
    def delete_all(self):
        area_list = self.payload["client_request_data"]["listing_requested"]["area"]

        length = len(area_list)
        for i in range(0, length):
           self.payload["client_request_data"]["listing_requested"]["area"].pop()
        return self
    
    def get_area(self, area):
        pass

    def print_area(self, type):
        area_list = self.payload["client_request_data"]["listing_requested"]["area"]

        if(type == 'all'):
            for area in area_list:
                print("All Area:", area)
        else:
            for area in area_list:
                print("Area found:", area)
        return self

    def send_calls(self):
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(self.endpoint_url, json=self.payload, headers=headers)
            #print(response.text, ' text body recieved')
            return response.text
        except Exception as error:
            print("Error:", error)
            return response.status_code


class ResideImageryAPI():

    def __init__(self):
        self.automation_endpoint_url = "http://localhost:5000/Automations"
        self.reside_images_endpoint_url = "http://localhost:5000/ResideLibrary/Images"
        self.general_search = GeneralSearchPayload(self.automation_endpoint_url)
        self.specific_search = SpecificSearchPayload(self.reside_images_endpoint_url)
    
    def set_host(self, IP, PORT):
        self.automation_endpoint_url = "http://" + IP + ":" + str(PORT) + "/Automations"
        self.reside_images_endpoint_url = "http://" + IP + ":" + str(PORT) + "/ResideLibrary/Images"
        self.general_search.set_url(self.automation_endpoint_url)
        self.specific_search.set_url(self.reside_images_endpoint_url)

    def area(self):
        return self.general_search
    
    def housing(self):
        return self.specific_search

"""
api = ResideImageryApi()
api.area().add_filters("For rent")
val = api.area().add_area("El Cajon, CA").send_calls()

api.area().add_filters("For sale")
val = api.area().add_area("El Cajon, CA").send_calls()

print(">>")
api.area().add_area("La Mesa, CA").delete_all().print_area()
val = api.housing().add_housing("5210 Rain Creek Pkwy, Austin, TX").add_housing(" 4210 Spring St, La Mesa, CA").add_housing("105 Via de la Valle, Del Mar, CA").send_calls()
"""
"""api = ResideImageryAPI()
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
api.set_host("38.56.138.77", 6666)
val = api.housing().add_housing("3834 La Rosa Dr, Unit B, San Marcos, CA 92078").send_calls()
print(val)"""
