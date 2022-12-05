import API_Pull_TFT
import Excel_Push
import DataCleaning

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

    allData = API_Pull_TFT.dataCollection(sample_size, num_games)

    file_name = "TFT_Data_SS100_NG10_v3.xlsx"
    Excel_Push.createFileNew(file_name, allData)
    
    print("All finished.")