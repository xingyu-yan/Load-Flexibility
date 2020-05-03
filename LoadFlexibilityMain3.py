# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 09:11:39 2020
At GEIDCO, Beijing
@author: Xingyu
Objective: Load Flexibility Calculation 
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from FlexibilityFunc import FlexibilityCalculate, Ave_Resi_Load

# 读取csv文件
csvFile = open("HourlyData_Region_2035_NetLoad_OR.csv", "r")

# 方法1
# reader = csv.DictReader(csvFile) 
# column = [row['FR'] for row in reader] # 选取法国的数据作为计算对象
# print('The Column Number of All Load is %d' % len(column))
# Load = list(map(float, column)) # 字符串转换为数字  

# 方法2
reader = csv.reader(csvFile) 
rows = [row for row in reader]
print('File info: ' + str(rows[0][0]))
FirstLine = rows[4]
for index in range(len(FirstLine)):
    print('The column %d is: ' % index + str(FirstLine[index]))

# Load = np.mat(rows[5:len(rows)])[0:8761,3:16]    
Load = np.mat(rows[4:len(rows)])[0:8761]

# #Plot the Load of PRC  
# plt.figure()
# plt.plot(Load[1:8761,7])
# # plt.plot(Load[0:168])
# plt.title('NetLoad profile of PRC')
# plt.ylabel('MW')
# plt.xlabel('Time (Hour)')
# plt.show()

# Country = input('Which Country Do You Want to Choose: ')
    
Flexibility_Day = []
Flexibility_Week = []
Flexibility_Year = []

Ave_Hourly_Load = []
Hourly_Graddient = []
for i in range(13):
    # 字符串转换为数字
    if i == 4:
        print()
        print('Skip the ' + Load[0,i+3] )
        print()
    else:
        Load_Sub = list(map(float,Load[1:8761,i+3]))
        Load_Sub_Name = 'Load_' + Load[0,i+3]
        print('Calculating the Flexibility of ' + Load_Sub_Name)
        
        (Flexi_Day, Flexi_Week, Flexi_Year) = FlexibilityCalculate(Load_Sub, Load_Sub_Name)
        Flexibility_Day.append(Flexi_Day)
        Flexibility_Week.append(Flexi_Week)
        Flexibility_Year.append(Flexi_Year)   
        
        (AVE_Hour, Hourly_Grad) = Ave_Resi_Load(Load_Sub, Load_Sub_Name)
        Ave_Hourly_Load.append(AVE_Hour)
        Hourly_Graddient.append(Hourly_Grad)

    
# Plot the load flexibility result  
# plt.figure()
# # labels = ['GB', 'EPT', 'EUR_SE', 'Central Asia', 'PRC', 'FR', 'BNL', 'DE', 'CH', 'PL', 'SC', 'BL', 'IT']
# Locations = ['GB', 'EPT', 'EUR_SE', 'Central Asia', 'FR', 'BNL', 'DE', 'CH', 'PL', 'SC', 'BL', 'IT']
# x = np.arange(len(Locations))
# width = 0.3
# plt.bar(x, Flexibility_Day, width, label='Daily Load Flexibility', fc = 'y')
# plt.bar(x + width, Flexibility_Week, width, label='Weekly Load Flexibility', fc = 'r')
# plt.bar(x + 2*width, Flexibility_Year, width, label='Yearly Load Flexibility', fc = 'b')
# plt.xticks(x+width/3, labels, rotation='vertical') # rotation=45
# plt.title('NetLoad Flexibility')
# plt.ylabel('TWh')
# plt.xlabel('Country/Region')
# plt.legend()
# plt.show() 

# plt.figure()
# Locations = ['GB', 'EPT', 'EUR_SE', 'Cent_Asia', 'FR', 'BNL', 'DE', 'CH', 'PL', 'SC', 'BL', 'IT']
# x = np.arange(len(Locations))
# plt.subplot(3, 1, 1)
# plt.bar(x, Flexibility_Day, label='Daily Load Flexibility', fc = 'y')
# plt.ylabel('TWh')
# plt.legend()
# plt.title('NetLoad Flexibility')
# plt.subplot(3, 1, 2)
# plt.bar(x, Flexibility_Week, label='Weekly Load Flexibility', fc = 'r')
# plt.ylabel('TWh')
# plt.legend()
# plt.subplot(3, 1, 3)
# plt.bar(x, Flexibility_Year, label='Yearly Load Flexibility', fc = 'b')
# plt.ylabel('GWh')
# plt.legend()
# plt.xticks(x, Locations, rotation=30) # rotation='vertical'
# plt.xlabel('Country/Region')
# plt.show() 

fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, dpi = 600)
Locations = ['GB', 'EPT', 'EUR_SE', 'Cent_Asia', 'FR', 'BNL', 'DE', 'CH', 'PL', 'SC', 'BL', 'IT']
x = np.arange(len(Locations))
labels = ['Daily Load Flexibility', 'Weekly Load Flexibility', 'Yearly Load Flexibility']
fig.suptitle('NetLoad Flexibility')
ax1.bar(x, Flexibility_Day, color='red', label=labels[0])
ax1.legend(loc="upper right")
ax1.set_ylabel('TWh')
ax2.bar(x, Flexibility_Week, color='orange', label=labels[1])
ax2.legend(loc="upper left")
ax2.set_ylabel('TWh')
ax3.bar(x, Flexibility_Year, color='blue', label=labels[2])
ax3.legend(loc="upper left")
ax3.set_ylabel('GWh')
plt.xticks(x, Locations, rotation='vertical') # rotation='vertical'
plt.xlabel('Country/Region')
plt.show() 

# Plot the average daily residual load results
#Plot the Load of PRC  
plt.figure(dpi = 600)
label = ['GB', 'EPT', 'EUR_SE', 'Cent_Asia', 'FR', 'BNL', 'DE', 'CH', 'PL', 'SC', 'BL', 'IT']
for i in range(len(Ave_Hourly_Load)):
    plt.plot(Ave_Hourly_Load[i], label=label[i])
# plt.plot(Load[0:168])
plt.title('Average Residual Load')
plt.ylabel('GW')
plt.xlabel('Time (Hour)')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

plt.figure(dpi = 600)
label = ['GB', 'EPT', 'EUR_SE', 'Cent_Asia', 'FR', 'BNL', 'DE', 'CH', 'PL', 'SC', 'BL', 'IT']
for i in range(len(Ave_Hourly_Load)):
    plt.plot(Hourly_Graddient[i], label=label[i])
# plt.plot(Load[0:168])
plt.title('Average Residual Load Ramp Rate')
plt.ylabel('GWh')
plt.xlabel('Time (Hour)')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

print('Congratulations, task completed !') 
