from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flag import Flag
from GeoMapper import CountryResolver
import copy


TEMPLATE = {
    "_id":"country_name",
    "_abbreviation":"",
    "_states":{
        "California":{

        }
    }
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
        self.meta_data_collection = self.database["@MetaData"]
        super().__init__()
        self._current_listing = None
        self._current_city = None
        self._current_state = None
        self._current_country = None

    def __collection_exists(self):
        PATH  = self._current_country + "/" + self._current_state + "/" + self._current_city
       
        list = self.database.list_collection_names()
        if(PATH in list):
            return True
        else:
            return False
        
    def __listing_exists(self):
        if(self.__collection_exists() == False):
            return False
        
        PATH  = self._current_country + "/" + self._current_state + "/" + self._current_city
        collection = self.database[PATH]
        value = collection.find_one({"Address":self._current_listing})
        #BUG HERE, value is returning none if not found but if statement below is not catching it
        if(str(type(value)) == "<class 'NoneType'>"):
            return False
        else:
            return True
        

    def recieve_meta_data(self, data):
        self._current_listing = data['listing']
        self._current_city = data['city']
        self._current_state = data['state']
        self._current_country = data['country']

    def Create(self, data=None):
        if(self.__listing_exists() == True):
            return True
        
        if(self.__collection_exists() == False):
            self.database.create_collection(self._current_country + "/" + self._current_state + "/" + self._current_city)
        
        collection = self.database[self._current_country + "/" + self._current_state + "/" + self._current_city]
        if(data == None):
            template = {
                'Address':"",
                'City':"",
                'State':""
            }
            template['Address'] = self._current_listing
            template['City'] = self._current_city
            template['State'] = self._current_state
            value = collection.insert_one(template)
            if(value == None): return False
            else:return True
        else:
            data['Address'] = self._current_listing
            data['City'] = self._current_city
            data['State'] = self._current_state
            value = collection.insert_one(data)
            if(value == None): return False
            else:return True
        

    def Delete(self):
        if(self.__listing_exists() == False):
            return True
        
        collection = self.database[self._current_country + "/" + self._current_state + "/" + self._current_city]
        value = collection.find_one_and_delete({"Address":self._current_listing})
        if(value == None):return False
        else:return True
    
    def Search(self):
        return self.__listing_exists()
    

    def Update(self, data):
        if(self.__listing_exists() == False):
            return False
        
        collection = self.database[self._current_country + "/" + self._current_state + "/" + self._current_city]
        listing = collection.find_one({"Address":self._current_listing})

        for item in data.items():
            listing[item[0]] = item[1]

        value = collection.find_one_and_update({"Address":self._current_listing}, {"$set":listing})
        if(value == None): return False
        else:return True
        


class City(__CRUD__):

    def __init__(self, database):
        super().__init__()
        self.database = database
        self.meta_data_collection = self.database["@MetaData"]
        
        self.listing = Listing(database)

        self._current_city = None
        self._current_state = None
        self._current_state = None
    
    def __city_exists(self):
        try:
            value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
            states = value["_states"]
            city = states[self._current_state][self._current_city]
            return True
        except Exception as error:
            return False

    def recieve_meta_data(self, data):
        self._current_city = data['city']
        self._current_state = data['state']
        self._current_country = data['country']

    def Create(self, params=None):
        if(self.__city_exists() == True):
            return True
        
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        state = states[self._current_state]
        state[self._current_city] = {}

        self.meta_data_collection.find_one_and_update({"_id":self._current_country}, {"$set":value})
        return True

    def Delete(self):
        if(self.__city_exists() == False):
            return False
        
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        states[self._current_state].pop(self._current_city)
        self.meta_data_collection.find_one_and_update({"_id":self._current_country}, value)
        return True
    
    
    def Search(self):
        if(self.__city_exists() == False):
            return False
        
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        try:
            city = states[self._current_state][self._current_city]
            return True
        except Exception as error:
            return False
        
        
    def Update(self, city_data):
        if(self.__city_exists() == False):
            return False
        
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        state = states[self._current_state]
        listings = state[self._current_city]

        for item in city_data.items():
            listings[item[0]] = item[1]

        self.meta_data_collection.find_one_and_update({"_id":self._current_country}, value)

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
    
    def __state_exists(self):
        try:
            value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
            
            value = value["_states"][self._current_state]
    
            return True
        except Exception as error:
            print(error)
            return False

    def recieve_meta_data(self, data):
        self._current_state = data['state']
        self._current_country = data['country']


    def Create(self, date=None):
        #CHECK
        if(self.__state_exists() == True):
            return True
        
        print("country", self._current_country)
        print("state", self._current_state)
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        state = value["_states"]
        state[self._current_state] = {}
        self.meta_data_collection.find_one_and_update({"_id":self._current_country}, {"$set":value})
        return True
        
    def Delete(self):
        #CHECK
        if(self.__state_exists() == False):
            return False
    
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        value["_states"].pop(self._current_state)
        self.meta_data_collection.find_one_and_update({"_id":self._current_country}, {"$set":value})
        return True

    def Search(self):
        if(self.__state_exists() == False):
            return False
        
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        
        if(self._current_state in states.keys()):
            return True

        return False

    def Update(self, state_data):
        if(self.__state_exists() == False):
            return False
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        cities = states[self._current_state]
        
        for item in state_data.items():
            cities[item[0]] = item[1]
        
        self.meta_data_collection.find_one_and_update({"_id":self._current_country}, {"$set":value})
        return True
    
    
    def Fetch(self):
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        
        for state in states.keys():
            if(state == self._current_state):
                return state
        return False
    
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
    
    def __country_exists(self):
        value = self.meta_data_collection.find_one({"_id":self._current_country})
        if(value == None):return False
        else: return True
        
    def recieve_meta_data(self, data):
        self._current_country = data['country']

    def Create(self, data=None):
        #Check if it already exists if yes then exit
        if(self.__country_exists()==True):
            return True

        template = copy.copy(TEMPLATE)
        template["_id"] = self._current_country
        template["_abbreviation"]= CountryResolver.ResolveToAbbr(self._current_country)

        value = self.meta_data_collection.insert_one(template)
        if(value == None):return False
        else: return True
    
    def Delete(self):
        #Delete the collections as well
        if(self.__country_exists() == False):
            return False
        
        value = self.meta_data_collection.find_one_and_delete({"_id":self._current_country})
        if(value != None):
            return True
        else: return False 

    def Search(self):
        if(self.__country_exists() == False):
            return False
        
        value = self.meta_data_collection.find_one({"_id":self._current_country})
        if(value == None):
            return False
        elif(value != None):
            return True

    def Fetch(self):
        if(self.__country_exists() == False):
            return False
        
        document = self.meta_data_collection.find_one({"_id":self._current_country})
        if(document != None):
            return dict(document)
        return False

    def Update(self, updated_template):
        if(self.__country_exists() == True):
            return True
        
        if(("_id" in updated_template.keys()) == False):
            return False
        
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        
        for item in updated_template.items():
            states[item[0]] = item[1]

        self.meta_data_collection.find_one_and_update({"_id":self._current_country}, {"$set":value})
        if(value == None):return False
        else: return True

    def State(self, name):
        data = {
            'country':self._current_country,
            'state':name
        }
        self.state.recieve_meta_data(data)
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
value = open_visuals.ResideActionChain().Country("United States of America").Create()
print(value)
#value = open_visuals.ResideActionChain().Country("United States of America").State("California").Update({})
value = open_visuals.ResideActionChain().Country("United States of America").State("California").City("Otay Ranch").Listing("111 Roosevelt S").Search()
#value = open_visuals.ResideActionChain().Country("United States of America").State("California").City("Otay Ranch").Listing("111 Roosevelt St").Update({"Filter":None, "HomeCard":"maphome_135"})
print(value)