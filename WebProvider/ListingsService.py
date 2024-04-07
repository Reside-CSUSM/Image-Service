import sys, os
sys.path.insert(0, r'C:\Users\yasha\Visual Studio Workspaces\OpenVisuals\OpenVisuals')
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
from MongoDB.OpenVisualDB import OpenVisualDB, string_filter, STATE_ABBREVIATION, STATE_NAMES
import copy

class ListingService():

    def __init__(self):
        self.open_visual = OpenVisualDB()
        self.response = "None"
    
    def get_response(self):
        return self.response
    
    def fetch(self, address):
        #Use good techniques to extract the State, City, and Listing values. 
        #Address must be formatted as "Street, City, State" For example "5500 Grand Lake Dr, San Antonio, TX 78244"
        global state_abbreviation, state
        state = ""
        first_list = address.split(",")
        second_list = address.split(", ")
        list = first_list
        address_line = ""
        city = ""

        if(len(first_list) >= 3):
            address_line = first_list[0]
            if("Unit" in first_list[1]):
                print("orginal address (" + address_line + ")")
                address_line += " " + string_filter(first_list[1])
                print("new address", address_line)
            city = string_filter(first_list[-2])
            print("STATE ABR recieved Original: (" + first_list[-1] + ")")

            #If Zipcode isn't given then just the abbr will be in the array for eg ['CA'] instead of ['CA', '91912']
            state_abbreviation = string_filter(copy.copy(first_list)[-1]).split(" ")[0]
            print("STATE ABR", state_abbreviation)
            list = first_list


        elif(len(second_list) >= 3):
            address_line = second_list[0]
            if("Unit" in second_list[1]):
                address_line = string_filter(address_line)
                print("orginal address (" + address_line + ")")
                address_line += " " + string_filter(second_list[1])
                print("new address", address_line)
            
            city = string_filter(second_list[-2])
            print("STATE ABBR prev:", second_list[-1])
            #state_abbreviation =  string_filter(copy.copy(second_list[-1].split(" ")[0]))
            state_abbreviation = second_list[-1].split(" ")[0]
            print("STATE ABR", state_abbreviation)
            list = second_list

        else:
            print("ERROR: State, City or Address component missing")
            return None


        if(len(list[2]) < 2):
            print("Invalid State Abbreviation Extracted: ", state_abbreviation)
            return None
        
        elif(len(list[2]) > 2):
            state_abbreviation  = state_abbreviation.replace(" ", "")

        try:
            #state = STATE_ABBREVIATION[state_abbreviation]
            state = STATE_NAMES[state_abbreviation].GetFullName()
            print("State Abbr   = (" + state_abbreviation, "     len = " + str(len(state_abbreviation)))
            print("State        = (" + state, "     len = " + str(len(state)))
            print("City         = (" + city, "     len = " + str(len(city)))
            print("Address      = (" + address_line, "     len = " + str(len(address_line)))
        except Exception as error:
            print("THERE'S NO SUCH STATE", state_abbreviation)

        else:
            try:
        
                val = self.open_visual.ResideActionChain().Country("USA").State(state).City(city).Listing(address_line).Search()
                #val = False
                if(val == False): return None
                self.response = {
                    'ListingIdentifier':address,
                    'MatchedWith':val['Address'],
                    'Images':val['Images']
                }
                return self.response
            except Exception as error:
                print(error)
                return False
        
            
        def fetch2(self, address):
            #NOTE: ADDRESS EXAMPLE: "Street, City, State" For example "5500 Grand Lake Dr, San Antonio, TX 78244"
            global state_abbreviation, state
            state = ""
            first_list = address.split(", ")
            second_list = address.split(",")
            list = first_list
            address_line = ""
            city = ""

            if(len(first_list) >= 3):
                address_line = first_list[0]
                city = first_list[1]
                state_abbreviation = first_list[2]
                list = first_list

            elif(len(second_list) >= 3):
                address_line = second_list[0]
                city = second_list[1]
                state_abbreviation = copy.copy(second_list[2])
                list = second_list

            else:
                print("ERROR: State, City or Address component missing")
                return False


            if(len(list[2]) < 2):
                print("Invalid State Abbreviation Extracted: ", state_abbreviation)
                return False
            
            elif(len(list[2]) > 2):
                state_abbreviation  = state_abbreviation.replace(" ", "")

            try:
                state = STATE_ABBREVIATION[state_abbreviation]
                print("State Abbr   = ", state_abbreviation, "     len = " + str(len(state_abbreviation)))
                print("State        = ", state, "     len = " + str(len(state)))
                print("City         = ", city, "     len = " + str(len(city)))
                print("Address      = ", address_line, "     len = " + str(len(address_line)))
            except Exception as error:
                print("THERE'S NO SUCH STATE", state_abbreviation)

            else:
                val = self.open_visual.ResideActionChain().State(state).City(city).Listing(address_line).Search()
                if(val == False):
                    return None
                else:
                    self.response = val["Images"]
                    return self.response