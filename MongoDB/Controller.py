from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flag import Flag
from GeoMapper import CountryResolver
import copy


TEMPLATE = {
    "_id":"country_name",
    "_abbreviation":"",
    "_states":{}
}

class __CRUD__():
    
    def __init__(self):
        pass
    
    def Create(self):
        pass

    def Delete(self):
        pass

    def Search(self):
        pass

    def Update(self, name):
        pass

    def Fetch(self):
        pass


class Listing(__CRUD__):

    def __init__(self, database):
        self.database = database
        super().__init__()
        self._current_listing = None
        self._current_city = None
        self._current_state = None
        self._current_country = None

    def recieve_meta_data(self, data):
        self._current_listing = data['listing']
        self._current_city = data['city']
        self._current_state = data['state']
        self._current_country = data['country']

    def Create(self):
        pass

    def Delete(self):
        pass
    
    def Search(self):
        pass

    def Update(self, name):
        pass


class City(__CRUD__):

    def __init__(self, database):
        super().__init__()
        self.database = database
        self.meta_data_collection = self.database["@MetaData"]
        
        self.listing = Listing(database)

        self._current_city = None
        self._current_state = None
        self._current_state = None
    
    def recieve_meta_data(self, data):
        self._current_city = data['city']
        self._current_state = data['state']
        self._current_country = data['country']

    def Create(self, name):
        pass

    def Delete(self, name):
        pass
    
    def Search(self, name):
        pass

    def Update(self, name):
        pass

    def Listing(self, name):
        data = {
            'country':self._current_country,
            'state':self._current_state,
            'city':self._current_city,
            'listing':name
        }
        self.listing.recieve_meta_data(data)
        return self.listing
    

class State(__CRUD__):

    
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.meta_data_collection = self.database["@MetaData"]    
        self.city = City(database)
        self._current_state = None
        self._current_country = None
    

    def recieve_meta_data(self, data):
        self._current_state = data['state']
        self._current_country = data['country']


    def Create(self):
        #CHECK
        try:
            value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
            value = self.meta_data_collection["_states"][self._current_state]
            return True
        except Exception as error:

            return False
        
        pass

    def Delete(self):
        pass

    def Search(self):
        pass

    def Update(self, name):
        pass
    
    def Fetch(self):
        pass
    
    def City(self, name):
        data = {
            'country':self._current_country,
            'state':self._current_state,
            'city':name
        }
        self.city.recieve_meta_data(data)
        return self.city


class Country(__CRUD__):

    def __init__(self, database):
        super().__init__()
        self.database = database
        self.meta_data_collection = self.database["@MetaData"]
        self.state = State(database)
        self._current_country = None
    
    def recieve_meta_data(self, data):
        self._current_country = data['country']

    def Create(self):
        #Check if it already exists if yes then exit
        collection = self.meta_data_collection.find_one({"_id":self._current_country}) 
        if(collection != None): return None

        template = copy.copy(TEMPLATE)
        template["_id"] = self._current_country
        template["_abbreviation"]= CountryResolver.ResolveToAbbr(self._current_country)

        value = self.meta_data_collection.insert_one(template)
        if(value == None):return False
        else: return True
    
    def Delete(self):
        #Delete the collections as well
        value = self.meta_data_collection.find_one_and_delete({"_id":self._current_country})
        if(value != None):
            return True
        else: return False 

    def Search(self):
        value = self.meta_data_collection.find_one({"_id":self._current_country})
        if(value == None):
            return False
        elif(value != None):
            return True

    def Fetch(self):
        document = self.meta_data_collection.find_one({"_id":self._current_country})
        if(document != None):
            return dict(document)
        return False

    def Update(self, updated_template):
        if(("_id" in updated_template.keys()) == False):
            return False
        value = self.meta_data_collection.find_one_and_update({"_id":self._current_country}, {"$set":updated_template})
        if(value == None):return False
        else: return True

    def State(self, name):
        data = {
            'country':None,
            'state':name
        }
        self.state.__recieve_meta_data(data)
        return self.state


class ActionChainRoot():

    def __init__(self, database):
        self.country = Country(database)

    def Country(self, name):
        data = {
            'country':name
        }
        self.country.recieve_meta_data(data)
        return self.country


class OpenVisual():

    def __init__(self):
        self.uri = "mongodb+srv://yashaswikul:yash18hema06@cluster0.vktjrwl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.mongo_client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.database = self.mongo_client["OpenVisualDB"]
        self.action_chain_root = ActionChainRoot(self.database)

    def ResideActionChain(self):
        return self.action_chain_root


open_visuals = OpenVisual()
value = open_visuals.ResideActionChain().Country("India").Search()
print(value)
value = open_visuals.ResideActionChain().Country("India").Delete()
print(value)
value = open_visuals.ResideActionChain().Country("India").Create()
print(value)
