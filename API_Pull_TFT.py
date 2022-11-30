'''
THIS IS FOR TFT

FOR PUUIDs MAKE SURE TO USE THE DEV_KEY
'''
import requests
import json
import random
import time


dev_key = "RGAPI-ab777641-f21a-42b2-94a7-19fc650c0a44"
tft_key = "RGAPI-eaba5c4f-0b41-40d7-8325-9a8cc6bad130"

highElo = ["challenger", "grandmaster", "master"]
lowElo = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]
divisions  = ["I", "II", "III", "IV"]
setNum = 7

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
def testFunction(rank, num_games):
    data = {}
    
    gameIDs = highEloGames(rank, num_games)
    
    for game in gameIDs:
            matchID = game.replace('"','')
            time.sleep(0.5)
            try:
                print("Data found for " + matchID)
                gameData = matchOrganize(matchData(matchID))
                gameData["matchID"] = matchID
                gameData["rank"] = rank
                gameData["division"] = "I"
                data[game] = gameData
            except KeyError:
                print("Data not found for " + matchID)
    
    return data



def dataCollection(sample_size, num_games):
    data = {}
    #high elo collection
    for rank in highElo:
        
        gameIDs = highEloGames(rank, num_games)
        
        '''
        gameIDs getting collected as something like ""\"NA_123456"\"", so needs to be cleaned to just have the NA_123456 portion
        Plug the list of gameIDs into matchOrganize, which should sort the data into a dictionary
        I didn't include the rank in the game dict, so add a dict entry with key "rank" and value of the rank variable from the for loop
        Pass each game dict into the data dict
        '''
        for game in gameIDs:
            matchID = game.replace('"','')
            time.sleep(1)
            try:
                print("Data found for " + matchID)
                gameData = matchOrganize(matchData(matchID))
                gameData["matchID"] = matchID
                gameData["rank"] = rank
                gameData["division"] = "I"
                data[game] = gameData
            except KeyError:
                print("Data not found for " + matchID)
        

    #low elo collection
    for rank in lowElo:
        for division in divisions:
            gameIDs = lowEloGames(rank, division, sample_size, num_games)
            
            for game in gameIDs:
                matchID = game.replace('"','')
                time.sleep(1)
                try:
                    print("Data found for " + matchID)
                    gameData = matchOrganize(matchData(matchID))
                    gameData["matchID"] = matchID
                    gameData["rank"] = rank
                    gameData["division"] = division
                    data[game] = gameData
                except KeyError:
                    print("Data not found for " + matchID)
    
    return data



def idTransfer(leagueID):
    properID = leagueID.replace(" ", "%20")
    response = requests.get("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + properID + "?api_key=" + dev_key)
    
    #print(jsonText(response.json()))
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
        response = requests.get("https://na1.api.riotgames.com/tft/league/v1/challenger?api_key=" + tft_key)
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
        
        time.sleep(1)
        
        try:
            history = matchHistory(player["summonerName"], num_games)
            
            rand_game = jsonText(history[random.randint(0, num_games - 1)])
            
            if rand_game not in unique_gameIDs:
                unique_gameIDs.append(rand_game)
        except KeyError:
            print("Invalid Game.")
            
        if len(unique_gameIDs) == 100:
            break
    
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
    
    print("Collecting " + rank + " " + division + " games. This will take a while.")
    
    unique_gameIDs = []
    used_players = []
    for x in range(sample_size):
        flag = False
        
        while flag == False:
            random_index = random.randint(0, len(response.json()) - 1)
            if random_index not in used_players:
                used_players.append(random_index)
                flag = True
        
        #basically pretty similar to highEloGames
        #might need "entries" key, might not
        
        time.sleep(1)
        
        try:
            player  = response.json()[random_index]
            history = matchHistory(player["summonerName"], num_games)
            rand_game = jsonText(history[random.randint(0, len(history) - 1)])
            
            if rand_game not in unique_gameIDs:
                unique_gameIDs.append(rand_game)
                print("Entry " + str(x) + " out of " + str(sample_size) + " possible entries in " + rank + " " + division)
        except KeyError:
            print("Invalid Game")
        
        if len(unique_gameIDs) == 100:
            break
        
        if len(used_players) == len(response.json()):
            page_num += 1
            response = requests.get("https://na1.api.riotgames.com/tft/league/v1/entries/" + rank + "/" + division + "?page=" + str(page_num) + "&api_key=" + tft_key)
            used_players = []
    
    return unique_gameIDs



def matchOrganize(matchData):
    matchDict = {}
    matchDict["players"] = {}
    matchDict["set_num"] = jsonText(matchData["info"]["tft_set_number"])
    
    for player in matchData["info"]["participants"]:
        
        matchDict["players"][jsonText(player["puuid"])] = {}
        matchDict["players"][jsonText(player["puuid"])]["placement"] = jsonText(player["placement"])
        matchDict["players"][jsonText(player["puuid"])]["level"] = jsonText(player["level"])
        
        #For the following two data points, they will be stored in tuples, containing (name, tier)
        unit_list = []
        for unit in player["units"]:
            unit_list.append((jsonText(unit["character_id"]), jsonText(unit["tier"])))
        matchDict["players"][jsonText(player["puuid"])]["units"] = unit_list
        
        trait_list = []
        for trait in player["traits"]:
            if int(jsonText(trait["tier_current"])) != 0:
                trait_list.append((jsonText(trait["name"]), jsonText(trait["tier_current"])))
        matchDict["players"][jsonText(player["puuid"])]["traits"] = trait_list
        
    return matchDict



def matchData(matchID):
    response = requests.get("https://americas.api.riotgames.com/tft/match/v1/matches/" + matchID + "?api_key=" + tft_key)
    return response.json()


def jsonText(jsonObj):
    text = json.dumps(jsonObj, sort_keys=True, indent=0)
    return text
