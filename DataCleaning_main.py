import DataCleaning
import Excel_Push

if __name__ == '__main__':
    '''
    Cleaning data
    Alphabetize the dataframe's unit list
    '''
    file_name = "TFT_Data_SS100_NG10.xlsx"
    file_name2 = "TFT_Data_SS100_NG10_cleaned.xlsx"
    df = DataCleaning.compSort(file_name)
    print(df)
    Excel_Push.createFileClean(file_name2, df)