import csv
from datetime import datetime

import matplotlib.pyplot as plt

filename = 'C:\\Users\\Joel\\Desktop\\work_portfolio\\Golden_Weather\\Golden_AirTemp_Precip_2010_Annual.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    for index, column_header in enumerate(header_row):              ##The enumerate() function returns both the index and value of each item.
        print(index, column_header)

    #Get dates and high/low temperatures from this file:
    dates, norm_max_temps, norm_avg_temps, norm_min_temps, precips = [], [], [], [], []
    for row in reader:
        current_date = datetime.strptime(row[5], '%m')
        norm_max_temp = float(row[9])
        norm_avg_temp = float(row[8])
        norm_min_temp = float(row[10])
        dates = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        norm_max_temps.append(norm_max_temp)
        norm_avg_temps.append(norm_avg_temp)
        norm_min_temps.append(norm_min_temp)
        # precips.append(precip)

print(norm_avg_temps)


## Plot the high and low temperatures.
plt.style.use('seaborn')
fig, ax = plt.subplots()
l1, = ax.plot(dates, norm_max_temps, c='red')
l2, = ax.plot(dates, norm_avg_temps, c='green')
l3, = ax.plot(dates, norm_min_temps, c='blue')
# l4, = ax.plot(dates, precips, c='blue')
ax.legend([l1, l2, l3], ['Max Temp', 'Avg Temp', 'Min Temp'], loc='best', shadow=True)
plt.fill_between(dates, norm_max_temps, norm_min_temps, facecolor='green', alpha=0.1)

## Format plot
plt.title("Monthly Min, Avg & Max Temperatures\n Golden, CO - 2010", fontsize=24)
plt.xlabel("Month", fontsize=16)
# fig.autofmt_xdate()
plt.xticks(dates)
# plt.yticks()
plt.ylabel("Temperature (F)", fontsize=16)
plt.tick_params(axis='x', which='minor', labelsize=5)

plt.show()

## A legend was attempted but appears to be used with plt.legend() and not ax.plot().

