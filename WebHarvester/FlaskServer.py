import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
from flask import Flask, request
from AutomationService import AutomationService
app = Flask(__name__)


class ServerResponse():

    def __init__(self):
        
        self.payload = {
            'RecipientPayload':None,
            'Errors':False,
            'ErrorLog':[]
        }
    
    def put_payload(self, payload):
        self.payload['RecipientPayload'] = payload
    
    def get(self, field=None):
        if(field == None):
            return self.payload
        else:
            try:
                return self.payload[field]
            except Exception as error:
                return None
    
    def set_error(self, val):
        if(isinstance(val, bool) == False):
            raise "\x1b[31m ServerResponse: Error Flag Not Boolean!!\x1b[0m"
        self.payload['Errors'] = val
    
    def put_error_log(self, log):
        self.payload['ErrorLog'].append(log)



automation_service = AutomationService()

@app.route("/")
def root():
    return "cloud server is running"

@app.route("/automations/query=<value>", methods=["POST","GET"])
def SecondaryAutomationEndpoint(value):
        automation_service.handle("/query="+value, 'POST')
        response = automation_service.get_response()
        print("Automation route works")
        if(isinstance(response, str) == False):
            return str(response)    
        return response
    
@app.route("/Automations", methods=["POST", "GET"])
def PrimaryAutomationEndpoint():
        if(request.is_json == False):
            return "Data wasn't json"
        #RIGHT THERE IMPLEMENT ERROR PROPAGATION USING ERROR() OBJECTS
        response = automation_service.handle2(request.get_json(), 'POST').get_response()
        return str(response)
         
          
@app.route("/endpoint", methods=["POST", "GET", "PUT"])
def endpoint():
    try:
        object = "None"
        if(request.is_json == True):
            object = request.get_json()
        else:
            object = request.get_data()
        print(str(object))
    except Exception as error:
        print(error)
    return "this is endpoint"


#FLASK CONFIGURED WITH GUNICORN
#WSGI IP PORT = 0.0.0.0 FOR EXTERNAL ACCESS
if __name__ == "__main__":
    print("entered wsgi.py ....")
    print("app is running")
    app.run(host='0.0.0.0', port=80)
