import sys, os
sys.path.insert(0, r'C:\Users\yasha\Visual Studio Workspaces\OpenVisuals\OpenVisuals')
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
import copy
import json
import urllib.parse

#AUTOMATION MODULES
from Automations.Redfin.interface import *
from Automations.Redfin.redfind_errors import *


class RedfinLauncher():

    def __init__(self):
        self.response = "No Response"
        self.data = {
            'Area':"None",
            "Filter":"None"
        }

    def save_settings(self, data):
        #save settings 
        self.data['Area'] = data['Area']
        self.data['Filter'] = data['Filter']

    def launch(self):
        #ALL these steps need need to happen in order run the bot
        RedfinInterface.create_bot()
        RedfinInterface.activate()
        RedfinInterface.type("general")
        RedfinInterface.apply_filters([self.data['Filter']])
        self.response = RedfinInterface.search_images(self.data['Area'])
        RedfinInterface.close_bot()
        return self.response
        

class AutomationLauncher():

    def __init__(self):
        self.current_automation = None
        self.response = None
        self.available_automations = {
            'Redfin':RedfinLauncher()
        }
    
    def handover_settings(self, data):
        #handover the recieved settings from client to the bot launcher
        if(self.current_automation == None): return
        self.available_automations[self.current_automation].save_settings(data)
    
    def select_automation(self, name):
        #slect the which automation to run
        try:
            self.current_automation = name
        except Exception as error:
            self.current_automation = None

    def launch(self):
        #launch the automation
        if(self.current_automation == None): return
        self.response = self.available_automations[self.current_automation].launch()
        

