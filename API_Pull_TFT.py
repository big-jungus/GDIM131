'''
THIS IS FOR TFT

FOR PUUIDs MAKE SURE TO USE THE DEV_KEY
'''
import requests
import json
import random

dev_key = "RGAPI-ebe0d733-b653-45a9-a554-6f7547afc09c"
tft_key = "RGAPI-eaba5c4f-0b41-40d7-8325-9a8cc6bad130"

'''
Use matchID's as dictionary keys

For each rank, repeat until 100 games collected
For lower divisions, try to collect unique games (games without the same players in them)
    If unable to find unique games, ignore the unique games


num_games refers to population size to sample from

    
Functions

idTransfer(LeagueID): leagueID -> puuID
    Converts ID's received into usable puuID
    returns puuID as string
    
idCheck(match1, match2): UniqueID checker
    Checks between two matches if there are any shared puuID's
    returns bool (true if unique)
    
matchPull(rank, division): Pulls matches from API
    returns JSON object containing single match
    
matchOrganize(matchJSON): JSON to dict
    Organizes match data into dict
    returns dict
    
jsonText(jsonObj): jsonObj to string
    returns string
'''
def testFunction(matchID):
    match1_response = requests.get("https://americas.api.riotgames.com/tft/match/v1/matches/" + matchID + "?api_key=" + tft_key)
    
    return matchOrganize(match1_response.json())



def dataCollection():
    #loop through each group
    return



def idTransfer(leagueID):
    properID = leagueID.replace(" ", "%20")
    response = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + properID + "?api_key=" + dev_key)
    
    return jsonText(response.json()["puuid"])



def idCheck(match1, match2):
    match1_response = requests.get("https://americas.api.riotgames.com/tft/match/v1/matches/" + match1 + "?api_key=" + tft_key)
    match2_response = requests.get("https://americas.api.riotgames.com/tft/match/v1/matches/" + match2 + "?api_key=" + tft_key)
    
    for player in match1_response.json()["metadata"]["participants"]:
        if player in match2_response.json()["metadata"]["participants"]:
            return False
    
    return True
    
    
    
def matchHistory(leagueID, num_games):
    properID = idTransfer(leagueID).replace('"',"")
    response = requests.get("https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/" + properID + "/ids?start=0&count=" + str(num_games) + "&api_key=" + dev_key)
    return response.json()



def highEloGames(rank, num_games):
    if rank == "challenger":
        response = requests.get("https://na1.api.riotgames.com/tft/league/v1/grandmaster?api_key=" + tft_key)
    elif rank == "grandmaster":
        response = requests.get("https://na1.api.riotgames.com/tft/league/v1/grandmaster?api_key=" + tft_key)
    elif rank == "master":
        response = requests.get("https://na1.api.riotgames.com/tft/league/v1/master?api_key=" + tft_key)
    else:
        print("Incorrect Rank (challenger, grandmaster, or master)")
        return 
    
    print("Processing " + rank + " games. This will take a while.")
    
    unique_gameIDs = []
    for player in response.json()["entries"]:
        print("Entry " + str(response.json()["entries"].index(player) + 1) + " out of " + str(len(response.json()["entries"])) + " possible entries")
        
        history = matchHistory(player["summonerName"], num_games)
        
        rand_game = jsonText(history[random.randint(0, num_games - 1)])
        
        if rand_game not in unique_gameIDs:
            unique_gameIDs.append(rand_game)
    
    print("Found " + str(len(unique_gameIDs)) + " games in " + rank)
    
    return unique_gameIDs


'''
For this function, num_games serves as the goal sample size
If the function is unable to 

Need to handle if not enough players to sample
'''
def lowEloGames(rank, division, sample_size, num_games):
    page_num = 1
    response = requests.get("https://na1.api.riotgames.com/tft/league/v1/entries/" + rank + "/" + division + "?page=" + str(page_num) + "&api_key=" + tft_key)
    
    unique_gameIDs = []
    used_players = []
    for x in range(sample_size):
        flag = False
        
        while flag == False:
            random_index = random.randint(0, len(response.json()) - 1)
            if random_index not in used_players:
                flag = True
        
        #basically pretty similar to highEloGames
        
        
        if len(used_players) == len(response.json()):
            page_num += 1
            response = requests.get("https://na1.api.riotgames.com/tft/league/v1/entries/" + rank + "/" + division + "?page=" + str(page_num) + "&api_key=" + tft_key)
    
    return



def matchOrganize(matchData):
    matchDict = {}
    for player in matchData["info"]["participants"]:
        matchDict[jsonText(player["puuid"])] = {}
        matchDict[jsonText(player["puuid"])]["placement"] = jsonText(player["placement"])
        matchDict[jsonText(player["puuid"])]["level"] = jsonText(player["level"])
        
        #For the following two data points, they will be stored in tuples, containing (name, tier)
        unit_list = []
        for unit in player["units"]:
            unit_list.append((jsonText(unit["character_id"]), jsonText(unit["tier"])))
        matchDict[jsonText(player["puuid"])]["units"] = unit_list
        
        trait_list = []
        for trait in player["traits"]:
            if int(jsonText(trait["tier_current"])) != 0:
                trait_list.append((jsonText(trait["name"]), jsonText(trait["tier_current"])))
        matchDict[jsonText(player["puuid"])]["traits"] = trait_list
        
    return matchDict



def jsonText(jsonObj):
    text = json.dumps(jsonObj, sort_keys=True, indent=0)
    return text