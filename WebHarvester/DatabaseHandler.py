from MongoDB.OpenVisualDB import OpenVisualDB, STATE_ABBREVIATION, string_filter
from WebHarvester.AutomationService import AutomationService


OpenVisual_DB = OpenVisualDB()
Automation_Service = AutomationService()


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
    
    def perform(self):
        self._response = OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(self.request_data['State']).City(self.request_data['City']).Delete()
        
        
        

class OperationAddHandler(Operation):
     
    def __init__(self):
        super().__init__()
        self._response = None
    
    def perform(self):
        self._response = OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(self.request_data['State']).City(self.request_data['City']).Create()


class OperationDeleteHandler(Operation):
     
    def __init__(self):
        super().__init__()
        self._response = None
    
    def perform(self):
        self._response = OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(self.request_data['State']).City(self.request_data['City']).Delete()
        pass

    def response(self):
        pass

class OperationSearchHandler(Operation):
     
    def __init__(self):
        super().__init__()
        self._response = None
    
    def perform(self):
        self._response = OpenVisual_DB.ResideActionChain().Country(self.request_data['Country']).State(self.request_data['State']).City(self.request_data['City']).Search()

    def response(self):
        return self._response



class OpenVisualDatabaseHandler():

    def __init__(self):
        self.operation_value = None
        self.response = None
        self.data = None

        self.operations = {
            'UPDATE':OperationUpdateHandler(),
            'DELETE':OperationDeleteHandler(),
            'ADD':OperationAddHandler(),
            'SEARCH':OperationSearchHandler()
        }

    def __start_operation(self):
        self.operations[self.data['Operation']].perform()

    def __prepare_operation(self):
        self.operations[self.data['Operation']].save_data(self.data)

    def handle(self, data):
        self.operation_value = data['Operation']
        self.data = data
        self.__prepare_operation()
        self.__start_operation()
    
    def get_response(self):
        return self.operations[self.operation_value].response()