#sys.path.insert(0, r"C:\Users\kulsh001\AppData\Local\Programs\Python\Python311\Lib\site-packages")
import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
print(sys.path[0], "<--this")
from flask import Flask, request
from .ListingsService import ListingService
app = Flask(__name__)


class ServerResponse():

    def __init__(self):
        
        self.payload = {
            'RecipientPayload':None,
            'Errors':False,
            'ErrorLog':[]
        }
    
    def put_payload(self, payload):
        self.payload['RecipientPayload'] = payload
    
    def get(self, field=None):
        if(field == None):
            return self.payload
        else:
            try:
                return self.payload[field]
            except Exception as error:
                return None
    
    def set_error(self, val):
        if(isinstance(val, bool) == False):
            raise "\x1b[31m ServerResponse: Error Flag Not Boolean!!\x1b[0m"
        self.payload['Errors'] = val
    
    def put_error_log(self, log):
        self.payload['ErrorLog'].append(log)



listing_images_service = ListingService()

@app.route("/")
def root():
    return "cloud listing provider server is running"

@app.route("/details")
def details():
    Details = """
    OpenVisual Cloud deployment
    ____________________________

    [Details]
    Component: WebProvider
    Platform:  Vercel
    Language:  Python

    Component: WebHarvester
    Platform:  Vercel
    Language: Python

    [Tech Stack For Reside Platform]:
    Selenium
    MongoDB
    SpringBoot
    React.js
    Next.js
    Vercel(Cloud Deployment)
    
    Platform Languages: Python, Type Script, JavaScript and Java


    [About]:
    OpenVisual is a service which provides access to Real Estate and Rental Images to users.
    It has three main components. 

    1) Image Collection System:
       This system allows OpenVisual to extract images by using large scale webscraping.
       OpenVisual Launches Bots periodically to collect Images and store them in central database.
       Flexible system allows many bots to be launched remotely from a client
    
    2) Image Provider system:
       This system allows users on internet to connect over Http:// Endpoint and request images on a given
       property address. Upon Match server returns the images. Users can request multiple listings or single listings
       over two different endpoints. 
    
    3) Admin Client
       A program that allows OpenVisual Admins to manage, control and update central database by remotely launching
       bots over a private http:// endoint
    """
    return Details

@app.route("/ResideLibraryVerbose/Images", methods=["POST", "GET"])
def ListingImagesEndpointVerbose():
    responses = []
    response = ServerResponse()
        
    print("inside route")
    if(request.is_json == True):
        try:
            array = request.get_json()["Listings"]
            print("array here",array)
            if(len(array) == 0):
                response.set_error(True)
                response.put_error_log('No Images when listings are not given')
                return response.get()
        
        except KeyError as error:
            response.set_error(True)
            response.put_error_log("'Listing' key is  missing in json data")
            print("'Listing' key is  missing in json data")
            return response.get()
        
        for element in array:
            print("element array")
            responses.append(listing_images_service.fetch(element))         
            response.set_error(False)
            response.put_payload(responses)
            return response.get()
        
    else:
        response.set_error(True)
        response.put_error_log('Data is not json')
        return response.get()
               
@app.route("/ResideLibrary/Images", methods=["POST", "GET"])
def ListingImagesEndpoint():
    if(request.is_json == True):
        try:
            address = request.get_json()["Listing"]
            print("listing here",address)
            if(len(address) == 0):
                print('No Images when listing are not given')
                return 'None'
            
        except KeyError as error:
            print("'Listing' key is  missing in json data")
            return 'None'
        
        listing = listing_images_service.fetch(address)
        if(listing != None and listing != False):
            print(listing)
            return listing["Images"]
        else:
            return 'None'
    else:
        return 'None'
     

@app.route("/endpoint", methods=["POST", "GET", "PUT"])
def endpoint():
    try:
        object = "None"
        if(request.is_json == True):
            object = request.get_json()
        else:
            object = request.get_data()
        print(str(object))
    except Exception as error:
        print(error)
    return "this is endpoint"


#FLASK CONFIGURED WITH GUNICORN
#WSGI IP PORT = 0.0.0.0 FOR EXTERNAL ACCESS
if __name__ == "__main__":
    print("entered wsgi.py ....")
    print("app is running")
    app.run(host='0.0.0.0', port=80)