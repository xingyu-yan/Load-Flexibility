# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 16:50:35 2020
At GEIDCO, Beijing
@author: Xingyu

Objective: Load Flexibility Calculation 
"""

import csv
import numpy as np
import matplotlib.pyplot as plt

# 读取csv文件
# csvFile = open("HourlyData_Region_2035.csv", "r")
csvFile = open("HourlyData_Region_2035_NetLoad.csv", "r")

reader = csv.DictReader(csvFile) 
column = [row['FR'] for row in reader] # 选取法国的数据作为计算对象

print('The Column Number of All Load is %d' % len(column))
# print(column[0:5])

# 字符串转换为数字
FR_Load = list(map(float, column))    
# print(GB_Load[0:5])
# print('I am here.')

#Plot the result  
plt.figure()
plt.plot(FR_Load[0:168])
# plt.plot(GB_Load[0:168])
plt.title('NetLoad profile of FR')
plt.ylabel('MW')
plt.xlabel('Time (Hour)')
plt.show()  

FR_Load_Mat = np.reshape(np.mat(FR_Load), (-1, 24))
print('The Data Shape of FR Load Is')
print(FR_Load_Mat.shape)
print(FR_Load_Mat[0,:])

# a = FR_Load_Mat[0:6,:].tolist()
# b = FR_Load_Mat[7:13,:].tolist()

# plt.figure(2)
# plt.plot(a[0])
# plt.plot(b[0])
# plt.title('Load profile of GB')
# plt.ylabel('MW')
# plt.xlabel('Time')
# plt.show()

# 日波动性计算

# 1计算每日平均值
print('Calculating the Daily Load Flexibility ...')
AVE_Day = np.mean(FR_Load_Mat, axis=1)
print('The Data Shape of Average Day Load is')
print(AVE_Day.shape)

# 2计算每日每小时波动性
FR_Load_Mat_Dif = FR_Load_Mat - AVE_Day
# print(GB_Load_Mat_Dif.shape)
# print(GB_Load_Mat_Dif[0,:])

# plot the daily flexibility
FR_Load_Mat_Dif_toList = FR_Load_Mat_Dif[0,:].tolist()

FR_Load_Mat_Dif_toList_ThreeDays = np.reshape(np.mat(FR_Load_Mat_Dif[0:3,:]), (1, -1)).tolist()

# plt.figure()
# plt.plot(FR_Load_Mat_Dif_toList_ThreeDays[0])
# # plt.plot(FR_Load_Mat_Dif_toList1[0])
# plt.title('I am the test figure')
# plt.ylabel('MW')
# plt.xlabel('Time (Hour)')
# plt.show()

# 计算日灵活性 Flexibility
Flexi_Day_FR = np.abs(FR_Load_Mat_Dif).sum()
print('Daily Flexibility of FR Load is %d MWh' % Flexi_Day_FR)

x = FR_Load[0:72]
y = np.array(FR_Load[0:72]) - np.array(FR_Load_Mat_Dif_toList_ThreeDays[0])
plt.figure()
plt.plot(x, label="FR_Load")
plt.plot(y, label="Daily Average Load")
# plt.plot(np.abs(FR_Load_Mat_Dif_toList_ThreeDays[0]), label="Daily Flexibility")
plt.tight_layout()
plt.fill_between(range(72), x, y, facecolor="orange", # The fill color
                 color='blue',       # The outline color
                 alpha=0.2)                 
plt.title('Daily Load Flexibility of FR')
plt.ylabel('MW')
plt.xlabel('Time (Hour)')
# plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
plt.legend()
plt.show()

# 周波动性计算

# 1计算每周平均值
print('Calculating the Weekly Load Flexibility ...')
FR_Load_Mat_Week = np.reshape(np.mat(FR_Load[0:8736]), (-1, 168))

AVE_Week = np.mean(FR_Load_Mat_Week, axis=1)
print('The Data Shape of Average Weekly Load Is')
print(AVE_Week.shape)

# 2计算每周中每天的波动性
FR_Load_Mat_Week_Day = np.reshape(np.mat(AVE_Day[0:364]), (-1, 7)) # 每天平均值
FR_Load_Mat_Week_Day_Dif = FR_Load_Mat_Week_Day - AVE_Week

print(FR_Load_Mat_Week_Day_Dif.shape)
print(FR_Load_Mat_Week_Day_Dif[0,:])

# 一周里面每天的平均值
FR_Load_Mat_Week_Day_toList = FR_Load_Mat_Week_Day[0,:].tolist() 
# 三周里面每天的平均值
FR_Load_Mat_Week_Day_toList_3Weeks = np.reshape(np.mat(FR_Load_Mat_Week_Day[0:3,:]), (1, -1)).tolist()

# 一周里面每天的波动性
FR_Load_Mat_Week_Day_Dif_toList = FR_Load_Mat_Week_Day_Dif[0,:].tolist() 
# 三周里面每天的波动性
FR_Load_Mat_Week_Day_Dif_toList_3Weeks = np.reshape(np.mat(FR_Load_Mat_Week_Day_Dif[0:3,:]), (1, -1)).tolist()

plt.figure()
plt.plot(FR_Load_Mat_Week_Day_Dif_toList_3Weeks[0])
plt.title('NetLoad Weekly Variability of FR')
plt.ylabel('MW')
plt.xlabel('Time (Day)')
plt.show()

# 计算日灵活性 Flexibility
Flexi_Week_FR = np.abs(FR_Load_Mat_Week_Day_Dif).sum()
print('Weekly Flexibility of FR Load is %d MWh' % Flexi_Week_FR)

# plt.figure()
# plt.plot(FR_Load_Mat_Week_Day_toList_3Weeks[0], label="Average Daily FR_Load")
# plt.plot(FR_Load_Mat_Week_Day_toList_3Weeks[0] - np.array(FR_Load_Mat_Week_Day_Dif_toList_3Weeks[0]), label="Weekly Average Load")
# plt.plot(np.abs(FR_Load_Mat_Week_Day_Dif_toList_3Weeks[0]), label="Weekly Flexibility")
# plt.tight_layout()
# plt.fill_between(range(21), np.abs(FR_Load_Mat_Week_Day_Dif_toList_3Weeks[0]), 0)
# plt.title('Weekly Load Flexibility of FR')
# plt.ylabel('MW')
# plt.xlabel('Time (Day)')
# # plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
# plt.legend()
# plt.show()

x = FR_Load_Mat_Week_Day_toList_3Weeks[0]
y = FR_Load_Mat_Week_Day_toList_3Weeks[0] - np.array(FR_Load_Mat_Week_Day_Dif_toList_3Weeks[0])
plt.figure()
plt.plot(x, label="Average Daily FR_Load")
plt.plot(y, label="Weekly Average Load")
# plt.plot(np.abs(FR_Load_Mat_Week_Day_Dif_toList_3Weeks[0]), label="Weekly Flexibility")
plt.tight_layout()
plt.fill_between(range(21), x, y, facecolor="orange", # The fill color
                 color='blue',       # The outline color
                 alpha=0.2)
plt.title('Weekly Load Flexibility of FR')
plt.ylabel('MW')
plt.xlabel('Time (Day)')
# plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
plt.legend()
plt.show()