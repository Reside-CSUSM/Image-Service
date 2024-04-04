
COUNTRY_ABBREVIATION = {
    "India":"IND",
    "United States of America":{
        "_abbreviation":"USA",
        "_states":{
            "California":"CA",
            "Arizona":"AZ"
        }
        },
    "Australia":"AUS",
    "China":"CN"
}


class CountryResolver():

    def ResolveToAbbr(name):
        try:
            return COUNTRY_ABBREVIATION[name]
        except Exception as error:
            return None

    def ResolveToName(abbr):
        list = COUNTRY_ABBREVIATION.items()
        for item in list:
            if(item[1] == abbr):
                return item[0]
        return None
    


class City():

    def __init__(self):
        self._current_city = None
        self._current_state = None
        self._current_country = None

    def recieve_data(self, data):
        self._current_city = data['city']
        self._current_state = data['state']
        self._current_country = data['country']
    
    def GetAbbr(self):
        pass
    
    def GetList(self):
        pass

    def Add(self):
        pass

    def Delete(self):
        pass

    def Search(self):
        pass


    
class State():

    def __init__(self):
        self._current_state = None
        self._current_country = None
        self.city = City()

    def recieve_data(self, data):
        self._current_state = data['state']
        self._current_country = data['country']
    
    def GetAbbr(self):
        pass

    def City(self, name):
        pass
    
    def GetList(self):
        pass
    
    def Add(self):
        pass

    def Delete(self):
        pass

    def Search(self):
        pass

class Country():

    def __init__(self):
        self._current_country = None
        self.state = State()
        pass
    
    def GetList(self):
        pass
    
    def GetAbbr(self):
        pass
    
    def State(self, name):
        data = {
            'country':self._current_country
        }
        self.state.recieve_data(data)
        return self.state
        
    def Country(self, name):
        self._current_country = name

    def Add(self):
        pass

    def Delete(self):
        pass

    def Search(self):
        pass

class Map():

    country = Country()
    def GeoMap():
        return Map.country
