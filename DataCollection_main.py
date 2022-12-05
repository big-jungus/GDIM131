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
    
    #print(API_Pull_TFT.matchData("NA1_4492623739"))
    #print(API_Pull_TFT.matchOrganize((API_Pull_TFT.matchData("NA1_4492623739"))))

    allData = API_Pull_TFT.dataCollection(sample_size, num_games)
    #Excel_Push.formatData(API_Pull_TFT.testFunction("challenger", 10))
    
    
    '''
    Pushing data to an Excel sheet
    '''
    file_name = "TFT_Data_SS100_NG10_v3.xlsx"
    Excel_Push.createFile(file_name, allData)
    
    
    print("All finished.")