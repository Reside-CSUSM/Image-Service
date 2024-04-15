import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
sys.path.insert(0, sys.path[0] + "\\MongoDB")
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from MongoDB.GeoMapper import CountryResolver
from MongoDB.utility import string_filter, STATE_ABBREVIATION, Flag, STATE_FULL_NAME, STATE_NAMES
import copy


TEMPLATE = {
    "_id":"country_name",
    "_abbreviation":"",
    "_states":{
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

#FAKE ROOT CLASS
class _Generic():

    def __init__(self):
        pass

    def Create(self):
        print("Parent doesn't exist to perform child.Create()")
        return False
    
    def Upate(self):
        print("Paren't doesn't exist to perform child.Update()")
        return False

    def Search(self):
        print("Parent doesn't exist to child.search()")
        return False
    
    def Delete(self):
        print("Parent doesn't exist to child.delete()")
        return False

#FAKE CLASS:
class _Listing(_Generic):

    def __init__(self):
        super().__init__()

#FAKE CLASS:
class _City(_Generic):

    def __init__(self):
        super().__init__()
        self.listing = _Listing()
    
    def Listing(self, name):
        return self.listing

#FAKE STATE
class _State(_Generic):

    def __init__(self):
        super().__init__()
        self.city = _City()

    def City(self, name):
        return self.city

#FAKE CLASS
class _Country(_Generic):

    def __init__(self):
        super().__init__()
        self.state = _State()
    
    def State(self, name):
        return self.state
    

#FAKE CLASSES (LAZY PATCH):
#Description: Fake classes are created to prevent chains from breaking if error is thrown
#Example: OpenVisualDB.CRUD().Country("USA").State("CA").City("San Diego").Update()
#Here if any of these things (country, states, cities and listings) throw error because parent doesn't exist
#the chain would break causing managment issues when chains are used as commands. 
#So fake classes are returned are used instead of thrown error 'None' so since parent doesn't exist/invalid
#then all the actions of childs become invalid also because exact same functions are empty in fake classes

# (NOT A GOOD SOLUTION): It's possibly to detect parent-child relationship validity without stupid fake class solution
#NOTE: Needed to work on many more backlogged features and this kinda got left out
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
        
    def __listing_exists(self, get_listing=False):
        if(self.__collection_exists() == False):
            return False
        
        PATH  = self._current_country + "/" + self._current_state + "/" + self._current_city
        collection = self.database[PATH]
        document = collection.find_one({"Address":self._current_listing})
        #BUG HERE, value is returning none if not found but if statement below is not catching it
        if(str(type(document)) == "<class 'NoneType'>"):
            return False
        else:
            if(get_listing == True):
                return dict(document)
            return True

    def recieve_meta_data(self, data):
        self._current_listing = data['listing']
        self._current_city = data['city']
        self._current_state = data['state']
        self._current_country = data['country']

    def Create(self, data=None):
        print("Listing", self._current_listing, end="")
        if(self.__listing_exists() == True):
            print("...Already exists")
            return True
        
        #If listing doesn't exist then create the collection
        if(self.__collection_exists() == False):
            self.database.create_collection(self._current_country + "/" + self._current_state + "/" + self._current_city)
        
        #Fetch the collection from the database now
        collection = self.database[self._current_country + "/" + self._current_state + "/" + self._current_city]
       
       #If data is not given for the current listing then just create a basic template
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
            if(value == None): 
                print("...Couldn't create(error)")
                return False
            else:
                print("...Created")
                return True

        #Otherwise set the key values to given current values of city, state and country
        else:
            data['Address'] = self._current_listing
            data['City'] = self._current_city
            data['State'] = self._current_state
            value = collection.insert_one(data)
            if(value == None):
                print("...Couldn't create(error)")
                return False
            else:
                print("...Created")
                return True
        
    def Delete(self):
        print("Deleted", self._current_listing, end="")
        if(self.__listing_exists() == False):
            print("...Doesn't exist to Delete")
            return False
        
        #Get the collection
        collection = self.database[self._current_country + "/" + self._current_state + "/" + self._current_city]
        #Delete the collection
        value = collection.find_one_and_delete({"Address":self._current_listing})
        if(value == None):
            print("...\x1b[31mCouldn't delete (error)/x1b[0m")
            return False
        else:
            print("...Deleted")
            return True
    
    def Search(self):
        print("Searching", self._current_listing, end="")
        doc = self.__listing_exists(True)

        if(isinstance(doc, dict) == True):
            return doc
        
        if(doc == True):
            print("...Found")
            return True
        
        print("...Not found")
        return False
    

    def Update(self, data):
        print("Updating", self._current_listing, end="")
        if(self.__listing_exists() == False):
            print("...Doesn't exist to update")
            return False
        
        #Get collection
        collection = self.database[self._current_country + "/" + self._current_state + "/" + self._current_city]
        #Get listing from the collection 
        listing = collection.find_one({"Address":self._current_listing})

        #create the same keys in listing as well and assign them second value
        for item in data.items():
            listing[item[0]] = item[1]

        #Update the givend data
        value = collection.find_one_and_update({"Address":self._current_listing}, {"$set":listing})
        if(value == None):
            print("...Couldn't Update(error)")
            return False
        
        else:
            print("...Updated")
            return True


class City(__CRUD__):

    def __init__(self, database):
        super().__init__()
        self.database = database
        self.meta_data_collection = self.database["@MetaData"]
        
        self.listing = Listing(database)

        self._current_city = None
        self._current_state = None
        self._current_state = None
    
    #Checks if city exists
    def __city_exists(self):
        try:
            value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
            states = value["_states"]
            city = states[self._current_state][self._current_city]
            return True
        except Exception as error:
            return False

    def __collection_exists(self, get_collection=False):
        PATH  = self._current_country + "/" + self._current_state + "/" + self._current_city
        list = self.database.list_collection_names()
        if(PATH in list):
            if(get_collection==True):
                return self.database[PATH]
            return True
        else:
            return False
        
    def recieve_meta_data(self, data):
        self._current_city = data['city']
        self._current_state = data['state']
        self._current_country = data['country']

    def SelectCity(self, name):
        self._current_city = name
        return self
    
    def GetCurrentCity(self):
        return self._current_city

    def Create(self, params=None):
        print("Creating City", self._current_city, end = "")
        if(self.__city_exists() == True):
            print("...Already Exists")
            return True
        
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        state = states[self._current_state]
        state[self._current_city] = {}

        self.meta_data_collection.find_one_and_update({"_id":self._current_country}, {"$set":value})
        print("...Created")
        return True

    def Delete(self):
        print("Deleting City", self._current_city, end = "")
        if(self.__city_exists() == False):
            print("...Doesn't exist to delete")
            return False
        
        #Find the state from @MetaData then from state get the city and then update it with 'value'
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        states[self._current_state].pop(self._current_city)
        self.meta_data_collection.find_one_and_update({"_id":self._current_country}, {"$set":value})

        #CHECK: If collection exists for current city then delete it
        collection = self.__collection_exists(True)
        if(collection != False):
            collection.drop()
        print("...Deleted")
        return True
    
    def Search(self):
        print("Searching", self._current_city, end="")
        if(self.__city_exists() == False):
            print("...Not found")
            return False
        
        print("...Found")
        return True
        
        
    def Update(self, city_data):
        print("Updating", self._current_city, end="")
        if(self.__city_exists() == False):
            print("...Doesn't exist to Update")
            return False
        
        #Get the state and then the city 
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        state = states[self._current_state]
        listings = state[self._current_city]

        #Create same keys as in city_data with the value of item assigned in listing for those keys
        for item in city_data.items():
            listings[item[0]] = item[1]

        #Update the data here
        self.meta_data_collection.find_one_and_update({"_id":self._current_country}, value)
        print("...Updated")

    def Listing(self, name):
       
        if(self.__city_exists() == False):
            return _Listing()
            #return None
        
        data = {
            'country':self._current_country,
            'state':self._current_state,
            'city':self._current_city,
            'listing':name
        }
        self.listing.recieve_meta_data(data)
        return self.listing
    
    def EstimateListings(self):
        return self.__collection_exists(True).estimate_document_count()
    
    def GetAllListings(self):
        list = self.__collection_exists(True).find({})
        new_list = []

        for listing in list:
            new_list.append(listing['Address'])
        return new_list



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

    def SelectState(self, name):
        self._current_state = name
        return self
    
    def GetCurrentState(self):
        return self._current_state
    
    def Create(self, date=None):
        #CHECK if the state already exists
        print("Creating", self._current_state, end="")
        if(self.__state_exists() == True):
            print("...Already exists")
            return True
        
        #Find the country and then find the state
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        state = value["_states"]
        state[self._current_state] = {}

        #Update the country->state chain now using latest value
        self.meta_data_collection.find_one_and_update({"_id":self._current_country}, {"$set":value})
        print("...Created")
        return True
    

    def Delete(self):
        #CHECK
        print("Deleting", self._current_state, end="")
        if(self.__state_exists() == False):
            print("...Already Doesn't exists")
            return False
    
        #Get all city object and delete them
        to_be_deleted = self.GetAllCities()
        
        #Invoke city object and use it to delete collections which represent areas
        for city in to_be_deleted:
            data = {'city':city, 'country':self._current_country, 'state':self._current_state}
            self.city.recieve_meta_data(data)
            self.city.SelectCity(city).Delete()

        #Then find current country then state from metadata file and delete that entry as well
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        value["_states"].pop(self._current_state)
        self.meta_data_collection.find_one_and_update({"_id":self._current_country}, {"$set":value})
        print("...Deleted")
        return True


    def EstimateCities(self):
        #KEEP Track of the count number and return it
        pass
    
    def GetAllCities(self):
        list = self.database.list_collection_names()
        new_list = []
        for element in list:
            if(self._current_country + "/" + self._current_state  in element):
                new_list.append(element.split("/")[2])
        return new_list


    def Search(self):
        print("Searching", self._current_state, end="")
        if(self.__state_exists() == False):
            print("...Doesn't exist to search")
            return False
        
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        
        if(self._current_state in states.keys()):
            print("...Found")
            return True

        print("...Not Found")
        return False


    def Update(self, state_data):
        print("Update", self._current_state, end="")
        if(self.__state_exists() == False):
            print("...Doesn't exist to update")
            return False
        
        #Find state and then city
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        cities = states[self._current_state]
        
        #Create or atleast use same keys in cities as given in state_data then assign back the values
        for item in state_data.items():
            cities[item[0]] = item[1]
        
        #Update the entries in metadata as well
        self.meta_data_collection.find_one_and_update({"_id":self._current_country}, {"$set":value})
        print("...Updated")
        return True
    
    
    def Fetch(self):
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        
        for state in states.keys():
            if(state == self._current_state):
                return state
        return False
    
    def City(self, name):
       
        if(self.__state_exists() == False):
            #return None
            return _City()
        data = {
            'country':self._current_country,
            'state':self._current_state,
            'city':name
        }
        self.city.recieve_meta_data(data)
        return self.city


class Country(__CRUD__):

    def __init__(self, database):
        #Initialize, database, metadata collection, state object for chaining 
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

    def SelectCountry(self, name):
        self._current_country = name
        return self

    def GetCurrentCountry(self):
        return self._current_country
    
    def Create(self, data=None):
        #Check if it already exists if yes then exit
        print("Creating", self._current_country, end="")
        if(self.__country_exists()==True):
            print("....Country Already Exists")
            return True

        #create a copy of template
        template = copy.copy(TEMPLATE)
        #set the id to the name
        template["_id"] = self._current_country

        try:
            #Convert the full name of country to it's abbreviation
            template["_abbreviation"] = CountryResolver.ResolveToAbbr(self._current_country)
        except Exception as error:
            template["_abbreviation"] = self._current_country

        #create a new template for the new country within metadata collection which stores templates
        #for every country
        value = self.meta_data_collection.insert_one(template)
        if(value == None):
            print(".../x1b[31mCouldn't Create (error)/x1b[0m")
            return False
    
        else: 
            print("...Created")
            return True
    
    def Delete(self):
        #Delete the collections as well
        print("Deleting", self._current_country, end="")
        if(self.__country_exists() == False):
            print("... Doesn't exist to Delete")
            return False
        
        #Get all the states and delete them
        to_be_deleted = self.GetAllStates()

        for state in to_be_deleted:
            data = {'country':self._current_country, 'state':state}
            self.state.recieve_meta_data(data)
            self.state.SelectState(state).Delete()

        value = self.meta_data_collection.find_one_and_delete({"_id":self._current_country})
        if(value == None):
            print(".../x1b[31mCouldn't delete (error)/x1b[0m")
            return False
        print("...Deleted")
        return True 
    

    def EstimateStates(self):
        #KEEP Track of the count number and return it
        pass
    
    def GetAllStates(self):
        new_list = []
        list = self.database.list_collection_names()

        for element in list:
            if(self._current_country in element):
                new_list.append(element.split("/")[1])
        return new_list
    
    def Search(self):
        print("Searching", self._current_country, end="")
        if(self.__country_exists() == False):
            print("...Doesn't exist to search")
            return False
        
        value = self.meta_data_collection.find_one({"_id":self._current_country})
        if(value == None):
            print(".../x1b[31mNot Found (error)/x1b[0m")
            return False
        elif(value != None):
            print("...Found")
            return True

    def Fetch(self):
        if(self.__country_exists() == False):
            return False
        
        document = self.meta_data_collection.find_one({"_id":self._current_country})
        if(document != None):
            return dict(document)
        return False

    def Update(self, updated_template):
        print("Updating", self._current_country, end="")
        if(self.__country_exists() == True):
            print("...Doesn't Exist to Update")
            return True
        
        if(("_id" in updated_template.keys()) == False):
            print(".../x1b[31mCouldn't update (error)/x1b[0m")
            return False
        
        value = dict(self.meta_data_collection.find_one({"_id":self._current_country}))
        states = value["_states"]
        
        for item in updated_template.items():
            states[item[0]] = item[1]

        self.meta_data_collection.find_one_and_update({"_id":self._current_country}, {"$set":value})
        if(value == None):
            print(".../x1b[31mCouldn't update (error)/x1b[0m")
            return False
    
        else: 
            print("...Updated")
            return True

    def State(self, name):
        if(self.__country_exists() == False):
            #Important to return None to preserve the action relationship between structured entities. 
            #User shudn't be able to perform operation on child entity unless parent entity exists
            #If state doesn't city can't exist either so why perform operations.
            #The reason being is child shouldn't have to worry about if parent exists or not when processing infor
            #This reduces code and ensures that child entities don't have to keep a check on parents to know if parent's attributes/instance itself exists in database
            #return None
            return _State()
        
        data = {
            'country':self._current_country,
            'state':name
        }
        print("End of state")
        self.state.recieve_meta_data(data)
        return self.state


#Shouldn't need to use this technique
#SOLUTION: In order to prevent child keeping check on parents, parents can let child know by setting a flag.
#then those child can let their child know by setting the flag. At most mongoDB would return None if database[Country][State][City] Didn't exist
#also same thing for collection right now just do _Generic but fix this issue as soon as possible

class ActionChainRoot():

    def __init__(self, database):
        self.database = database
        self.country = Country(database)

    def EstimateCountries(self):
        #KEEP Track of the count number and return it
        pass
    
    def GetAllCountries(self):
        new_list = []
        list = self.database.list_collection_names()

        for element in list:
            new_list.append(element.split("/")[0])
        
        return new_list
    
    def Country(self, name):
        print("Inside Country()")
        data = {
            'country':name
        }
        self.country.recieve_meta_data(data)
        return self.country

    def Delete(self):
        print("Deleting All Collection")
        to_be_deleted = self.GetAllCountries()

        for country in to_be_deleted:
            data = {'country':country}
            self.country.recieve_meta_data(data)
            self.country.SelectCountry(country).Delete()

        print("....Deleted")
    

class OpenVisualDB():

    def __init__(self):
        self.uri = "mongodb+srv://yashaswikul:yash18hema06@cluster0.vktjrwl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.mongo_client = MongoClient(self.uri, server_api=ServerApi('1'))
        self.database = self.mongo_client["OpenVisualDB"]
        self.action_chain_root = ActionChainRoot(self.database)
        self.disable_flag = False
        
    def disable(self):
        self.disable_flag = True

    def enable(self):
        self.disable_flag = False
        
    def ResideActionChain(self):
        if(self.disable_flag == True):
            return None
        
        return self.action_chain_root
