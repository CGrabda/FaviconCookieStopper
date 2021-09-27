'''
Written by Christopher Grabda

Creates or overwrites config.ini file
Takes user input construct settings
'''
import os

WHITELIST_STRING = "; Whitelist your own sites to the list following the format below!\n;\n; This functions to save the favicons of websites not bookmarked\n[Whitelist]\nlinks = \n    https://www.reddit.com/,\n    https://github.com/,\n    https://inloop.github.io/sqlite-viewer/,\n    https://stackoverflow.com/"

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

if __name__ == "__main__":
    string = "[Settings]\n"
 
    try:
        username = os.environ["USERNAME"]
    except:
        username = os.environ["USER"]
        
    string += "USER_PATH: C:/Users/" + username + "\n"
    string += "HAS_MSEDGE: " + ynInput("Would you like to use this on Microsoft Edge? (y/n)\n> ") + "\n"
    string += "HAS_CHROME: " + ynInput("Would you like to use this on Google Chrome? (y/n)\n> ") + "\n"
    # string += "HAS_FFOX: " + ynInput("Would you like to use this on FireFox? (y/n)\n> ") + "\n"
    string += "HAS_FFOX: False\n"

    with open("./resources/config.ini", "w") as config:
        config.write(string)
    
    # If file does not exist, creates a template Whitelist file
    if (not os.path.exists("Whitelist.ini")):
        with open("Whitelist.ini", "w") as whitelist:
            whitelist.write(WHITELIST_STRING)

