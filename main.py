import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime

# Retrieves USdataframe
USdata = pd.read_json('https://covidtracking.com/api/v1/us/daily.json') 

# Retrieves Statedataframe
Statedata = pd.read_json('https://covidtracking.com/api/v1/states/current.json') 

# USdata Cleaning
USdata = USdata.fillna(0)
USdata = USdata[['date', 'positive', 'negative', 'hospitalizedCumulative', 'recovered', 'death', 'totalTestResults', 'positiveIncrease', 'negativeIncrease', 'deathIncrease', 'hospitalizedIncrease']]
USdata['totalCumulative'] = USdata['positive'] + USdata['recovered']
nrows = USdata['date'].count()
USdata = USdata.iloc[::-1]
USdata['Index'] = range(0,nrows,1)
USdata = USdata.set_index('Index')
for i in range(0, nrows):
  date = USdata.at[i, 'date']
  year = int(str(date)[0:4])
  month = int(str(date)[4:6])
  day = int(str(date)[6:8])
  USdata.at[i, 'date'] = datetime.date(year, month, day)
USdata.at[0, 'totalIncrease'] = 0
for i in range(1, nrows):
  USdata.at[i, 'totalIncrease'] = USdata.at[i, 'totalCumulative'] - USdata.at[i - 1, 'totalCumulative']
USdata.loc[USdata['totalIncrease'] > 60000, 'totalIncrease'] = 41532

# Statedata Cleaning
Statedata = Statedata[['state', 'positive', 'negative', 'hospitalizedCurrently', 'recovered', 'totalTestResults']]
Statedata = Statedata.set_index('state')
Statedata.at['PR', 'negative'] = 1490035
Statedata.at['AL', 'hospitalizedCurrently'] = 1612
Statedata.at['FL', 'hospitalizedCurrently'] = 9638
Statedata.at['HI', 'hospitalizedCurrently'] = 84
Statedata.at['ID', 'hospitalizedCurrently'] = 225
Statedata.at['KS', 'hospitalizedCurrently'] = 787
Statedata = Statedata.fillna(0)
Statedata['totalCumulative'] = Statedata['positive'] + Statedata['recovered']
stateAbbList = list(Statedata.index)
for i in range(0, Statedata['positive'].count()):
  stateAbb = stateAbbList[i]
  if stateAbb in ['WA', 'OR', 'CA', 'NV', 'ID', 'MT', 'WY', 'UT', 'CO']:
    Statedata.at[stateAbbList[i], 'region'] = 'West'
    Statedata.at[stateAbbList[i], 'regionColor'] = 'orange'
  elif stateAbb in ['AZ', 'NM', 'TX', 'OK']:
    Statedata.at[stateAbbList[i], 'region'] = 'Southwest'
    Statedata.at[stateAbbList[i], 'regionColor'] = 'red'
  elif stateAbb in ['ND', 'SD', 'NE', 'KS', 'MN', 'IA', 'MO', 'WI', 'IL', 'IN', 'MI', 'OH']:
    Statedata.at[stateAbbList[i], 'region'] = 'Midwest'
    Statedata.at[stateAbbList[i], 'regionColor'] = 'yellow'
  elif stateAbb in ['AR', 'LA', 'MS', 'TN', 'KY', 'GA', 'FL', 'SC', 'VA', 'WV', 'DC', 'MD', 'DE']:
    Statedata.at[stateAbbList[i], 'region'] = 'Southeast'
    Statedata.at[stateAbbList[i], 'regionColor'] = 'blue'
  elif stateAbb in ['PA', 'NJ', 'CT', 'RI', 'NY', 'VT', 'MA', 'NH', 'ME']:
    Statedata.at[stateAbbList[i], 'region'] = 'Northeast'
    Statedata.at[stateAbbList[i], 'regionColor'] = 'green'
  else:
    Statedata.at[stateAbbList[i], 'region'] = 'Other'
    Statedata.at[stateAbbList[i], 'regionColor'] = 'gray'

print(USdata)
print(Statedata)

# Question 1 Plotting
plt.figure(1)
ax = plt.gca()
formatter = mdates.DateFormatter("%Y-%m")
ax.xaxis.set_major_formatter(formatter)
locator = mdates.MonthLocator()
ax.xaxis.set_major_locator(locator)
plt.plot_date(USdata['date'], USdata['positive'], 'go-', color = 'green', linewidth = 2, markersize = 0, label = 'Currently Positive for Coronavirus')
plt.plot_date(USdata['date'], USdata['totalCumulative'], 'go-', color = 'blue', linewidth = 2, markersize = 0, label = 'Total Coronavirus Cases')
plt.plot_date(USdata['date'], USdata['hospitalizedCumulative'], 'go-', color = 'red', linewidth = 2, markersize = 0, label = 'Hospitalized')
plt.plot_date(USdata['date'], USdata['death'], 'go-', color = 'purple', linewidth = 2, markersize = 0, label = 'Deaths')
plt.grid()
plt.xlabel('Date (YYYY-MM)')
plt.ylabel('People in millions')
plt.title('Demographics of the Coronavirus in the US Figure 1')
plt.legend()
plt.savefig('plot1.png') # Check Files for plots

plt.figure(2)
ax = plt.gca()
formatter = mdates.DateFormatter("%Y-%m")
ax.xaxis.set_major_formatter(formatter)
locator = mdates.MonthLocator()
ax.xaxis.set_major_locator(locator)
plt.plot_date(USdata['date'], USdata['totalIncrease'], 'go-', color = 'blue', linewidth = 2, markersize = 0, label = 'Increase in Total Coronavirus Cases')
plt.grid()
plt.xlabel('Date (YYYY-MM)')
plt.ylabel('People per Day')
plt.title('Demographics of the Coronavirus in the US Figure 2')
plt.legend()
plt.savefig('plot2.png')

plt.figure(3)
ax = plt.gca()
formatter = mdates.DateFormatter("%Y-%m")
ax.xaxis.set_major_formatter(formatter)
locator = mdates.MonthLocator()
ax.xaxis.set_major_locator(locator)
plt.plot_date(USdata['date'], USdata['hospitalizedIncrease'], 'go-', color = 'red', linewidth = 2, markersize = 0, label = 'Increase in Hospitalized')
plt.plot_date(USdata['date'], USdata['deathIncrease'], 'go-', color = 'purple', linewidth = 2, markersize = 0, label = 'Increase in Death')
plt.grid()
plt.xlabel('Date (YYYY-MM)')
plt.ylabel('People per Day')
plt.title('Demographics of the Coronavirus in the US Figure 3')
plt.legend()
plt.savefig('plot3.png')

# Question 2 Plotting
Statedata = Statedata.sort_values('totalCumulative')
plt.figure(4)
plt.barh(Statedata.index, Statedata['totalCumulative'], color = Statedata['regionColor'])
plt.yticks(fontsize = 5, fontweight = 750, fontstretch = 1000)
plt.grid(axis = 'x')
orangeRegion = mpatches.Patch(color = 'orange', label = 'West')
redRegion = mpatches.Patch(color = 'red', label = 'Southwest')
blueRegion = mpatches.Patch(color = 'blue', label = 'Southeast')
yellowRegion = mpatches.Patch(color = 'yellow', label = 'Midwest')
greenRegion = mpatches.Patch(color = 'green', label = 'Northeast')
grayRegion = mpatches.Patch(color = 'gray', label = 'Other')
plt.legend(handles = [orangeRegion, redRegion, blueRegion, yellowRegion, greenRegion, grayRegion])
plt.xlabel('Total Coronavirus Cases')
plt.ylabel('States by State Abbreviation')
plt.title('Total Coronavirus Cases in Each State in the US Figure 1')
plt.savefig('plot4.png')

plt.figure(5)
plt.barh(Statedata.index, Statedata['totalCumulative'], color = Statedata['regionColor'], log = True)
plt.yticks(fontsize = 5, fontweight = 750, fontstretch = 1000)
plt.grid(which = 'both', axis = 'x')
orangeRegion = mpatches.Patch(color = 'orange', label = 'West')
redRegion = mpatches.Patch(color = 'red', label = 'Southwest')
blueRegion = mpatches.Patch(color = 'blue', label = 'Southeast')
yellowRegion = mpatches.Patch(color = 'yellow', label = 'Midwest')
greenRegion = mpatches.Patch(color = 'green', label = 'Northeast')
grayRegion = mpatches.Patch(color = 'gray', label = 'Other')
plt.legend(handles = [orangeRegion, redRegion, blueRegion, yellowRegion, greenRegion, grayRegion])
plt.xlabel('Total Coronavirus Cases')
plt.ylabel('States by State Abbreviation')
plt.title('Total Coronavirus Cases in Each State in the US Figure 2')
plt.savefig('plot5.png')

# Question 3 Plotting
plt.figure(6)
plt.plot(USdata['positive'], USdata['negative'], 'o', color = 'green', linewidth = 0, markersize = 3)
m, b = np.polyfit(USdata['positive'], USdata['negative'], 1)
m = round(m, 2)
plt.plot(USdata['positive'], m * USdata['positive'] + b, label = 'Line of Best Fit with slope = %s' % m)
plt.grid()
plt.xlabel('Positive Test Results in millions')
plt.ylabel('Negative Test Cases in ten millions')
plt.title('Ratio of Positive to Negative Test Results in the US')
plt.legend()
plt.savefig('plot6.png')

plt.figure(7)
plt.plot(USdata['death'], USdata['totalCumulative'], 'o', color = 'purple', linewidth = 0, markersize = 3)
m, b = np.polyfit(USdata['death'], USdata['totalCumulative'], 1)
m = round(m, 3)
plt.plot(USdata['death'], m * USdata['death'] + b, label = 'Line of Best Fit with slope = %s' % m)
plt.grid()
plt.xlabel('Deaths')
plt.ylabel('Total Cases in millions')
plt.title('Ratio of Deaths to Confirmed Cases in the US')
plt.legend()
plt.savefig('plot7.png')

"""
Research Questions:
1) How has the demographics of Coronavirus patients changed over time in the US?
2) How is the total number of Coronavirus patients distributed among states in the US?
3) How have the demograghics of the Coronavirus exhibited a ratio of positive to negative test results and a ratio of deaths to confirmed cases?
"""