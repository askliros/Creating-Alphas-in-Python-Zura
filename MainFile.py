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
from FindingPnL import *
from VariousAlphas import *
import matplotlib.pyplot as plt



#os.chdir("C:\\Users\\aris_\\AlphaDevelopment")  
#os.chdir() 

def SelectAlpha(AlphaIndex,NumberOfStocksTrading,TradingFrequency,startDate,TotalAmount,TransactionCosts,percentageOfHistory,n):                                                                                                                                                                                                                                     
    PD1=ProcessData("OpenStock2.csv","CloseStock2.csv","HighStock2.csv","LowStock2.csv","VolumeStock2.csv","MarketCapStock2.csv","IndustryStock2.csv","SectorStock2.csv","AdjacencyMatrixStockSector.csv","AdjacencyMatrixStockIndustry.csv")
    PD1.GetData()
    
    if(AlphaIndex==1):
        Alpha11=AlphaNegReturns(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading)
        Alpha11.SetAlphaParameters(n)
    elif(AlphaIndex==2):
        Alpha11=AlphaRank(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading)
        Input=PD1.Prices.copy()
        Alpha11.SetAlphaParameters(Input)
    elif(AlphaIndex==3):
        Alpha11=AlphaRank(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading)
        Input=PD1.Prices.copy()
        Alpha11.SetAlphaParameters(Input)
    elif(AlphaIndex==3):
        Alpha11=AlphaCorrelation(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading)
        Input1=PD1.Prices.copy()
        Input2=PD1.Prices.shift(periods=10,fill_value=0).copy()
        Alpha11.SetAlphaParameters(Input1,Input2,10)
    else:
        Alpha11=AlphaNegReturns(PD1,TotalAmount,startDate,TradingFrequency,TransactionCosts,NumberOfStocksTrading)
        Alpha11.SetAlphaParameters(n)
        
    PnLAlpha11=PnL(Alpha11)
    PnLAlpha11.getAlphaPnL(percentageOfHistory)
    plt.plot(PnLAlpha11.CumPnLVector.index,PnLAlpha11.CumPnLVector)        
    plt.xlabel("Time")
    plt.ylabel("PnL")     
    
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
    PnLAlpha=SelectAlpha(s,NumberOfStocksTrading,TradingFrequency,startDate,TotalAmount,TransactionCosts,percentageOfHistory,n)

if __name__ == "__main__":
    ThePnLAlpha=main()
