import pandas as pd
from scipy.stats import ttest_ind

path = 'C:\\Users\\fmeza\\Documents\\Coursera\\Python_DataScience\\course1_downloads\\university_towns.txt'
GDP = 'C:\\Users\\fmeza\\Documents\\Coursera\\Python_DataScience\\course1_downloads\\gdplev.xls'
houses = 'C:\\Users\\fmeza\\Documents\\Coursera\\Python_DataScience\\course1_downloads\\City_Zhvi_AllHomes.csv'
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
def get_list_of_university_towns():
    towns = pd.read_table(path,header=None,names=["RegionName"])

    current_state = ""
    def get_state(cell):
        if cell.endswith("[edit]"):
            global current_state
            current_state = cell[:-6]
            return cell[:-6]
        else:
            return current_state

    towns["State"] = towns["RegionName"].map(get_state)

    towns = towns[~towns["RegionName"].str.endswith("[edit]")]
    towns["RegionName"] = towns["RegionName"].map(lambda x:x.split("(")[0].strip())

    return towns[['State','RegionName']]

data = get_list_of_university_towns()

change = 0
def pick_recession(cell):
 return ''
def get_recession_start():
	gdp = pd.read_excel(GDP, sheet_name=0, index_col=None, skiprows=5, usecols = [4,6], names=['Quarter','Value']).dropna()
	gdp_2000 = gdp[gdp['Quarter'] >= '2000q1']
	gdp_negative = gdp_2000[gdp_2000['Value'].diff()<0]
	for i,val in enumerate(gdp_negative.index):
		try:
			if gdp_negative.iloc[i].name - gdp_negative.iloc[i+1].name == -1:
				return gdp_2000.loc[val-1]['Quarter']
		except:
			continue

def get_recession_end():
	'''Returns the year and quarter of the recession end time as a 
	string value in a format such as 2005q3'''
	gdp = pd.read_excel(GDP, sheet_name=0, index_col=None, skiprows=5, usecols = [4,6], names=['Quarter','Value']).dropna()
	gdp_2000 = gdp[gdp['Quarter'] >= get_recession_start()]
	gdp_negative = gdp_2000[gdp_2000['Value'].diff()>0]
	for i,val in enumerate(gdp_negative.index):
		try:
			if gdp_negative.iloc[i].name - gdp_negative.iloc[i+1].name == -1:
				return gdp_2000.loc[val+1]['Quarter']
		except:
			continue

def get_recession_bottom():
	'''Returns the year and quarter of the recession bottom time as a 
	string value in a format such as 2005q3'''
	gdp = pd.read_excel(GDP, sheet_name=0, index_col=None, skiprows=5, usecols = [4,6], names=['Quarter','Value']).dropna()
	gdp_2000 = gdp[gdp['Quarter'] >= get_recession_start()] 
	gdp_2000 = gdp_2000[gdp_2000['Quarter'] <= get_recession_end()]
	gdp_min = gdp_2000[gdp_2000['Value']==gdp_2000['Value'].min()]
	return gdp.loc[gdp_min['Quarter'].index.values[0]]['Quarter']

import datetime
def convert_housing_data_to_quarters():
	'''Converts the housing data to quarters and returns it as mean 
	values in a dataframe. This dataframe should be a dataframe with
	columns for 2000q1 through 2016q3, and should have a multi-index
	in the shape of ["State","RegionName"].

	Note: Quarters are defined in the assignment description, they are
	not arbitrary three month periods.

	The resulting dataframe should have 67 columns, and 10,730 rows.
	'''
	data = pd.read_csv(houses)
	
	def quarter(col):
		data_quarter = ""
		if col.startswith('2'):
			date_f = datetime.datetime.strptime(col,'%Y-%m')
			quarter = round(date_f.month-1)//3 + 1
			data_quarter = str(date_f.year)+'q'+str(quarter)
		return data_quarter

	data['State'].replace(states, inplace=True)
	data.set_index(['State','RegionName'],inplace=True)
	cols = [i for i in data.columns.values if i.startswith('2')]
	data = data.filter(items=cols)
	housing = data.groupby(quarter,axis = 1).mean()
	return housing


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    housing = convert_housing_data_to_quarters()[[get_recession_start(),get_recession_bottom()]]
    housing['price_ratio'] = housing[get_recession_start()].div(housing[get_recession_bottom()])
    university_towns = get_list_of_university_towns().set_index(["State", "RegionName"])
    housing_university = pd.merge(housing,university_towns,how='inner',left_index=True,right_index=True).dropna()
    housing_not_university = housing[~housing.index.isin(housing_university.index)].dropna()
    t_stat, p_value = ttest_ind(housing_university["price_ratio"],
								housing_not_university["price_ratio"])
    return (True if p_value < 0.01 else False,p_value, "university town" if t_stat > 0 else "non-university town")
print(run_ttest())