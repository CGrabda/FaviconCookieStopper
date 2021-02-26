'''
Written by Christopher Grabda

Gets names of bookmarked sites and cross-references, with favicons
Saves list of matched favicons and overwrites the Favicons file
'''
import sqlite3 as s
import json

FAVICONS_FILEPATH = "C:/Users/cgrab/AppData/Local/Microsoft/Edge/User Data/Default/Favicons"
BOOKMARKS_FILEPATH = "C:/Users/cgrab/AppData/Local/Microsoft/Edge/User Data/Default/Bookmarks"

#stores list of bookmarked URLs
url_list = []

with open(BOOKMARKS_FILEPATH) as bookmarks:
    #parses json bookmark data
    bjs = json.load(bookmarks)
    #goes through each bookmark and appens its url to list
    for each in bjs["roots"]["bookmark_bar"]["children"]:
        url_list.append(each["url"])
    print(url_list)

con = s.connect(FAVICONS_FILEPATH)

cur = con.cursor()

