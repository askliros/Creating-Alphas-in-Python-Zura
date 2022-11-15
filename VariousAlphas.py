# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 11:52:50 2020

@author: aris_
"""


import os
os.getcwd()
import pandas as pd
import numpy as np
from CreatingAlphaTradingFrequency import *

class AlphaNegReturns(Alpha):
    def SetAlphaParameters(self,n):
        self.n=n
        if(self.n<=self.startDate):
            pass
        else:
            self.startDate=self.n
        #self.FillingZeros()   
        self.TheAlphaReturns=self.CreatingReturns(n)
            
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.Value=-self.TheAlphaReturns.iloc[dateIndex,1:]
        self.Value.fillna(value=0,inplace=True)
        self.dateIndex=dateIndex
        self.PrepareAlpha(dateIndex, TotalAvailable)  
        self.IndNeut2()
        #self.PCANeut2(NumberOfDays=10,NumberOfPCA=3)
        # self.IndSector2()          
        return self.Value
        

class AlphaRank(Alpha):
    def SetAlphaParameters(self,Input):        
        self.Input=Input.copy()
        #self.FillingZeros()
    def GenerateAlpha(self,dateIndex,TotalAvailable):
        self.dateIndex=dateIndex
        AuxInput=self.Input.iloc[dateIndex,1:]
        AuxInput.loc[AuxInput<0]=-AuxInput.loc[AuxInput<0]
        self.Input.iloc[dateIndex,1:]=AuxInput
        self.Value=(1.0/np.max(self.Input.iloc[dateIndex,1:]))*self.Input.iloc[dateIndex,1:].sort_values(ascending=False)        
        #self.PrepareAlpha(dateIndex, TotalAvailable) 
        self.PrepareAlpha(dateIndex, TotalAvailable)  
        # self.IndNeut2()
        # self.IndSector2()         
        return self.Value
        
class AlphaInverseInput(Alpha):
    def SetAlphaParamemters(self,Input):
        self.Input=Input.copy()
        self.CurrentIndex=0
        #self.FillingZeros()
    def Inverter(self,x):
        if(x==0):
            return 0
        else:
            return 1/x
        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.Value=self.Input.iloc[dateIndex,1:].apply(self.Inverter)        
        self.PrepareAlpha(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()           
        return self.Value
        
        
class AlphaCorrelation(Alpha):
    def SetAlphaParameters(self,Input1,Input2,n):
        self.Input1=Input1.copy()
        self.Input2=Input2.copy()
        self.CurrentIndex=0
        self.n=n
        #self.FillingZeros()
    def Correlation(self,col):
        return -(self.Input1.iloc[self.dateIndex-self.n+1:self.dateIndex+1,col].astype('float64')).corr(self.Input2.iloc[self.dateIndex-self.n+1:self.dateIndex+1,col].astype('float64'))
    
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        if(dateIndex<self.n):
            pass
        else:        
            self.dateIndex=dateIndex
            self.ValueOld=pd.DataFrame(list(map(self.Correlation,range(1,self.Input1.shape[1]))))
            self.ValueOld=self.ValueOld.transpose()         
            self.Value=self.ValueOld.copy()
            self.Value.columns=self.Input1.iloc[:,1:].columns
            self.Value.fillna(value=0,inplace=True) 
            #self.PrepareAlpha2(dateIndex, TotalAvailable)            
            self.PrepareAlpha2(dateIndex, TotalAvailable) 
            # self.IndNeut2()
            # self.IndSector2()
            return self.Value.iloc[0,:]