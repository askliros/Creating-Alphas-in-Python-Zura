# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 17:57:59 2020

@author: aris_
"""
self.Value=0*self.AuxiliaryAlpha2.iloc[dateIndex,1:].copy()
for kkk in range(1,self.AuxiliaryAlpha1.shape[1]):
    self.Value.iloc[kkk]= HistoryOpen.iloc[:,kkk].corr(HistoryClose.iloc[:,kkk])
#slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency)
class Alpha9Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.DaysOfLag,self.startDate):
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]-self.Close.iloc[dateIndex-self.DaysOfLag,1:]
    def SetAlphaParameters(self,daysOfTS,DaysOfLag): 
        self.daysOfTS=daysOfTS
        self.DaysOfLag=DaysOfLag
        self.TheAlphaReturns=self.CreatingReturns(self.TradingFrequency)
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1         
        if( ( (self.daysOfTS+self.DaysOfLag)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfTS+self.DaysOfLag)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
    
import pandas as pd
import numpy as np
A=pd.DataFrame(np.random.randn(100,10))
TradingFrequency=1
dateIndex=50
Days=10
stringVariable='A'
string1='History=A.iloc[slice(dateIndex-Days*TradingFrequency,dateIndex,TradingFrequency),1:]'
exec(string1)