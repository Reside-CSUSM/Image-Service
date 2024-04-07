import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path + "\\Redfin")
print(sys.path[0], "<--this")
from Redfin.redfin_bot import RedfinBot


class RedfinInterface():

    BOT  = None
    TYPE = 'specific'

    def create_bot():
        RedfinInterface.BOT = RedfinBot()

    def close_bot():
        RedfinInterface.BOT.close()

    def activate():
        RedfinInterface.BOT.activate()

    def search_images(value):
        #RedfinInterface.BOT.activate()
        type = RedfinInterface.TYPE
        response = RedfinInterface.BOT.location(RedfinInterface.TYPE).address(value).get_response()
        #RedfinInterface.BOT.close()
        return response
    
    def type(value):
        RedfinInterface.TYPE = value

    def apply_filters(filters):
        RedfinInterface.BOT.save_filters(filters)
