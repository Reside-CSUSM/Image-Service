
# DATE: 4/15/2024 7:25 PM
#1) When update is trigger from Console.py after the city is deleted it still launches the bot which will cause stuff be stored back in database
    If city doesn't exist then UPDATE shudn't occur unless the city exists in the first place.
# SOL: Put a check that solves this problem in databasehandler.py



# DATE 4/25/2024 9:14PM
#1) When scraping listings of a city sometimems, reedfin lists listings from nearby 
cities as well. So in the database, it will store listings of wrong county if that happens


#2) If city entered in redfin search is bar kinda confusing to redfin then redfin 
would show you a dialog box after u enter in the search bar, the bot doesn't handle it
real life example of whatever the date this was written on.
eg Coronado, CA      if you type this in it would show dialog box after u enter this in saerch box. 



# DATE 5/8/2024 10:59 PM
1) Noticed that 'images' attribute in mongoDb document for each listing only contained at most 3 image urls. After debugging later it was found that 
   redfin has changed how the images are loaded and displayed on those little listing boxes. If you click little arrows then you can clearly see rest of the other images just loading after the arrow button is clicked. This is why it has been happening. 

   SOL: To adapt the code to this change by clicking on the arrow button as well so that it doesn't happen again