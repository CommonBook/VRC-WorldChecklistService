import atexit
import time
import login
import Worlds
from Worlds import searchWorlds
import data_handler
from data_handler import worldID_Data

import vrchatapi
from vrchatapi.api import users_api
from vrchatapi.api.users_api import UsersApi
#from vrchatapi.api.users_api import UsersAPI

configuration = vrchatapi.Configuration(
        username = input("Input username: "),
        password = input("Input password: "),
    )

def get_user_location(api_client, userID : str):
    usersApi = UsersApi(api_client)

    userData = usersApi.get_user(userID)
    #userName = userData['displayName']

    locationScripts = userData.location.split(":")

    return locationScripts[0]

def _on_exit(api_client, dataStruct : worldID_Data):
    print("\nSigning out...")
    #login.apiLogout(api_client)
    print("Exporting data...")
    #dataStruct.export()
    '''try:
        dataStruct.export()
    except:
        print("Export failed. :(")'''
    print("Completing execution.")

if __name__ == "__main__":
    print("\nHello, world!\n")
    
    with vrchatapi.ApiClient(configuration) as api_client:
        api_client.user_agent = "WorldChecklistService/0.0.1 jcmart701@gmail.com"
        allData = worldID_Data()

        #login.apiLogin(api_client, configuration)
        atexit.register(_on_exit, api_client, allData)

        curLocation = ""
        commands = ["1", "2", "x", "h"]
        helpMessage : str = "1: World watcher service\n" \
                            "2: World scraping\n" \
                            "x: End execution\n" \
                            "h <args>: View this message again. Optionally, include a command for more details. e.g. \"h 2\" for world scraping info\n"

        print("\nOutput is teathered to modes. Please select one by entering the corresponding number.")
        print(helpMessage)

        while True:
            mode : str = input(">>  ")
            
            match mode.lower()[0]:
                case "1":
                    print("!- To end the service, enter CTRL+C")
                    print("!- Disclaimer: The default interval for checks is 3 minutes. This is because the VRChat API has an enforced " \
                    "rate limit. Exceeding this limit will cause the service to crash. If you wish to override this limit, enter a number here. Otherwise, " \
                    "leave the field empty to continue with the default value\n")
                    timeSetting = input("Enter time (seconds) or press enter: ")
                    timeoutLimit = int(timeSetting) if timeSetting != "" and timeSetting.isdigit() else (60*3)

                    while True:
                        try:
                            new_location = get_user_location(api_client, login.get_current_user_ID(api_client))
                            if new_location != curLocation:
                                curLocation = new_location
                                print(f"\nPlayer moved to {curLocation}!\n")
                                
                                if curLocation in allData.data.keys() and allData.data[curLocation]["visited"] == True:
                                    print("But that location has already been documented.")
                                else:
                                    print("Saving data...")

                                newLocationInfo = Worlds.getWorldInfo(api_client, curLocation)
                                newLocationInfo.update({"visited": True})

                                allData.data.update({curLocation: newLocationInfo})

                            else:
                                print("Player did not move worlds.")
                            break

                        except KeyboardInterrupt:
                            break
                        
                        except:
                            print("Whoopsie- something went wrong.")
                            break
                        
                case "2":
                    print("press CTRL+C to return")
                    while True:
                        
                        try:
                            print("!- This feature not implemented")

                        except KeyboardInterrupt:
                            break

                        except:
                            print("Whoopsie- logging out...")
                            break

                case "x":
                    break

                case "h":
                    args = mode.split(" ")
                    #print(args)
                    if len(args) < 2:
                        print(helpMessage)
                    else:
                        match args[1]:
                            case "1":
                                print("World watcher service. \nRuns silently and periodically checks if the user has moved worlds. If they have," \
                                " that world's info is saved to the databank and is exported to the spreadsheet once the application is closed." \
                                "Will run perpectually until stopped by an error or a keyboard interrupt (CTRL+C).")
                            case "2":
                                print("World scraper. \nThe user may input search terms and the first 100 results will be saved and exported to a spreadsheet. " \
                                "Additionally exports a text file with a link to each world.")
                            case "x":
                                print("This closes the app. Are you stupid or something?")
                            case "h":
                                print("Very clever... " \
                                "Provides help.")



