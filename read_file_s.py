import pandas as pd
def convert_housing_data_to_quarters():
    '''Converts the housing data given in monthly format to quarters
    from 2000q1 through 2016q3 and returns it as mean values in a
    dataframe. This dataframe have a multi-index in the shape of
    ["State","RegionName"].
    '''
    all_homes = pd.read_csv("C:\\Users\\fmeza\\Documents\\Coursera\\Python_DataScience\\course1_downloads\\City_Zhvi_AllHomes.csv")

    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa',
              'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National',
              'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska',
              'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana',
              'IL': 'Illinois', 'TN': 'Tennessee',
              'DC': 'District of Columbia', 'VT': 'Vermont',
              'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine',
              'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin',
              'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey',
              'AZ': 'Arizona','GU': 'Guam', 'MS': 'Mississippi',
              'PR': 'Puerto Rico','NC': 'North Carolina', 'TX': 'Texas',
              'SD': 'South Dakota', 'MP': 'Northern Mariana Islands',
              'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut',
              'WV': 'West Virginia', 'SC': 'South Carolina',
              'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York',
              'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida',
              'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania',
              'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island',
              'MN': 'Minnesota', 'VI': 'Virgin Islands',
              'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia',
              'ND': 'North Dakota', 'VA': 'Virginia'}
    # Replaces the abbreviations with the names of the states
    all_homes["State"].replace(states, inplace = True)
    all_homes = all_homes.set_index(["State","RegionName"])
    all_homes = all_homes.iloc[:, 49:250] # Discards irrelavant columns

    def quarters(col):
        if col.endswith(("01", "02", "03")):
            s = col[:4] + "q1"
        elif col.endswith(("04", "05", "06")):
            s = col[:4] + "q2"
        elif col.endswith(("07", "08", "09")):
            s = col[:4] + "q3"
        else:
            s = col[:4] + "q4"
        return s
    print(quarters)
    # Groups the monthly columns into quarters using mean value of
    # the four monthly columns
    housing = all_homes.groupby(quarters, axis = 1).mean()
    housing = housing.sort_index()
    return housing

housing = convert_housing_data_to_quarters()
print("Columns: \n", housing.columns)
print("# Rows: ", len(housing))