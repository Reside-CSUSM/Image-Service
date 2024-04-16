
# DATE: 4/15/2024 7:25 PM
#1) When update is trigger from Console.py after the city is deleted it still launches the bot which will cause stuff be stored back in database
    If city doesn't exist then UPDATE shudn't occur unless the city exists in the first place.
# SOL: Put a check that solves this problem in databasehandler.py

