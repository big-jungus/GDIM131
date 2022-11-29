import API_Pull_TFT
import Excel_Push

'''
This script focuses on both collecting data from Riot API, and pushes data into Excel sheet
'''

if __name__ == '__main__':
    '''
    Collecting data
    Function returns single dictionary containing sub-dictionaries with X number of game data
    '''
    sample_size = 100
    num_games = 10
    
    #print(Excel_Push.formatData(API_Pull_TFT.testFunction("NA1_4492623739"))["MatchID"])

    
    allData = API_Pull_TFT.dataCollection(sample_size, num_games)
    
    '''
    Pushing data to an Excel sheet
    '''
    file_name = "TFT_Data_SS100_NG10"
    Excel_Push.createFile(file_name, allData)
    
    
    print("All finished.")