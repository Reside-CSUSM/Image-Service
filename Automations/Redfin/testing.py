from Redfin.redfin_bot import RedfinBot, OpenVisual_DB


#OpenVisual_DB.disable()
bot = RedfinBot()
bot.activate()
bot.save_filters(['For rent'])
print(bot.address('5210 Rain Creek Pkwy, Austin, TX', 'specific').location('specific').get_response())
print(bot.address('Chula Vista, CA').location('general').get_response())