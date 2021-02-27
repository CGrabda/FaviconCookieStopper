'''
Written by Christopher Grabda

Creates or overwrites config.ini file
Takes user input construct settings
'''
def ynInput(message):
    while(True):
        try:
            userInput = input(message)
            userInput = userInput.strip().lower()
        except:
            print("----------------\nInvalid Input\n----------------")
        
        if (userInput == "y"):
            return "True"
        elif (userInput == "n"):
            return "False"
    
def pathInput():
    print()
    try:
        userInput = input("Please enter your user path exactly as shown\nC:/Users/cgrab \n: ")
        userInput = userInput.strip()
    except:
        print("----------------\nInvalid Input\n----------------")
    
    return userInput

if __name__ == "__main__":
    running = True
    string = "[Settings]\n"
 
    string += "USER_PATH: " + pathInput() +"\n"
    string += "HAS_MSEDGE: " + ynInput("Would you like to use this on Microsoft Edge? (y/n)\n: ") + "\n"
    string += "HAS_CHROME: " + ynInput("Would you like to use this on Google Chrome? (y/n)\n: ") + "\n"
    # string += "HAS_FFOX: " + ynInput("Would you like to use this on FireFox? (y/n)\n: ") + "\n"
    string += "HAS_FFOX: False\n"

    with open("config.ini", "w") as config:
        config.write(string)

