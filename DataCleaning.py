import pandas
'''
Comp Summary

Sorts and organizes unit data (Units need to be sorted alphabetically
'''

def compSort(file_name):
    
    excel_data = pandas.read_excel("D:/GitHub/GDIM131/GDIM131/" + file_name)
    df = pandas.DataFrame(excel_data, columns=["Set_Num", "Rank", "Division", "PlayerID", "Placement", "Level", "Units", "Traits"])
    
    all_units = df.loc[:, "Units"]
    
    for x in range(len(all_units)):
        
        unit_list = all_units[x]
        unit_list = unit_list.lstrip(unit_list[0]).rstrip(unit_list[-1])
        
        new_unit_list = []
        
        while True:
            start = unit_list.find("(")
            stop = unit_list.find(")")
            new_unit_list.append(unit_list[start:stop + 1])
            
            if stop + 3 > len(unit_list):
                break
            else:
                unit_list = unit_list[stop + 3:]
        
        sorted_list = sorted(new_unit_list)
        df.loc[x, "Units"] = str(sorted_list)
        
    return df