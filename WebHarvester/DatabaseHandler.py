from MongoDB.OpenVisualDB import OpenVisualDB, STATE_ABBREVIATION, string_filter,  STATE_FULL_NAME, STATE_NAMES
from WebHarvester.AutomationService import AutomationService
from WebHarvester.AutomationLauncher import AutomationLauncher

OpenVisual_DB = OpenVisualDB()
Automation_Service2 = AutomationService()
Automation_Service = AutomationLauncher()

class Operation():

    def __init__(self):
        self.operation_name = "None"
        self.request_data = "None"
        self._response = "None"
    
    def perform(self):
        pass
    
    def response(self):
        return self._response
    
    def save_data(self, data):
        self.request_data = data


class OperationUpdateHandler(Operation):

    def __init__(self):
        super().__init__()
        self.automation_settings = {
            'Area':"None",
            'Filter':'None'
        }
    
    def perform(self):
        #What if commands were dynamic and then you had to use parameters
        #Possibility is to use Binary tree or some data structure based method with parent-child relationship
        try: state = STATE_NAMES[self.request_data['State']].GetFullName()
        except: state = self.request_data['State']
        commands = {
            'Country':OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']),
            'State':OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(state),
            'City':OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(state).City(self.request_data['City']),
            'Listing':OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(state).City(self.request_data['City']).Listing(self.request_data['Listing'])
        }


        if(self.request_data['Listing'] != '$None'):
            delete_response = commands['Listing'].Delete()
            if(delete_response == True):
                if(self.request_data['AdditionalListingData'] != '$None'):
                    create_response = commands['Listing'].Create(self.request_data['AdditionalListingData'])
                    print("added data")
                else: create_response = commands['Listing'].Create()
            
        elif(self.request_data['City'] != '$None'): 
            delete_response_city = commands['City'].Delete()
            if(delete_response_city == True):
                create_response = commands['City'].Create()

        #DON'T ALLOW OPERATION ON STATES AND COUNTRIES
        elif(self.request_data['State'] != '$None'): 
            delete_response = commands['State'].Delete()
            if(delete_response == True):
                create_response = commands['State'].Create()

        elif(self.request_data['Country'] != '$None'): 
            delete_response = commands['Country'].Delete()
            if(delete_response == True):
                create_response = commands['Country'].Create()

        #Invoke Automation Launcher to re collect data and update the database

        try: state_abbr = STATE_NAMES[self.request_data['State']].GetAbbr()
        except: state_abbr = self.request_data['State']
        self.automation_settings['Area'] = self.request_data['City'] + ", " + state_abbr
        self.automation_settings['Filter'] = 'For sale'
        Automation_Service.select_automation('Redfin')
        Automation_Service.handover_settings(self.automation_settings)
        Automation_Service.launch()

        self.automation_settings['Filter'] = 'For rent'
        Automation_Service.select_automation('Redfin')
        Automation_Service.handover_settings(self.automation_settings)
        Automation_Service.launch()


class OperationAddHandler(Operation):
     
    def __init__(self):
        super().__init__()
        self._response = "None"
        self.automation_settings = {
            'Area':"None",
            'Filter':'None'
        }
    
    def perform(self):
        try: state = STATE_NAMES[self.request_data['State']].GetFullName()
        except: state = self.request_data['State']

        #CHAIN: Country->state->city->listing
        #For a given chain of any number of nodes, check if the chain already exists if not then add otherwise don't add and don't launch bots

        response = False
        #Shouldn't launch bots if city is already there
        if(self.request_data['Country'] != '$None'):
            self._response = OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).Create()
        
            if(self.request_data['State'] != '$None'):
                self._response = OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(state).Create()
                
                if(self.request_data['City'] != '$None'):
                    response = OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(state).City(self.request_data['City']).Search()
                    self._response = OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(state).City(self.request_data['City']).Create()
                    
                    if(self.request_data['Listing'] != '$None'):
                        if(self.request_data['AdditionalListingData'] != '$None'):
                            self._response = OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(state).City(self.request_data['City']).Listing(self.request_data['Listing']).Create(self.request_data['AdditionalListingData'])
                            return
                        self._response = OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(state).City(self.request_data['City']).Listing(self.request_data['Listing']).Create()


        #Invoke Automation Handler To add new cities
        if(response == True): return

        #Run the following automation commands only when areas are given.
        if(self.request_data['State'] != '$None' and self.request_data['City'] != '$None' and self.request_data['Listing'] == '$None'):
            try: state_abbr = STATE_NAMES[self.request_data['State']].GetAbbr()
            except: state_abbr = self.request_data['State']
            self.automation_settings['Area'] = self.request_data['City'] + ", " + state_abbr
            self.automation_settings['Filter'] = 'For sale'
            Automation_Service.select_automation('Redfin')
            Automation_Service.handover_settings(self.automation_settings)
            Automation_Service.launch()

            self.automation_settings['Filter'] = 'For rent'
            Automation_Service.select_automation('Redfin')
            Automation_Service.handover_settings(self.automation_settings)
            Automation_Service.launch()



class OperationDeleteHandler(Operation):
     
    def __init__(self):
        super().__init__()
        self._response = "None"
    
    def perform(self):
        commands = {
            'Country':"$None",
            'State':'$MNone',
            'City':'$None',
            'Listing':'$None'
        }

        #Convert the given state in either form abr/full name to fullname
        try: state = STATE_NAMES[self.request_data['State']].GetFullName()
        except: state = self.request_data['State']

        #Get the individual chain nodes like Country->state->city->listing
        commands['Country'] = OpenVisual_DB.ResideActionChain().Country(self.request_data['Country'])
        commands['State'] = OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(state)
        commands['City'] = OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(state).City(self.request_data['City'])
        commands['Listing'] = OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(state).City(self.request_data['City']).Listing(self.request_data['Listing'])

        print(self.request_data, " perform delete")
        #If any OpenVisual_DB commands return 'None' then use try except to prevent termination
        if(self.request_data['Listing'] != '$None'): self._response = commands['Listing'].Delete()
        elif(self.request_data['City'] != '$None'): self._response = commands['City'].Delete()
        elif(self.request_data['State'] != '$None'): self._response = commands['State'].Delete()
        elif(self.request_data['Country'] != '$None'): self._response = commands['Country'].Delete()
          

class OperationSearchHandler(Operation):
     
    def __init__(self):
        super().__init__()
        self._response = "None"
    
    def perform(self):

        #Get the state name by converting it to fullname otherwise just get whatever value is for state
        try: state = STATE_NAMES[self.request_data['State']].GetFullName()
        except: state = self.request_data['State']

        #Store the different structures like 'Country' 'State' and 'City and 'Listing'
        #Chain Country->State->City->Listing
        #Important because the operations can be performed on chains of any number of nodes.
        commands = {
            'Country':OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']),
            'State':OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(state),
            'City':OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(state).City(self.request_data['City']),
            'Listing':OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(state).City(self.request_data['City']).Listing(self.request_data['Listing'])
        }

        if(self.request_data['Listing'] != '$None'): self._response = commands['Listing'].Search()
        elif(self.request_data['City'] != '$None'): self._response = commands['City'].Search()
        elif(self.request_data['State'] != '$None'): self._response = commands['State'].Search()
        elif(self.request_data['Country'] != '$None'): self._response = commands['Country'].Search()


class OpenVisualDatabaseHandler():

    def __init__(self):
        self.operation_value = None
        self.response = "No response"
        self.data = None

        self.operations = {
            'UPDATE':OperationUpdateHandler(),
            'DELETE':OperationDeleteHandler(),
            'ADD':OperationAddHandler(),
            'SEARCH':OperationSearchHandler()
        }

    #Run the operation by fetching correct key and invoking operation object
    def __start_operation(self):
        try:
            self.response = self.operations[self.data['Operation']].perform()
        except Exception as error:
            print("can't ___start() operation OpenVisualDatabaseHandler()", error)

    #Initialize and select the correct operation by fetching 'operation' to perform
    def __prepare_operation(self):
        try:
            self.operations[self.data['Operation']].save_data(self.data)
        except Exception as error:
            print("can't ___prepare() operation OpenVisualDatabaseHandler()", error)

    def handle(self, data):
        self.operation_value = data['Operation']
        self.data = data
        self.__prepare_operation()
        self.__start_operation()
    
    def get_response(self):
        return self.operations[self.operation_value].response()
