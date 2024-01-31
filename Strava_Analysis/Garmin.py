import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.dates import HourLocator
import datetime as dt
import seaborn as sns

# Let's start by combining all the different files in folder 

files = [file for file in os.listdir("C:/Users/Nicolas/Documents/Python/Projects/Python Project/Strava Data/Garmin/DI_CONNECT/DI-Connect-Aggregator/Steps")]

all_data = pd.DataFrame()

for file in files:
	df = pd.read_json("C:/Users/Nicolas/Documents/Python/Projects/Python Project/Strava Data/Garmin/DI_CONNECT/DI-Connect-Aggregator/Steps/"+file)
	all_data = pd.concat([all_data, df])


#we'll check to make sure the rows have been combined in one dataframe
print(all_data.shape)

all_data["calendarDate"] = pd.to_datetime(all_data['calendarDate'], format="%Y-%m-%d")


grouped_data = pd.DataFrame()

grouped_data = all_data

grouped_data['year']= grouped_data['calendarDate'].dt.year
grouped_data['month']= grouped_data['calendarDate'].dt.month




# so, over the last 2-3 years I have worn my watch almost every single day, but there are still days where for some reason or another,
# I had to take it off or it died and I couldn't charge it so for the sake of trying to keep the daily average a bit more accurate,
# we'll exclude any days that have under 4000 steps as I feel confident enough saying that in a full day, even an inactive one, I get 
# more steps than 4000

#totalSteps
grouped_data = grouped_data[grouped_data["totalSteps"] >4000]


print(grouped_data['totalSteps'].min())
print(grouped_data['totalSteps'].max())



#With this dataset all together now, we're going to do a monthly average of daily steps to compare 2021 to 2022 

group_final= pd.DataFrame()

group_final['year'] = grouped_data['year']
group_final['month'] = grouped_data['month']
group_final['Steps'] = grouped_data['totalSteps']


###this will be used for the normal distribution later

dist_2021 = group_final[(group_final["year"]==2021) & (group_final["month"] >= 10) | (group_final["year"]==2022) & (group_final["month"] <= 5)]

dist_2022 = group_final[(group_final["year"]==2022) & (group_final["month"] >= 10) | (group_final["year"]==2023) & (group_final["month"] <= 5)]


group_final = group_final.groupby(["year", "month"]).mean().reset_index()


## This part is for comparing the average daily steps for the two winters

group_final['Steps']=group_final['Steps'].round()

print(group_final.head())

filtered_2021 = group_final[(group_final["year"]==2021) & (group_final["month"] >= 10) | (group_final["year"]==2022) & (group_final["month"] <= 5)]

filtered_2022 = group_final[(group_final["year"]==2022) & (group_final["month"] >= 10) | (group_final["year"]==2023) & (group_final["month"] <= 5)]


filtered_2021['month']= pd.to_datetime(filtered_2021['month'], format ='%m').dt.month_name()

filtered_2022['month']= pd.to_datetime(filtered_2022['month'], format ='%m').dt.month_name()


plt.plot(filtered_2021['month'],filtered_2021['Steps'], label = "Canada: 2021 - 2022", c = 'steelblue', lw = 3 )
plt.plot(filtered_2022['month'],filtered_2022['Steps'], label = "Thailand: 2022 - 2023", c= 'seagreen', lw= 3 )
plt.ylabel("Average Daily Steps")
plt.title("Step Comparison: Canada Vs. Thailand")
plt.xticks(rotation = 45)
plt.legend()
plt.tight_layout()
plt.show()



# and then do a normal distribution of the daily steps 

fig,axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

sns.distplot(dist_2021['Steps'], color = 'steelblue', ax=axes[0])
axes[0].set_title("Step Distribution: Canada")
plt.xlabel("Steps") 



sns.distplot(dist_2022['Steps'], color = 'seagreen', ax=axes[1])
axes[1].set_title("Step Distribution: Thailand")
plt.xlabel("Steps")
plt.ylabel("")
plt.tight_layout()
plt.show()



## Doesn't give us as much info as we would like, let's try doing a box and whiskers plot side by side


colors = ['steelblue','seagreen']
labels= ['Canada','Thailand']
bp=plt.boxplot([dist_2021['Steps'],dist_2022['Steps']], 0, '', labels =labels,patch_artist=True)
plt.title("Step Distribution: Canada vs. Thailand")
plt.setp(bp['whiskers'][0:2], color='steelblue',linewidth =1.5 )
plt.setp(bp['boxes'][0], color= 'steelblue',alpha = 0.3, linewidth =1.5)
plt.setp(bp['caps'][0:2], color= 'steelblue', linewidth =1.5)


plt.setp(bp['whiskers'][2:4], color='seagreen',linewidth =1.5 )
plt.setp(bp['boxes'][1], color= 'seagreen', facecolor='seagreen', alpha = 0.3 , linewidth =1.5)
plt.setp(bp['caps'][2:4], color= 'seagreen', linewidth =1.5)


plt.show()


print(dist_2021['Steps'].describe())
print(dist_2022['Steps'].describe())


