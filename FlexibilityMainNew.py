# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 22:15:03 2020
At GEIDCO, Beijing
@author: Xingyu
Objective: Power System Flexibility Identification 
"""
 
import csv
import numpy as np
import matplotlib.pyplot as plt
from FlexibilityFunc import FlexibilityCalculate, Ave_Resi_Load
from ThermalMinCapFunc import thermalMinCap, thermalMinCapDifKind
from generationMixFunc import genMix
from xlwt import Workbook

# *****************************************************************************
# **************************** Part 0: Area LMP End ***************************
# import os
# print('getcwd: ', os.getcwd())
# print('__file__: ', __file__)

# 读取csv文件

# *****************************************************************************
# ****** Part 1: Build a dictionary of Min Capacity for Each Generator ********
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

# *****************************************************************************
# ****** Part 2: Identify the Min Capacity for Each Operating Generator *******
# Read HourlyData_Generator_2035.csv file 
with open('HourlyData_Generator_2035_16GW.csv', 'r') as csvFile:
    reader = csv.reader(csvFile) 
    rows = [row for row in reader]
    print('File info: ' + str(rows[0]))

rowsMat = np.mat(rows[4:len(rows)])

(it, pl, cn, gb, sc, casia, de, fr, eur, bl, bnl, ept, ch) = thermalMinCap(rowsMat, dictionary)
    
thermalMC = [gb, ept, eur, casia, cn, fr, bnl, de, ch, pl, sc, bl, it]

FirstLine = (rowsMat[0,3:-1].tolist())[0]
splitName = []
for index in range(len(FirstLine)):
    # print('The column %d is: ' % index + str(FirstLine[index]))
    splitName.append((FirstLine[index]).split('_'))

ThermalGen = []
NameGen = []
NameCoun = []

# pick up all the thermal generators
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
thermalGenMinCap = thermalGen.copy()

for i in range(len(thermalGenMinCap[0,:])):
    itemName = thermalGenMinCap[0,i].lower()    
    minCapGen = float(dictionary[itemName])
    print('The Pmin of', itemName, 'is', minCapGen)
    
    itemNameCountry = (itemName.split('_'))[1]
    
    for j in range(len(thermalGenMinCap[0:-1,0])):        
        if float(thermalGenMinCap[j+1,i]) >= 0.1:
            thermalGenMinCap[j+1,i] = float(minCapGen)
        else:
            thermalGenMinCap[j+1,i] = float(0) 

it_Pmin = []
pl_Pmin = []
cn_Pmin = []
gb_Pmin = []
sc_Pmin = []
casia_Pmin = []
de_Pmin = []
fr_Pmin = []
eur_Pmin = []
bl_Pmin = []
bnl_Pmin = []
ept_Pmin = []
gr_Pmin = []
ch_Pmin = []

for i in range(len(thermalGenMinCap[0,:])):
    itemName = thermalGenMinCap[0,i].lower()    
    minCapGen = float(dictionary[itemName])
   
    itemNameCountry = (itemName.split('_'))[1]
    
    for j in range(len(thermalGenMinCap)):   
        if itemNameCountry == 'it':
            it_Pmin.append(thermalGenMinCap[j,i])
        elif itemNameCountry == 'pl':
            pl_Pmin.append(thermalGenMinCap[j,i])
        elif itemNameCountry == 'cn':
            cn_Pmin.append(thermalGenMinCap[j,i])
        elif itemNameCountry == 'gb':
            gb_Pmin.append(thermalGenMinCap[j,i])
        elif itemNameCountry == 'casia':
            casia_Pmin.append(thermalGenMinCap[j,i])
        elif itemNameCountry == 'de':
            de_Pmin.append(thermalGenMinCap[j,i])
        elif itemNameCountry == 'fr':
            fr_Pmin.append(thermalGenMinCap[j,i])
        elif itemNameCountry == 'eur':
            if (itemName.split('_'))[2] == 'c':
                pl_Pmin.append(thermalGenMinCap[j,i])
            elif (itemName.split('_'))[2] == 'se':
                eur_Pmin.append(thermalGenMinCap[j,i])
            else:
                pass
                # print('Attention! There is a problem with area EUR.')
        elif itemNameCountry == 'bl':
            bl_Pmin.append(thermalGenMinCap[j,i])
        elif itemNameCountry == 'bnl':
            bnl_Pmin.append(thermalGenMinCap[j,i])
        elif itemNameCountry == 'ept':
            ept_Pmin.append(thermalGenMinCap[j,i])
        elif itemNameCountry == 'gr':
            gr_Pmin.append(thermalGenMinCap[j,i])
        elif (itemNameCountry == 'ch')or(itemNameCountry == 'at'):
            ch_Pmin.append(thermalGenMinCap[j,i])
        else:
            pass
            # print('Attention! There is no ', itemName)

# it_Pmin = np.array(np.reshape(it_Pmin, (8761, -1), order='F'))

# pl_Pmin = np.array(np.reshape(pl_Pmin, (8761, -1), order='F'))
# cn_Pmin = np.array(np.reshape(cn_Pmin, (8761, -1), order='F'))
# gb_Pmin = np.array(np.reshape(gb_Pmin, (8761, -1), order='F'))
# sc_Pmin = np.array(np.reshape(sc_Pmin, (8761, -1), order='F'))
# casia_Pmin = np.array(np.reshape(casia_Pmin, (8761, -1), order='F'))
de_Pmin = np.array(np.reshape(de_Pmin, (8761, -1), order='F'))
Pmin_DE = genMix(de_Pmin)

# fr_Pmin = np.array(np.reshape(fr_Pmin, (8761, -1), order='F'))
# eur_Pmin = np.array(np.reshape(eur_Pmin, (8761, -1), order='F'))
# bl_Pmin = np.array(np.reshape(bl_Pmin, (8761, -1), order='F'))
# bnl_Pmin = np.array(np.reshape(bnl_Pmin, (8761, -1), order='F'))
# ept_Pmin = np.array(np.reshape(ept_Pmin, (8761, -1), order='F'))
# # gr_Pmin = np.array(np.reshape(gr_Pmin, (8760, -1), order='F'))
# ch_Pmin = np.array(np.reshape(ch_Pmin, (8761, -1), order='F'))


# ************************* Part 3: 计算各类发电机组发电量  **************************
FirstLine = (rowsMat[0,3:-1].tolist())[0]
splitName = []
for index in range(len(FirstLine)):
    # print('The column %d is: ' % index + str(FirstLine[index]))
    splitName.append((FirstLine[index]).split('_'))

ThermalGen = []
NameGen = []
NameCoun = []

# pick up all the thermal generators
for i in range(len(splitName)):
    NameGen.append((splitName[i])[0].lower())
    NameCoun.append((splitName[i])[1].lower())

nameGen = set(NameGen)
nameCoun = set(NameCoun)
print(nameGen)
print(nameCoun)

it_GenMix = []
# pl_GenMix = []
# cn_GenMix = []
# gb_GenMix = []
# sc_GenMix = []
# casia_GenMix = []
de_GenMix = []
# fr_GenMix = []
# eur_GenMix = []
# bl_GenMix = []
# bnl_GenMix = []
# ept_GenMix = []
# gr_GenMix = []
# ch_GenMix = []

for i in range(len(FirstLine)):
    gN = (splitName[i])[0].lower()
    cN = (splitName[i])[1].lower()
    gen = rowsMat[:,i+3]
    
    if cN == 'it':
        it_GenMix.append(gen)  
    # elif cN == 'pl':
    #     pl_GenMix.append(gen)
    # elif cN == 'cn':
    #     cn_GenMix.append(gen)  
    # elif cN == 'gb':
    #     gb_GenMix.append(gen)        
    # elif cN == 'sc':
    #     sc_GenMix.append(gen)  
    # elif cN == 'casia':
    #     casia_GenMix.append(gen)
    elif cN == 'de':
        de_GenMix.append(gen)  
    # elif cN == 'fr':
    #     fr_GenMix.append(gen) 
    # elif cN == 'eur':
    #     eur_GenMix.append(gen)  
    # elif cN == 'bl':
    #     bl_GenMix.append(gen)        
    # elif cN == 'bnl':
    #     bnl_GenMix.append(gen)  
    # elif cN == 'ept':
    #     ept_GenMix.append(gen)
    # elif cN == 'gr':
    #     gr_GenMix.append(gen)  
    # elif cN == 'ch':
    #     ch_GenMix.append(gen)
    # else:
    #     print('There is a problem here ' + str(cN) + str(i))

# CountryRegion = ['gr', 'cn', 'sc', 'eur', 'bnl', 'casia', 'ch', 'pl', 'bl', 'de', 'fr', 'gb', 'ept', 'it']

k = de_GenMix
A = []
for i in range(len(k)):
    gen = k[i]
    for j in range(len(gen)):
        A.append(gen[j,0])
allGenerators = np.reshape(A, (len(k), -1)).T 
  
GenMix_DE = genMix(allGenerators)

for i in range(len(Pmin_DE[0])):
    genPminN = Pmin_DE[0,i]
    for j in range(len(GenMix_DE[0])):
        genN = GenMix_DE[0,j]
        if genPminN == genN:
            print("Find a Pmin colomne: " + genN)
            for k in range(len(GenMix_DE)-1):
                GenMix_DE[k+1,j] = float(GenMix_DE[k+1,j]) - float(Pmin_DE[k+1,i])
        else:
            print("It is not a Pmin colomne: " + genN)
         
# *****************************************************************************
# ***** Part 4: Calculate the Residual Load (NetLoad Minus Min Capacity) ******
with open('HourlyData_Region_NetLoad_2035_16GW.csv', 'r') as csvFile:
    reader = csv.reader(csvFile) 
    rows = [row for row in reader]

NetLoad = np.mat(rows[4:len(rows)])[0:8761]  

ResidualLoad = NetLoad.copy() # attention, use copy to duplicate
for i in range(13):
    for j in range(8760):
        ResidualLoad[j+1,i+3] = float(NetLoad[j+1,i+3]) - thermalMC[i][j]
        
    # #Plot the Net Load of each Region 
    # Load_Name = ResidualLoad[0,i+3]
    # plt.figure()
    # plt.plot(NetLoad[1:8761,i+3], label='Load minus PV and Wind')
    # plt.plot(ResidualLoad[1:8761,i+3], label='Load minus PV, Wind, and Min Cap')
    # plt.plot(thermalMC[i], label='Thermal Min Cap')
    # label = ['GB', 'EPT', 'EUR_SE', 'Cent_Asia', 'FR', 'BNL', 'DE', 'CH', 'PL', 'SC', 'BL', 'IT']
    # plt.title('ResidualLoad profile of ' + Load_Name)
    # plt.ylabel('MW')
    # plt.xlabel('Time (Hour)')
    # plt.legend()
    # plt.show()
        
# *****************************************************************************
# ************** Part 4: Calculate the Residual Load Flexibility **************
# Country = input('Which Country Do You Want to Choose: ')

"""   
Flexibility_Day = []
Flexibility_Week = []
Flexibility_Year = []

Ave_Hourly_Load = []
Hourly_Graddient = []

for i in range(13):
    Load_Sub = list(map(float, ResidualLoad[1:8761,i+3])) # 字符串转换为数字
    Load_Sub_Name = 'Load_' + ResidualLoad[0,i+3]
    print('Calculating the Flexibility of ' + Load_Sub_Name)        
    
    (Flexi_Day, Flexi_Week, Flexi_Year) = FlexibilityCalculate(Load_Sub, Load_Sub_Name)
    Flexibility_Day.append(Flexi_Day)
    Flexibility_Week.append(Flexi_Week)
    Flexibility_Year.append(Flexi_Year)   
    
    (AVE_Hour, Hourly_Grad) = Ave_Resi_Load(Load_Sub, Load_Sub_Name)
    Ave_Hourly_Load.append(AVE_Hour)
    Hourly_Graddient.append(Hourly_Grad)
"""
# *****************************************************************************
# ******************* Part 5: Flexible Resource Contributions *****************
# 需要用到的数据： GenMix_DE， ResidualLoad , and Interconnection 
# ['Date', ' Hour', ' TOU', 'GB', 'EPT', 'EUR_SE', 'Central Asia', 
#         'PRC', 'FR', 'BNL', 'DE', 'CH', 'PL', 'SC', 'BL', 'IT']

# 互联线路参数
with open('Hourly_ZonalLink2035_DE_16GW.csv', 'r') as csvFile:
    reader = csv.reader(csvFile) 
    rows = [row for row in reader]
NetLoad = np.mat(rows[4:len(rows)])[0:8761]  
Inter = NetLoad[:,9].copy() # attention, use copy to duplicate

#******************************** 数据预处理 ********************************
GenMixAll = np.c_[GenMix_DE,Inter] #所有类型发电量+互联输送容量,包括solar and wind
# 先删除 solar 和 wind  # C = np.delete(C, 1, 1)  # 删除C的第二列 
GenMix = np.delete(GenMixAll, [1,3], 1) #
FirstLine = GenMix[0,:]
GenMix = GenMix[1:8761,:].astype(np.float) #去除solar and wind

#1 日灵活性资源分布
#计算每小时各种发电资源的总发电量，绝对值 
GenSumDay = []
for i in range(len(GenMix)):
    t = np.sum(np.abs(GenMix[i,:]))
    GenSumDay.append(t)

# 剩余负荷
ResiL = ResidualLoad[1:8761,10].astype(np.float)    # 德国，选择第10列
     
#******************************** 日波动性计算 ********************************
# 1计算每日平均值
AVE_Day = np.reshape(np.mean(np.reshape(ResiL, (-1, 24)), axis=1), (-1, 1))

# 2计算每日每小时波动性: Load_Mat - AVE_Day
# 3计算日波动性 Flexibility
ResiL_Day_Diff = np.reshape(np.abs(np.reshape(ResiL, (-1, 24)) - AVE_Day), (-1, 1)) 
# 分别计算各种类型发电机组的发电量
GenMix_Fin = GenMix.copy()

DayFlexSum = []
for i in range(len(np.array(GenMix_Fin[0])[0])):
    for j in range(len(GenMix_Fin)):
        if GenSumDay[j] <= 0.1:
            GenSumDay[j] = 1
        GenMix_Fin[j,i] = abs(GenMix[j,i])/GenSumDay[j]*ResiL_Day_Diff[j,0]
    DayFlexSum.append(np.sum(GenMix_Fin[:,i])/1000000/2)  # 分别求和输出

#********************************** 周波动性计算 ******************************
# 1计算每周平均值
AVE_Week = np.reshape(np.mean(np.reshape(ResiL[0:52*7*24], (-1, 168)), axis=1), (-1, 1))

# 2计算每周中每天的波动性: Load_Mat_Week - AVE_Week
# 3计算周波动性 Flexibility
ResiL_Week = np.reshape(np.mat(AVE_Day[0:364]), (-1, 7)) #这个地方需要乘以24
# 计算周灵活性 Flexibility
ResiL_Week_Diff = np.reshape(np.abs(ResiL_Week - AVE_Week)*24, (-1, 1))

# 分别计算各种类型发电机组的发电量
GenMix_Week = GenMix_Fin[0:365,:].copy()
for i in range(len(np.array(GenMix_Week[0])[0])):
    Data = np.reshape(GenMix[0:8736,i], (-1, 24))
    for j in range(364):
        GenMix_Week[j,i] = np.abs(np.sum(Data[j]))
        
#求每天各种种电源发电量之和    
GenSumWeek = []  
for i in range(364):
    GenSumWeek.append(np.sum(GenMix_Week[i,:])) 
    
#求每天各种种电源发电量对灵活性的贡献     
WeekFlexSum = []
for i in range(len(np.array(GenMix_Week[0])[0])):
    for j in range(364):
        if GenSumWeek[j] <= 0.1:
            GenSumWeek[j] = 1
        GenMix_Week[j,i] = GenMix_Week[j,i]/GenSumWeek[j]*ResiL_Week_Diff[j,0]
    WeekFlexSum.append(np.sum(GenMix_Week[:,i])/1000000/2)  # 分别求和输出 

#******************************** 年波动性计算 ********************************
# 1计算剩余负荷月平均值
ResiL_Month = np.mean(np.reshape(ResiL, (-1, 730)), axis=1)
# 每年平均值
AVE_Year = np.mean(ResiL) 

# 2计算每年中每月的波动性: 
ResiL_Month_Diff = np.abs(ResiL_Month - AVE_Year)*730

# 计算年灵活性贡献 Flexible resources
# 分别计算各种类型发电机组的发电量
GenMix_Year = GenMix[0:12,:].copy()
for i in range(len(np.array(GenMix_Year[0])[0])):
    Data = np.reshape(GenMix[0:8760,i], (-1, 730))
    for j in range(12):
        GenMix_Year[j,i] = np.abs(np.sum(Data[j]))
        
#求每天各种种电源发电量之和    
GenSumYear = []  
for i in range(12):
    GenSumYear.append(np.sum(GenMix_Year[i,:])) 
    
#求每天各种种电源发电量对灵活性的贡献     
YearFlexSum = []
for i in range(len(np.array(GenMix_Year[0])[0])):
    for j in range(len(GenMix_Year)):
        if GenSumYear[j] <= 0.1:
            GenSumYear[j] = 1
        GenMix_Year[j,i] = GenMix_Year[j,i]/GenSumYear[j]*ResiL_Month_Diff[j,0]
    YearFlexSum.append(np.sum(GenMix_Year[:,i])/1000000/2)  

# *****************************************************************************
# ************************* Part 5: Save the Results **************************
# NetLoad_Flexibility_file = 'NetLoad_Flexibility.csv'      
# with open(NetLoad_Flexibility_file, "w", newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow('Flexibility_Day')
#         writer.writerows([Flexibility_Day])
#         writer.writerow('Flexibility_Week')
#         writer.writerows([Flexibility_Week])
#         writer.writerow('Flexibility_Year')
#         writer.writerows([Flexibility_Year])
#         writer.writerow('Average Hourly Load')
#         writer.writerows(Ave_Hourly_Load)
#         writer.writerow('HourlyGraddient')
#         writer.writerows(Hourly_Graddient)
#         f.close()
        
# Method2
book = Workbook()

# Create a new sheet in the workbook
sheet1 = book.add_sheet('Summary')
sheet2 = book.add_sheet('Flexibility')
sheet3 = book.add_sheet('Average Hourly Load')
sheet4 = book.add_sheet('Hourly Graddient')
sheet5 = book.add_sheet('Flexible Resource Contributions')

# ************************************ sheet 1: Summary Start **************************************
# Write summary information in sheet 1
sheet1.write(0, 0, "Sheet")
sheet1.write(0, 1, "Data")
sheet1.write(1, 0, "Flexibility")
sheet1.write(1, 1, "Regional Daily, Weekly, and Yearly Flexibility '(MW or GW)' ")
sheet1.write(2, 0, "Regional Average Hourly Residual Load")
sheet1.write(2, 1, "Average Residual Load (GW), Data from 1 to 24h")
sheet1.write(3, 0, "Regional Hourly Gradient")
sheet1.write(3, 1, "Residual Load Ramp Rate (GWh), Data from 1 to 24h")
# *************************** sheet 1: Summary End ****************************
# *************************** sheet 2: Flexibility ****************************
# Get Area Hourly Variable Setting
# sheet2.write(1, 0, "Daily Flexibility")
# sheet2.write(2, 0, "Weekly Flexibility")
# sheet2.write(3, 0, "Yearly Flexibility")
# for i in range(0, len(Flexibility_Day)):
#     sheet2.write(0, i+1, label[i])
#     sheet2.write(1, i+1, Flexibility_Day[i])
#     sheet2.write(2, i+1, Flexibility_Week[i])
#     sheet2.write(3, i+1, Flexibility_Year[i])

# *********************** sheet 3: Average Hourly Load ************************
# Get Area Hourly Variable Setting
# for i in range(0, 24):
#     sheet3.write(0, i+1, i+1)
    
# for i in range(0, len(label)):
#     sheet3.write(i+1, 0, label[i])
#     for j in range(0, 24):
#         sheet3.write(i+1, j+1, Ave_Hourly_Load[i][j])

# ****************** sheet 4: Average Hourly Gradient *************************
# Get Area Hourly Variable Setting
# for i in range(0, 24):
#     sheet4.write(0, i+1, i+1)
    
# for i in range(0, len(label)):
#     sheet4.write(i+1, 0, label[i])
#     for j in range(0, 24):
#         sheet4.write(i+1, j+1, Hourly_Graddient[i][j])

# ********************* sheet 4: Flexible Resource Contributions **************
# Get Area Hourly Variable Setting
# for i in range(0, 24):
#     sheet5.write(0, i+1, i+1)

Totol = [DayFlexSum, WeekFlexSum, YearFlexSum]  
for i in range(0, 3):
    # sheet5.write(0, i+1, FirstLine[0,i])
    for j in range(0, len(np.array(GenMix[0])[0])):
        sheet5.write(i+1, j+1, Totol[i][j])
        
CasePath = "C:\\Users\\Xingyu\\Desktop"
# Save the workbook to a selected CasePath        
book.save(CasePath+'\Residual Load Flexibility.xls')

print('Congratulations, task completed !') 