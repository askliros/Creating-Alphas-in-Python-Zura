# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 16:21:41 2020

@author: aris_
"""


import os
os.getcwd()
import pandas as pd
import numpy as np
from CreatingAlphaTradingFrequency import *

class PnL:
    def __init__(self,Alpha):
        self.Alpha=Alpha
    
    def getAlphaPnLWQ(self,percentageOfHistory):
        TransactionCostPerStockTrading=self.Alpha.TransactionCosts
        self.Returns=self.Alpha.TheAlphaReturns
        self.AlphaA=self.Returns.copy()
        self.AlphaA.iloc[:,1:]=0*self.Returns.iloc[:,1:]
        self.PnL=self.Returns.copy()
        self.PnL.iloc[:,1:]=0*self.Returns.iloc[:,1:]
        self.PnLWithCosts=self.PnL.iloc[:int(percentageOfHistory*self.Alpha.Prices.shape[0])].sum(axis=1) 
        self.TotalPnL=0
        summ=0
        self.MeanReturn=0
        self.MeanSquareReturn=0
        summm=0
        for kkk in range(self.Alpha.startDate,int(percentageOfHistory*self.Alpha.Prices.shape[0]),self.Alpha.TradingFrequency):
            summm=summm+1
            self.AlphaA.iloc[kkk,1:]=self.Alpha.GenerateAlpha(kkk,self.Alpha.TotalAmount) 
            if((summm%3)==0):
                Keys1=self.Alpha.MarketCapToday.keys()
            elif((summm%3)==1):
                Keys2=self.Alpha.MarketCapToday.keys()
            elif((summm%3)==2):
                Keys3=self.Alpha.MarketCapToday.keys()
            if(self.AlphaA is None):
                pass
            else:
                if(summm>2):
                    summ=summ+1
                    TheAlpha=self.AlphaA.iloc[kkk-2*self.Alpha.TradingFrequency,1:]
                    # TheAlpha.loc[self.Alpha.MarketCapToday.keys()]
                    # Returns.loc[kkk,self.Alpha.MarketCapToday.keys()]
                    if((summm%3)==0):
                        self.PnL.iloc[kkk,1:]=TheAlpha.loc[Keys2]*self.Returns.loc[kkk,Keys1] 
                        #print(TheAlpha.loc[Keys2])
                    elif((summm%3)==1):
                        self.PnL.iloc[kkk,1:]=TheAlpha.loc[Keys3]*self.Returns.loc[kkk,Keys2]
                        #print(TheAlpha.loc[Keys3])
                    elif((summm%3)==2):
                        self.PnL.iloc[kkk,1:]=TheAlpha.loc[Keys1]*self.Returns.loc[kkk,Keys3] 
                        #print(TheAlpha.loc[Keys1])
                    TheReturn=self.PnL.iloc[kkk,1:].sum()/self.Alpha.TotalAmount
                    self.MeanReturn=(float(summ-1)/float(summ))*self.MeanReturn+(float(1.0)/float(summ))*TheReturn
                    self.MeanSquareReturn=(float(summ-1)/float(summ))*self.MeanSquareReturn+(float(1.0)/float(summ))*TheReturn*TheReturn
                    self.VarianceReturn=self.MeanSquareReturn-self.MeanReturn*self.MeanReturn
                    self.Sharpe=self.MeanReturn/np.sqrt(self.VarianceReturn)
                    self.TotalPnL=self.TotalPnL+self.PnL.iloc[kkk,1:].sum() 
                    print("The kkk is:")
                    print(kkk)
                    print("The summm is:")
                    print(summm)
                    print("The summ is:")
                    print(summ)
                    print("The current PnL is:")
                    print(self.PnL.iloc[kkk,1:].sum())
                    print("The total PnL is:")    
                    print(self.TotalPnL)
                    print("The current Sharpe is:")
                    print(self.Sharpe)
                   
        self.PnLVector =self.PnL.iloc[:int(percentageOfHistory*self.Alpha.Prices.shape[0])].sum(axis=1) 
        self.CumPnLVector=self.PnLVector.cumsum()     
        self.NumberOfStocks  = self.AlphaA.iloc[:int(percentageOfHistory*self.Alpha.Prices.shape[0]),1:].div(self.Alpha.Close.iloc[self.Alpha.TradingFrequency :int(percentageOfHistory*self.Alpha.Prices.shape[0])+self.Alpha.TradingFrequency ,1:]) 
        self.NumberOfStocks.fillna(value=0,inplace=True)
        self.ChangeInNumberOfStocks=self.NumberOfStocks-self.NumberOfStocks.shift(self.Alpha.TradingFrequency )
        self.ChangeInNumberOfStocks.fillna(value=0,inplace=True)
        self.DeltaAlpha=self.AlphaA.iloc[:int(percentageOfHistory*self.Alpha.Prices.shape[0]),1:]-self.AlphaA.iloc[:int(percentageOfHistory*self.Alpha.Prices.shape[0]),1:].shift(self.Alpha.TradingFrequency )
        self.DeltaAlpha.fillna(value=0,inplace=True)
        self.TransactionCosts=np.count_nonzero(self.DeltaAlpha, axis=1)*TransactionCostPerStockTrading
        self.TransactionCosts=pd.DataFrame(self.TransactionCosts)
        self.PnLWithCostsVector=self.PnLVector- self.TransactionCosts.iloc[:,0]