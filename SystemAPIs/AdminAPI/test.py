from AdminAPI.OpenVisualAPI import OpenVisualAPI

open_visual_api = OpenVisualAPI()

#value = open_visual_api.CRUD().Add().Country("USA").State("California").City("Otay Ranchers").Perform()
data = {
    'Images':[]
}
value = open_visual_api.CRUD().Update().Country("USA").State("California").City("La Mesa").Perform()
#value = open_visual_api.CRUD().Add().Country("USA").State("California").City("")
print(value)

"""
[IDEA]:  #PURPOSE:
        #1) Launch individual automations on a remote server with 'save data' mode disabled
        #2) Configure Automation setting to be parsed onto the server

[UPDATE]#Server will first delete the entire cache for specific area first in mongoDB
        #Server then will launch bots with 'collection' mode enabled for to add the same area again
        #Will update country, state or city depending on what's provided

[DELETE]#Requires Country, State and City to be listed
        #Sends command to server to delete a specific collection in database

[ADD] #Simply sends command to server create a new collection in database

"""