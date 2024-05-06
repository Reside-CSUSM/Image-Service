#sys.path.insert(0, r"C:\Users\kulsh001\AppData\Local\Programs\Python\Python311\Lib\site-packages")
import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
print(sys.path[0], "<--this")
from flask import Flask, request

#Remove this header please
from bson import ObjectId
from WebProvider.ListingsService import ListingService

#Enable this header pls
#from .ListingsService import ListingService


########### [TEMPORARY IMPORTS]###########
#CODE SECTION ID: JAVA_BACKEND
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
#########################################

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
    OpenVisual Cloud deployment\n
    ____________________________\n

    [Details]\n
    Component: WebProvider\n
    Platform:  Vercel\n
    Language:  Python\n
    \n
    Component: WebHarvester\n
    Platform:  Vercel\n
    Language: Python\n
    \n
    [Tech Stack For Reside Platform]:\n
    Selenium\n
    MongoDB\n
    SpringBoot\n
    React.js\n
    Next.js\n
    Vercel(Cloud Deployment)\n
    \n
    Platform Languages: Python, Type Script, JavaScript and Java\n
    \n
    \n
    [About]:\n
    OpenVisual is a service which provides access to Real Estate and Rental Images to users.\n
    It has three main components.\n 
    \n
    1) Image Collection System:\n
       This system allows OpenVisual to extract images by using large scale webscraping.\n
       OpenVisual Launches Bots periodically to collect Images and store them in central database.\n
       Flexible system allows many bots to be launched remotely from a client\n
    \n
    2) Image Provider system:\n
       This system allows users on internet to connect over Http:// Endpoint and request images on a given\n
       property address. Upon Match server returns the images. Users can request multiple listings or single listings\n
       over two different endpoints.\n 
    \n
    3) Admin Client\n
       A program that allows OpenVisual Admins to manage, control and update central database by remotely launching\n
       bots over a private http:// endoint\n
       \n
    """
    return Details

#################################### [TEMPORARY]####################
#CODE SECTION ID: JAVA_BACKEND
#Temporary routes, only available because of java deployment doesn't work
##Added 5/5/2024

uri2 = "mongodb+srv://to-Gabriel:zynsog-5Ziwso-syfniw@residecluster.uyk5fmd.mongodb.net/reside-backend"
uri = "mongodb+srv://yashaswikul:yash18hema06@cluster0.vktjrwl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(uri2, server_api=ServerApi('1'))
database = mongo_client["reside-backend"]

@app.route("/addUserFavoriteListing", methods=['GET', 'POST'])
def AddUserFavoriteListing():
    listingId = request.args.get('listingId', type=str ,default='')
    listingId = ObjectId(listingId)
    userId = request.args.get('userId', type=str ,default='')

    #Adds the user which favorited to listing collection which contains seenBy array
    listing_collection = database.get_collection("listings")  
    listing = listing_collection.find_one({"_id":listingId})

    print("args:", listingId, userId)
    #Return with message if listing doesn't exist  
    if(listing == None):
        print(listing, " failed value")
        return "Listing with this ID doesn't exists"
    
    for id in listing["viewedBy"]:
        if(userId == id):
            return "user already exists"
        
    #Add the user here
    #WARNING: It doesn't check here the status of update command here before returning success message
    listing["viewedBy"].append(userId)
    listing_collection.find_one_and_update({"_id":listingId}, {"$set":listing})
    return "user has been successfully added to listing viewedBy array"

@app.route("/deleteUserFavoriteListing", methods=['GET', 'POST'])
def DeleteUserFavoriteListing():
    listingId = request.args.get('listingId', type=str ,default='')
    listingId = ObjectId(listingId)
    userId = request.args.get('userId', type=str ,default='')

    #removes the user which favorited to listing collection which contains seenBy array
    listing_collection = database.get_collection("listings")  
    listing = listing_collection.find_one({"_id":listingId})

    print("args:", listingId, userId)
    #Return with message if listing doesn't exist  
    if(listing == None):
        print(listing, " failed value")
        return "Listing with this ID doesn't exists"
    
    found = False
    for id in listing["viewedBy"]:
        if(userId == id):
            found = True
    
    if(found == False):
        return "User already doesn't exists"
    
    #Add the user here
    #WARNING: It doesn't check here the status of update command here before returning success message
    listing["viewedBy"].remove(userId)
    listing_collection.find_one_and_update({"_id":listingId}, {"$set":listing})
    return "user has been successfully removed from the listing viewedBy array"

####################################################################################################




@app.route("/ResideLibraryVerbose/Images", methods=["POST", "GET"])
def ListingImagesEndpointVerbose():
    responses = []
    response = ServerResponse()
        
    print("inside route")
    #Check if the data is json or not
    if(request.is_json == True):
        try:
            #get the json data and extract listings requested in it
            array = request.get_json()["Listings"]
            print("array here",array)
            if(len(array) == 0):
                response.set_error(True)
                response.put_error_log('No Images when listings are not given')
                return response.get()
        
        except KeyError as error:
            #if listing wasn't given construct a response
            response.set_error(True)
            response.put_error_log("'Listing' key is  missing in json data")
            print("'Listing' key is  missing in json data")
            return response.get()
        
        for element in array:
            #process each listing that was given and append resulsts
            print("element array")
            responses.append(listing_images_service.fetch(element))         
            response.set_error(False)
            response.put_payload(responses)
            return response.get()
        
    else:
        #return the error code if request was not json
        response.set_error(True)
        response.put_error_log('Data is not json')
        return response.get()


#On this route, only send image data in very simple format
@app.route("/ResideLibrary/Images", methods=["POST", "GET"])
def ListingImagesEndpoint():

    #Check if client put data in a correct json format
    if(request.is_json == True):
        try:

            #If yes then parse 'listing' s from it 
            address = request.get_json()["Listing"]
            print("listing here",address)
            if(len(address) == 0):
                print('No Images when listing are not given')
                return 'None'
            
        except KeyError as error:
            #Otherwise indicate client didn't put in 'listing' key
            print("'Listing' key is  missing in json data")
            return 'None'
        
        #Invoke the service to fetch images on the given address
        listing = listing_images_service.fetch(address)

        #if anything else except None and False is recieved then no images were found
        if(listing != None and listing != False):
            print(listing)
            return listing["Images"]
        
        #otherwise indicate images weren't found
        else:
            return 'None'
    
    #Request data isn't json
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