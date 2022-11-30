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
    dataframe = {"Set_Num": list(), "Rank": list(), "Division": list(), "MatchID": list(), "PlayerID": list(), "Placement": list(), "Level": list(), "Units": list(), "Traits": list()}

    for singleMatch in data:        
        for player in data[singleMatch]["players"]:
            dataframe["Set_Num"].append(data[singleMatch]["set_num"])
            dataframe["Rank"].append(data[singleMatch]["rank"])
            dataframe["Division"].append(data[singleMatch]["division"])
            dataframe["MatchID"].append(data[singleMatch]["matchID"])
            
            dataframe["PlayerID"].append(player)
            dataframe["Placement"].append(data[singleMatch]["players"][player]["placement"])
            dataframe["Level"].append(data[singleMatch]["players"][player]["level"])
            dataframe["Units"].append(data[singleMatch]["players"][player]["units"])
            dataframe["Traits"].append(data[singleMatch]["players"][player]["traits"])
    
    df = pandas.DataFrame(data=dataframe)
    print(df)
    return df