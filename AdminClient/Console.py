import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
print(sys.path[0], "<--this")
from SystemAPIs.AdminAPI.OpenVisualAPI import *



OpenVisualAPI = OpenVisualAPI()

class Host():
    TARGET_IP = ''
    TARGET_PORT = ''

def console():
    
    while(True):
        os.system('cls')
        print("\x1b[31mNOTICE: Please type in correct city names otherwise redfin site search goes haywire")
        print("It then causes wrong addresses to be stored under wrong city in database\x1b[0m")
        print("Select Options: [add area, set host,  exit,  delete area, update area, start updates]")
        val = input()

        if(val == "exit"):
            return
        
        elif(val == "update area"):
            print("\n/UPDATE AREA> ", end="")
            print("Enter the name of (State) ", end="")
            state = input()
                
            if(state == "exit"):break
            elif(state == "none"):continue

            print("Enter the name of (City) ", end="")
            city = input()
            if(city == "exit"):break
            elif(city == "none"):continue

            print("\x1b[31mupdating\x1b[0m....")
            value = OpenVisualAPI.CRUD().Update().Country("USA").State(state).City(city).Perform()    
            print("Report Status: ", value)

            input()


        elif(val == "add area"):
            print("\n/ADD  AREA> ", end="")
            print("Enter the name of (State) ", end="")
            state = input()
                
            if(state == "exit"):break
            elif(state == "none"):continue

            print("Enter the name of (City) ", end="")
            city = input()
            if(city == "exit"):break
            elif(city == "none"):continue

            print("\x1b[31mAdding\x1b[0m....")
            value = OpenVisualAPI.CRUD().Add().Country("USA").State(state).City(city).Perform()  
            print("Report Status: ", value)

            input()
        
        elif(val == "delete area"):
            print("\n/ADD  AREA> ", end="")
            print("Enter the name of (State) ", end="")
            state = input()
                
            if(state == "exit"):break
            elif(state == "none"):continue

            print("Enter the name of (City) ", end="")
            city = input()
            if(city == "exit"):break
            elif(city == "none"):continue
            
            print("\x1b[31mDeleting\x1b[0m....")
            value = OpenVisualAPI.CRUD().Delete().Country("USA").State(state).City(city).Perform() 
            print("Report Status: ", value) 

            input()

        elif(val == "set host"):
            print("\n\n/set host> ", end="")
            print("Enter host server ip: ", end="")
            ip = input()
            if(ip == "exit"):
                continue
            print("\nEnter host server port: ", end="")
            port = input()
            if(port == "exit"):
                continue
            OpenVisualAPI.ConnectWithIP(ip, port)
        
        
        
            

      

       
    print("\n\n Program exited....")


def ConsoleStartUp():
    while(True):
        print("\n\nEnter the target/host IP: ", end = "")
        IP = input()
        if(IP == "exit"):
            return
        

        print("Enter the target/host PORT: ", end="")
        PORT = input()

        if(PORT == "exit"):
            return

        print("\n\n")
        print("\x1b[34mYour Server IP\x1b[0m: " + IP)
        print("\x1b[34mYour Server PORT\x1b[0m: " + str(PORT))
        print("Enter Y/N: ")
        value = input()

        if(value == "y" or value == "Y"):
            OpenVisualAPI.ConnectWithIP(IP, PORT)
            console()
            break

        elif(value == "N" or value == "n"):
            print("\x1b[31mConsole Exited\x1b[0m")
            break

ConsoleStartUp()