import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
import time
from ImageryAdapter import ResideImageryAdapter
image_api = ResideImageryAdapter()


TARGET_IP = ''
TARGET_PORT = ''

class Host():
    TARGET_IP = ''
    TARGET_PORT = ''


class AreaUpdate(ResideImageryAdapter):

    def __init__(self, city, state):
        self._city = city
        self._state = state
        self.filter1 = 'For rent'
        self.filter2 = 'For sale'
        ResideImageryAdapter.__init__(self)
        self.initialize(Host.TARGET_IP, Host.TARGET_PORT)

    def run(self):
        print("["+self._city+", " + self._state +"]", "\x1b[32mUPDATING.....\x1b[0m")
        self.add_general_search_filter(self.filter2)
        self.add_areas(self._city + ", " + self._state)
        try:
            val = self.search_area()
            print(val)
        except Exception as error:
            print("\x1b[31m Update 'For sale' Failed!\x1b[0m")
            #print(error)
            #print("\x1b[31mConnection closed or host in correct,  use 'set host' to set ip and port\x1b[0m")

        time.sleep(1)
        self.add_general_search_filter(self.filter1)
        self.add_areas(self._city + ", " + self._state)
        
        try:
            val = self.search_area()
            print(val)
        except Exception as error:
            print("\x1b[31m Update 'For rent' Failed!\x1b[0m")
            #print(error)
            #print("\x1b[31mConnection closed or host in correct,  use 'set host' to set ip and port\x1b[0m")
        print("Update Finished.....\n\n\n")


class CacheUpdates():

    def __init__(self):
        self.list = []

    def run(self):
        for list in self.list:
            list.run()
    
    def append(self, update):
        if(isinstance(update, AreaUpdate) == False):
            return False
        self.list.append(update)


def console():
    image_api.initialize('38.56.138.77', 8888)
    cache_updates = CacheUpdates()
    while(True):
        os.system('cls')
        print("Select Options: [add areas, set host, run search, exit, show areas, delete, update areas, start updates, search housing]")
        val = input()

        if(val == "update areas"):
            while(True):
                print("\n/update> ", end="")
                print("Enter the name of (State) ", end="")
                state = input()
                
                if(state == "exit"):break
                elif(state == "none"):continue

                print("Enter the name of (City) ", end="")
                city = input()
                if(city == "exit"):break
                elif(city == "none"):continue
                cache_updates.append(AreaUpdate(city, state))


        elif(val == "start updates"):
            cache_updates.run()
            val = input()

        elif(val == "search housing"):

            while(True):
                print("\n/search housing> ", end="")
                print("Enter the full address(Street Addr, City, State, ZipCode) ", end="")
                value = input()

                if(value == "exit"):
                    break
                response = image_api.housing().add_housing(value).send_calls()
                image_api.housing().delete_all()

                print("\x1b[32m___API Response___\x1b[0m")
                print(response)
                
            
        elif(val == "add areas"):

            while(True):
                print("\n/add> ", end="")
                print("Enter the name of (City, State) ", end="")
                val = input()
                area = ""
                filter = ""
                if(val == "exit"):break
                elif(val == "none"):continue
                else: area = val

                print("['For rent', 'For sale']", end="")
                print("  Enter Filters: ", end="")
                filter = input()

                if(filter == "exit"):break
                if(filter == "none"): continue

                image_api.add_general_search_filter(filter)
                image_api.add_areas(area)
        
        elif (val == 'delete'):
            print("\n\n/delete> choose area: ", end="")
            val = input()
            image_api.delete_area(val)

        elif(val == "set host"):
            print("\n\n/set host> ", end="")
            print("Enter host server ip: ", end="")
            ip = input()

            print("\nEnter host server port: ", end="")
            port = input()
            image_api.initialize(ip, port)
            pass

        elif (val == "show areas"):
            print("\n\n/show areas> ", end="")
            image_api.print_areas()
            input()

        elif(val == "run search"):
            print("\n\n/run search> ", end="")
            print("Posted request for searching all areas.......")
            try:
                val = image_api.search_area()
                print(val)
            except Exception as error:
                print(error)
                print("\x1b[31mConnection closed or host in correct,  use 'set host' to set ip and port\x1b[0m")

            val = input()
        elif(val == "exit"):
            break

       
    print("\n\n Program exited....")


def ConsoleStartUp():
    while(True):
        print("\n\nEnter the target/host IP: ", end = "")
        IP = input()

        print("Enter the target/host PORT: ", end="")
        PORT = input()

        print("\n\n")
        print("\x1b[34mYour Server IP\x1b[0m: " + IP)
        print("\x1b[34mYour Server PORT\x1b[0m: " + str(PORT))
        print("Enter Y/N: ")
        value = input()

        if(value == "y" or value == "Y"):
            Host.TARGET_IP = IP
            Host.TARGET_PORT = PORT
            console()
            break

        elif(value == "N" or value == "n"):
            print("\x1b[31mConsole Exited\x1b[0m")
            break


ConsoleStartUp()