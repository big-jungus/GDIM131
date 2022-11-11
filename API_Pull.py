import requests
import json

'''
This script focuses on pulling game data from the Riot Games API

***NOTE
    Riot Games API uses rate limits on API requests
        20 requests every 1 seconds
        100 requests every 2 minutes
'''

def test_pull(key):
    response = requests.get("https://na1.api.riotgames.com/tft/league/v1/challenger?api_key=" + key)
    
    for x in response.json()["entries"]:
        print(jsonText(x) + "\n")
    
    return 


'''
This method is the main function used by DataCollection_main
Receives API key string value 'key'

Receives inputs int value 'num_games' and string 'rank'
    Creates dictionary with num_games key:value pairs
'''
def API_Pull(key, rank):
    if rank == "recent":
        output = []
        for matchID in recentPull(key):
            output.append(organizeMatch(key, matchID))
        return output
    
    elif rank == "top":
        pass
    return 

'''
This method pulls and returns a list of Match IDs from API for recent matches played
'''

def recentPull(key):
    URL = "https://na1.api.riotgames.com/val/match/v1/recent-matches/by-queue/competitive?api_key=" + key
    response = requests.get(URL)
    
    cleaned_list = list()
    for ID in response.json()["matchIds"]:
        cleaned_list.append(jsonText(ID))
    
    return cleaned_list

'''
This method organizes individual match data
returns the following data:
[map, avgRank, Deaths : {
                    RoundNum : {
                        Player ID : [pre/post plant, location],
                        ...
                        },
                    ...
                    }
'''
def organizeMatch(key, matchID):
    URL = "https://na1.api.riotgames.com/val/match/v1/matches/" + matchID + "?api_key=" + key
    response = requests.get(URL)
    
    gameDeathsDict = dict()
    
    for roundNum in response.json()["roundResults"]:
        gameDeathsDict[jsonText(roundNum["roundNum"])] = dict()
        
        for player in roundNum["playerStats"]:
            for killLog in player["kills"]:
                
                puuid = jsonText(killLog["victim"])
                
                #Determines if kill was pre/post plant
                plant = ""
                
                if int(jsonText(killLog["timeSinceRoundStartMillis"])) > int(jsonText(roundNum["plantRoundTime"])):
                    plant = "post"
                else:
                    plant = "pre"
                
                
                location = jsonText(killLog["victimLocation"])
                
                gameDeathsDict[jsonText(roundNum["roundNum"])][puuid] = [plant, location]
    
    #Determines average rank of players
    rank = 0
    for player in response.json()["players"]:
        rank += int(jsonText(player["competitiveTier"]))
        
    rank /= 10
    
    output = [jsonText(response.json()["matchInfo"]["mapId"]), rank, gameDeathsDict]
    
    return output


'''
Converts json file to text 
'''
def jsonText(jsonObj):
    text = json.dumps(jsonObj, sort_keys=True, indent=0)
    return text

'''
Exceptions
COME BACK TO LATER
'''
