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
from FlexibilityFunc import FlexibilityCalculate

# 读取csv文件
csvFile = open("HourlyData_Region_2035_NetLoad.csv", "r")

# 方法1
# reader = csv.DictReader(csvFile) 
# column = [row['FR'] for row in reader] # 选取法国的数据作为计算对象
# print('The Column Number of All Load is %d' % len(column))
# Load = list(map(float, column)) # 字符串转换为数字  

# 方法2
reader = csv.reader(csvFile) 
rows = [row for row in reader]
Load = np.mat(rows)

Flexibility_Day = []
Flexibility_Week = []

for i in range(13):
    # 字符串转换为数字
    Load_Sub = list(map(float,Load[1:8761,i+3]))
    Load_Sub_Name = 'Load_' + Load[0,i+3]
    (Flexi_Day, Flexi_Week) = FlexibilityCalculate(Load_Sub, Load_Sub_Name)
    Flexibility_Day.append(Flexi_Day)
    Flexibility_Week.append(Flexi_Week)
    print('Calculating the Flexibility of ' + Load_Sub_Name)
    

# Plot the result  
plt.figure()
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
labels = ['GB', 'EPT', 'EUR_SE', 'Central Asia', 'PRC', 'FR', 'BNL', 'DE', 'CH', 'PL', 'SC', 'BL', 'IT']
plt.plot(x, Flexibility_Day, label='Daily Load Flexibility')
plt.plot(x, Flexibility_Week, label='Weekly Load Flexibility')
plt.xticks(x, labels, rotation='vertical') # rotation=45
plt.title('NetLoad Flexibility')
plt.ylabel('MWh')
plt.xlabel('Time (Hour)')
plt.legend()
plt.show()  