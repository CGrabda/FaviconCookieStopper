'''
Written by Christopher Grabda

Gets names of bookmarked sites and cross-references, with favicons
Saves list of matched favicons and overwrites the Favicons file
'''
import configparser
import sqlite3 as s
import json
import os
from shutil import copyfile


config = configparser.ConfigParser()
config.read("./resources/config.ini")
# Gets settings data from config.ini
USER_PATH = config.get("Settings", "USER_PATH")
HAS_MSEDGE = config.getboolean("Settings", "HAS_MSEDGE")
HAS_CHROME = config.getboolean("Settings", "HAS_CHROME")
HAS_FFOX = config.getboolean("Settings", "HAS_FFOX")

config.read("Whitelist.ini")
EXTRA_LINKS = config.get("Whitelist", "links")

# Filepaths for msedge Favicons database and Bookmarks library
EDGE_FAVICONS_FILEPATH = USER_PATH + "/AppData/Local/Microsoft/Edge/User Data/Default/Favicons"
EDGE_BOOKMARKS_FILEPATH = USER_PATH +  "/AppData/Local/Microsoft/Edge/User Data/Default/Bookmarks"

# Filepaths for Chrome Favicons database and Bookmarks library
CHROME_FAVICONS_FILEPATH = USER_PATH + "/AppData/Local/Google/Chrome/User Data/Default/Favicons"
CHROME_BOOKMARKS_FILEPATH = USER_PATH + "/AppData/Local/Google/Chrome/User Data/Default/Bookmarks"

TEMPORARY_FAVICONS_FILE = "./resources/Favicons"

'''
Turns Whitelist.ini file into a list of provided strings
'''
def parseWhitelist(list):
    string = ""
    new_list = []

    for item in list:
        if (item == "\n" or item == ","):
            if (string != ""):
                new_list.append(string)
            string = ""

        else:
            string += item
    
    return new_list


'''
Parses the Bookmarks json file and returns a list of bookmarks
'''
def parseBookmarks(filename):
    # Stores list of bookmarked URLs
    url_list = []

    with open(filename) as bookmarks:
        # Parses json bookmark data
        bjs = json.load(bookmarks)
        # Goes through each bookmark and appens its url to list
        for each in bjs["roots"]["bookmark_bar"]["children"]:
            url_list.append(each["url"])
    
    links = parseWhitelist(EXTRA_LINKS)

    for link in links:
        url_list.append(link)

    return url_list

'''
Deletes the Favicons database in this folder, creates a new database
Populates new database with data that matches URL list provided

url -> icon_mapping row -> icon_id -> favicon_bitmaps row -> id -> favicons
Grabs data of all the links provided in the order following above, populates tables of new database
Copies new database over old database
'''
def createDatabase(urls, faviconsfile):
    # Deletes existing newFavicons file
    try:
        os.remove(TEMPORARY_FAVICONS_FILE)
    except:
        pass

    # Initializes new database
    newcon = s.connect(TEMPORARY_FAVICONS_FILE)
    newcur = newcon.cursor()

    # Creates favicon_bitmaps, favicons, and icon_mapping tables in local Favicons
    newcur.execute(""" 
        CREATE TABLE favicon_bitmaps(
            id integer PRIMARY KEY AUTOINCREMENT,
            icon_id integer,
            last_updated integer,
            image_data blob,
            width integer,
            height integer,
            last_requested integer
        )
    """)
    newcur.execute(""" 
        CREATE TABLE favicons(
            id integer PRIMARY KEY AUTOINCREMENT,
            url longvarchar,
            icon_type integer
        )
    """)
    newcur.execute(""" 
        CREATE TABLE icon_mapping(
            id integer PRIMARY KEY AUTOINCREMENT,
            page_url longvarchar,
            icon_id integer
        )
    """)
    newcur.execute(""" 
        CREATE TABLE meta(
            key longvarchar,
            value longvarchar
        )
    """)
    newcon.commit()


    # Initialize edge database
    con = s.connect(faviconsfile)
    cur = con.cursor()

    cur.execute("SELECT * FROM icon_mapping")

    iconIdList = []
    
    # Goes through database, matches icon maps to url in bookmark
    idNum = 1
    for row in cur.fetchall():
           if (row[1] in urls):
               newcur.execute("INSERT INTO icon_mapping VALUES(?,?,?);", row)
               newcur.execute("""
                    UPDATE icon_mapping
                    SET id=?
                    WHERE page_url=?;
               """, (idNum, row[1]))
               
               iconIdList.append(row[2])
               idNum += 1


    cur.execute("SELECT * FROM favicon_bitmaps")
    
    bitmapIdList = []

    idNum = 1
    iconIdNum = 2
    for row in cur.fetchall():
        if (row[1] in iconIdList):
            if (row[0] % 2 == 0):
                bitmapIdList.append(row[0])

            # This statement prevents a duplicate bitmap from stopping execution, value must be unique
            try:
                newcur.execute("""
                    UPDATE OR IGNORE favicon_bitmaps
                    SET id=?, icon_id=?
                    WHERE last_updated=?;
                    """, (idNum, iconIdNum//2, row[2]))
                newcur.execute("INSERT INTO favicon_bitmaps VALUES(?,?,?,?,?,?,?);", row)
                newcur.execute("""
                        UPDATE icon_mapping
                        SET icon_id=?
                        WHERE icon_id=?;
                        """, (iconIdNum//2, row[1]))

                idNum += 1
                iconIdNum += 1
            except:
                pass
    

    # Divides all values of bitmapIdList by 2 because 2 bitmaps per favicon
    faviconIdList = [each//2 for each in bitmapIdList]


    cur.execute("SELECT * FROM favicons")

    idNum = 1
    for row in cur.fetchall():
        if (row[0] in faviconIdList):
            newcur.execute("INSERT INTO favicons VALUES(?,?,?);", row)
            newcur.execute("""
                    UPDATE favicons
                    SET id=?
                    WHERE url=?;
                    """, (idNum, row[1]))
            idNum += 1
    

    # Copies 'meta' table from original file
    newcur.execute("ATTACH '" + faviconsfile + "' AS oldFav;")
    newcur.execute("INSERT INTO meta SELECT * FROM oldFav.meta;")
    

    newcon.commit()

    # Close databse curosrs and connections
    cur.close()
    newcur.close()
    con.close()
    newcon.close()


if __name__ == "__main__":
    if (HAS_MSEDGE):
        urls = parseBookmarks(EDGE_BOOKMARKS_FILEPATH)
        createDatabase(urls, EDGE_FAVICONS_FILEPATH)
        copyfile(TEMPORARY_FAVICONS_FILE, EDGE_FAVICONS_FILEPATH)

    if (HAS_CHROME):
        urls = parseBookmarks(CHROME_BOOKMARKS_FILEPATH)
        createDatabase(urls, CHROME_FAVICONS_FILEPATH)
        copyfile(TEMPORARY_FAVICONS_FILE, CHROME_FAVICONS_FILEPATH)
    
    if (HAS_FFOX):
        pass