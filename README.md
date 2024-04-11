# OpenVisuals
A service which provides real estate property images for Reside Housing Platform.


#Design
Service consists of two main components, a collector and a provider. Collector collects images through websraping and is provider=D over a public http endpoint "https://open-visuals.vercel.app/ResideLibrary/Images" using flask. Entire project is hosted on vercel platform.

WebHarvester Folder -> Collector component
WebProvider Folder -> Provider component

#HOW TO START PROJECT

1) Clone the repository on your pc
   
2) Running collector service

    2.1) Navigate to FlaskServer.py under WebHarvester


