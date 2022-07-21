#%%
# Q1
from numpy.core.fromnumeric import shape
import pandas as pd 
import numpy as np
df = pd.read_csv('NISPUF17.csv', index_col = 0)
df.head()

edu = df['EDUC1'].sort_values(ascending = False)

# edu frequency
freq = edu.value_counts()

# proportion_of_education
ratio = freq / np.sum(freq)

poe = dict()
poe["less than high school"] = ratio[1]
poe["high school"] = ratio[2] 
poe["more than high school but not college"] = ratio[3]
poe["college"] = ratio[4]

print(poe)

# %%
# Q2
cbf_flu = df.loc[:, ['CBF_01','P_NUMFLU']].dropna()
cbf_flu.head()

cbf_flu1=cbf_flu[cbf_flu['CBF_01'] ==1]
cbf_flu2=cbf_flu[cbf_flu['CBF_01'] ==2]

# average number of influenza vaccines for those children we know received breastmilk
avg_receve = sum(cbf_flu1.loc[:, 'P_NUMFLU']) / len(cbf_flu1.loc[:, 'P_NUMFLU'])
avg_not = sum(cbf_flu2.loc[:, 'P_NUMFLU']) / len(cbf_flu2.loc[:, 'P_NUMFLU'])
print((avg_receve, avg_not))

# %%
# Q3
# the ratio of the number of children who contracted chickenpox but were vaccinated against it versus those who were vaccinated but did not contract chicken pox.
cpo_vrc_sex = df.loc[:,['HAD_CPOX','P_NUMVRC','SEX']]
cpo_vrc_sex.head()

cpo_sex = cpo_vrc_sex[cpo_vrc_sex['P_NUMVRC'].gt(0) & df['HAD_CPOX'].lt(3)].loc[:,['HAD_CPOX','SEX']].dropna()

#Male 1 Female 2
cpo1_sex1=len(cpo_sex[(cpo_sex['HAD_CPOX']==1) & (cpo_sex['SEX']==1)])
cpo2_sex1=len(cpo_sex[(cpo_sex['HAD_CPOX']==2) & (cpo_sex['SEX']==1)])
cpo1_sex2=len(cpo_sex[(cpo_sex['HAD_CPOX']==1) & (cpo_sex['SEX']==2)])
cpo2_sex2=len(cpo_sex[(cpo_sex['HAD_CPOX']==2) & (cpo_sex['SEX']==2)])

cbs = dict()
cbs['male']=cpo1_sex1/(cpo1_sex1+cpo2_sex1)
cbs['female']=cpo1_sex2/(cpo1_sex2+cpo2_sex2)

cbs

# %%
# Q4
# if there is a correlation between having had the chicken pox and the number of chickenpox vaccine doses
import scipy.stats as stats
df=df[df['HAD_CPOX'].lt(3)].loc[:,['HAD_CPOX','P_NUMVRC']].dropna()
df.head()

corr, pval = stats.pearsonr(df["HAD_CPOX"],df["P_NUMVRC"])
print(corr,pval)