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

# 1 Read IOCurve_Thermal.csv file to build a dict for minCap of each generator
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

rowsMat = np.mat(rows[4:len(rows)])

FirstLine = (rowsMat[0,3:-1].tolist())[0]

splitName = []
for index in range(len(FirstLine)):
    # print('The column %d is: ' % index + str(FirstLine[index]))
    splitName.append((FirstLine[index]).split('_'))

ThermalGen = []
NameGen = []
NameCoun = []

for i in range(len(splitName)):
    gN = (splitName[i])[0].lower()
    NameGen.append((splitName[i])[0].lower())
    NameCoun.append((splitName[i])[1].lower())
    gen = rowsMat[:,i+3]
    if (gN == 'bio')or(gN == 'gas')or(gN == 'nuclear')or(gN == 'coal'):
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
bnl = []
ept = []
gr = []
ch = []

for i in range(len(thermalGenMinCap[0,:])):
    itemName = thermalGenMinCap[0,i].lower()    
    minCapGen = float(dictionary[itemName])
    print('The min capacity of', itemName, 'is', minCapGen)
    
    itemNameCountry = (itemName.split('_'))[1]
    
    for j in range(8760):        
        if float(thermalGenMinCap[j+1,i]) >= 0.1:
            thermalGenMinCap[j+1,i] = float(minCapGen)
        else:
            thermalGenMinCap[j+1,i] = float(0) 
        
    if itemNameCountry == 'it':
        it = it + thermalGenMinCap[1:8761,i].tolist()
    elif itemNameCountry == 'pl':
        pl = pl + thermalGenMinCap[1:8761,i].tolist()
    elif itemNameCountry == 'cn':
        cn = cn + thermalGenMinCap[1:8761,i].tolist()
    elif itemNameCountry == 'gb':
        gb = gb + thermalGenMinCap[1:8761,i].tolist()
    elif itemNameCountry == 'casia':
        casia = casia + thermalGenMinCap[1:8761,i].tolist()
    elif itemNameCountry == 'de':
        de = de + thermalGenMinCap[1:8761,i].tolist()
    elif itemNameCountry == 'fr':
        fr = fr + thermalGenMinCap[1:8761,i].tolist()
    elif itemNameCountry == 'eur':
        if (itemName.split('_'))[2] == 'c':
            pl = pl + thermalGenMinCap[1:8761,i].tolist()
        elif (itemName.split('_'))[2] == 'se':
            eur = eur + thermalGenMinCap[1:8761,i].tolist()
        else:
            print('Attention! There is a problem with area EUR.')
    elif itemNameCountry == 'bl':
        bl = bl + thermalGenMinCap[1:8761,i].tolist()
    elif itemNameCountry == 'bnl':
        bnl = bnl + thermalGenMinCap[1:8761,i].tolist()
    elif itemNameCountry == 'ept':
        ept = ept + thermalGenMinCap[1:8761,i].tolist()
    elif itemNameCountry == 'gr':
        gr = gr + thermalGenMinCap[1:8761,i].tolist()
    elif (itemNameCountry == 'ch')or(itemNameCountry == 'at'):
        ch = ch + thermalGenMinCap[1:8761,i].tolist()
    else:
        print('Attention! There is no ', itemName)
            
        # if itemNameCountry == 'it':
        #     it.append(thermalGenMinCap[j+1,i])
        # elif itemNameCountry == 'pl':
        #     pl.append(thermalGenMinCap[j+1,i])
        # elif itemNameCountry == 'cn':
        #     cn.append(thermalGenMinCap[j+1,i])
        # elif itemNameCountry == 'gb':
        #     gb.append(thermalGenMinCap[j+1,i])
        # elif itemNameCountry == 'casia':
        #     casia.append(thermalGenMinCap[j+1,i])
        # elif itemNameCountry == 'de':
        #     de.append(thermalGenMinCap[j+1,i])
        # elif itemNameCountry == 'fr':
        #     fr.append(thermalGenMinCap[j+1,i])
        # elif itemNameCountry == 'eur':
        #     if (itemName.split('_'))[2] == 'c':
        #         pl.append(thermalGenMinCap[j+1,i])
        #     elif (itemName.split('_'))[2] == 'se':
        #         eur.append(thermalGenMinCap[j+1,i])
        #     else:
        #         print('Attention! There is a problem with area EUR.')
        # elif itemNameCountry == 'bl':
        #     bl.append(thermalGenMinCap[j+1,i])
        # elif itemNameCountry == 'bnl':
        #     bnl.append(thermalGenMinCap[j+1,i])
        # elif itemNameCountry == 'ept':
        #     ept.append(thermalGenMinCap[j+1,i])
        # elif itemNameCountry == 'gr':
        #     gr.append(thermalGenMinCap[j+1,i])
        # elif (itemNameCountry == 'ch')or(itemNameCountry == 'at'):
        #     ch.append(thermalGenMinCap[j+1,i])
        # else:
        #     print('Attention! There is no ', itemName)

# a = [0,1,2,3,4,5,6,7]
# a1= np.array(np.reshape(a, (4, -1)), dtype = 'float_')
# a2= np.array(np.reshape(a, (4, -1), order='F'), dtype = 'float_')
# a3= np.array(np.reshape(a, (4, -1)), dtype = 'float_').sum(axis=1).tolist()
# a4= np.array(np.reshape(a, (4, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()

it = np.array(np.reshape(it, (8760, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()
pl = np.array(np.reshape(pl, (8760, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()
cn = np.array(np.reshape(cn, (8760, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()
gb = np.array(np.reshape(gb, (8760, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()
sc = np.array(np.reshape(sc, (8760, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()
casia = np.array(np.reshape(casia, (8760, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()
de = np.array(np.reshape(de, (8760, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()
fr = np.array(np.reshape(fr, (8760, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()
eur = np.array(np.reshape(eur, (8760, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()
bl = np.array(np.reshape(bl, (8760, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()
bnl = np.array(np.reshape(bnl, (8760, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()
ept = np.array(np.reshape(ept, (8760, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()
# gr = np.array(np.reshape(gr, (8760, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()
ch = np.array(np.reshape(ch, (8760, -1), order='F'), dtype = 'float_').sum(axis=1).tolist()

thermalMCnoCN = [gb, ept, eur, casia, fr, bnl, de, ch, pl, sc, bl, it] # Skip cn

#Plot the Load of PRC  
plt.figure(dpi = 600)
label = ['GB', 'EPT', 'EUR_SE', 'Cent_Asia', 'FR', 'BNL', 'DE', 'CH', 'PL', 'SC', 'BL', 'IT']
for i in range(len(thermalMCnoCN)):
    plt.plot(np.array(thermalMCnoCN[i])/1000, label=label[i])
plt.title('Min Capacity of Thermal Units')
plt.ylabel('GW')
plt.xlabel('Time (Hour)')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()