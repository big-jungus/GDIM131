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
    #Ask for new key (Riot API requires new key every 24 hours)
    key = input("Enter updated API key:\n")
    rank = input("Enter desired rank:\n")
    num_games = input("Enter number of games:\n")
    
    print("Processing data for following variables:")
    print("Ranks targeted: " + rank)
    print("Number of games retrieved: " + num_games)
    
    '''
    Pushing data to an Excel sheet
    '''
    try:
        print("penis")
        
    except:
        print("Excel push failed")
