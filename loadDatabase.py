from flask_sqlalchemy import SQLAlchemy
from refreshtoken import load_access_token
import requests
from database import Database, db


API_getMostPopularListURL = ('https://api.myanimelist.net/v2/anime/ranking?ranking_type=bypopularity&limit=500')

def getPopularityRanking_api(my_headers):
    try:
        
        data = requests.get(API_getMostPopularListURL, headers=my_headers).json()
    except Exception as exc:
        print(exc)
        data = None 
    return data

def loadDatabase():
    
    token_data = load_access_token()
    my_headers = {'Authorization' : token_data["token_type"] + ' ' + token_data["access_token"]}
    resp = getPopularityRanking_api(my_headers)
        
    Database.query.delete()
    db.session.commit()
            
    next = True 
    while(next):
        
            
        for x in range(0, len(resp["data"])):

                
            entry = Database(int(resp["data"][x]["ranking"]["rank"]), int(resp["data"][x]["node"]["id"]),resp["data"][x]["node"]["title"]) 
            db.session.add(entry)
            
            
        if ("next" in resp["paging"]):
            resp = requests.get(resp["paging"]["next"], headers=my_headers).json()
            next = True
        else:
            next = False
    db.session.commit()
             

if __name__ == "__main__":

    loadDatabase()
