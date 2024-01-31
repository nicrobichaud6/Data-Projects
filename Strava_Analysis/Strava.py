import pandas as pd 
import numpy as np
from time import strftime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from matplotlib.dates import HourLocator
import datetime as dt

strava_in = pd.read_csv('activities.csv')


## Cleaning and reformatting the names of the columns
def clean_col(c):
    c= c.strip()
    c= c.replace(" ", "_")
    c =c.lower()
    return c

new_columns = []
for columns in strava_in.columns:
    clean =  clean_col(columns)
    new_columns.append(clean)

strava_in.columns =new_columns


def clean_meters(m):
    return round(m/1000, 2)

strava_in['distance.1'] = strava_in['distance.1'].apply(clean_meters)



## There are two columns named "distance" so pandas renamed the second one distance.1.
## We'll change the name to distance_kms

strava_in.rename({'distance.1':'distance_km'}, axis= 1, inplace=True)

## Need to change the distance from a string to a float, first we need to replace the , to . so that it can convert

strava_in['distance_km'] = strava_in['distance_km'].astype(float)


## I noticed that back country skiing is its own activity when it should be nordic skiing
## so we'll replace backcountry by nordic. Also, windsurfing is really just sailing so 
## we'll replace that as well

## We could also do this after the count but doesn't make a lot of difference in this case

strava_in['activity_type']= strava_in['activity_type'].replace('Backcountry Ski', 'Nordic Ski') 
strava_in['activity_type']= strava_in['activity_type'].replace('Windsurf', 'Sailing')
strava_in['activity_type']= strava_in['activity_type'].replace('Stand Up Paddling', 'SUP')


## these df are for the mean time
act_total= strava_in['activity_type'].value_counts().reset_index()

time_mean= strava_in.groupby("activity_type")['elapsed_time'].mean().reset_index()


## this df is for the total distance per activity
distances = strava_in
distances['activity_type'] = distances['activity_type'].replace('Virtual Ride', 'Ride')
distances = strava_in.groupby("activity_type")['distance_km'].sum().reset_index()
distances = distances.sort_values(by= ['distance_km'], ascending= False).reset_index()


distances = distances[distances['distance_km']>0.01]

count_n_time = pd.merge(act_total, time_mean, on="activity_type", how= 'inner')

count_n_time['elapsed_time'] = count_n_time['elapsed_time'].round()

count_n_time['elapsed_time'] = pd.to_timedelta(count_n_time['elapsed_time'],'s')

count_n_time['elapsed_time'] = count_n_time['elapsed_time'].dt.total_seconds()

count_n_time['elapsed_time'] = count_n_time['elapsed_time'].apply(lambda x: '{:02}:{:02}:{:02}'.format(int(x // 3600), int((x % 3600) // 60), int(x % 60)))

time_fin = count_n_time

time_fin['elapsed_time'] = pd.to_timedelta(time_fin['elapsed_time'])
time_fin= time_fin.sort_values(by = 'elapsed_time', ascending = False).reset_index()



## Time to group activities per month activity_date, elapsed_time



grouped_time = strava_in

grouped_time['elapsed_time'] =  grouped_time['elapsed_time'].round()

grouped_time['elapsed_time'] = pd.to_timedelta(grouped_time['elapsed_time'],'s')

grouped_time['elapsed_time'] = grouped_time['elapsed_time'].dt.total_seconds()


grouped_time["date_activity"] = pd.to_datetime(strava_in['activity_date'], format='%d %b %Y, %H:%M:%S')

grouped_time['year'] = grouped_time["date_activity"].dt.year
grouped_time['month'] = grouped_time["date_activity"].dt.month

group_final= pd.DataFrame()

group_final['year'] = grouped_time['year']
group_final['month'] = grouped_time['month']
group_final['Time'] = grouped_time['elapsed_time']


group_final = group_final.groupby(["year", "month"]).sum().reset_index()


filtered_2021 = group_final[(group_final["year"]==2021) & (group_final["month"] >= 10) | (group_final["year"]==2022) & (group_final["month"] <= 5)]

filtered_2022 = group_final[(group_final["year"]==2022) & (group_final["month"] >= 10) | (group_final["year"]==2023) & (group_final["month"] <= 5)]

filtered_2021['month']= pd.to_datetime(filtered_2021['month'], format ='%m').dt.month_name()

filtered_2022['month']= pd.to_datetime(filtered_2022['month'], format ='%m').dt.month_name()


filtered_2021['Time'] = round(filtered_2021['Time'] / 3600, 1)

filtered_2022['Time'] = round(filtered_2022['Time'] / 3600, 1)


plt.plot(filtered_2021['month'],filtered_2021['Time'], label = "Canada: 2021 - 2022", color = 'steelblue' , lw= 3)
plt.plot(filtered_2022['month'],filtered_2022['Time'], label = "Thailand: 2022 - 2023", color = 'seagreen', lw= 3 )
plt.ylabel("Hours of Activity")
plt.title("Hours of Activity in the Winter: Canada Vs. Thailand")
plt.xticks(rotation = 45)
plt.legend()
plt.tight_layout()
plt.show()




plt.barh(count_n_time['activity_type'], count_n_time['count'], edgecolor="white")
plt.title('Activity Count Per Type')
plt.xlabel('Frequency')
for index, value in enumerate(count_n_time['count']):
    plt.text(value, index,
             str(value))

plt.xticks()
plt.tight_layout()

plt.show()

#width=1, linewidth=0.7
plt.figure().set_figwidth(11)
plt.barh(distances['activity_type'], distances['distance_km'],edgecolor="white")
plt.title('KM Per Type of Activity')
plt.xlabel('Total Kilometers')
plt.tick_params(axis = 'x',rotation = 60)
for index, value in enumerate(distances['distance_km']):
    plt.text(value, index,
             str(round(value,1)))


plt.tight_layout()


plt.show()








