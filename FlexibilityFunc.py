# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 08:28:32 2020

@author: Xingyu
"""

import numpy as np
import matplotlib.pyplot as plt

# 净负荷波动性计算
def FlexibilityCalculate(Load, Load_Name):
    print('Calculating the Daily Load Flexibility ...')
    # Load_Mat = np.reshape(np.mat(Load), (-1, 24))
    Load_Mat = np.reshape(Load, (-1, 24))
    
    # 日波动性计算
    # 1计算每日平均值
    AVE_Day = np.reshape(np.mean(Load_Mat, axis=1), (-1, 1))
    
    # 2计算每日每小时波动性
    Load_Mat_Dif = Load_Mat - AVE_Day

    # 3计算日灵活性 Flexibility
    Flexi_Day = np.abs(Load_Mat_Dif).sum()
    print('Daily Flexibility of ' + Load_Name + ' Is %d MWh' % Flexi_Day)
    
    # plot the daily flexibility
    
    Load_Mat_Dif_toList_ThreeDays = np.reshape(np.mat(Load_Mat_Dif[0:3,:]), (1, -1)).tolist()
    x = Load[0:72]
    y = np.array(Load[0:72]) - np.array(Load_Mat_Dif_toList_ThreeDays[0])
    plt.figure()
    plt.plot(x, label="Load")
    plt.plot(y, label="Daily Average Load")
    # plt.plot(np.abs(Load_Mat_Dif_toList_ThreeDays[0]), label="Daily Flexibility")
    plt.tight_layout()
    plt.fill_between(range(72), x, y, facecolor="orange", # The fill color
                     color='blue',       # The outline color
                     alpha=0.2)                 
    plt.title('Daily Load Flexibility of ' + Load_Name)
    plt.ylabel('MW')
    plt.xlabel('Time (Hour)')
    # plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
    plt.legend()
    plt.show()

    # 周波动性计算
    # 1计算每周平均值
    print('Calculating the Weekly Load Flexibility ...')
    Load_Mat_Week = np.reshape(np.mat(Load[0:8736]), (-1, 168))

    AVE_Week = np.mean(Load_Mat_Week, axis=1)
    print('The Data Shape of Average Weekly Load Is '  + str(AVE_Week.shape))

    # 2计算每周中每天的波动性
    # 每天平均值
    Load_Mat_Week_Day = np.reshape(np.mat(AVE_Day[0:364]), (-1, 7)) 
    Load_Mat_Week_Day_Dif = Load_Mat_Week_Day - AVE_Week

    # 计算周灵活性 Flexibility
    Flexi_Week = np.abs(Load_Mat_Week_Day_Dif).sum()
    print('Weekly Flexibility of ' + Load_Name + ' Is %d MWh' % Flexi_Week)    
    
    # plot the daily flexibility
    Load_Mat_Week_Day_toList_3Weeks = np.reshape(np.mat(Load_Mat_Week_Day[0:3,:]), (1, -1)).tolist()
    Load_Mat_Week_Day_Dif_toList_3Weeks = np.reshape(np.mat(Load_Mat_Week_Day_Dif[0:3,:]), (1, -1)).tolist()
    x = Load_Mat_Week_Day_toList_3Weeks[0]
    y = Load_Mat_Week_Day_toList_3Weeks[0] - np.array(Load_Mat_Week_Day_Dif_toList_3Weeks[0])
    plt.figure()
    plt.plot(x, label="Average Daily Load")
    plt.plot(y, label="Weekly Average Load")
    # plt.plot(np.abs(Load_Mat_Week_Day_Dif_toList_3Weeks[0]), label="Weekly Flexibility")
    plt.tight_layout()
    plt.fill_between(range(21), x, y, facecolor="orange", # The fill color
                     color='blue',       # The outline color
                     alpha=0.2)
    plt.title('Weekly Load Flexibility of ' + Load_Name)
    plt.ylabel('MW')
    plt.xlabel('Time (Day)')
    # plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)
    plt.legend()
    plt.show()
    
    return Flexi_Day, Flexi_Week