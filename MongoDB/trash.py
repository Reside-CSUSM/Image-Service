from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import copy
#mongodb+srv://yashaswikul:<password>@cluster0.vktjrwl.mongodb.net/
uri = "mongodb+srv://yashaswikul:yash18hema06@cluster0.vktjrwl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


LISTING_TEMPLATE = {
    "Address": "",
    "Price": "",
    "State": "",
    "City": "",
    "ZipCode": "",
    "Street": "",
    "Stats": [
        "$1,945/mo",
        "1 bed",
        "1 bath",
        "\u2014 sq ft",
        "21 Del Mar Ave, Chula Vista, CA 91910",
        "A/C \u2022 Somewhat walkable \u2022 Some transit",
        "Request a tour"
    ],
    "ListingNumber": "",
    "WebElementID": "MapHomeCard_93",
    "Filters": {
        "Filter Settings": {
            "Payement Type": "None",
            "Price Range": {
                "Price Range": {
                    "Minimum": "None",
                    "Maximum": "None"
                }
            },
            "Home Type": "None",
            "BedsAndBath": {
                "BedsAndBath": {
                    "Beds": "None",
                    "Baths": "None"
                }
            },
            "Payment Type": {
                "Payment Type": "For rent"
            },
            "Home type": {
                "Home Type": "None"
            }
        }
    },
    "Images": [
        "https://ssl.cdn-redfin.com/photo/rent/0f9060b1-ce29-4a37-a466-7a322d29e180/islphoto/genIsl.0_1.jpg",
        "https://ssl.cdn-redfin.com/photo/rent/0f9060b1-ce29-4a37-a466-7a322d29e180/islphoto/genIsl.1_1.jpg",
        "https://ssl.cdn-redfin.com/photo/rent/0f9060b1-ce29-4a37-a466-7a322d29e180/islphoto/genIsl.2_1.jpg",
        "https://ssl.cdn-redfin.com/photo/rent/0f9060b1-ce29-4a37-a466-7a322d29e180/islphoto/genIsl.3_1.jpg",
        "https://ssl.cdn-redfin.com/photo/rent/0f9060b1-ce29-4a37-a466-7a322d29e180/islphoto/genIsl.4_1.jpg",
        "https://ssl.cdn-redfin.com/photo/rent/0f9060b1-ce29-4a37-a466-7a322d29e180/islphoto/genIsl.5_1.jpg",
        "https://ssl.cdn-redfin.com/photo/rent/0f9060b1-ce29-4a37-a466-7a322d29e180/islphoto/genIsl.6_1.jpg",
        "https://ssl.cdn-redfin.com/photo/rent/0f9060b1-ce29-4a37-a466-7a322d29e180/islphoto/genIsl.7_1.jpg",
        "https://ssl.cdn-redfin.com/photo/rent/0f9060b1-ce29-4a37-a466-7a322d29e180/islphoto/genIsl.8_1.jpg",
        "https://ssl.cdn-redfin.com/photo/rent/0f9060b1-ce29-4a37-a466-7a322d29e180/islphoto/genIsl.9_1.jpg",
        "https://ssl.cdn-redfin.com/photo/rent/0f9060b1-ce29-4a37-a466-7a322d29e180/islphoto/genIsl.10_1.jpg"
    ]
}

#States, Cities, Listings
class Database():

    def __init__(self):
        self.database = client["OpenVisualDB"]
        pass

    def create_collection(self, name):
        self.database.create_collection(name)

    def search_collection(self, name):
        collection = self.database[name]
        return collection

    def udpate_collection(self, name, data):
        collection = self.database[name]
        document = collection.find_one({"_id":data["_id"]})
        if(document == None): return
        document = dict(document)
        document["San Jose"] = []
        print(document)
        document.pop("San Jose")
        print(document)
        collection.find_one_and_update({"_id":data["_id"]}, {"$set":document})
        collection.find_one_and_delete()
        collection.estimated_document_count()

    def delete_collection(self, name):
        collection = self.database[name]
        collection.drop()


database = Database()
#database.create_collection("California/San-Diego")

USA = {
    "_id":"TUSA",
    "California":{
        "San-Diego":"this"
    },
    "Texas":[],
    "Argentina":[],
    "San Fransico":[]
}

database.udpate_collection("@MetaData", USA)
#CRUD on States, Cities, and Listings


"""value = open_visuals.ResideActionChain().Country("United States of America").State("Texas").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("California").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("California").City("Al Paso").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("California").City("Al Paso").Listing("222 Roosevelt St").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("California").City("Al Paso").Listing("222 Roosevelt St").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("California").City("Al Paso").Listing("222 Roosevelt St").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("Texas").City("Al Paso").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("Texas").City("Al Paso").Listing("222 Roosevelt St").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("Texas").City("Al Paso").Listing("222 Roosevelt St").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("Texas").City("Al Paso").Listing("222 Roosevelt St").Create()"""


"""value = open_visuals.ResideActionChain().Country("United States of America").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("Texas").Create()

value = open_visuals.ResideActionChain().Country("United States of America").State("Texas").City("Al Paso").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("Texas").City("Al Paso").Listing("111 Roosevelt St").Create()




value = open_visuals.ResideActionChain().Country("United States of America").State("California").Create()

value = open_visuals.ResideActionChain().Country("United States of America").State("California").City("San Diego").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("California").City("San Diego").Listing("222 Roosevelt St").Create()


value = open_visuals.ResideActionChain().Country("United States of America").State("California").City("San Marcos").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("California").City("San Marcos").Listing("333 Roosevelt St").Create()



value = open_visuals.ResideActionChain().Country("United States of America").State("Arizona").Create()

value = open_visuals.ResideActionChain().Country("United States of America").State("Arizona").City("San Diego").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("Arizona").City("San Diego").Listing("222 Roosevelt St").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("Arizona").City("San Marcos").Create()
value = open_visuals.ResideActionChain().Country("United States of America").State("Arizona").City("San Marcos").Listing("333 Roosevelt St").Create()
"""