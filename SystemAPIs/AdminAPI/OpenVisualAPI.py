import requests
import copy
import json
import socket




class AutomationLauncher():

    def __init__(self):
        #PURPOSE:
        #1) Launch individual automations on a remote server with 'save data' mode disabled
        #2) Configure Automation setting to be parsed onto the server
        self.automation_settings = None
    
    def LaunchAutomation(self):
        return self
    
    def ConfigureSettings(self, settings):
        pass



class OpenVisualCRUD():

    def __init__(self):
        #PURPOSE:
        #Sends individual CRUD commands to server which will initiate commands to database
        pass

    def Update(self):
        #Server will first delete the entire cache for specific area first in mongoDB
        #Server then will launch bots with 'collection' mode enabled for to add the same area again
        #Will update country, state or city depending on what's provided
        pass

    def Add(self):
        #Simply sends command to server create a new collection in database
        pass
    
    def Delete(self):
        #Requires Country, State and City to be listed
        #Sends command to server to delete a specific collection in database
        pass

    def Search(self):
        pass


#Server needs to send complete logs of what's happending during each process when deleting, updating or adding areas.
class OpenVisualAPI():

    def __init__(self):
        pass