# -*- coding: utf-8 -*-
"""
Created on Sat May  9 15:40:28 2020
At GEIDCO, Beijing
@author: Xingyu
Objective: Load Flexibility Calculation 
"""
 
import csv
import numpy as np
import matplotlib.pyplot as plt

# import os
# print('getcwd: ', os.getcwd())
# print('__file__: ', __file__)

# 1 Read IOCurve_Thermal.csv file to build a d'ict for minCap of' each generator
with open('IOCurve_Thermal.csv', 'r') as csvFile:
    reader = csv.reader(csvFile) 
    rows = [row for row in reader]

print('File info: ' + str(rows[0]))
FirstLine = rows[2]
for index in range(len(FirstLine)):
    print('The column %d is: ' % index + str(FirstLine[index]))

rowsMat = np.mat(rows[3:len(rows)])   
generator_Name = []
minCap = []

for i in range(len(rows)-3):
    generator_Name.append(rowsMat[i,1].lower())
    minCap.append(rowsMat[i,5])
 
dictionary = dict(zip(generator_Name, minCap))

# for i in range(len(dictionary)):
#     print(dictionary[rowsMat[i,1]])

# for item in dictionary.items():
#     print(item)

# for key,value in dictionary.items():
#     print('The minimum output of ', key,' is ', value,' MW')
    
# print(dictionary[rowsMat[0,1]])
# print(dictionary['Coal_GB'])

# 2 Read HourlyData_Generator_2035.csv file 
with open('HourlyData_Generator_2035.csv', 'r') as csvFile:
    reader = csv.reader(csvFile) 
    rows = [row for row in reader]

print('File info: ' + str(rows[0]))
FirstLine = (rows[4])[3:-1]

rowsMat = np.mat(rows[4:len(rows)])

splitName = []
for index in range(len(FirstLine)):
    # print('The column %d is: ' % index + str(FirstLine[index]))
    splitName.append((FirstLine[index]).split('_'))

ThermalGen = []
NameGen = []
NameCoun = []

for i in range(len(splitName)):
    a = (splitName[i])[0].lower()
    b = (splitName[i])[1].lower()
    NameGen.append(a)
    NameCoun.append(b)
    gen = rowsMat[:,i+3]
    if (a == 'bio')or(a == 'gas')or(a == 'nuclear')or(a == 'coal'):
        ThermalGen.append(gen)
        # print('This good colomn is ' + str((splitName[i])[0]))
    else:
        # print('This bad colomn is ' + str((splitName[i])[0]))
        pass

nameGen = set(NameGen)
nameCoun = set(NameCoun)
print(nameGen)
print(nameCoun)

A = []
for i in range(len(ThermalGen)):
    gen = ThermalGen[i]
    for j in range(len(gen)):
        A.append(gen[j,0])
thermalGen = np.reshape(A, (len(ThermalGen), -1)).T    

# 通过查表将机组出力转换为最小出力，并分国家归类
thermalGenMinCap = thermalGen
it = []
pl = []
cn = []
gb = []
sc = []
casia = []
de = []
fr = []
eur = []
bl = []
at = []
bnl = []
ept = []
gr = []
ch = []

for i in range(len(thermalGenMinCap[0,:])):
    itemName = thermalGenMinCap[0,i].lower()    
    minCapGen = float(dictionary[itemName])
    print('The min capacity of', itemName, 'is', minCapGen)
    for j in range(len(thermalGenMinCap[0:-1,0])):        
        if float(thermalGenMinCap[j+1,i]) >= 0.1:
            thermalGenMinCap[j+1,i] = minCapGen
        else:
            thermalGenMinCap[j+1,i] = 0        
    
    itemNameCountry = (itemName.split('_'))[1]
    if itemNameCountry == 'it':
        it.append(thermalGenMinCap[:,i])
    elif itemNameCountry == 'pl':
        pl.append(thermalGenMinCap[:,i])
    elif itemNameCountry == 'cn':
        cn.append(thermalGenMinCap[:,i])
    elif itemNameCountry == 'gb':
        gb.append(thermalGenMinCap[:,i])
    elif itemNameCountry == 'casia':
        casia.append(thermalGenMinCap[:,i])
    elif itemNameCountry == 'de':
        de.append(thermalGenMinCap[:,i])
    elif itemNameCountry == 'fr':
        fr.append(thermalGenMinCap[:,i])
    elif itemNameCountry == 'eur':
        eur.append(thermalGenMinCap[:,i])
    elif itemNameCountry == 'bl':
        bl.append(thermalGenMinCap[:,i])
    elif itemNameCountry == 'at':
        at.append(thermalGenMinCap[:,i])
    elif itemNameCountry == 'bnl':
        bnl.append(thermalGenMinCap[:,i])
    elif itemNameCountry == 'ept':
        ept.append(thermalGenMinCap[:,i])
    elif itemNameCountry == 'gr':
        gr.append(thermalGenMinCap[:,i])
    elif itemNameCountry == 'ch':
        ch.append(thermalGenMinCap[:,i])
    else:
        print('Attention! There is no this kind of generator.')

    
# #Plot the Load of PRC  
# plt.figure()
# plt.plot(Load[1:8761,7])
# # plt.plot(Load[0:168])
# plt.title('NetLoad profile of PRC')
# plt.ylabel('MW')
# plt.xlabel('Time (Hour)')
# plt.show()