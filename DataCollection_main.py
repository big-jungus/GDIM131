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
    
    allData = API_Pull_TFT.dataCollection(sample_size, num_games)
    
    '''
    Pushing data to an Excel sheet
    '''
    #file_name = input("Enter file name:\n")
    
    #if file != exist, create new file
    #Excel_Push.createFile(file_name, collected_data)
    
    #else append
    
    '''

    '''
    
    
    
    print("penis")