import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
dir = parent_dir_path.replace("\Automations", "")
sys.path.insert(0, dir)
print(sys.path[0], "<--this")
from Redfin.redfin_bot import RedfinBot, OpenVisual_DB


OpenVisual_DB.disable()
bot = RedfinBot()
bot.activate()
bot.save_filters(['For sale'])
#print(bot.address('5210 Rain Creek Pkwy, Austin, TX', 'specific').location('specific').get_response())
#print(bot.address('Chula Vista, CA').location('general').get_response())
print(bot.address('Austin, TX').location('general').get_response())