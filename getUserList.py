from flask import url_for
import requests
import json

from AnimeEntry import AnimeEntry
from refreshtoken import load_access_token
from database import Database, db
from loadDatabase import loadDatabase



API_getUserListURL = ('https://api.myanimelist.net/v2/users/{}/animelist?fields=list_status&limit=1000')



def getUserList_api(username, my_headers):
    try:
        
        data = requests.get(API_getUserListURL.format(username), headers=my_headers).json()
    except Exception as exc:
        print(exc)
        data = None
    return data



def appendInList(username):

    token_data = load_access_token()
    my_headers = {'Authorization' : token_data["token_type"] + ' ' + token_data["access_token"]}

    resp = getUserList_api(username, my_headers)
    userAnimeList_ID = []
    next = True
    
    while(next):
        

        for x in range(0, len(resp["data"])):

            status = resp["data"][x]["list_status"]["status"]
            if status == "completed":
                status = "Completed"
            elif status == "plan_to_watch":
                status = "Plan To Watch"
            elif status == "watching":
                status = "Watching"
            elif status == "dropped":
                status = "Dropped"
            else:
                status = "On Hold"

            try:
                picture = resp["data"][x]["node"]["main_picture"]["medium"]
            except:
                picture = url_for('static', filename = 'wot.png')

            userAnimeList_ID.append(AnimeEntry(resp["data"][x]["node"]["title"], int(resp["data"][x]["node"]["id"]), "", picture, status, resp["data"][x]["list_status"]["score"]))
            
            

           
          
        if ("next" in resp["paging"]):
            resp = requests.get(resp["paging"]["next"].format(username), headers=my_headers).json()
            next = True
        else:
            next = False
    return userAnimeList_ID
            
                
        

def sortListbyPopularity(username):
        
    try:
        
        global cur_username
        

        try: 
            cur_username
        except NameError:
            cur_username = ""

        if not(cur_username == username):

            cur_username = username
            list = []
        
        
            userAnimeList_ID = appendInList(username)

            for x in userAnimeList_ID:
                data = Database.query.filter_by(id = x.getId()).first()

                x.setGlobalRanking(data.ranking) 
                list.append(x)
      
            global sortedList
            sortedList = sort(list)
        return sortedList
        
    
        
    except:
            sortedList = []
        
    
        


def sortByStatusList(status):

    
    sortedList_byStatus = []
    for x in sortedList:
        if status == x.getStatus():
            sortedList_byStatus.append(x)

    if not sortedList_byStatus:
            sortedList_byStatus.append(AnimeEntry("very empty...", "", "", url_for('static', filename = 'wot.PNG'), status, ""))
    return sortedList_byStatus

 


def sort(templist):

    less = []
    equal = []
    greater = []

    if len(templist) > 1:
        pivot = int(templist[0].getGlobalRanking())
        for x in templist:
            if int(x.getGlobalRanking()) < pivot:
                less.append(x)
            elif int(x.getGlobalRanking()) == pivot:
                equal.append(x)
            elif int(x.getGlobalRanking()) > pivot:
                greater.append(x)

        return sort(less)+equal+sort(greater)  
    else:  
        return templist
 
