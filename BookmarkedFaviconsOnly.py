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
config.read("config.ini")
#gets settings data from config.ini
USER_PATH = config.get("Settings", "USER_PATH")
HAS_MSEDGE = config.get("Settings", "HAS_MSEDGE")
HAS_CHROME = config.get("Settings", "HAS_CHROME")
HAS_FFOX = config.get("Settings", "HAS_FFOX")

#filepaths for msedge Favicons database and Bookmarks library
EDGE_FAVICONS_FILEPATH = USER_PATH + "/AppData/Local/Microsoft/Edge/User Data/Default/Favicons"
EDGE_BOOKMARKS_FILEPATH = USER_PATH +  "/AppData/Local/Microsoft/Edge/User Data/Default/Bookmarks"

#filepaths for Chrome Favicons database and Bookmarks library
CHROME_FAVICONS_FILEPATH = USER_PATH + "/AppData/Local/Google/Chrome/UserData/Default/Favicons"
CHROME_BOOKMARKS_FILEPATH = USER_PATH + "/AppData/Local/Google/Chrome/UserData/Default/Bookmarks"

def tupleToValueString(tuple): 
    string = "("
    for each in tuple:
        string += str(each) + ", "
    string += ")"
    return string

def parseBookmarks(filename):
    #stores list of bookmarked URLs
    url_list = []

    with open(filename) as bookmarks:
        #parses json bookmark data
        bjs = json.load(bookmarks)
        #goes through each bookmark and appens its url to list
        for each in bjs["roots"]["bookmark_bar"]["children"]:
            url_list.append(each["url"])
    
    return url_list

def createDatabase(urls, faviconsfile):
    #deletes existing newFavicons file
    try:
        os.remove("Favicons")
    except:
        pass

    #initializes new database
    newcon = s.connect("Favicons")
    newcur = newcon.cursor()

    #creates favicon_bitmaps, favicons, and icon_mapping tables in local Favicons
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
    #commits new tables
    newcon.commit()


    #initialize edge database
    con = s.connect(faviconsfile)
    cur = con.cursor()

    #grabs data from icon_mapping
    cur.execute("SELECT * FROM icon_mapping")

    #makes new list of icon_ids
    iconIdList = []
    
    #goes through database, matches icon maps to url in bookmark
    #iconId list used to match with bitmaps
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


    #grabs data from favicon_bitmaps
    cur.execute("SELECT * FROM favicon_bitmaps")
    
    #list of favicon bitmap ids that correlate to favicons table
    bitmapIdList = []

    idNum = 1
    iconIdNum = 2
    for row in cur.fetchall():
        if (row[1] in iconIdList):
            #adds second row of a favicon to list
            if (row[0] % 2 == 0):
                bitmapIdList.append(row[0])
            newcur.execute("INSERT INTO favicon_bitmaps VALUES(?,?,?,?,?,?,?);", row)
            newcur.execute("""
                    UPDATE icon_mapping
                    SET icon_id=?
                    WHERE icon_id=?;
                    """, (iconIdNum//2, row[1]))
            newcur.execute("""
                    UPDATE favicon_bitmaps
                    SET id=?, icon_id=?
                    WHERE last_updated=?;
                    """, (idNum, iconIdNum//2, row[2]))
            idNum += 1
            iconIdNum += 1
    

    #divides all values of bitmapIdList by 2 to use for favicons
    faviconIdList = [each//2 for each in bitmapIdList]

    #grabs data from favicons
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
    

    #copies 'meta' table from original file
    newcur.execute("ATTACH '" + faviconsfile + "' AS oldFav;")
    newcur.execute("INSERT INTO meta SELECT * FROM oldFav.meta;")
    

    #commit changes
    newcon.commit()

    #close databse curosrs and connections
    cur.close()
    newcur.close()
    con.close()
    newcon.close()

def replaceEdgeFavicons():
    return

if __name__ == "__main__":
    if (HAS_MSEDGE == "True"):
        urls = parseBookmarks(EDGE_BOOKMARKS_FILEPATH)
        createDatabase(urls, EDGE_FAVICONS_FILEPATH)
        copyfile("Favicons", EDGE_FAVICONS_FILEPATH)

    if (HAS_CHROME == "True"):
        urls = parseBookmarks(CHROME_BOOKMARKS_FILEPATH)
        createDatabase(urls, CHROME_FAVICONS_FILEPATH)
        copyfile("Favicons", CHROME_FAVICONS_FILEPATH)
    
    if (HAS_FFOX == "True"):
        pass