import pandas

'''
This script focuses on the Excel pushing
'''

'''
This method takes the dictionary returned from API_pull and creates a Excel sheet with data
'''

def createFile(file_name, data):
    formattedData = formatData(data)
    formattedData.to_excel(file_name, engine='xlsxwriter')
    return

def appendData(file_name, data):
    formattedData = formatData(data)
    
    with pandas.ExcelWriter(file_name, mode='a') as writer:
        formattedData.to_excel(writer)
    writer.save()
    writer.close()
    return

def formatData(data):
    dataframe = {"Rank": list(), "Division": list(), "MatchID": list(), "PlayerID": list(), "Placement": list(), "Level": list(), "Units": list(), "Traits": list()}
    
    for singleMatch in data:
        for player in singleMatch["players"]:
            dataframe["Rank"].append(singleMatch["rank"])
            dataframe["Division"].append(singleMatch["division"])
            dataframe["MatchID"].append(singleMatch["matchID"])
            
            dataframe["PlayerID"].append(player)
            dataframe["Placement"].append(singleMatch["players"][player]["placement"])
            dataframe["Level"].append(singleMatch["players"][player]["level"])
            dataframe["Units"].append(singleMatch["players"][player]["units"])
            dataframe["Traits"].append(singleMatch["players"][player]["traits"])
    
    df = pandas.DataFrame(data=dataframe)
    return df