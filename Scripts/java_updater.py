import requests
import time

city = ""
state = ""
url = "http://localhost:8080/listings/createByCityState?city="+city+"&state="+state
#http://localhost:8080/listings/createByCityState?city=San+Diego&state=California


locations = [("Carlsbad", "California"),
             ("Chula Vista", "California"),
             ("Del Mar", "California"),
             ("El Cajon", "California"),
             ("Encinitas", "California"),
             ("Escondido", "California"),
             ("Imperial Beach", "California"),
             ("La Mesa", "California"),
             ("Lemon Grove", "California"),
             ("National City", "California"),
             ("Oceanside", "California"),
             ("Poway", "California"),
             ("San Diego", "California"),
             ("San Marcos", "California"),
             ("Santee", "California"),
             ("Solana Beach", "California"),
             ("Vista", "California"),
             ("San Ysidro", "California"),
             ("La Jolla", "California"),
             ("Spring Valley", "California"),
             ("Ramona", "California"),
             ("Valley Center", "California"),
             ("Bonsall", "California"),
             ("Rancho Santa Fe", "California"),
             ("Pauma Valley", "California"),
             ("Jamul", "California"),
             ("Bonita", "California"),
             ("Coronado", "California"),
             ("Julian", "California"),
             ("Pine Valley", "California"),
             ("Descanso", "California")
             ]


def add_plus(city):
    print("add_plus() before", city)
    if(city.find(" ") == -1):
        return city
    city = city.replace(" ", "+")

    print("add_plus() after", city)
    return city


def add_rentcast_listings_by_city_state(city, state):
    headers =  {'Content-Type': 'application/json'}
    try:
            url = "http://localhost:8080/listings/createByCityState?city="+city+"&state="+state
            response = requests.post(url, headers=headers)
            print(response.json())
            time.sleep(1)
    except Exception as error:
            print(city, state, " error!")


def process_listings():      
      for location in locations:
            print("\x1b[31mPROCESSING: \x1b[0m", location[0], location[1])
            add_rentcast_listings_by_city_state(add_plus(location[0]), location[1])

def console_hardcoded():
    #processes everything in the locations list

    print("begin processing everything in the locations array? N/Y")
    val = input()
    if(val == "N" or val == "n"):
        return
    
    elif(val == "Y" or val == "y"):
         process_listings()
         pass
    
      

def console_ask_user():
    #asks user for city and state
    while(True):
        print("Enter city for rentcast", end=" ")
        city = input()
        if(city == "none"):
             continue
        elif(city == "exit"):
             break
        

        print("\nEnter the state NAME (California, Texas..etc) for rentcast", end=" ")
        state = input()
        if(state == "none"):
             continue
        elif(state == "exit"):
             break
        
        add_rentcast_listings_by_city_state(add_plus(city), state)

def start():
      
      while(True):
        print("[1] Use hardcoded values in locations array")
        print("[2] Ask for each (City, State) each time")
        print("[3] Exit")
        val = input()

        if(val == "1"):
            console_hardcoded()
            
        elif(val == "2"):
            console_ask_user()
        
        elif(val == "3"):
             break
        else: continue
        break
      

start()



"""
#HOW DOES THIS UPDATE WORK?
This script basically connects to endpoint of reside java backend called createByCityState/
it will put in the city and state into the url so that backend and put in those areas in the primary database


#Clone the reside-backend in a folder first
#Run the java backend on local machine now
    - Make sure gradle, springboot and java jdk are installed

#Now listing_updater can use the reside backend's url which is hosted in local host

#Now make the request to createByCityState endpoint to update the listings using rentcast.

"""