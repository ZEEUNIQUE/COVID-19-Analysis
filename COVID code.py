import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# the data was imported from github page of John Hopkins University Hospital
confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
confirmed.head()

deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
deaths.head()

recoveries = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
recoveries.head()

most_recent=confirmed.columns[-1]
# most_recent would be used to extract the last updated column of COVID19 data

conf1 = pd.pivot_table(confirmed, values=most_recent, index=['Country/Region'], aggfunc=np.sum)
death1 = pd.pivot_table(deaths, values=most_recent, index=['Country/Region'], aggfunc=np.sum)
recov1 = pd.pivot_table(recoveries, values=most_recent, index=['Country/Region'], aggfunc=np.sum)


#Now, dataframe of confirmed cases would be merged to the dataframes for 
#recovered and deaths. So we would have a single dataframe that has confirmed cases,
#recovery and deaths as seperate columns


mergedDf = conf1.merge(recov1[most_recent], left_index=True, right_index=True)
mergedDf = mergedDf.merge(death1[most_recent], left_index=True, right_index=True)

mergedDf.columns = ['Confirmed_cases','Recoveries','Deaths']
mergedDf['recovery_rate']=mergedDf['Recoveries']/mergedDf['Confirmed_cases']
mergedDf['death_rate']=mergedDf['Deaths']/mergedDf['Confirmed_cases']

#Now, the worst hit countries were filtered using the sort_values(),
#head() and tails() methods 


top7_confirmed = mergedDf['Confirmed_cases'].sort_values(ascending=False).head(7)
top7_recovery = mergedDf['recovery_rate'].sort_values(ascending=False).head(7)
top7_death = mergedDf['death_rate'].sort_values(ascending=False).head(7)

top7_confirmed.plot(kind='bar')
plt.ylabel("Counts of Confirmed Cases of COVID19")
plt.title("Confirmed Cases in Worst Hit Countries")


top7_recovery.plot(kind='bar')
plt.ylabel("Death Rates")
plt.title("Countries with Highest Death Rates")


top7_death.plot(kind='bar')
plt.ylabel("Death Rates")
plt.title("Countries with Highest Death Rates")
