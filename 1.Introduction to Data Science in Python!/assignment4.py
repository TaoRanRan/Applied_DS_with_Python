#%%
# Q1 
import pandas as pd
import numpy as np
import scipy.stats as stats
import re
# %%
cities = pd.read_html("wikipedia_data.html")[1].iloc[:-1,[0,3,5,6,7,8]]
cities.head()
# %%
cities.rename(columns = {"Population (2016 est.)[8]":"Population"},inplace=True)
cities['NFL'] = cities['NFL'].str.replace(r"\[.*\]","")
cities['MLB'] = cities['MLB'].str.replace(r"\[.*\]","")
cities['NBA'] = cities['NBA'].str.replace(r"\[.*\]","")
cities['NHL'] = cities['NHL'].str.replace(r"\[.*\]","")
print(cities.shape)
cities.head()
# %%

Big4='NHL'

team = cities[Big4].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')
team['Metropolitan area']=cities['Metropolitan area']
team = pd.melt(team, id_vars=['Metropolitan area']).drop(columns=['variable']).replace("",np.nan).replace("—",np.nan).dropna().reset_index().rename(columns = {"value":"team"})
team = pd.merge(team,cities,how='left',on = 'Metropolitan area').iloc[:,1:4]
team = team.astype({'Metropolitan area': str, 'team': str, 'Population': int})
team.head()
# %%
nhl_df=pd.read_csv("nhl.csv")
nhl_df = nhl_df[nhl_df['year'] == 2018]
nhl_df['team'] = nhl_df['team'].str.replace(r'\*',"")
nhl_df = nhl_df[['team','W','L']]
# %%
dropList=[]
for i in range(nhl_df.shape[0]):
    row=nhl_df.iloc[i]
    if row['team']==row['W'] and row['L']==row['W']:
#         print(row['team'],'will be dropped!')
        dropList.append(i)
nhl_df=nhl_df.drop(dropList)
# nhl_df['team'] = nhl_df['team'].str.extract('(?:[A-Z][a-z]*)(.*)')
nhl_df['team'] = nhl_df['team'].str.replace('[\w.]*\ ','')
# nhl_df['team'] = nhl_df['team'].str.replace('.','')
nhl_df = nhl_df.astype({'team': str,'W': int, 'L': int})
nhl_df['WLRatio'] = nhl_df['W']/(nhl_df['W']+nhl_df['L'])
# %%

team['team']=team['team'].str.replace('[\w]*\ ','')
merge=pd.merge(team,nhl_df,'outer', on = 'team')

merge=merge.groupby('Metropolitan area').agg({'WLRatio': np.nanmean, 'Population': np.nanmean})
print(merge.shape)
merge


# %%
# Q2
cities = pd.read_html("wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
cities.rename(columns={"Population (2016 est.)[8]": "Population"},
              inplace=True)
cities['NFL'] = cities['NFL'].str.replace(r"\[.*\]", "")
cities['MLB'] = cities['MLB'].str.replace(r"\[.*\]", "")
cities['NBA'] = cities['NBA'].str.replace(r"\[.*\]", "")
cities['NHL'] = cities['NHL'].str.replace(r"\[.*\]", "")

Big4='NBA'

def nba_correlation():
    
    team = cities[Big4].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')
    team['Metropolitan area']=cities['Metropolitan area']
    team = pd.melt(team, id_vars=['Metropolitan area']).drop(columns=['variable']).replace("",np.nan).replace("—",np.nan).dropna().reset_index().rename(columns = {"value":"team"})
    team=pd.merge(team,cities,how='left',on = 'Metropolitan area').iloc[:,1:4]
    team = team.astype({'Metropolitan area': str, 'team': str, 'Population': int})
    team['team']=team['team'].str.replace('[\w.]*\ ','')

    _df=pd.read_csv(""+str.lower(Big4)+".csv")
    _df = _df[_df['year'] == 2018]
    _df['team'] = _df['team'].str.replace(r'[\*]',"")
    _df['team'] = _df['team'].str.replace(r'\(\d*\)',"")
    _df['team'] = _df['team'].str.replace(r'[\xa0]',"")
    _df = _df[['team','W/L%']]
    _df['team'] = _df['team'].str.replace('[\w.]* ','')
    _df = _df.astype({'team': str,'W/L%': float})
    
    merge=pd.merge(team,_df,'outer', on = 'team')
    merge=merge.groupby('Metropolitan area').agg({'W/L%': np.nanmean, 'Population': np.nanmean})

    population_by_region = merge['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = merge['W/L%'] # pass in win/loss ratio from _df in the same order as cities["Metropolitan area"]   

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
nba_correlation()

# %%
# Q3 
import pandas as pd
import numpy as np
import scipy.stats as stats
import re

cities = pd.read_html("wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
cities.rename(columns={"Population (2016 est.)[8]": "Population"},
              inplace=True)
cities['NFL'] = cities['NFL'].str.replace(r"\[.*\]", "")
cities['MLB'] = cities['MLB'].str.replace(r"\[.*\]", "")
cities['NBA'] = cities['NBA'].str.replace(r"\[.*\]", "")
cities['NHL'] = cities['NHL'].str.replace(r"\[.*\]", "")

Big4='MLB'

def mlb_correlation(): 
    
    team = cities[Big4].str.extract('([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)([A-Z]{0,2}[a-z0-9]*\ [A-Z]{0,2}[a-z0-9]*|[A-Z]{0,2}[a-z0-9]*)')
    team['Metropolitan area']=cities['Metropolitan area']
    team = pd.melt(team, id_vars=['Metropolitan area']).drop(columns=['variable']).replace("",np.nan).replace("—",np.nan).dropna().reset_index().rename(columns = {"value":"team"})
    team=pd.merge(team,cities,how='left',on = 'Metropolitan area').iloc[:,1:4]
    team = team.astype({'Metropolitan area': str, 'team': str, 'Population': int})
    team['team']=team['team'].str.replace('\ Sox','Sox')
    team['team']=team['team'].str.replace('[\w.]*\ ','')

    _df=pd.read_csv(""+str.lower(Big4)+".csv")
    _df = _df[_df['year'] == 2018]
    _df['team'] = _df['team'].str.replace(r'[\*]',"")
    _df['team'] = _df['team'].str.replace(r'\(\d*\)',"")
    _df['team'] = _df['team'].str.replace(r'[\xa0]',"")
    _df = _df[['team','W-L%']]
    _df.rename(columns={"W-L%": "W/L%"},inplace=True)
    _df['team']=_df['team'].str.replace('\ Sox','Sox')
    _df['team'] = _df['team'].str.replace('[\w.]* ','')
    _df = _df.astype({'team': str,'W/L%': float})
    
    merge=pd.merge(team,_df,'outer', on = 'team')
    merge=merge.groupby('Metropolitan area').agg({'W/L%': np.nanmean, 'Population': np.nanmean})
    
    population_by_region = merge['Population'] # pass in metropolitan area population from cities
    win_loss_by_region = merge['W/L%'] # pass in win/loss ratio from _df in the same order as cities["Metropolitan area"]   

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]
mlb_correlation()
# %%
