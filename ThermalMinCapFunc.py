# -*- coding: utf-8 -*-
"""
Created on Thu May 14 08:42:29 2020

@author: Xingyu
"""

import numpy as np

def thermalMinCap(rowsMat, dictionary: dict):
    
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
        
        for j in range(len(thermalGenMinCap[0:-1,0])):        
            if float(thermalGenMinCap[j+1,i]) >= 0.1:
                thermalGenMinCap[j+1,i] = float(minCapGen)
            else:
                thermalGenMinCap[j+1,i] = float(0) 
               
            if itemNameCountry == 'it':
                it.append(thermalGenMinCap[j+1,i])
            elif itemNameCountry == 'pl':
                pl.append(thermalGenMinCap[j+1,i])
            elif itemNameCountry == 'cn':
                cn.append(thermalGenMinCap[j+1,i])
            elif itemNameCountry == 'gb':
                gb.append(thermalGenMinCap[j+1,i])
            elif itemNameCountry == 'casia':
                casia.append(thermalGenMinCap[j+1,i])
            elif itemNameCountry == 'de':
                de.append(thermalGenMinCap[j+1,i])
            elif itemNameCountry == 'fr':
                fr.append(thermalGenMinCap[j+1,i])
            elif itemNameCountry == 'eur':
                if (itemName.split('_'))[2] == 'c':
                    pl.append(thermalGenMinCap[j+1,i])
                elif (itemName.split('_'))[2] == 'se':
                    eur.append(thermalGenMinCap[j+1,i])
                else:
                    print('Attention! There is a problem with area EUR.')
            elif itemNameCountry == 'bl':
                bl.append(thermalGenMinCap[j+1,i])
            elif itemNameCountry == 'bnl':
                bnl.append(thermalGenMinCap[j+1,i])
            elif itemNameCountry == 'ept':
                ept.append(thermalGenMinCap[j+1,i])
            elif itemNameCountry == 'gr':
                gr.append(thermalGenMinCap[j+1,i])
            elif (itemNameCountry == 'ch')or(itemNameCountry == 'at'):
                ch.append(thermalGenMinCap[j+1,i])
            else:
                print('Attention! There is no ', itemName)
    
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
    
    # return it, pl, cn, gb, sc, casia, de, fr, eur, bl, at, bnl, ept, gr, ch  
    return it, pl, cn, gb, sc, casia, de, fr, eur, bl, bnl, ept, ch 