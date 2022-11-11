import API_Pull
import Excel_Push

'''
This script focuses on both collecting data from Riot API, and pushes data into Excel sheet
'''

if __name__ == '__main__':
    '''
    Collecting data
    Function returns single dictionary containing sub-dictionaries with X number of game data
    '''
    key = "RGAPI-8fe0836a-b6f2-4ed9-b11b-8822129ed60f"
    #key = input("Enter API key:\n")
    
    '''
    rank = input("Enter desired rank:\n")
    '''
    collected_data = API_Pull.API_Pull(key, "recent")
    
    '''
    Pushing data to an Excel sheet
    '''
    file_name = input("Enter file name:\n")
    
    #if file != exist, create new file
    Excel_Push.createFile(file_name, collected_data)
    
    #else append
    
    '''
    deaths = {}
    deaths["roundNum"] = {}
    deaths["roundNum"]["playerID"] = ["xD", "foreskin"]
    matchData = ["penis", "hehe", deaths]
    sample_data = [matchData]
    
    print(Excel_Push.formatData(sample_data))
    '''