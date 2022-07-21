#%%
def answer_one():
    import pandas as pd
    import numpy as np

    Energy = pd.read_excel('Energy Indicators.xls',
    # For all countries which have missing data (e.g. data with "...") 
    na_values=["..."],header = None,skiprows=18,skipfooter= 38,usecols=[2,3,4,5],names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])

     # Convert Energy Supply to gigajoules 
    Energy['Energy Supply'] = Energy['Energy Supply'].apply(lambda x: x*1000000)

    # Remove parenthesis in some countries' names 
    Energy['Country'] = Energy['Country'].str.replace(r" \(.*\)","")
    Energy['Country'] = Energy['Country'].str.replace(r"\d*","")

    Energy['Country'] = Energy['Country'].replace({'Republic of Korea' : 'South Korea',
                                                'United States of America' : 'United States',
                                                'United Kingdom of Great Britain and Northern Ireland':'United Kingdom',
                                                'China, Hong Kong Special Administrative Region':'Hong Kong'})
        
    GDP = pd.read_csv('world_bank.csv', skiprows = 4)
    GDP['Country Name'] = GDP['Country Name'].replace({'Korea, Rep.': 'South Korea', 
                                                    'Iran, Islamic Rep.': 'Iran', 
                                                    'Hong Kong SAR, China' : 'Hong Kong'}) 

    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    ScimEn.head()

    # merge those three datasets
    merge1 = pd.merge(ScimEn,Energy,how="inner",left_on="Country",right_on="Country")
    merge1 = merge1[merge1["Rank"]<=15]

    GDP.rename(columns = {"Country Name":"Country"},inplace=True)
    GDP = GDP.loc[:,['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015',"Country"]]
    merge2 = pd.merge(merge1,GDP,how="inner",left_on="Country",right_on="Country").set_index("Country")
 
    return merge2
# %%
answer_one()

# %%
# Q2
import pandas as pd
import numpy as np
from pandas.core.indexes.base import Index

Energy = pd.read_excel('Energy Indicators.xls',
# For all countries which have missing data (e.g. data with "...") 
na_values=["..."],header = None,skiprows=18,skipfooter= 38,usecols=[2,3,4,5],names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])

    # Convert Energy Supply to gigajoules 
Energy['Energy Supply'] = Energy['Energy Supply'].apply(lambda x: x*1000000)

# Remove parenthesis in some countries' names 
Energy['Country'] = Energy['Country'].str.replace(r" \(.*\)","")
Energy['Country'] = Energy['Country'].str.replace(r"\d*","")

Energy['Country'] = Energy['Country'].replace({'Republic of Korea' : 'South Korea',
                                            'United States of America' : 'United States',
                                            'United Kingdom of Great Britain and Northern Ireland':'United Kingdom',
                                            'China, Hong Kong Special Administrative Region':'Hong Kong'})
    
GDP = pd.read_csv('world_bank.csv', skiprows = 4)
GDP['Country Name'] = GDP['Country Name'].replace({'Korea, Rep.': 'South Korea', 
                                                'Iran, Islamic Rep.': 'Iran', 
                                                'Hong Kong SAR, China' : 'Hong Kong'}) 

ScimEn = pd.read_excel('scimagojr-3.xlsx')
ScimEn.head()

# merge those three datasets
merge1 = pd.merge(ScimEn,Energy,how="inner",left_on="Country",right_on="Country")

GDP.rename(columns = {"Country Name":"Country"},inplace=True)
GDP = GDP.loc[:,['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015',"Country"]]
merge2 = pd.merge(merge1,GDP,how="inner",left_on="Country",right_on="Country").set_index("Country")

merge_keep = merge2[merge2["Rank"]<=15]
merge_lose = merge2[~merge2.isin(merge_keep)].dropna()
# how many entries are lost:
len(merge_lose)

# %%
# Q3
info=answer_one()
# What are the top 15 countries for average GDP over the last 10 years?
info['avgGDP'] = info[["2006","2007","2008","2009","2010","2011","2012","2013","2014","2015"]].apply(np.mean,axis = 1).sort_values(ascending = False)
info.head()

# %%
# Q4
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
g6 = info.index[5]
info.loc[g6]["2015"] - info.loc[g6]["2006"]

# %%
# Q5
# What is the mean energy supply per capita?
info.loc[:,'Energy Supply per Capita'].mean()

# %%
# Q6
# What country has the maximum % Renewable and what is the percentage?
result = info.sort_values('% Renewable', ascending=False).iloc[0]
print(type(result))
(result.name, result['% Renewable'])

# %%
# Q7
info['ratio'] = info.loc[:,'Self-citations'] / info.loc[:,'Citations']
result = info.sort_values('ratio', ascending = False).iloc[0]
(result.name, result['ratio'])

# %%
# Q8
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. What is the third most populous country according to this estimate?
info['population'] = info['Energy Supply'] / info['Energy Supply per Capita']
info.sort_values('population', ascending=False).iloc[2].name

# %%
# Q9
# What is the correlation between the number of citable documents per capita and the energy supply per capita?
info['citation per capita'] = info['Citations'] / info['population']
df = info.loc[:,['citation per capita','Energy Supply per Capita']]
print(df.head())
df.corr().iloc[0,1]

# %%
# Q10
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
Renewable_median = info['% Renewable'].median()
info['HighRenew'] = info['% Renewable'].apply(lambda x: 0 if x < Renewable_median else 1)
info['HighRenew']

# %%
# Q11
# Use the following dictionary to group the Countries by Continent
ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

# index is country
info['continent'] = pd.Series(ContinentDict)

# displays the sample size and the sum, mean, and std deviation for the estimated population
info.groupby('continent')['population'].agg([np.size, np.mean, np.std])

# %%
# Q12
# Cut % Renewable into 5 bins
info['renewable_grp'] = pd.cut(info['% Renewable'],5)

# How many countries are in each of these groups?
info.groupby(['continent', 'renewable_grp'])['continent'].agg(np.size).dropna()

# %%
# Q13
# Convert the Population Estimate series to a string with thousands separator
info['population'].apply(lambda x: f'{x:,}')

# %%
