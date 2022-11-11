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
    dataframe = {"Map": list(), "Average Rank": list(), "Pre/Post": list(), "Location": list()}
    
    for singleMatch in data:
        for roundNum in singleMatch[2]:
            for playerID in singleMatch[2][roundNum]:
                dataframe["Map"].append(singleMatch[0])
                dataframe["Average Rank"].append(singleMatch[1])
                
                dataframe["Pre/Post"].append(singleMatch[2][roundNum][playerID][0])
                dataframe["Location"].append(singleMatch[2][roundNum][playerID][1])
    
    df = pandas.DataFrame(data=dataframe)
    return df