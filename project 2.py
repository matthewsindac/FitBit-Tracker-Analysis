import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy import stats


heartratedata = pd.read_csv("heartrate_seconds_merged.csv")

def heartrategraphs(heartratedata):
    users = [2022484408, 4558609924, 2347167796, 4020332650, 4388161847, 5577150313, 6117666160]

    heartratedata['Time'] = pd.to_datetime(heartratedata['Time'])
    heartratedata = heartratedata[heartratedata['Id'].isin(users)]
    n = heartratedata.set_index('Time')
    nresample = n.groupby('Id')['Value'].resample('D').mean().reset_index()

    fig, ax = plt.subplots()

    date = mdates.DateFormatter("%m/%d/%Y")
    ax.xaxis.set_major_formatter(date)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval = 1))
    ax.set_ylim(0, 130)
    ax.set_yticks(range(0, 130, 10))

    lines = []

    for id, data in nresample.groupby('Id'):
        line, = ax.plot(data['Time'], data['Value'], label = f'User {id}')
        lines.append(line)

    plt.grid(True)

    legend = plt.legend(loc = 'upper left', bbox_to_anchor = (1, 1))
    ax.add_artist(legend)
    plt.xticks(rotation = 45)

    def toggleline(event):
        if event.key.isdigit() and 1 <= int(event.key) <= len(lines):
            id = int(event.key) - 1
            for i, line in enumerate(lines):
                line.set_visible(i == id)
            plt.draw()
        elif event.key == '0':
            for line in lines:
                line.set_visible(True)
            plt.draw()

    # 1-7 on the keyboard displays the lines individually, 0 resets it to see it all.
    fig.canvas.mpl_connect('key_press_event', toggleline)

    plt.title("Daily Average Heartrates of Users")
    plt.xlabel("Days")
    plt.ylabel("Average Heartrates")

    plt.subplots_adjust(left = 0.1, right = 0.8, top = 0.9, bottom = 0.2)

    plt.show()

heartrategraphs(heartratedata)

dailysleepdata = pd.read_csv("sleepDay_merged.csv")

def dailysleepgraphs(dailysleepdata):
    dailysleepdata['SleepDay'] = pd.to_datetime(dailysleepdata['SleepDay'],
                                                format = '%m/%d/%Y %I:%M:%S %p')

    n = dailysleepdata.groupby(['Id', 'SleepDay'])['TotalMinutesAsleep'].mean().reset_index()
    average = n.groupby('SleepDay')['TotalMinutesAsleep'].mean().reset_index()

    fig, ax = plt.subplots()

    date = mdates.DateFormatter("%m/%d")
    ax.xaxis.set_major_formatter(date)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval = 1))

    ax.scatter(dailysleepdata['SleepDay'], dailysleepdata['TotalMinutesAsleep'], s = 10,
               alpha = 0.3, color = 'blue', label = 'All Users')

    ax.plot(average['SleepDay'], average['TotalMinutesAsleep'], color = 'red',
            label = 'Daily Average of All Users', linewidth = 2)

    z = stats.zscore(dailysleepdata['TotalMinutesAsleep'])
    threshold = 3
    theoutliers = (z > threshold) | (z < -threshold)
    outliers = dailysleepdata[theoutliers]
    sort = outliers.sort_values(by = 'Id')
    unique = sort['Id'].unique()

    for user in unique:
        useroutliers = sort[sort['Id'] == user]
        ax.scatter(useroutliers['SleepDay'], useroutliers['TotalMinutesAsleep'],
                   s = 20, label = f'(Outlier) User {user}', color = 'black')

    plt.grid(True)
    plt.legend(loc = 'upper left', bbox_to_anchor = (1.0, 1.0))
    plt.xticks(rotation = 45)

    plt.title("Daily Sleep Per User (Scatterplot) With Daily Total Averages")
    plt.xlabel("Days From 4/11/2016 - 5/13/2016")
    plt.ylabel("Total Minutes Slept Per Day")

    plt.subplots_adjust(left = 0.05, right = 0.8, top = 0.9, bottom = 0.2)

    plt.show()

dailysleepgraphs(dailysleepdata)

dailystepsdata = pd.read_csv("dailySteps_merged.csv")

def dailystepsgraph(dailystepsdata):
    dailystepsdata['ActivityDay'] = pd.to_datetime(dailystepsdata['ActivityDay'])

    nresample = dailystepsdata.groupby(['Id', 'ActivityDay'])['StepTotal'].mean().reset_index()
    average = nresample.groupby('ActivityDay')['StepTotal'].mean().reset_index()

    fig, ax = plt.subplots()

    date = mdates.DateFormatter("%m/%d")
    ax.xaxis.set_major_formatter(date)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval = 1))



    ax.scatter(dailystepsdata['ActivityDay'], dailystepsdata['StepTotal'], s = 10,
               alpha = 0.1, color = 'blue', label = 'All Users')

    ax.plot(average['ActivityDay'], average['StepTotal'], color = 'red',
            label = 'Daily Average of All Users', linewidth = 2)

    z = stats.zscore(dailystepsdata['StepTotal'])
    threshold = 3
    theoutliers = (z > threshold) | (z < -threshold)
    outliers = dailystepsdata[theoutliers]
    sort = outliers.sort_values(by = 'Id')
    unique = sort['Id'].unique()

    for user in unique:
        useroutliers = sort[sort['Id'] == user]
        ax.scatter(outliers['ActivityDay'], outliers['StepTotal'],
                   s = 20, color = 'black', label = f'(Outlier) User {user}')


    plt.grid(True)
    plt.legend(loc = 'upper left', bbox_to_anchor = (1.01, 1.0))
    plt.xticks(rotation = 45)

    plt.title("Daily Steps per User (Scatterplot) with Daily Total Averages")
    plt.xlabel("Days From 4/11/2016 - 5/13/2016")
    plt.ylabel("Total Steps Per Day")

    plt.subplots_adjust(left = 0.1, right = 0.8, top = 0.9, bottom = 0.2)

    plt.show()

dailystepsgraph(dailystepsdata)

weightrecorddata = pd.read_csv('weightLogInfo_merged.csv')

def weightgraph(weightrecorddata):
    highestrecords = weightrecorddata['Id'].value_counts().idxmax()
    newdata = weightrecorddata[weightrecorddata['Id'] == highestrecords].reset_index(drop = True)
    newdata['Date'] = pd.to_datetime(newdata['Date'], format = '%m/%d/%Y %I:%M:%S %p')

    newdata['Date'] = newdata['Date'] - pd.DateOffset(days = 1)

    plt.scatter(newdata['Date'], newdata['WeightKg'], label = 'Weight Data Per Day', color = 'blue')
    plt.plot(newdata['Date'], newdata['WeightKg'], label = 'Weight Data Over Time', color = 'red')

    days = mdates.DayLocator()
    daysformat = mdates.DateFormatter('%m/%d')
    plt.gca().xaxis.set_major_locator(days)
    plt.gca().xaxis.set_major_formatter(daysformat)

    plt.title(f"Weight Change of User {highestrecords}")
    plt.xlabel("Days From 4/11/2016 - 5/13/2016")
    plt.ylabel("Weight (KG)")
    plt.legend(loc = 'upper left', bbox_to_anchor = (1.02, 1.0))
    plt.xticks(rotation = 45)
    plt.grid(True)
    plt.subplots_adjust(left = 0.1, right = 0.8, top = 0.9, bottom = 0.2)
    plt.show()

weightgraph(weightrecorddata)

hourlystepsdata = pd.read_csv('hourlySteps_merged.csv')
hourlyintensitiesdata = pd.read_csv('hourlyIntensities_merged.csv')
hourlycaloriesdata = pd.read_csv('hourlyCalories_merged.csv')

minutecaloriesndata = pd.read_csv('minuteCaloriesNarrow_merged.csv')
minuteintensitiesndata = pd.read_csv('minuteIntensitiesNarrow_merged.csv')
minutemetsndata = pd.read_csv('minuteMETsNarrow_merged.csv')

dailysleepdata = pd.read_csv('sleepDay_merged.csv')
dailyactivitydata = pd.read_csv('dailyActivity_merged.csv')

heartratedata = pd.read_csv("heartrate_seconds_merged.csv")

def processdata(hourlystepsdata, hourlyintensitiesdata, hourlycaloriesdata,
                minutecaloriesndata, minuteintensitiesndata, minutemetsndata,
                dailysleepdata, dailyactivitydata,
                heartratedata):

    hourly = hourlystepsdata.merge(hourlyintensitiesdata, on = ['Id', 'ActivityHour'], how = 'inner') \
        .merge(hourlycaloriesdata, on = ['Id', 'ActivityHour'], how = 'inner')

    minutely = minutemetsndata.merge(minuteintensitiesndata, on = ['Id', 'ActivityMinute'], how = 'inner') \
        .merge(minutecaloriesndata, on = ['Id', 'ActivityMinute'], how = 'inner')

    dailysleepdata['Date'] = pd.to_datetime(dailysleepdata['SleepDay'], format = '%m/%d/%Y %I:%M:%S %p')
    dailyactivitydata['Date'] = pd.to_datetime(dailyactivitydata['ActivityDate'], format = '%m/%d/%Y')
    hourly['Date'] = pd.to_datetime(hourly['ActivityHour'], format = '%m/%d/%Y %I:%M:%S %p')
    minutely['Date'] = pd.to_datetime(minutely['ActivityMinute'], format = '%m/%d/%Y %I:%M:%S %p')

    heartratedata['Time'] = pd.to_datetime(heartratedata['Time'])
    heartratedata = heartratedata.set_index('Time')
    averageheartratedata = heartratedata.groupby('Id')['Value'].resample('T').mean().reset_index()

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    print(dailysleepdata.head(5))
    print(minutely.head(5))
    print(hourly.head(5))
    print(dailyactivitydata.head(5))
    print(averageheartratedata.head(5))

processdata(hourlystepsdata, hourlyintensitiesdata, hourlycaloriesdata,
            minutecaloriesndata, minuteintensitiesndata, minutemetsndata,
            dailysleepdata, dailyactivitydata,
            heartratedata)

def comparehourly(hourlystepsdata, hourlyintensitiesdata, hourlycaloriesdata):
    stepscalories = hourlystepsdata.merge(hourlycaloriesdata,
                                          on = ['Id', 'ActivityHour'], how = 'inner')
    intensitycalories = hourlyintensitiesdata.merge(hourlycaloriesdata,
                                                    on = ['Id', 'ActivityHour'], how = 'inner')

    plt.figure(figsize = (10, 5))
    plt.subplot(1, 2, 1)
    plt.scatter(stepscalories['StepTotal'], stepscalories['Calories'], s = 1, color = 'blue')
    plt.title('Steps vs. Calories')
    plt.xlabel('Steps')
    plt.ylabel('Calories')

    plt.subplot(1, 2, 2)
    plt.scatter(intensitycalories['TotalIntensity'], intensitycalories['Calories'], s = 1, color = 'red')
    plt.title('Intensity vs. Calories')
    plt.xlabel('Intensity')
    plt.ylabel('Calories')

    plt.tight_layout()
    plt.show()

comparehourly(hourlystepsdata, hourlyintensitiesdata, hourlycaloriesdata)

def sleepcorrelation(dailysleepdata):
    plt.scatter(dailysleepdata['TotalMinutesAsleep'], dailysleepdata['TotalTimeInBed'], s = 2)
    plt.xlabel('Total Minutes Asleep')
    plt.ylabel('Total Time In Bed')
    plt.title('Total Minutes Asleep vs Total Time In Bed')


    slope, intercept, rvalue, pvalue, stderr =\
        stats.linregress(dailysleepdata['TotalMinutesAsleep'], dailysleepdata['TotalTimeInBed'])

    plt.plot(dailysleepdata['TotalMinutesAsleep'],
             slope * dailysleepdata['TotalMinutesAsleep'] + intercept,
             color='red', label = 'Regression Line')

    plt.legend(loc='upper left', bbox_to_anchor = (1.02, 1.0))
    plt.subplots_adjust(left = 0.1, right = 0.8, top = 0.9, bottom = 0.1)

    plt.show()

sleepcorrelation(dailysleepdata)

def intensitydistribution(hourlyintensities):
    hourlyintensities['Time'] = pd.to_datetime(hourlyintensities['ActivityHour'], format = '%m/%d/%Y %I:%M:%S %p')

    hourlyintensities['Date'] = hourlyintensities['Time'].dt.date
    hourlyintensities['TimeOfDay'] = hourlyintensities['Time'].dt.hour
    datafilter = hourlyintensities[hourlyintensities['Time'].dt.date == pd.to_datetime('4/12/2016').date()].\
        reset_index(drop = True)

    for id, group in datafilter.groupby('Id'):
        plt.bar(group['TimeOfDay'], group['TotalIntensity'], label = f'Id {id}', alpha = 0.15)

    plt.xticks(range(24))
    legend = plt.legend(title = 'Id', loc = 'upper left', bbox_to_anchor = (1.02, 1.13))
    for text in legend.get_texts():
        text.set_fontsize(8)
    plt.subplots_adjust(left = 0.1, right = 0.8, top = 0.9, bottom = 0.2)
    plt.title('Total Intensity Per Hour By User On 4/12/2016')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Total Intensity')
    plt.show()

intensitydistribution(hourlyintensitiesdata)

dailysleepdata = pd.read_csv('sleepDay_merged.csv')
dailyintensitiesdata = pd.read_csv('dailyIntensities_merged.csv')

def sleepandsedentary(dailysleepdata, dailyintensitiesdata):
    dailysleepdata['Date'] = pd.to_datetime(dailysleepdata['SleepDay'], format = '%m/%d/%Y %I:%M:%S %p')
    dailyintensitiesdata['Date'] = pd.to_datetime(dailyintensitiesdata['ActivityDay'])

    newdata = dailysleepdata.merge(dailyintensitiesdata, on = ['Id', 'Date'], how = 'inner')


    plt.scatter(newdata['TotalMinutesAsleep'], newdata['SedentaryMinutes'], s = 2)
    plt.xlabel('Total Minutes Asleep')
    plt.ylabel('Sedentary Minutes')
    plt.title('Total Minutes Asleep vs Sedentary Minutes')

    plt.show()

sleepandsedentary(dailysleepdata, dailyintensitiesdata)

dailyactivitydata = pd.read_csv('dailyActivity_merged.csv')

def caloriescorrelation(dailyactivitydata):

    group1 = dailyactivitydata[dailyactivitydata['LightlyActiveMinutes']\
                               > dailyactivitydata['LightlyActiveMinutes'].mean()]
    group2 = dailyactivitydata[dailyactivitydata['LightlyActiveMinutes']\
                               <= dailyactivitydata['LightlyActiveMinutes'].mean()]

    tstatlight, pvaluelight = stats.ttest_ind(group1['Calories'], group2['Calories'])

    # print(group1)
    # print(group2)

    group3 = dailyactivitydata[dailyactivitydata['SedentaryMinutes'] \
                               > dailyactivitydata['SedentaryMinutes'].mean()]
    group4 = dailyactivitydata[dailyactivitydata['SedentaryMinutes'] \
                               <= dailyactivitydata['SedentaryMinutes'].mean()]

    tstatsedentary, pvaluesedentary = stats.ttest_ind(group3['Calories'], group4['Calories'])

    # print(group3)
    # print(group4)

    print(tstatlight, pvaluelight)
    # 5.7406402066972575, 1.2730479146564296e-08
    print(tstatsedentary, pvaluesedentary)
    # -1.8802978707120994, 0.06037716807778881

caloriescorrelation(dailyactivitydata)





