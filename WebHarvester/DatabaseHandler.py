

class Operation():

    def __init__(self):
        self.operation_name = "None"
    
    def perform(self):
        pass
    
    def response(self):
        pass

class OperationUpdate(Operation):

    def __init__(self):
        super().__init__()
    
    def perform(self):
        pass

    def response(self):
        pass

class OperationAdd(Operation):
     
    def __init__(self):
        super().__init__()
        self._response = None
    
    def perform(self):
        pass

    def response(self):
        pass

class OperationDelete(Operation):
     
    def __init__(self):
        super().__init__()
        self._response = None
    
    def perform(self):
        pass

    def response(self):
        pass

class OperationSearch(Operation):
     
    def __init__(self):
        super().__init__()
        self._response = None
    
    def perform(self):
        pass

    def response(self):
        pass

class OpenVisualDatabaseHandler():

    def __init__(self):
        self.operation_value = None
        self.response = None

        self.operations = {
            'UPDATE':OperationUpdate(),
            'DELETE':OperationDelete(),
            'ADD':OperationAdd(),
            'SEARCH':OperationSearch()
        }

    def __start_operation(self, name):
        self.operations[name].perform()

    def handle(self, operation_value):
        self.operation_value = operation_value
    
    def get_response(self):
        return self.operations[self.operation_value].response()

