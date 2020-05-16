# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 08:28:32 2020

@author: Xingyu
"""

import numpy as np
import matplotlib.pyplot as plt

# average daily residual load
def Ave_Resi_Load(Load: list, Load_Sub_Name: str): 
    print('Calculating the Average Daily Residual Load of ' + Load_Sub_Name +' ...')
    Load_Mat = np.reshape(Load, (-1, 24))/1000  # /1000: MW to GW
    
    # Average daily residual load
    AVE_Hour = np.reshape(np.mean(Load_Mat, axis=0), (1, -1)).tolist()[0]
    
    # Hourly Gradients
    Hourly_Grad = []
    for i in range(len(AVE_Hour)):
        if i == 0:
            HourlyGrad = AVE_Hour[i] - AVE_Hour[len(AVE_Hour)-1]
        else:
            HourlyGrad = AVE_Hour[i] - AVE_Hour[i-1]
        Hourly_Grad.append(HourlyGrad)
    
    # plt.figure()
    # x = range(len(AVE_Hour))
    # plt.plot(x, AVE_Hour, label='Average Residual Load')  
    # plt.plot(x, Hourly_Grad, label='Ramp Rate') 
    # plt.title('Hourly Average Residual Load and Ramp Rate for ' + Load_Sub_Name)
    # plt.ylabel('GW')
    # plt.xlabel('Time (Hour)')
    # # plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
    # plt.legend()
    # plt.show()
    
    fig, ax1 = plt.subplots()
    x = range(len(AVE_Hour))
    color = 'tab:red'
    ax1.set_xlabel('Time (Hour)')
    ax1.set_ylabel('Average Residual Load (GW)', color=color)
    ax1.plot(x, AVE_Hour, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.legend()
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis 
    color = 'tab:blue'
    ax2.set_ylabel('Ramp Rate (GWh)', color=color)  # we already handled the x-label with ax1
    ax2.plot(x, Hourly_Grad, color=color)
    ax2.tick_params(axis='y', labelcolor=color)    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title('Hourly Average Residual Load and Ramp Rate for ' + Load_Sub_Name)
    plt.legend()
    plt.show()
    
    return AVE_Hour, Hourly_Grad
    
    
# 净负荷波动性计算
def FlexibilityCalculate(Load, Load_Name):
    print('Calculating the Load Flexibility of ' + Load_Name +' ...')
    # Load_Mat = np.reshape(np.mat(Load), (-1, 24))
    # Load = Load/1000  # /1000: MW to GW
    Load_Mat = np.reshape(Load, (-1, 24))
    
    # 日波动性计算
    # 1计算每日平均值
    AVE_Day = np.reshape(np.mean(Load_Mat, axis=1), (-1, 1))
    
    # 2计算每日每小时波动性
    Load_Mat_Dif = Load_Mat - AVE_Day

    # 3计算日灵活性 Flexibility
    # Flexi_Day = np.abs(Load_Mat_Dif).sum()
    Flexi_Day = np.array(np.abs(Load_Mat_Dif).sum())/2/1000/1000 
    # # /2:只计算平均值上面部分； /1000/1000: MWh to TWh
    print('Daily Flexibility of ' + Load_Name + ' Is %d TWh' % Flexi_Day)
    
    # plot the daily flexibility
    NumDayPlot = 4  # The number of consecutive days to plot
    Load_Mat_Dif_toList_Days = np.reshape(np.mat(Load_Mat_Dif[0:NumDayPlot,:]), (1, -1)).tolist()
    x = np.array(Load[0:(24*NumDayPlot)])/1000
    y = np.array(Load[0:(24*NumDayPlot)])/1000 - np.array(Load_Mat_Dif_toList_Days[0])/1000
    plt.figure()
    plt.plot(x, label="Hourly Load")        # /1000: MW to GW
    plt.plot(y, label="Daily Average Load") # /1000: MW to GW
    # plt.plot(np.abs(Load_Mat_Dif_toList_Days[0]), label="Daily Flexibility")
    plt.tight_layout()
    plt.fill_between(range(24*NumDayPlot), x, y, facecolor="orange", # The fill color
                     color='blue',       # The outline color
                     alpha=0.2)                 
    plt.title('Daily Load Flexibility of ' + Load_Name)
    plt.ylabel('GW')
    plt.xlabel('Time (Hour)')
    # plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
    plt.legend()
    plt.show()

    # 周波动性计算
    # 1计算每周平均值
    Load_Mat_Week = np.reshape(np.mat(Load[0:int(len(Load)/(24*7))*(24*7)]), (-1, 168))

    AVE_Week = np.mean(Load_Mat_Week, axis=1)
    # print('The Data Shape of Average Weekly Load Is '  + str(AVE_Week.shape))

    # 2计算每周中每天的波动性
    # 每天平均值
    Load_Mat_Week_Day = np.reshape(np.mat(AVE_Day[0:364]), (-1, 7)) 
    Load_Mat_Week_Day_Dif = Load_Mat_Week_Day - AVE_Week

    # 计算周灵活性 Flexibility
    Flexi_Week = np.array(np.abs(Load_Mat_Week_Day_Dif).sum())/2/1000/1000 
    # /2:只计算平均值上面部分； /1000/1000: MWh to TWh
    print('Weekly Flexibility of ' + Load_Name + ' Is %d TWh' % Flexi_Week)    
    
    # plot the daily flexibility
    NumWeekPlot = 4  # The number of consecutive weeks to plot
    Load_Mat_Week_Day_toList_Weeks = np.reshape(np.mat(Load_Mat_Week_Day[0:NumWeekPlot,:]), (1, -1)).tolist()
    Load_Mat_Week_Day_Dif_toList_Weeks = np.reshape(np.mat(Load_Mat_Week_Day_Dif[0:NumWeekPlot,:]), (1, -1)).tolist()
    x = np.array(Load_Mat_Week_Day_toList_Weeks[0])/1000  # /1000: MW to GW
    y = np.array(Load_Mat_Week_Day_toList_Weeks[0] - np.array(Load_Mat_Week_Day_Dif_toList_Weeks[0]))/1000
    plt.figure()
    plt.plot(x, label="Average Daily Load")  
    plt.plot(y, label="Weekly Average Load") # /1000: MW to GW
    # plt.plot(np.abs(Load_Mat_Week_Day_Dif_toList_Weeks[0]), label="Weekly Flexibility")
    plt.tight_layout()
    plt.fill_between(range(7*NumWeekPlot), x, y, facecolor="orange", # The fill color
                     color='blue',       # The outline color
                     alpha=0.2)
    plt.title('Weekly Load Flexibility of ' + Load_Name)
    plt.ylabel('GW')
    plt.xlabel('Time (Day)')
    # plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
    plt.legend()
    plt.show()
    
    # 年波动性计算
    # 1计算剩余负荷月平均值
    Load_Mat_Month = np.reshape(np.mat(Load[0:len(Load)]), (-1, 730))
    
    AVE_Month = np.mean(Load_Mat_Month, axis=1)
    # print('The Data Shape of Average Weekly Load Is '  + str(AVE_Week.shape))

    # 2计算每年中每月的波动性
    # 每年平均值
    AVE_Year = np.mean(Load) 
    Load_Year_Month_Dif = AVE_Month - AVE_Year

    # 计算周灵活性 Flexibility
    Flexi_Year = np.array(np.abs(Load_Year_Month_Dif).sum())/2/1000
    # 2:只计算平均值上面部分； /1000: MWh to GWh
    print('Yearly Flexibility of ' + Load_Name + ' Is %d GWh' % Flexi_Year)    
    
    # plot the yearly flexibility

    x = np.reshape((np.repeat(AVE_Year, 12))/1000, (1, -1)).tolist()[0]  # /1000: MW to GW  
    Load_Year_Month_Dif_toList = (np.reshape(np.mat(Load_Year_Month_Dif)/1000, (1, -1)).tolist())[0]
    y =  [x[i]+Load_Year_Month_Dif_toList[i] for i in range(0,len(x))]
    
    plt.figure()
    plt.plot(x, label="Annual Average Load")  
    plt.plot(y, label="Monthly Average Load") # /1000: MW to GW
    plt.fill_between(range(12), x, y, facecolor="orange", # The fill color
                      color='blue',       # The outline color
                      alpha=0.2 )
    plt.title('Yearly Load Flexibility of ' + Load_Name)
    plt.ylabel('GW')
    plt.xlabel('Time (Month)')
    # plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
    plt.legend()
    plt.show()
       
    return Flexi_Day, Flexi_Week, Flexi_Year