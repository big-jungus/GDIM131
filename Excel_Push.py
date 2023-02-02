import pandas

'''
This script focuses on the Excel pushing
'''

'''
This method takes the dictionary returned from API_pull and creates a Excel sheet with data
'''

def createFileNew(file_name, data):
    formattedData = formatData(data)
    writer = pandas.ExcelWriter(file_name, engine='xlsxwriter')
    formattedData.to_excel(writer, sheet_name = "Sheet1")
    writer.close()
    return



def createFileClean(file_name, data):
    writer = pandas.ExcelWriter(file_name, engine='xlsxwriter')
    data.to_excel(writer, sheet_name = "Sheet1")
    writer.close()
    
    

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
            dataframe["Units"].append(sorted(data[singleMatch]["players"][player]["units"], key=lambda tup: tup[0]))
            dataframe["Traits"].append(sorted(data[singleMatch]["players"][player]["traits"], key=lambda tup: tup[0]))
    
    df = pandas.DataFrame(data=dataframe)
    
    return df