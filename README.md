# OpenVisuals
A service which provides real estate property images for Reside Housing Platform.


#Design
Service consists of two main components, a collector and a provider. Collector collects images through websraping and is provider=D over a public http endpoint 
"https://image-service-pi.vercel.app/ResideLibrary/Images" using flask. Entire project is hosted on vercel platform.

WebHarvester Folder -> Collector component
WebProvider Folder -> Provider component

#HOW TO START PROJECT

1) Clone the repository on your pc
   
2) Running collector service
    #How it works?  It basically launches a selenium bot which scrapes the data from redfin site.

    2.1) Navigate to FlaskServer.py under WebHarvester
         and run the file
    2.2) Now Navigate to console.py under AdminClient and run the file
         You will see several command options to run now
         you can select options such as 'delete area', 'update area' and 'add area' and more. After entering type in relevant details
         States can be typed in either abbreviation or fullname with first letter capital
         Cities need to have first letter capital in their name for each word

4) Provider service is run automatically which is hosted on vercel. Use the public http endoint to recieve cached images on a given address
   how it works? All the data is stored in mongoDB database which is provided through a webserver flask app which has public http endpoints

6) Edit Vercel Hosting configuration for project
   4.1) Go to requirements.txt to add the required modules for the project
   4.2) You can also edit vercel.json file to configure what builds to run as well any default routes that should run specific files
        More fields can be added for routing as well any other needs.


         


