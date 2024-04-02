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
        document["San Jose"] = []
        collection.find_one_and_update({"_id":data["_id"]}, {"$set":document})

    def delete_collection(self, name):
        collection = self.database[name]
        collection.drop()


database = Database()
#database.create_collection("California/San-Diego")
USA = {
    "_id":"USA",
    "California":{
        "San-Diego":"this"
    },
    "Texas":[],
    "Argentina":[],
    "San Fransico":[]
}

database.udpate_collection("@MetaData", USA)
#CRUD on States, Cities, and Listings