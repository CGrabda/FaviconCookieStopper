'''
Written by Christopher Grabda

Gets names of bookmarked sites and cross-references, with favicons
Saves list of matched favicons and overwrites the Favicons file
'''
import sqlite3 as s
import json
import os

EDGE_FAVICONS_FILEPATH = "C:/Users/cgrab/AppData/Local/Microsoft/Edge/User Data/Default/Favicons"
EDGE_BOOKMARKS_FILEPATH = "C:/Users/cgrab/AppData/Local/Microsoft/Edge/User Data/Default/Bookmarks"


def tupleToValueString(tuple): 
    string = "("
    for each in tuple:
        string += str(each) + ", "
    string += ")"
    return string

def parseEdgeBookmarks(filename):
    #stores list of bookmarked URLs
    url_list = []

    with open(filename) as bookmarks:
        #parses json bookmark data
        bjs = json.load(bookmarks)
        #goes through each bookmark and appens its url to list
        for each in bjs["roots"]["bookmark_bar"]["children"]:
            url_list.append(each["url"])
    
    return url_list

def createEdgeDatabase(urls):
    #clears Favicons table
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
            id integer,
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
            id integer,
            url longvarchar,
            icon_type integer
        )
    """)
    newcur.execute(""" 
        CREATE TABLE icon_mapping(
            id integer,
            page_url longvarchar,
            icon_id integer
        )
    """)
    #commits new tables
    newcon.commit()


    #initialize edge database
    con = s.connect(EDGE_FAVICONS_FILEPATH)
    cur = con.cursor()

    #grabs data from icon_mapping
    cur.execute("SELECT * FROM icon_mapping")

    #makes new list of icon_ids
    iconidList = []
    
    idNum = 1
    for row in cur.fetchall():
           if (row[1] in urls):
               newcur.execute("INSERT INTO icon_mapping VALUES(?,?,?);", row)
               newcur.execute("""
                    UPDATE icon_mapping
                    SET id=?
                    WHERE page_url=?;
               """, (idNum, row[1]))
               
               iconidList.append(row[2])
               idNum += 1
    #commits changes
    newcon.commit()
    print("Changes committed!")


    
    
    cur.close()
    newcur.close()
    con.close()
    newcon.close()

if __name__ == "__main__":
    urls = parseEdgeBookmarks(EDGE_BOOKMARKS_FILEPATH)
    print(len(urls))
    createEdgeDatabase(urls)

