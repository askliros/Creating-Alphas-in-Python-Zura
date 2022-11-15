# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 10:55:37 2020

@author: aris_
"""


import os
os.getcwd()
import pandas as pd
import numpy as np
from CreatingAlphaTradingFrequency import *
from FindingPnLWQ import *
from VariousAlphasWQ import *
import matplotlib.pyplot as plt



#os.chdir("C:\\Users\\aris_\\AlphaDevelopment")  
#os.chdir() 

def SelectAlpha(AlphaIndex,NumberOfStocksTrading,TradingFrequency,startDate,TotalAmount,TransactionCosts,percentageOfHistory,n,PD1):                                                                                                                                                                                                                                     
    
    
    if(AlphaIndex==102):
        Alpha11=AlphaNegReturns(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading)
        Alpha11.SetAlphaParameters(n)
    elif(AlphaIndex==103):
        Alpha11=AlphaRank(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading)
        Input=PD1.Prices.copy()
        Alpha11.SetAlphaParameters(Input)
    elif(AlphaIndex==104):
        Alpha11=AlphaRank(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading)
        Input=PD1.Prices.copy()
        Alpha11.SetAlphaParameters(Input)
    elif(AlphaIndex==105):
        Alpha11=AlphaCorrelation(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading)
        Input1=PD1.Prices.copy()
        Input2=PD1.Prices.shift(periods=10,fill_value=0).copy()
        Alpha11.SetAlphaParameters(Input1,Input2,10)
    elif(AlphaIndex==1):
        Alpha11=Alpha1Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading)        
        Alpha11.SetAlphaParameters(daysOfReturns=20,Power=2.0,DaysOfTsRank=5) 
    elif(AlphaIndex==2):
        Alpha11=Alpha2Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=6,DaysOfLag=2)
    elif(AlphaIndex==3):
        Alpha11=Alpha3Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=10,DaysOfLag=0)
    elif(AlphaIndex==4):
        Alpha11=Alpha4Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=9,DaysOfLag=0)
    elif(AlphaIndex==6):
        Alpha11=Alpha6Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=10,DaysOfLag=0)
    elif(AlphaIndex==7):
        Alpha11=Alpha7Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfTSRank=60,DaysOfLag=7,DaysOfVolume=20)
    elif(AlphaIndex==8):
        Alpha11=Alpha8Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfSum=5,DaysOfDelay=10)
    elif(AlphaIndex==9):
        Alpha11=Alpha9And10Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfTS=5,DaysOfLag=1)
    elif(AlphaIndex==10):
        Alpha11=Alpha9And10Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfTS=4,DaysOfLag=1)
    elif(AlphaIndex==12):
        Alpha11=Alpha12Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(DaysOfLag=1)
    elif(AlphaIndex==13):
        Alpha11=Alpha13Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCovariance=5)
    elif(AlphaIndex==14):
        Alpha11=Alpha14Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfTS=10,DaysOfLag=3)
    elif(AlphaIndex==15):
        Alpha11=Alpha15Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=3,DaysOfSum=3)
    elif(AlphaIndex==16):
        Alpha11=Alpha16Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCovariance=5)
    elif(AlphaIndex==17):
        Alpha11=Alpha17Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfTSRank1=10,daysOfTSRank2=5,DaysOfLag=1,DaysOfADV=20)
    elif(AlphaIndex==18):
        Alpha11=Alpha18Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfTS=5,DaysOfCorrelation=10)
    elif(AlphaIndex==19):
        Alpha11=Alpha19Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfLag1=7,daysOfReturns=250)
    elif(AlphaIndex==20):
        Alpha11=Alpha20Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(DaysOfLag=1)
    elif(AlphaIndex==21):
        Alpha11=Alpha21Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(DaysOfLag1=8,DaysOfLag2=2,DaysOfVolume=20,mul1=0.5,mul2=0.125)
    elif(AlphaIndex==22):
        Alpha11=Alpha22Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=5,daysOfStD=20,daysOfLag=5)
    elif(AlphaIndex==23):
        Alpha11=Alpha23Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfTS=20,DaysOfLag=2)
    elif(AlphaIndex==24):
        Alpha11=Alpha24Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfTS=100,DaysOfLag=3)
    elif(AlphaIndex==26):
        Alpha11=Alpha26Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfTS=5,DaysOfCorrelation=5,daysOfTSMax=3)
    elif(AlphaIndex==28):
        Alpha11=Alpha28Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfADV=20,DaysOfCorrelation=5)
    elif(AlphaIndex==29):
        Alpha11=Alpha29Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfLag=5,daysOfTSmin=5,daysOfSum=5,daysOfProd=1,daysOfTsMin2=1,daysOfdelay=6,daysOfTSRank=5)
    elif(AlphaIndex==30):
        Alpha11=Alpha30Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(DaysOfLag1=1,DaysOfLag2=1,DaysOfLag3=2,DaysOfLag4=2,DaysOfLag5=3,daysADV1=5,daysADV2=20)
    elif(AlphaIndex==31):
        Alpha11=Alpha31Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfADV=20,daysOfCorrelation=12,daysOfLag1=10,daysOfLag2=3,daysOfLinearDecay=10)
    elif(AlphaIndex==33):
        Alpha11=Alpha33Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters()
    elif(AlphaIndex==34):
        Alpha11=Alpha34Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfstd1=2,daysOfstd2=5,DaysOfLag=1)
    elif(AlphaIndex==35):
        Alpha11=Alpha35Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfTSRank1=32,daysOfTSRank2=16,daysOfTSRank3=32)
    elif(AlphaIndex==37):
        Alpha11=Alpha37Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=200,daysOfDelay=1)
    elif(AlphaIndex==38):
        Alpha11=Alpha38Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfTSRank=10)
    elif(AlphaIndex==39):
        Alpha11=Alpha39Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfLag=7,daysOfADV=20,daysOfDecay=9,daysOfSum=250)
    elif(AlphaIndex==40):
        Alpha11=Alpha40Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=10,daysOfStd=10)
    elif(AlphaIndex==43):
        Alpha11=Alpha43Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfLag=7,daysOfADV=20,daysOfTSRank1=20,daysOfTSRank2=8)
    elif(AlphaIndex==44):
        Alpha11=Alpha44Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=5)
    elif(AlphaIndex==45):
        Alpha11=Alpha45Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=2,daysSum1=20,daysSum2=2,daysOfDelay=5,daysOfMean=20)
    elif(AlphaIndex==46):
        Alpha11=Alpha46Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfLag1=20,daysOfLag2=10,daysOfLag3=10,daysOfLag4=1)
    elif(AlphaIndex==48):
        Alpha11=Alpha48Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfDelta=1,daysOfLag=1,daysOfCorrelation=250,daysOfSum=250)
    elif(AlphaIndex==49):
        Alpha11=Alpha49Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfLag1=20,daysOfLag2=10,daysOfLag3=10,daysOfLag4=1)
    elif(AlphaIndex==51):
        Alpha11=Alpha51Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfLag1=20,daysOfLag2=10,daysOfLag3=10,daysOfLag4=1)
    elif(AlphaIndex==52):
        Alpha11=Alpha52Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfTSRank1=5,daysOfTSRank2=5,daysOfDelay=5,daysOfSum1=240,daysOfSum2=20)
    elif(AlphaIndex==53):
        Alpha11=Alpha53Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfDelta=9)
    elif(AlphaIndex==54):
        Alpha11=Alpha54Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters()
    elif(AlphaIndex==55):
        Alpha11=Alpha55Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfTS=12,daysOfCorrelation=6)
    elif(AlphaIndex==56):
        Alpha11=Alpha56Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfTS=10,daysOfSum=6)
    elif(AlphaIndex==60):
        Alpha11=Alpha60Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysTS=10)
    elif(AlphaIndex==68):
        Alpha11=Alpha68Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=9,daysOfADV=15,daysOfTSRank=14,daysOfLag=1,w1=0.5)
    elif(AlphaIndex==80):
        Alpha11=Alpha80Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=5,daysOfADV=10,daysOfTSRank=4,daysOfLag=4,w1=0.85,w2=0.15)
    elif(AlphaIndex==82):
        Alpha11=Alpha82Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=7,daysOfDecayLinear1=14,daysOfDecayLinear2=15,daysOfTSRank=14,daysOfDelta=2,w1=0.65,w2=.35)
    elif(AlphaIndex==85):
        Alpha11=Alpha85Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation1=10,daysOfCorrelation2=7,daysOfTSRank1=4,daysOfTSRank2=10,daysOfADV=30,w1=0.85,w2=.15)
    elif(AlphaIndex==88):
        Alpha11=Alpha88Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=9,daysOfDecayLinear1=8,daysOfDecayLinear2=8,daysOfTSRank1=7,daysOfTSRank2=8,daysOfTSRank3=8,daysOfADV=60)
    elif(AlphaIndex==90):
        Alpha11=Alpha90Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=6,daysOfTSRank=4,daysOfTSMax=5,daysOfADV=40)
    elif(AlphaIndex==92):
        Alpha11=Alpha92Zura(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading) 
        Alpha11.SetAlphaParameters(daysOfCorrelation=19,daysOfTSRank1=13,daysOfTSRank2=13,daysOfDecayLinear1=14,daysOfDecayLinear2=8,daysOfADV=30)
    else:
        Alpha11=AlphaNegReturns(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading)
        Alpha11.SetAlphaParameters(n)
        
    PnLAlpha11=PnL(Alpha11)
    PnLAlpha11.getAlphaPnLWQ(percentageOfHistory)
    PnLAlpha11.PnLVector.to_csv('Alpha'+str(AlphaIndex)+'Zura'+'.csv')
    plt.plot(PnLAlpha11.CumPnLVector.index,PnLAlpha11.CumPnLVector)        
    plt.xlabel("Time")
    plt.ylabel("PnL")  
    return PnLAlpha11
    
def main():
    print("Give the Alpha Index:")
    s = input()
    NumberOfStocksTrading=2000
    TradingFrequency=1
    startDate=5
    TotalAmount=200000
    TransactionCosts=60
    percentageOfHistory=0.8
    n=5
    s=1
    PD1=ProcessData("OpenStock2.csv","CloseStock2.csv","HighStock2.csv","LowStock2.csv","VolumeStock2.csv","MarketCapStock2.csv","IndustryStock2.csv","SectorStock2.csv","AdjacencyMatrixStockSector.csv","AdjacencyMatrixStockIndustry.csv")
    PD1.GetData()
    PD1.CreatingReturns(TradingFrequency)
    PnLAlpha=SelectAlpha(s,NumberOfStocksTrading,TradingFrequency,startDate,TotalAmount,TransactionCosts,percentageOfHistory,n,PD1)     
    #Debug Alpha60
    # for kkk in range(60,61):
    #     if(kkk in [27,32,36,41,42,47,50,57,58,59]):
    #         pass
    #     else:
    #         PnLAlpha=SelectAlpha(kkk,NumberOfStocksTrading,TradingFrequency,startDate,TotalAmount,TransactionCosts,percentageOfHistory,n,PD1)     
    for kkk in [68,80,82,85,88,90,92]:        
        PnLAlpha=SelectAlpha(kkk,NumberOfStocksTrading,TradingFrequency,startDate,TotalAmount,TransactionCosts,percentageOfHistory,n,PD1)     
         
    return PnLAlpha


if __name__ == "__main__":
    ThePnLAlpha=main()


for kkk in [68,80,82,85,88,90,92]:
    print(kkk)
