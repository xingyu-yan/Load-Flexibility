# -*- coding: utf-8 -*-
"""
Created on Thu May 14 11:26:41 2020
At GEIDCO, Beijing
@author: Xingyu
Objective: Load Flexibility Calculation 
"""
 
import csv
import numpy as np
import matplotlib.pyplot as plt
from FlexibilityFunc import FlexibilityCalculate, Ave_Resi_Load
from ThermalMinCapFunc import thermalMinCap

# import os
# print('getcwd: ', os.getcwd())
# print('__file__: ', __file__)

# 读取csv文件

with open('IOCurve_Thermal.csv', 'r') as csvFile:
    reader = csv.reader(csvFile) 
    rows = [row for row in reader]
    print('File info: ' + str(rows[0]))

# FirstLine = rows[2]
# for index in range(len(FirstLine)):
#     print('The column %d is: ' % index + str(FirstLine[index]))

rowsMat = np.mat(rows[3:len(rows)])   
generator_Name = []
minCap = []

for i in range(len(rows)-3):
    generator_Name.append(rowsMat[i,1].lower())
    minCap.append(rowsMat[i,5])
 
dictionary = dict(zip(generator_Name, minCap))

# 2 Read HourlyData_Generator_2035.csv file 
with open('HourlyData_Generator_2035.csv', 'r') as csvFile:
    reader = csv.reader(csvFile) 
    rows = [row for row in reader]
    print('File info: ' + str(rows[0]))

rowsMat = np.mat(rows[4:len(rows)])

(it, pl, cn, gb, sc, casia, de, fr, eur, bl, bnl, ept, ch) = thermalMinCap(rowsMat, dictionary)
    
thermalMC = [gb, ept, eur, casia, cn, fr, bnl, de, ch, pl, sc, bl, it]

#Plot the Load of PRC  
thermalMCnoCN = [gb, ept, eur, casia, fr, bnl, de, ch, pl, sc, bl, it] # Skip cn
plt.figure(dpi = 600)
label = ['GB', 'EPT', 'EUR_SE', 'Cent_Asia', 'FR', 'BNL', 'DE', 'CH', 'PL', 'SC', 'BL', 'IT']
for i in range(len(thermalMCnoCN)):
    plt.plot(np.array(thermalMCnoCN[i])/1000, label=label[i])
plt.title('Min Capacity of Thermal Units')
plt.ylabel('GW')
plt.xlabel('Time (Hour)')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

# HourlyData_Generator_2035 
with open('HourlyData_Region_2035_NetLoad_OR.csv', 'r') as csvFile:
    reader = csv.reader(csvFile) 
    rows = [row for row in reader]

print('File info: ' + str(rows[0][0]))
FirstLine = rows[4]
for index in range(len(FirstLine)):
    print('The column %d is: ' % index + str(FirstLine[index]))

# Load = np.mat(rows[5:len(rows)])[0:8761,3:16]    
Load = np.mat(rows[4:len(rows)])[0:8761]  

NetLoad = Load.copy() # attention, use copy to duplicate
for i in range(13):
    for j in range(8760):
        NetLoad[j+1,i+3] = float(Load[j+1,i+3]) - thermalMC[i][j]
        
    #Plot the Net Load of each Region 
    Load_Name = NetLoad[0,i+3]
    plt.figure()
    plt.plot(Load[1:8761,i+3], label='Load minus PV and Wind')
    plt.plot(NetLoad[1:8761,i+3], label='Load minus PV, Wind, and Min Cap')
    plt.plot(thermalMC[i], label='Thermal Min Cap')
    label = ['GB', 'EPT', 'EUR_SE', 'Cent_Asia', 'FR', 'BNL', 'DE', 'CH', 'PL', 'SC', 'BL', 'IT']
    plt.title('NetLoad profile of ' + Load_Name)
    plt.ylabel('MW')
    plt.xlabel('Time (Hour)')
    plt.legend()
    plt.show()
       
#Plot the Net Load of FR  
# plt.figure()
# plt.plot(Load[1:8761,8], label='Load minus PV and Wind')
# plt.plot(NetLoad[1:8761,8], label='Load minus PV, Wind, and Min Cap')
# plt.plot(thermalMC[5], label='Thermal Min Cap in FR')
# plt.title('NetLoad profile of FR')
# plt.ylabel('MW')
# plt.xlabel('Time (Hour)')
# plt.legend()
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
        print('Skip the ' + NetLoad[0,i+3])
        print()
    else:
        Load_Sub = list(map(float, NetLoad[1:8761,i+3]))
        Load_Sub_Name = 'Load_' + NetLoad[0,i+3]
        print('Calculating the Flexibility of ' + Load_Sub_Name)        
        
        (Flexi_Day, Flexi_Week, Flexi_Year) = FlexibilityCalculate(Load_Sub, Load_Sub_Name)
        Flexibility_Day.append(Flexi_Day)
        Flexibility_Week.append(Flexi_Week)
        Flexibility_Year.append(Flexi_Year)   
        
        (AVE_Hour, Hourly_Grad) = Ave_Resi_Load(Load_Sub, Load_Sub_Name)
        Ave_Hourly_Load.append(AVE_Hour)
        Hourly_Graddient.append(Hourly_Grad)

# NetLoad_Flexibility_file = 'NetLoad_Flexibility.csv'
# fileHeader = ['Load Flexibility']
# with open(NetLoad_Flexibility_file, "w", newline='') as f:
#         dict_writer = csv.DictWriter(f, fileHeader)
#         dict_writer.writerows({Flexibility_Day: Flexibility_Day})
#         # dict_writer.writerows({'Flexibility_Day': Flexibility_Week})
#         # dict_writer.writerows({'Flexibility_Day': Flexibility_Year})
#         dict_writer.writerows(Ave_Hourly_Load)
#         dict_writer.writerows(Hourly_Graddient)
#         f.close()

NetLoad_Flexibility_file = 'NetLoad_Flexibility.csv'      
with open(NetLoad_Flexibility_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow('Flexibility_Day')
        writer.writerows([Flexibility_Day])
        writer.writerow('Flexibility_Week')
        writer.writerows([Flexibility_Week])
        writer.writerow('Flexibility_Year')
        writer.writerows([Flexibility_Year])
        writer.writerow('Average Hourly Load')
        writer.writerows(Ave_Hourly_Load)
        writer.writerow('HourlyGraddient')
        writer.writerows(Hourly_Graddient)
        f.close()
    
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