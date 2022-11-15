
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
        self.TheAlphaReturns=self.ProcessData.Returns
            
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.Value=-self.TheAlphaReturns.iloc[dateIndex,1:]
        self.Value.fillna(value=0,inplace=True)
        self.dateIndex=dateIndex
        self.PrepareAlphaNeut(dateIndex, TotalAvailable)  
        self.IndNeut2()
        #self.PCANeut2(NumberOfDays=10,NumberOfPCA=3)
        # self.IndSector2()          
        return self.Value
        

class AlphaRank(Alpha):
    def SetAlphaParameters(self,Input):        
        self.Input=Input.copy()
        self.TheAlphaReturns=self.ProcessData.Returns
        #self.FillingZeros()
    def GenerateAlpha(self,dateIndex,TotalAvailable):
        self.dateIndex=dateIndex
        AuxInput=self.Input.iloc[dateIndex,1:]
        AuxInput.loc[AuxInput<0]=-AuxInput.loc[AuxInput<0]
        self.Input.iloc[dateIndex,1:]=AuxInput
        self.Value=(1.0/np.max(self.Input.iloc[dateIndex,1:]))*self.Input.iloc[dateIndex,1:].sort_values(ascending=False)        
        #self.PrepareAlpha(dateIndex, TotalAvailable) 
        self.PrepareAlphaNeut(dateIndex, TotalAvailable)  
        # self.IndNeut2()
        # self.IndSector2()         
        return self.Value
        
class AlphaInverseInput(Alpha):
    def SetAlphaParamemters(self,Input):
        self.Input=Input.copy()
        self.CurrentIndex=0
        #self.FillingZeros()
        self.TheAlphaReturns=self.ProcessData.Returns
    def Inverter(self,x):
        if(x==0):
            return 0
        else:
            return 1/x
        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.Value=self.Input.iloc[dateIndex,1:].apply(self.Inverter)        
        self.PrepareAlphaNeut(dateIndex, TotalAvailable) 
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
        self.TheAlphaReturns=self.ProcessData.Returns
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
            self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
            # self.IndNeut2()
            # self.IndSector2()
            return self.Value.iloc[0,:]
        
        
class Alpha1Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.TradingFrequency,self.startDate):
            IndexPositiveReturns=np.where(self.TheAlphaReturns.iloc[dateIndex,1:]>0)
            IndexPositiveReturns=IndexPositiveReturns[0]+1
            IndexNegativeReturns=np.where(self.TheAlphaReturns.iloc[dateIndex,1:]<0)
            IndexNegativeReturns=IndexNegativeReturns[0]+1
            SelectedReturns=self.TheAlphaReturns.loc[slice(dateIndex-self.daysOfReturns*self.TradingFrequency,dateIndex,self.TradingFrequency),:]
            #if  returns are positive then close
            self.AuxiliaryAlpha.iloc[dateIndex,IndexPositiveReturns]  = self.Close.iloc[dateIndex,IndexPositiveReturns]
            #if returns are negative then 20 periods standard deviation of returns
            self.AuxiliaryAlpha.iloc[dateIndex,IndexNegativeReturns]  = SelectedReturns.iloc[:,IndexNegativeReturns].std()
            #raise the Auxiliary Alpha at the power of self.Power
            self.AuxiliaryAlpha.iloc[dateIndex,1:]=self.AuxiliaryAlpha.iloc[dateIndex,1:].pow(self.Power)
            ##print(dateIndex)

        
    def SetAlphaParameters(self,daysOfReturns,Power,DaysOfTsRank):
        self.daysOfReturns=daysOfReturns
        self.Power=Power
        self.DaysOfTsRank=DaysOfTsRank
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha=0*self.AuxiliaryAlpha        
        if( (self.daysOfReturns*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=self.daysOfReturns*self.TradingFrequency
        self.GenerateAuxiliaryAlpha()
            
            
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        IndexPositiveReturns=np.where(self.TheAlphaReturns.iloc[dateIndex,1:]>0)
        IndexPositiveReturns=IndexPositiveReturns[0]+1
        IndexNegativeReturns=np.where(self.TheAlphaReturns.iloc[dateIndex,1:]<0)
        IndexNegativeReturns=IndexNegativeReturns[0]+1
        SelectedReturns=self.TheAlphaReturns.loc[slice(dateIndex-self.daysOfReturns*self.TradingFrequency,dateIndex,self.TradingFrequency),:]
        #if  returns are positive then close
        self.AuxiliaryAlpha.iloc[dateIndex,IndexPositiveReturns]  = self.Close.iloc[dateIndex,IndexPositiveReturns]
        #if returns are negative then 20 periods standard deviation of returns
        self.AuxiliaryAlpha.iloc[dateIndex,IndexNegativeReturns]  = SelectedReturns.iloc[:,IndexNegativeReturns].std()
        #raise the Auxiliary Alpha at the power of self.Power
        self.AuxiliaryAlpha.iloc[dateIndex,1:]=self.AuxiliaryAlpha.iloc[dateIndex,1:].pow(self.Power)
        self.dateIndex=dateIndex
        
        #Finding History of Auxiliary Alpha
        HistoryOfAuxiliaryAlpha=self.AuxiliaryAlpha.iloc[slice(self.dateIndex-self.DaysOfTsRank*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        #Finding Ts Arg Max of Auxiliary Alpha
        TSArgMax=HistoryOfAuxiliaryAlpha.idxmax() 
        #Rank of TSArgMax -0.5
        #We just need to divide with the double of the max of the absolute value 
        #Find the maximum of absolute values
        MaxOfAbsolute=TSArgMax.abs().max()
        #Divide with the maximum of of the absolute value
        RankTSArgMax=(1.0/(2.0*MaxOfAbsolute))*TSArgMax        
        self.Value=-RankTSArgMax
        self.Value.fillna(value=0,inplace=True)
        #self.PrepareAlpha(dateIndex, TotalAvailable)
        #self.PrepareAlphaNeut(dateIndex, TotalAvailable) 
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        #self.IndNeut2() #Never leave it alone
        #self.IndSector2()
        #self.PCANeut2(NumberOfDays=20,NumberOfPCA=3)
        return self.Value
        
        
        
class Alpha2Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Volume.iloc[dateIndex,1:].astype('int32').apply(np.log)-self.Volume.iloc[dateIndex-self.DaysOfLag,1:].astype('int32').apply(np.log)
            #Getting the Rank for AuxiliaryAlpha1:
            AuxiliaryAlpha1Max=self.AuxiliaryAlpha1.iloc[dateIndex,1:].abs().max()
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=(1.0/(2.0*AuxiliaryAlpha1Max))*self.AuxiliaryAlpha1.iloc[dateIndex,1:]
            Kpos1=np.where(self.AuxiliaryAlpha1.iloc[dateIndex,1:]>0)
            Kpos1=Kpos1[0]+1
            Kneg1=np.where(self.AuxiliaryAlpha1.iloc[dateIndex,1:]<0)
            Kneg1=Kneg1[0]+1
            self.AuxiliaryAlpha1.loc[dateIndex,Kpos1]=(0.5/self.AuxiliaryAlpha1.loc[dateIndex,Kpos1].max())*self.AuxiliaryAlpha1.loc[dateIndex,Kpos1]
            self.AuxiliaryAlpha1.loc[dateIndex,Kneg1]=(0.5/self.AuxiliaryAlpha1.loc[dateIndex,Kneg1].abs().max())*self.AuxiliaryAlpha1.loc[dateIndex,Kneg1]
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.AuxiliaryAlpha1.iloc[dateIndex,1:]+0.5
            #Auxiliary 2
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=(self.Close.iloc[dateIndex,1:]-self.Open.iloc[dateIndex,1:])/self.Open.iloc[dateIndex,1:]
            #Getting the Rank for AuxiliaryAlpha2:
            AuxiliaryAlpha2Max=self.AuxiliaryAlpha2.iloc[dateIndex,1:].abs().max()
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=(1.0/(2.0*AuxiliaryAlpha2Max))*self.AuxiliaryAlpha2.iloc[dateIndex,1:]
            Kpos=np.where(self.AuxiliaryAlpha2.iloc[dateIndex,1:]>0)
            Kpos=Kpos[0]+1
            Kneg=np.where(self.AuxiliaryAlpha2.iloc[dateIndex,1:]<0)
            Kneg=Kneg[0]+1
            self.AuxiliaryAlpha2.iloc[dateIndex,Kpos]=(0.5/self.AuxiliaryAlpha2.iloc[dateIndex,Kpos].max())*self.AuxiliaryAlpha2.iloc[dateIndex,Kpos]
            self.AuxiliaryAlpha2.iloc[dateIndex,Kneg]=(0.5/self.AuxiliaryAlpha2.iloc[dateIndex,Kneg].abs().max())*self.AuxiliaryAlpha2.iloc[dateIndex,Kneg]
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.AuxiliaryAlpha2.iloc[dateIndex,1:]+0.5
            

    def SetAlphaParameters(self,daysOfCorrelation,DaysOfLag):
        self.daysOfCorrelation=daysOfCorrelation
        self.DaysOfLag=DaysOfLag
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1 
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2 
        if( (self.daysOfCorrelation*self.TradingFrequency*(self.DaysOfLag+1))<=self.startDate):
            pass
        else:
            self.startDate=self.daysOfCorrelation*self.TradingFrequency*(self.DaysOfLag +1)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        #Auxiliary 1
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Volume.iloc[dateIndex,1:].astype('float32').apply(np.log)-self.Volume.iloc[dateIndex-self.DaysOfLag,1:].astype('float32').apply(np.log)
        #Getting the Rank for AuxiliaryAlpha1:
        AuxiliaryAlpha1Max=self.AuxiliaryAlpha1.iloc[dateIndex,1:].abs().max()
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=(1.0/(2.0*AuxiliaryAlpha1Max))*self.AuxiliaryAlpha1.iloc[dateIndex,1:]
        Kpos1=np.where(self.AuxiliaryAlpha1.iloc[dateIndex,1:]>0)
        Kpos1=Kpos1[0]+1
        Kneg1=np.where(self.AuxiliaryAlpha1.iloc[dateIndex,1:]<0)
        Kneg1=Kneg1[0]+1
        self.AuxiliaryAlpha1.loc[dateIndex,Kpos1]=(0.5/self.AuxiliaryAlpha1.loc[dateIndex,Kpos1].max())*self.AuxiliaryAlpha1.loc[dateIndex,Kpos1]
        self.AuxiliaryAlpha1.loc[dateIndex,Kneg1]=(0.5/self.AuxiliaryAlpha1.loc[dateIndex,Kneg1].abs().max())*self.AuxiliaryAlpha1.loc[dateIndex,Kneg1]
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.AuxiliaryAlpha1.iloc[dateIndex,1:]+0.5
        #Auxiliary 2
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=(self.Close.iloc[dateIndex,1:]-self.Open.iloc[dateIndex,1:])/self.Open.iloc[dateIndex,1:]
        #Getting the Rank for AuxiliaryAlpha2:
        AuxiliaryAlpha2Max=self.AuxiliaryAlpha2.iloc[dateIndex,1:].abs().max()
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=(1.0/(2.0*AuxiliaryAlpha2Max))*self.AuxiliaryAlpha2.iloc[dateIndex,1:]
        Kpos=np.where(self.AuxiliaryAlpha2.iloc[dateIndex,1:]>0)
        Kpos=Kpos[0]+1
        Kneg=np.where(self.AuxiliaryAlpha2.iloc[dateIndex,1:]<0)
        Kneg=Kneg[0]+1
        self.AuxiliaryAlpha2.iloc[dateIndex,Kpos]=(0.5/self.AuxiliaryAlpha2.iloc[dateIndex,Kpos].max())*self.AuxiliaryAlpha2.iloc[dateIndex,Kpos]
        self.AuxiliaryAlpha2.iloc[dateIndex,Kneg]=(0.5/self.AuxiliaryAlpha2.iloc[dateIndex,Kneg].abs().max())*self.AuxiliaryAlpha2.iloc[dateIndex,Kneg]
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.AuxiliaryAlpha2.iloc[dateIndex,1:]+0.5
        self.dateIndex=dateIndex
         #Finding History of Auxiliary Alphas
        HistoryOfAuxiliaryAlpha1=self.AuxiliaryAlpha1.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        HistoryOfAuxiliaryAlpha2=self.AuxiliaryAlpha2.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        self.Value=0*self.AuxiliaryAlpha2.iloc[dateIndex,1:].copy()
        self.Value=-HistoryOfAuxiliaryAlpha1.corrwith(HistoryOfAuxiliaryAlpha2,axis=0)
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
    
class Alpha3Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Open.iloc[dateIndex,1:]
            #Getting the Rank for AuxiliaryAlpha1:
            AuxiliaryAlpha1Max=self.AuxiliaryAlpha1.iloc[dateIndex,1:].abs().max()
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=(1.0/(2.0*AuxiliaryAlpha1Max))*self.AuxiliaryAlpha1.iloc[dateIndex,1:]
            Kpos1=np.where(self.AuxiliaryAlpha1.iloc[dateIndex,1:]>0)
            Kpos1=Kpos1[0]+1
            Kneg1=np.where(self.AuxiliaryAlpha1.iloc[dateIndex,1:]<0)
            Kneg1=Kneg1[0]+1
            self.AuxiliaryAlpha1.iloc[dateIndex,Kpos1]=(0.5/self.AuxiliaryAlpha1.iloc[dateIndex,Kpos1].max())*self.AuxiliaryAlpha1.iloc[dateIndex,Kpos1]
            self.AuxiliaryAlpha1.iloc[dateIndex,Kneg1]=(0.5/self.AuxiliaryAlpha1.iloc[dateIndex,Kneg1].abs().max())*self.AuxiliaryAlpha1.iloc[dateIndex,Kneg1]
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.AuxiliaryAlpha1.iloc[dateIndex,1:]+0.5
            #Auxiliary 2
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Volume.iloc[dateIndex,1:]
            #Getting the Rank for AuxiliaryAlpha2:
            AuxiliaryAlpha2Max=self.AuxiliaryAlpha2.iloc[dateIndex,1:].abs().max()
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=(1.0/(2.0*AuxiliaryAlpha2Max))*self.AuxiliaryAlpha2.iloc[dateIndex,1:]
            Kpos=np.where(self.AuxiliaryAlpha2.iloc[dateIndex,1:]>0)
            Kpos=Kpos[0]+1
            Kneg=np.where(self.AuxiliaryAlpha2.iloc[dateIndex,1:]<0)
            Kneg=Kneg[0]+1
            self.AuxiliaryAlpha2.iloc[dateIndex,Kpos]=(0.5/self.AuxiliaryAlpha2.iloc[dateIndex,Kpos].max())*self.AuxiliaryAlpha2.iloc[dateIndex,Kpos]
            self.AuxiliaryAlpha2.iloc[dateIndex,Kneg]=(0.5/self.AuxiliaryAlpha2.iloc[dateIndex,Kneg].abs().max())*self.AuxiliaryAlpha2.iloc[dateIndex,Kneg]
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.AuxiliaryAlpha2.iloc[dateIndex,1:]+0.5
            

    def SetAlphaParameters(self,daysOfCorrelation,DaysOfLag):
        self.daysOfCorrelation=daysOfCorrelation
        self.DaysOfLag=DaysOfLag
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1 
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2 
        if( (self.daysOfCorrelation*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=self.daysOfCorrelation*self.TradingFrequency
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        
        #Auxiliary 1
        self.AuxiliaryAlpha1.iloc[dateIndex,:]=self.Open.iloc[dateIndex,:]
        #Getting the Rank for AuxiliaryAlpha1:
        AuxiliaryAlpha1Max=self.AuxiliaryAlpha1.iloc[dateIndex,1:].abs().max()
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=(1.0/(2.0*AuxiliaryAlpha1Max))*self.AuxiliaryAlpha1.iloc[dateIndex,1:]
        Kpos1=np.where(self.AuxiliaryAlpha1.iloc[dateIndex,1:]>0)
        Kpos1=Kpos1[0]+1
        Kneg1=np.where(self.AuxiliaryAlpha1.iloc[dateIndex,1:]<0)
        Kneg1=Kneg1[0]+1
        self.AuxiliaryAlpha1.iloc[dateIndex,Kpos1]=(0.5/self.AuxiliaryAlpha1.iloc[dateIndex,Kpos1].max())*self.AuxiliaryAlpha1.iloc[dateIndex,Kpos1]
        self.AuxiliaryAlpha1.iloc[dateIndex,Kneg1]=(0.5/self.AuxiliaryAlpha1.iloc[dateIndex,Kneg1].abs().max())*self.AuxiliaryAlpha1.iloc[dateIndex,Kneg1]
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.AuxiliaryAlpha1.iloc[dateIndex,1:]+0.5
        #Auxiliary 2
        self.AuxiliaryAlpha2.iloc[dateIndex,:]=self.Volume.iloc[dateIndex,:]
        #Getting the Rank for AuxiliaryAlpha2:
        AuxiliaryAlpha2Max=self.AuxiliaryAlpha2.iloc[dateIndex,1:].abs().max()
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=(1.0/(2.0*AuxiliaryAlpha2Max))*self.AuxiliaryAlpha2.iloc[dateIndex,1:]
        Kpos=np.where(self.AuxiliaryAlpha2.iloc[dateIndex,1:]>0)
        Kpos=Kpos[0]+1
        Kneg=np.where(self.AuxiliaryAlpha2.iloc[dateIndex,1:]<0)
        Kneg=Kneg[0]+1
        self.AuxiliaryAlpha2.iloc[dateIndex,Kpos]=(0.5/self.AuxiliaryAlpha2.iloc[dateIndex,Kpos].max())*self.AuxiliaryAlpha2.iloc[dateIndex,Kpos]
        self.AuxiliaryAlpha2.iloc[dateIndex,Kneg]=(0.5/self.AuxiliaryAlpha2.iloc[dateIndex,Kneg].abs().max())*self.AuxiliaryAlpha2.iloc[dateIndex,Kneg]
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.AuxiliaryAlpha2.iloc[dateIndex,1:]+0.5
        self.dateIndex=dateIndex
         #Finding History of Auxiliary Alphas
        HistoryOfAuxiliaryAlpha1=self.AuxiliaryAlpha1.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        HistoryOfAuxiliaryAlpha2=self.AuxiliaryAlpha2.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        self.Value=0*self.AuxiliaryAlpha2.iloc[dateIndex,1:].copy()
        self.Value= -HistoryOfAuxiliaryAlpha1.corrwith(HistoryOfAuxiliaryAlpha2,axis=0)
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
    
    
class Alpha4Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Low.iloc[dateIndex,1:]
            #Getting the Rank for AuxiliaryAlpha1:
            AuxiliaryAlpha1Max=self.AuxiliaryAlpha1.iloc[dateIndex,1:].abs().max()
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=(1.0/(2.0*AuxiliaryAlpha1Max))*self.AuxiliaryAlpha1.iloc[dateIndex,1:]
            Kpos1=np.where(self.AuxiliaryAlpha1.iloc[dateIndex,1:]>0)
            Kpos1=Kpos1[0]+1
            Kneg1=np.where(self.AuxiliaryAlpha1.iloc[dateIndex,1:]<0)
            Kneg1=Kneg1[0]+1
            self.AuxiliaryAlpha1.iloc[dateIndex,Kpos1]=(0.5/self.AuxiliaryAlpha1.iloc[dateIndex,Kpos1].max())*self.AuxiliaryAlpha1.iloc[dateIndex,Kpos1]
            self.AuxiliaryAlpha1.iloc[dateIndex,Kneg1]=(0.5/self.AuxiliaryAlpha1.iloc[dateIndex,Kneg1].abs().max())*self.AuxiliaryAlpha1.iloc[dateIndex,Kneg1]
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.AuxiliaryAlpha1.iloc[dateIndex,1:]+0.5
    def SetAlphaParameters(self,daysOfCorrelation,DaysOfLag):
        self.daysOfCorrelation=daysOfCorrelation
        self.DaysOfLag=DaysOfLag
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1 
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2 
        if( (self.daysOfCorrelation*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=self.daysOfCorrelation*self.TradingFrequency
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        #Auxiliary 1
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Low.iloc[dateIndex,1:]
        #Getting the Rank for AuxiliaryAlpha1:
        AuxiliaryAlpha1Max=self.AuxiliaryAlpha1.iloc[dateIndex,1:].abs().max()
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=(1.0/(2.0*AuxiliaryAlpha1Max))*self.AuxiliaryAlpha1.iloc[dateIndex,1:]
        Kpos1=np.where(self.AuxiliaryAlpha1.iloc[dateIndex,1:]>0)
        Kpos1=Kpos1[0]+1
        Kneg1=np.where(self.AuxiliaryAlpha1.iloc[dateIndex,1:]<0)
        Kneg1=Kneg1[0]+1
        self.AuxiliaryAlpha1.iloc[dateIndex,Kpos1]=(0.5/self.AuxiliaryAlpha1.iloc[dateIndex,Kpos1].max())*self.AuxiliaryAlpha1.iloc[dateIndex,Kpos1]
        self.AuxiliaryAlpha1.iloc[dateIndex,Kneg1]=(0.5/self.AuxiliaryAlpha1.iloc[dateIndex,Kneg1].abs().max())*self.AuxiliaryAlpha1.iloc[dateIndex,Kneg1]
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.AuxiliaryAlpha1.iloc[dateIndex,1:]+0.5
        self.dateIndex=dateIndex
         #Finding History of Auxiliary Alphas
        HistoryOfAuxiliaryAlpha1=self.AuxiliaryAlpha1.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        #Finding -TS Rank
        self.Value=-((HistoryOfAuxiliaryAlpha1.iloc[-1,:]/(2*HistoryOfAuxiliaryAlpha1.abs().max()))+0.5)
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
    
class Alpha6Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Open.iloc[dateIndex,1:]
            
            #Auxiliary 2
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Volume.iloc[dateIndex,1:]          
            

    def SetAlphaParameters(self,daysOfCorrelation,DaysOfLag):
        self.daysOfCorrelation=daysOfCorrelation
        self.DaysOfLag=DaysOfLag
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1 
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2 
        if( (self.daysOfCorrelation*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=self.daysOfCorrelation*self.TradingFrequency
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        #Auxiliary 1
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Open.iloc[dateIndex,1:]            
        #Auxiliary 2
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Volume.iloc[dateIndex,1:]
        self.dateIndex=dateIndex
         #Finding History of Auxiliary Alphas
        HistoryOfAuxiliaryAlpha1=self.AuxiliaryAlpha1.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        HistoryOfAuxiliaryAlpha2=self.AuxiliaryAlpha2.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        self.Value=0*self.AuxiliaryAlpha2.iloc[dateIndex,1:].copy()
        self.Value= -HistoryOfAuxiliaryAlpha1.corrwith(HistoryOfAuxiliaryAlpha2,axis=0)
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
        
class Alpha7Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.DaysOfLag,self.startDate):
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]-self.Close.iloc[dateIndex-self.DaysOfLag,1:]
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.AuxiliaryAlpha1.iloc[dateIndex,1:].apply(np.sign)
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.AuxiliaryAlpha1.iloc[dateIndex,1:].apply(np.abs)
           
    def SetAlphaParameters(self,daysOfTSRank,DaysOfLag,DaysOfVolume):
        self.daysOfTSRank=daysOfTSRank
        self.DaysOfLag=DaysOfLag
        self.DaysOfVolume=DaysOfVolume
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1 
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2         
        if( (self.daysOfTSRank*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=self.daysOfTSRank*self.TradingFrequency
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        #Auxiliary 1
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]-self.Close.iloc[dateIndex-self.DaysOfLag,1:]
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.AuxiliaryAlpha1.iloc[dateIndex,1:].apply(np.sign)
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.AuxiliaryAlpha1.iloc[dateIndex,1:].apply(np.abs)
        HistoryOfAuxiliaryAlpha1=self.AuxiliaryAlpha1.iloc[slice(self.dateIndex-self.daysOfTSRank*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        Value1=(-((HistoryOfAuxiliaryAlpha1.iloc[-1,:]/(2*HistoryOfAuxiliaryAlpha1.abs().max()))+0.5))*self.AuxiliaryAlpha2.iloc[-1,1:]
        ADV=self.Volume.iloc[slice(self.dateIndex-self.DaysOfVolume*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:].mean()
        Difference=ADV-self.Volume.iloc[self.dateIndex,1:]
        IndexPos=np.where(Difference>=0)
        IndexPos=IndexPos[0]
        ##print(IndexPos)
        IndexNeg=np.where(Difference<0)
        IndexNeg=IndexNeg[0]
        self.Value=0*self.AuxiliaryAlpha2.iloc[dateIndex,1:].copy()
        self.Value.iloc[IndexPos]=-1
        self.Value.iloc[IndexNeg]=Value1.iloc[IndexNeg]
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha8Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfSum,self.startDate):
            self.dateIndex=dateIndex
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Open.iloc[slice(self.dateIndex-self.daysOfSum*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:].sum()
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.TheAlphaReturns.iloc[slice(self.dateIndex-self.daysOfSum*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:].sum()
            
           
    def SetAlphaParameters(self,daysOfSum,DaysOfDelay):
        self.daysOfSum=daysOfSum
        self.DaysOfDelay=DaysOfDelay
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1 
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2
        if( ( (self.daysOfSum+self.DaysOfDelay)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfSum+self.DaysOfDelay)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Open.iloc[slice(self.dateIndex-self.daysOfSum*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:].sum()
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.TheAlphaReturns.iloc[slice(self.dateIndex-self.daysOfSum*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:].sum()
        AuxValue1=self.AuxiliaryAlpha1.iloc[dateIndex,1:].shift(self.DaysOfDelay)
        AuxValue2=self.AuxiliaryAlpha2.iloc[dateIndex,1:].shift(self.DaysOfDelay)
        self.Value=self.AuxiliaryAlpha1.iloc[dateIndex,1:]*self.AuxiliaryAlpha2.iloc[dateIndex,1:]-AuxValue1*AuxValue2
        self.Value=-self.Rank(self.Value)
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
    
class Alpha9And10Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.DaysOfLag,self.startDate):
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]-self.Close.iloc[dateIndex-self.DaysOfLag*self.TradingFrequency,1:]
    def SetAlphaParameters(self,daysOfTS,DaysOfLag): 
        self.daysOfTS=daysOfTS
        self.DaysOfLag=DaysOfLag
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1         
        if( ( (self.daysOfTS+self.DaysOfLag)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfTS+self.DaysOfLag)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]-self.Close.iloc[dateIndex-self.DaysOfLag*self.TradingFrequency,1:]
        AuxiliaryAlpha1History=self.AuxiliaryAlpha1.iloc[slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        TSMin=AuxiliaryAlpha1History.min()
        TSMax=AuxiliaryAlpha1History.max()
        #Initially all the values to Delta Close
        self.Value=self.AuxiliaryAlpha1.iloc[dateIndex,1:].copy()
        #TSMinPos=np.where(TSMin>0)
        TSMinNeg=np.where(TSMin<0)
        #TSMaxPos=np.where(TSMax>0)
        TSMaxNeg=np.where(TSMax<0)
        #All the values that TSMin is neg negative
        self.Value.loc[TSMinNeg]=-self.Value.loc[TSMinNeg]
        #All the values that TSMAx negative(obviously TSMin neg as well) negative(negative of negative positive)
        self.Value.loc[TSMaxNeg]=-self.Value.loc[TSMinNeg]
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
        
class Alpha12Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.DaysOfLag,self.startDate):
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Volume.iloc[dateIndex,1:]-self.Volume.iloc[dateIndex-self.DaysOfLag,1:]
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]-self.Close.iloc[dateIndex-self.DaysOfLag,1:]
    def SetAlphaParameters(self,DaysOfLag): 
        
        self.DaysOfLag=DaysOfLag
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1   
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2  
        if( ( (self.DaysOfLag)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.DaysOfLag)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.Value=(self.AuxiliaryAlpha1.iloc[dateIndex,1:].apply(np.sign))*(-self.AuxiliaryAlpha1.iloc[dateIndex,1:])
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha13Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Rank(self.Close.iloc[dateIndex,1:])            
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Rank(self.Volume.iloc[dateIndex,1:])
    def SetAlphaParameters(self,daysOfCovariance): 
        self.daysOfCovariance=daysOfCovariance
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1   
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2   
        if( ( (self.daysOfCovariance)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfCovariance)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Rank(self.Close.iloc[dateIndex,1:])            
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Rank(self.Volume.iloc[dateIndex,1:])
        #
        HistoryAuxiliaryAlpha1=self.AuxiliaryAlpha1.iloc[slice(self.dateIndex-self.daysOfCovariance*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        HistoryAuxiliaryAlpha2=self.AuxiliaryAlpha2.iloc[slice(self.dateIndex-self.daysOfCovariance*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        self.Value=0*self.AuxiliaryAlpha2.iloc[dateIndex,1:].copy()
        self.Value= -HistoryAuxiliaryAlpha1.corrwith(HistoryAuxiliaryAlpha2,axis=0)
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
#slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency)
class Alpha14Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.DaysOfLag,self.startDate*self.TradingFrequency):
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.TheAlphaReturns.iloc[dateIndex,1:]-self.TheAlphaReturns.iloc[dateIndex-self.DaysOfLag,1:]
    def SetAlphaParameters(self,daysOfTS,DaysOfLag): 
        self.daysOfTS=daysOfTS
        self.DaysOfLag=DaysOfLag
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1         
        if( ( (self.daysOfTS+self.DaysOfLag)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfTS+self.DaysOfLag)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.TheAlphaReturns.iloc[dateIndex,1:]-self.TheAlphaReturns.iloc[dateIndex-self.DaysOfLag,1:]
        
        AuxiliaryAlpha2HistoryA=self.Open.iloc[slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        AuxiliaryAlpha2HistoryB=self.Volume.iloc[slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        self.Value=0*self.AuxiliaryAlpha1.iloc[dateIndex,1:].copy()
        
        
        self.Value= AuxiliaryAlpha2HistoryA.corrwith(AuxiliaryAlpha2HistoryB,axis=0)
        self.Value=-self.Rank(self.AuxiliaryAlpha1.iloc[dateIndex,1:])*self.Value
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
#slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency)
class Alpha15Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            self.dateIndex=dateIndex
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Rank(self.High.iloc[dateIndex,1:])
            #Auxiliary 2
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Rank(self.Volume.iloc[dateIndex,1:])
            # Rank of Correlation
            if(dateIndex>=self.daysOfCorrelation*self.TradingFrequency):
                HistoryAuxiliary1=self.AuxiliaryAlpha1.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
                HistoryAuxiliary2=self.AuxiliaryAlpha2.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
                
                self.AuxiliaryAlpha3.iloc[dateIndex,1:]= (HistoryAuxiliary1.corrwith(HistoryAuxiliary2,axis=0))
                self.AuxiliaryAlpha3.iloc[dateIndex,1:]=self.Rank(self.AuxiliaryAlpha3.iloc[dateIndex,1:])
    def SetAlphaParameters(self,daysOfCorrelation,DaysOfSum): 
        self.daysOfCorrelation=daysOfCorrelation
        self.DaysOfSum=DaysOfSum
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1 
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2   
        self.AuxiliaryAlpha3=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha3=0*self.AuxiliaryAlpha3   
        if( ( (self.daysOfCorrelation+self.DaysOfSum)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.DaysOfSum+self.daysOfCorrelation)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        #Auxiliary 1
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Rank(self.High.iloc[dateIndex,1:])
        #Auxiliary 2
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Rank(self.Volume.iloc[dateIndex,1:])
        HistoryAuxiliary1=self.AuxiliaryAlpha1.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        HistoryAuxiliary2=self.AuxiliaryAlpha2.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        # Rank of Correlation
        
        self.AuxiliaryAlpha3.iloc[dateIndex,1:]= (HistoryAuxiliary1.corrwith(HistoryAuxiliary2,axis=0))
        self.AuxiliaryAlpha3.iloc[dateIndex,1:]=self.Rank(self.AuxiliaryAlpha3.iloc[dateIndex,1:])
        
        HistoryAuxiliary3=self.AuxiliaryAlpha3.iloc[slice(self.dateIndex-self.DaysOfSum*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        self.Value=-HistoryAuxiliary3.sum()
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
    
#slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency)
class Alpha16Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Rank(self.High.iloc[dateIndex,1:])
            #Auxiliary 2
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Rank(self.Volume.iloc[dateIndex,1:])
            
    def SetAlphaParameters(self,daysOfCovariance): 
        self.daysOfCovariance=daysOfCovariance
        
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1   
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2 
        if( ( (self.daysOfCovariance)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfCovariance)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        #Auxiliary 1
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Rank(self.High.iloc[dateIndex,1:])
        #Auxiliary 2
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Rank(self.Volume.iloc[dateIndex,1:])
        
        HistoryAuxiliaryAlpha1=self.AuxiliaryAlpha1.iloc[slice(self.dateIndex-self.daysOfCovariance*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        HistoryAuxiliaryAlpha2=self.AuxiliaryAlpha2.iloc[slice(self.dateIndex-self.daysOfCovariance*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        
        self.Value=0*self.AuxiliaryAlpha2.iloc[dateIndex,1:].copy()
        
        self.Value= HistoryAuxiliaryAlpha1.corrwith(HistoryAuxiliaryAlpha2,axis=0)
        self.Value=-self.Rank(self.Value)    
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
#slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency)
class Alpha17Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.DaysOfLag,self.startDate):
            self.dateIndex=dateIndex
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]-self.Close.iloc[dateIndex-self.DaysOfLag,1:]            
            
            if(dateIndex>self.DaysOfADV):
                ADV20=self.AuxiliaryAlpha3.iloc[slice(dateIndex-self.DaysOfADV*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:].mean()
                self.AuxiliaryAlpha3.iloc[dateIndex,1:]=self.Volume.iloc[dateIndex,1:]/ADV20
                
    def SetAlphaParameters(self,daysOfTSRank1,daysOfTSRank2,DaysOfLag,DaysOfADV): 
        self.daysOfTSRank1=daysOfTSRank1
        self.daysOfTSRank2=daysOfTSRank2
        self.DaysOfLag=DaysOfLag
        self.DaysOfADV=DaysOfADV
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1  
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2
        self.AuxiliaryAlpha3=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha3=0*self.AuxiliaryAlpha3
        if( ( (self.DaysOfADV+self.daysOfTSRank2)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.DaysOfADV+self.daysOfTSRank2)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]-self.Close.iloc[dateIndex-self.DaysOfLag,1:]
        ADV20=self.Volume.iloc[slice(self.dateIndex-self.DaysOfADV*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:].mean()
        self.AuxiliaryAlpha3.iloc[dateIndex,1:]=self.Volume.iloc[dateIndex,1:]/ADV20
                
        AuxiliaryAlpha1History=self.AuxiliaryAlpha1.iloc[slice(self.dateIndex-self.daysOfTSRank1*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:] 
        TSRankAlpha1=self.TSRank(AuxiliaryAlpha1History)
        RankTSRankAlpha1=self.Rank(TSRankAlpha1)
        RankAuxiliaryAlpha2=self.Rank(self.AuxiliaryAlpha2.iloc[dateIndex,1:])
        AuxiliaryAlpha3History=self.AuxiliaryAlpha3.iloc[slice(self.dateIndex-self.daysOfTSRank2*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        RankTSRankAlpha3=self.Rank(self.TSRank(AuxiliaryAlpha3History))
        self.Value=(RankTSRankAlpha1*RankAuxiliaryAlpha2)*RankTSRankAlpha3
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
#slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency)
class Alpha18Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]-self.Open.iloc[dateIndex,1:]
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.AuxiliaryAlpha1.iloc[dateIndex,1:].abs()
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]-self.Open.iloc[dateIndex,1:]
    def SetAlphaParameters(self,daysOfTS,DaysOfCorrelation): 
        self.daysOfTS=daysOfTS
        self.DaysOfCorrelation=DaysOfCorrelation
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1  
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2 
        if( ( (self.daysOfTS+self.DaysOfCorrelation)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfTS+self.DaysOfCorrelation)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]-self.Open.iloc[dateIndex,1:]
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.AuxiliaryAlpha1.iloc[dateIndex,1:].abs()
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]-self.Open.iloc[dateIndex,1:]
        
        HistoryAuxiliaryAlpha1=self.AuxiliaryAlpha1.iloc[slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        
        HistoryOpen=self.Open.iloc[slice(self.dateIndex-self.DaysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        HistoryClose=self.Close.iloc[slice(self.dateIndex-self.DaysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        self.Value=0*self.AuxiliaryAlpha2.iloc[dateIndex,1:].copy()
        
        self.Value= HistoryOpen.corrwith(HistoryClose,axis=0)
        self.Value=self.Value+self.AuxiliaryAlpha2.iloc[dateIndex,1:]+HistoryAuxiliaryAlpha1.std()
        self.Value=-self.Rank(self.Value)
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
#slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency)
class Alpha19Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]-self.Close.iloc[dateIndex-self.daysOfLag1,1:]
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Close.iloc[dateIndex-self.daysOfLag1,1:]
            
    def SetAlphaParameters(self,daysOfLag1,daysOfReturns): 
        self.daysOfLag1=daysOfLag1
        self.daysOfReturns=daysOfReturns
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2          
        if( ( (self.daysOfReturns)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfReturns)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Close.iloc[dateIndex,1:]-self.Close.iloc[dateIndex-self.daysOfLag1,1:]
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Close.iloc[dateIndex-self.daysOfLag1,1:]
        HistoryReturns=self.TheAlphaReturns.iloc[slice(self.dateIndex-self.daysOfReturns*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        RankSumHistoryOfReturns=1+self.Rank(1+HistoryReturns.sum())
        Part1=self.Close.iloc[dateIndex,1:]-self.AuxiliaryAlpha2.iloc[dateIndex,1:]+self.AuxiliaryAlpha1.iloc[dateIndex,1:]
        Part1=-Part1.apply(np.sign)
        self.Value=Part1*RankSumHistoryOfReturns
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha20Zura(Alpha):
    def SetAlphaParameters(self,DaysOfLag):            
        self.DaysOfLag=DaysOfLag
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()            
        self.startDate=self.DaysOfLag
            
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.Value=-self.Rank(self.Open.iloc[dateIndex,1:]-self.High.iloc[dateIndex-self.DaysOfLag,1:])
        self.Value=self.Value*self.Rank(self.Open.iloc[dateIndex,1:]-self.Close.iloc[dateIndex-self.DaysOfLag,1:])
        self.Value=self.Value*self.Rank(self.Open.iloc[dateIndex,1:]-self.Low.iloc[dateIndex-self.DaysOfLag,1:])
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha21Zura(Alpha):
    def SetAlphaParameters(self,DaysOfLag1,DaysOfLag2,DaysOfVolume,mul1,mul2):            
            self.DaysOfLag1=DaysOfLag1
            self.DaysOfLag2=DaysOfLag2
            self.DaysOfVolume=DaysOfVolume
            self.mul1=mul1
            self.mul2=mul2
            self.TheAlphaReturns=self.ProcessData.Returns
            self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()            
            self.startDate=self.DaysOfVolume
            
    def GenerateAlpha(self,dateIndex, TotalAvailable):
            self.dateIndex=dateIndex
            HistoryClose1=self.Close.iloc[slice(self.dateIndex-self.DaysOfLag1*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
            HistoryClose2=self.Close.iloc[slice(self.dateIndex-self.DaysOfLag2*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
            HistoryVolume=self.Volume.iloc[slice(self.dateIndex-self.DaysOfVolume*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
            ADV=HistoryVolume.mean()
            self.Value=0*self.Close.iloc[dateIndex,1:].copy()
            AuxValue1=(self.mul1)*HistoryClose1.sum()+HistoryClose1.std()-(self.mul2)*HistoryClose2.sum()            
            self.Value.loc[AuxValue1<0]=-1
            AuxValue2=(self.mul2)*HistoryClose2.sum()+HistoryClose1.std()-(self.mul1)*HistoryClose1.sum()
            self.Value.loc[(AuxValue1>0)&(AuxValue2<0)]=1            
            AuxValue3=self.Volume.iloc[self.dateIndex,1:]/ADV
            self.Value.loc[(AuxValue1>0)&(AuxValue2>0)&(AuxValue3>=1)]=1
            self.Value.loc[(AuxValue1>0)&(AuxValue2>0)&(AuxValue3<1)]=-1
            self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
            # self.IndNeut2()
            # self.IndSector2()
            return self.Value
        
        
#slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency)
class Alpha22Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfLag,self.startDate):
            self.dateIndex=dateIndex
            #Auxiliary 1
            HistoryHigh=self.High.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
            HistoryVolume=self.Volume.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
            
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]= HistoryHigh.corrwith(HistoryVolume,axis=0)
    def SetAlphaParameters(self,daysOfCorrelation,daysOfStD,daysOfLag): 
        self.daysOfCorrelation=daysOfCorrelation
        self.daysOfStD=daysOfStD
        self.daysOfLag=daysOfLag
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2         
        if( ( (self.daysOfStD)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfStD)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        HistoryHigh=self.High.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        HistoryVolume=self.Volume.iloc[slice(self.dateIndex-self.daysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]= HistoryHigh.corrwith(HistoryVolume,axis=0)
        HistoryClose=self.Close.iloc[slice(self.dateIndex-self.daysOfStD*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        RankStDHistoryClose=self.Rank(HistoryClose.std())
        DeltaCorr=self.AuxiliaryAlpha1.iloc[dateIndex,1:]-self.AuxiliaryAlpha1.iloc[dateIndex-self.daysOfLag,1:]
        self.Value=RankStDHistoryClose*DeltaCorr
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value

#slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency)
class Alpha23Zura(Alpha):
    
    def SetAlphaParameters(self,daysOfTS,DaysOfLag): 
        self.daysOfTS=daysOfTS
        self.DaysOfLag=DaysOfLag
        self.TheAlphaReturns=self.ProcessData.Returns              
        if( ( (self.daysOfTS)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfTS)*self.TradingFrequency)
        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        Value1=self.High.iloc[slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:].mean()-self.High.iloc[self.dateIndex,1:]
        self.Value=0*self.Close.iloc[dateIndex,1:].copy()
        Difference=self.High.iloc[self.dateIndex,1:]-self.High.iloc[self.dateIndex-self.DaysOfLag,1:]
        self.Value.loc[Value1<0]=Difference.loc[Value1<0]
        self.Value.loc[Value1>=0]=0
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha24Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfTS,self.startDate):
            #Auxiliary 1            
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]= self.Close.iloc[slice(dateIndex-self.daysOfTS*self.TradingFrequency,dateIndex,self.TradingFrequency),1:].mean()

    
    def SetAlphaParameters(self,daysOfTS,DaysOfLag): 
        self.daysOfTS=daysOfTS
        self.DaysOfLag=DaysOfLag
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1         
        if( ( (self.daysOfTS)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=2*( (self.daysOfTS)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=  self.Close.iloc[slice(dateIndex-self.daysOfTS*self.TradingFrequency,dateIndex,self.TradingFrequency),1:].mean()
        AuxAlpha1=self.AuxiliaryAlpha1.iloc[dateIndex,1:]-self.AuxiliaryAlpha1.iloc[dateIndex-self.daysOfTS*self.TradingFrequency,1:]
        AuxAlpha2=self.Close.iloc[self.dateIndex-self.daysOfTS*self.TradingFrequency,1:]
        AuxAlpha3=AuxAlpha1/AuxAlpha2
        AuxAlpha4=-(self.Close.iloc[self.dateIndex,1:]-self.Close.iloc[slice(dateIndex-self.daysOfTS*self.TradingFrequency,dateIndex,self.TradingFrequency),1:].min())
        AuxAlpha5=-(self.Close.iloc[self.dateIndex,1:]-self.Close.iloc[self.dateIndex-self.DaysOfLag,1:] )
        self.Value=0*self.Close.iloc[dateIndex,1:].copy()
        self.Value.loc[AuxAlpha3<=0.05]=AuxAlpha4.loc[AuxAlpha3<=0.05]
        self.Value.loc[AuxAlpha3>0.05]=AuxAlpha5.loc[AuxAlpha3>0.05]
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
    


class Alpha26Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfTS,self.startDate):
            self.dateIndex=dateIndex
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.TSRank(self.Volume.iloc[slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:])
            self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.TSRank(self.High.iloc[slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:])
            if(dateIndex>=2*self.daysOfTS):                
                self.AuxiliaryAlpha3= self.AuxiliaryAlpha1.corrwith(self.AuxiliaryAlpha2,axis=0)              
                
            
    def SetAlphaParameters(self,daysOfTS,DaysOfCorrelation,daysOfTSMax): 
        self.daysOfTS=daysOfTS
        self.DaysOfCorrelation=DaysOfCorrelation
        self.daysOfTSMax=daysOfTSMax
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1 
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2 
        self.AuxiliaryAlpha3=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha3=0*self.AuxiliaryAlpha3             
        if( ( (self.daysOfTS+self.DaysOfCorrelation+self.daysOfTSMax)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfTS+self.DaysOfCorrelation+self.daysOfTSMax)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.TSRank(self.Volume.iloc[slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:])
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.TSRank(self.High.iloc[slice(self.dateIndex-self.daysOfTS*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:])
        if(dateIndex>=2*self.daysOfTS):            
            self.AuxiliaryAlpha3= self.AuxiliaryAlpha1.corrwith(self.AuxiliaryAlpha2,axis=0)
        self.Value=-self.AuxiliaryAlpha3.iloc[dateIndex,1:]
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha28Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfADV,self.startDate):
            self.dateIndex=dateIndex
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Volume.iloc[slice(self.dateIndex-self.daysOfADV*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:].mean()
            
    def SetAlphaParameters(self,daysOfADV,DaysOfCorrelation): 
        self.daysOfADV=daysOfADV
        self.DaysOfCorrelation=DaysOfCorrelation
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1 
              
        if( ( (self.daysOfADV+self.DaysOfCorrelation)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfADV+self.DaysOfCorrelation)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.Value=0*self.AuxiliaryAlpha1.iloc[dateIndex,1:].copy()
        
        HistoryAuxiliaryAlpha1=self.AuxiliaryAlpha1.iloc[slice(self.dateIndex-self.DaysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        HistoryLow=self.Low.iloc[slice(self.dateIndex-self.DaysOfCorrelation*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:]
        
        
        self.Value= HistoryAuxiliaryAlpha1.corrwith(HistoryLow,axis=0)
        self.Value=self.Value+0.5*self.High.iloc[dateIndex,1:]+0.5*self.Low.iloc[dateIndex,1:]-self.Close.iloc[dateIndex,1:]
        SumValues=self.Value.abs().sum()
        if(SumValues==0):
            pass
        else:
            self.Value=(1.0/SumValues)*self.Value
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha29Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfLag,self.startDate):
            self.dateIndex=dateIndex
            #Auxiliary 1
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Rank(-self.Rank(self.Delta(self.Close,self.daysOfLag)))
            if(dateIndex>self.daysOfdelay):
                self.AuxiliaryAlpha7.iloc[dateIndex,1:]=-self.TheAlphaReturns.iloc[dateIndex-self.daysOfdelay,1:]
                
            if(dateIndex>=self.daysOfLag+self.daysOfTSmin):
                self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.TSMin(self.AuxiliaryAlpha1,self.daysOfTSmin)
            if(dateIndex>=self.daysOfLag+self.daysOfTSmin+self.daysOfSum):
                self.AuxiliaryAlpha3.iloc[dateIndex,1:]=self.TSSum(self.AuxiliaryAlpha2,self.daysOfSum)
                self.AuxiliaryAlpha4.iloc[dateIndex,1:]=self.Rank(self.Rank(self.Scale(self.Log(self.AuxiliaryAlpha3.iloc[dateIndex,1:]))))
            if(dateIndex>=self.daysOfLag+self.daysOfTSmin+self.daysOfSum+self.daysOfProd):
                self.AuxiliaryAlpha5.iloc[dateIndex,1:]=self.TSProd(self.AuxiliaryAlpha4,self.daysOfProd)
                
                
    def SetAlphaParameters(self,daysOfLag,daysOfTSmin,daysOfSum,daysOfProd,daysOfTsMin2,daysOfdelay,daysOfTSRank): 
        self.daysOfLag=daysOfLag
        self.daysOfTSmin=daysOfTSmin
        self.daysOfSum=daysOfSum
        self.daysOfProd=daysOfProd
        self.daysOfTsMin2=daysOfTsMin2
        self.daysOfdelay=daysOfdelay
        self.daysOfTSRank=daysOfTSRank
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1 
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2   
        self.AuxiliaryAlpha3=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha3=0*self.AuxiliaryAlpha3 
        self.AuxiliaryAlpha4=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha4=0*self.AuxiliaryAlpha4 
        self.AuxiliaryAlpha5=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha5=0*self.AuxiliaryAlpha5
        self.AuxiliaryAlpha6=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha6=0*self.AuxiliaryAlpha6
        self.AuxiliaryAlpha7=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha7=0*self.AuxiliaryAlpha7
        
        if( ( (self.daysOfLag+self.daysOfTSmin+self.daysOfSum+self.daysOfProd+self.daysOfTsMin2)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfLag+self.daysOfTSmin+self.daysOfSum+self.daysOfProd+self.daysOfTsMin2)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Rank(-self.Rank(self.Delta(self.Close,self.daysOfdelay)))        
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.TSMin(self.AuxiliaryAlpha1,self.daysOfTSmin)        
        self.AuxiliaryAlpha3.iloc[dateIndex,1:]=self.TSSum(self.AuxiliaryAlpha2,self.daysOfSum)
        self.AuxiliaryAlpha4.iloc[dateIndex,1:]=self.Rank(self.Rank(self.Scale(self.Log(self.AuxiliaryAlpha3.iloc[dateIndex,1:]))))       
        self.AuxiliaryAlpha5.iloc[dateIndex,1:]=self.TSProd(self.AuxiliaryAlpha4,self.daysOfProd)
        self.AuxiliaryAlpha6.iloc[dateIndex,1:]=self.TSMin(self.AuxiliaryAlpha5,self.daysOfTsMin2)
        
        AuxiliaryAlpha7History=self.AuxiliaryAlpha7.iloc[slice(self.dateIndex-self.daysOfTSRank*self.TradingFrequency,self.dateIndex,self.TradingFrequency),1:] 
        TSRankAlpha7=self.TSRank(AuxiliaryAlpha7History)
        self.Value=self.AuxiliaryAlpha6.iloc[dateIndex,1:]+TSRankAlpha7
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    

class Alpha30Zura(Alpha):
    #def GenerateAuxiliaryAlpha(self):
    def SetAlphaParameters(self,DaysOfLag1,DaysOfLag2,DaysOfLag3,DaysOfLag4,DaysOfLag5,daysADV1,daysADV2): 
            self.DaysOfLag1=DaysOfLag1
            self.DaysOfLag2=DaysOfLag2
            self.DaysOfLag3=DaysOfLag3
            self.DaysOfLag4=DaysOfLag4
            self.DaysOfLag5=DaysOfLag5
            self.daysADV1=daysADV1
            self.daysADV2=daysADV2
            self.TheAlphaReturns=self.ProcessData.Returns
            self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
            self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1         
            if( ( (self.daysADV2)*self.TradingFrequency)<=self.startDate):
                pass
            else:
                self.startDate=( (self.daysADV2)*self.TradingFrequency)
        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        Value1=self.Sign(self.Close.iloc[dateIndex,1:]-self.Close.iloc[dateIndex-self.DaysOfLag1,1:])
        Value2=self.Sign(self.Close.iloc[dateIndex-self.DaysOfLag2,1:]-self.Close.iloc[dateIndex-self.DaysOfLag3,1:])
        Value3=self.Sign(self.Close.iloc[dateIndex-self.DaysOfLag4,1:]-self.Close.iloc[dateIndex-self.DaysOfLag5,1:])
        
        self.Value=(1.0-self.Rank(Value1+Value2+Value3))*(self.TSSum(self.Volume,self.daysADV1)/self.TSSum(self.Volume,self.daysADV2))
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    


class Alpha31Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfADV,self.startDate):
            #Auxiliary 1
            self.dateIndex=dateIndex
            self.ADV.iloc[dateIndex,1:]=self.TSMean(self.Volume,self.daysOfADV)
            if(dateIndex>=self.daysOfADV+self.daysOfCorrelation):
                self.Aux1.iloc[dateIndex,1:]=self.Sign(self.Scale(self.Correl(self.ADV,self.Low,self.daysOfCorrelation)))
            if(dateIndex>=self.daysOfADV+self.daysOfLag1):
                self.Aux2.iloc[dateIndex,1:]=self.Rank(-self.Delta(self.Close,self.daysOfLag1))
            if(dateIndex>=self.daysOfADV+self.daysOfLag2):
                self.Aux3.iloc[dateIndex,1:]=-self.Rank(self.Rank(self.Delta(self.Close,self.daysOfLag2)))
                
                
                
    
    def SetAlphaParameters(self,daysOfADV,daysOfCorrelation,daysOfLag1,daysOfLag2,daysOfLinearDecay): 
        self.daysOfADV=daysOfADV
        self.daysOfCorrelation=daysOfCorrelation
        self.daysOfLag1=daysOfLag1
        self.daysOfLag2=daysOfLag2
        self.daysOfLinearDecay=daysOfLinearDecay
        self.TheAlphaReturns=self.ProcessData.Returns
        self.ADV=self.TheAlphaReturns.copy()
        self.ADV=0*self.ADV  
        self.Aux1=self.TheAlphaReturns.copy()
        self.Aux1=0*self.Aux1 
        self.Aux2=self.TheAlphaReturns.copy()
        self.Aux2=0*self.Aux2
        self.Aux3=self.TheAlphaReturns.copy()
        self.Aux3=0*self.Aux3
        
        if( ( (daysOfADV+daysOfCorrelation+daysOfLag1+daysOfLag2+self.daysOfLinearDecay)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (daysOfADV+daysOfCorrelation+daysOfLag1+daysOfLag2+self.daysOfLinearDecay)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.ADV.iloc[dateIndex,1:]=self.TSMean(self.Volume,self.daysOfADV)
        self.Aux1.iloc[dateIndex,1:]=self.Sign(self.Scale(self.Correl(self.ADV,self.Low,self.daysOfCorrelation)))
        self.Aux2.iloc[dateIndex,1:]=self.Rank(-self.Delta(self.Close,self.daysOfLag1))
        self.Aux3.iloc[dateIndex,1:]=-self.Rank(self.Rank(self.Delta(self.Close,self.daysOfLag2)))
        self.Aux4=self.Rank(self.Rank(self.Rank(self.TSLinearDecay( self.Aux3 ,self.daysOfLinearDecay))))
        self.Value=self.Aux1.iloc[dateIndex,1:]+self.Aux2.iloc[dateIndex,1:]+self.Aux4
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
    
class Alpha33Zura(Alpha):   
    def SetAlphaParameters(self):
        self.TheAlphaReturns=self.ProcessData.Returns
        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.Value=self.Rank(-(1-(self.Open.iloc[self.dateIndex,1:]/self.Close.iloc[self.dateIndex,1:])))
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    

class Alpha34Zura(Alpha):
    def SetAlphaParameters(self,daysOfstd1,daysOfstd2,DaysOfLag): 
        self.daysOfstd1=daysOfstd1
        self.daysOfstd2=daysOfstd2
        self.DaysOfLag=DaysOfLag
        self.TheAlphaReturns=self.ProcessData.Returns
               
        if( ( (self.daysOfstd2)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfstd2)*self.TradingFrequency)
        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.Value=self.Rank((1.0-self.Rank( (self.TSSTD(self.TheAlphaReturns,self.daysOfstd1)/self.TSSTD(self.TheAlphaReturns,self.daysOfstd2)) ))+(1.0-self.Rank(self.Delta(self.Close,self.DaysOfLag))) )
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha35Zura(Alpha):
    def SetAlphaParameters(self,daysOfTSRank1,daysOfTSRank2,daysOfTSRank3): 
        self.daysOfTSRank1=daysOfTSRank1
        self.daysOfTSRank2=daysOfTSRank2
        self.daysOfTSRank3=daysOfTSRank3
        self.TheAlphaReturns=self.ProcessData.Returns
        self.Sum=0*self.Close.copy()
        self.Sum.iloc[:,1:]=self.Close.iloc[:,1:]+self.High.iloc[:,1:]-self.Low.iloc[:,1:]
               
        if( ( (self.daysOfTSRank1)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfTSRank1)*self.TradingFrequency)
        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.Value=self.TSRank(self.History(self.daysOfTSRank1,self.Volume))
        self.Value=self.Value*(1.0-  self.TSRank(self.History(self.daysOfTSRank2,self.Sum)) )
        self.Value=self.Value*(1.0-  self.TSRank(self.History(self.daysOfTSRank3,self.TheAlphaReturns)) )
          
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha37Zura(Alpha):
    def SetAlphaParameters(self,daysOfCorrelation,daysOfDelay):         
        self.daysOfCorrelation=daysOfCorrelation
        self.daysOfDelay=daysOfDelay
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1
        self.Difference=0*self.Open.copy()
        self.Difference.iloc[:,1:]=self.Open.iloc[:,1:].shift(1)-self.Close.iloc[:,1:].shift(1)        
        if( ( (self.daysOfCorrelation+self.daysOfDelay)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfCorrelation+self.daysOfDelay)*self.TradingFrequency)
    
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        
        self.Value=self.Rank(self.Correl(self.Difference,self.Close,self.daysOfCorrelation))+self.Rank(self.Open.iloc[self.dateIndex,1:]-self.Close.iloc[self.dateIndex,1:])
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha38Zura(Alpha):
    def SetAlphaParameters(self,daysOfTSRank):         
        self.daysOfTSRank=daysOfTSRank        
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1         
        if( ( (self.daysOfTSRank)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfTSRank)*self.TradingFrequency)
        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.Value=self.Rank(self.TSRank(self.History(self.daysOfTSRank,self.Close)))*self.Rank(self.Close.iloc[self.dateIndex,1:]/self.Open.iloc[self.dateIndex,1:])
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
        
class Alpha39Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfADV,self.startDate):
            #Auxiliary 1
            self.dateIndex=dateIndex
            self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.Volume.iloc[self.dateIndex,1:]/self.TSMean(self.Volume,self.daysOfADV)
    
    def SetAlphaParameters(self,daysOfLag,daysOfADV,daysOfDecay,daysOfSum):         
        self.daysOfLag=daysOfLag
        self.daysOfADV=daysOfADV
        self.daysOfDecay=daysOfDecay
        self.daysOfSum=daysOfSum       
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1         
        if( ( (self.daysOfSum)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfSum)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.Volume.iloc[self.dateIndex,1:]/self.TSMean(self.Volume,self.daysOfADV)
        
        self.Value=(-self.Rank(self.Delta(self.Close,self.daysOfLag)*(1.0-self.Rank(self.TSLinearDecay(self.AuxiliaryAlpha1,self.daysOfDecay)) )) )*(1.0+self.Rank(self.TSSum(self.TheAlphaReturns,self.daysOfSum)))
            
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha40Zura(Alpha):
    def SetAlphaParameters(self,daysOfCorrelation,daysOfStd):         
        self.daysOfCorrelation=daysOfCorrelation 
        self.daysOfStd=daysOfStd 
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1         
        if( ( (self.daysOfCorrelation)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfCorrelation)*self.TradingFrequency)        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.Value=-self.Rank(self.TSSTD(self.High,self.daysOfStd))*self.Correl(self.High,self.Volume,self.daysOfCorrelation)
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha43Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfTSRank2,self.startDate):
            self.dateIndex=dateIndex
            self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.Delta(self.Close,self.daysOfLag)
            #Auxiliary 1
            self.dateIndex=dateIndex
            if(dateIndex>=self.daysOfADV):
                self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.Volume.iloc[self.dateIndex,1:]/self.TSMean(self.Volume,self.daysOfADV)
    
    def SetAlphaParameters(self,daysOfLag,daysOfADV,daysOfTSRank1,daysOfTSRank2):         
        self.daysOfLag=daysOfLag
        self.daysOfADV=daysOfADV
        self.daysOfTSRank1=daysOfTSRank1
        self.daysOfTSRank2=daysOfTSRank2       
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1         
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2       
        if( ( (self.daysOfTSRank1+self.daysOfADV)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfTSRank1+self.daysOfADV)*self.TradingFrequency)
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.Volume.iloc[self.dateIndex,1:]/self.TSMean(self.Volume,self.daysOfADV)
        self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.Delta(self.Close,self.daysOfLag)        
        self.Value=self.TSRank(self.History(self.daysOfTSRank1,self.AuxiliaryAlpha1))*self.TSRank(self.History(self.daysOfTSRank2,self.AuxiliaryAlpha2))
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha44Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfCorrelation,self.startDate):
            self.dateIndex=dateIndex
            self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.Rank(self.Volume.iloc[self.dateIndex,1:])
            
    def SetAlphaParameters(self,daysOfCorrelation):         
        self.daysOfCorrelation=daysOfCorrelation         
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1.iloc[:,1:]=0*self.AuxiliaryAlpha1.iloc[:,1:]            
        if( ( (self.daysOfCorrelation)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfCorrelation)*self.TradingFrequency) 
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.Rank(self.Volume.iloc[self.dateIndex,1:])
        self.Value=-self.Correl(self.High,self.AuxiliaryAlpha1,self.daysOfCorrelation)
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha45Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfMean,self.startDate):
            self.dateIndex=dateIndex
            self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.TSMean(self.Close,self.daysOfMean)            
            self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.TSSum(self.Close,self.daysSum1)
            self.AuxiliaryAlpha3.iloc[self.dateIndex,1:]=self.TSSum(self.Close,self.daysSum2)
    def SetAlphaParameters(self,daysOfCorrelation,daysSum1,daysSum2,daysOfDelay,daysOfMean):         
        self.daysOfCorrelation=daysOfCorrelation
        self.daysSum1=daysSum1
        self.daysSum2=daysSum2
        self.daysOfDelay=daysOfDelay
        self.daysOfMean=daysOfMean         
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2 
        self.AuxiliaryAlpha3=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha3=0*self.AuxiliaryAlpha3                 
        if( ( (self.daysOfMean+self.daysOfDelay)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfMean+self.daysOfDelay)*self.TradingFrequency) 
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.TSMean(self.Close,self.daysOfMean)            
        self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.TSSum(self.Close,self.daysSum1)
        self.AuxiliaryAlpha3.iloc[self.dateIndex,1:]=self.TSSum(self.Close,self.daysSum2)
        Value1=self.Rank(self.AuxiliaryAlpha1.iloc[self.dateIndex-self.daysOfDelay,1:])
        Value2=self.Correl(self.Close,self.Volume,self.daysOfCorrelation)
        Value3=self.Rank(self.Correl(self.AuxiliaryAlpha2,self.AuxiliaryAlpha3,self.daysOfCorrelation))
        self.Value=-Value1*Value2*Value3
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha46Zura(Alpha):
                
    def SetAlphaParameters(self,daysOfLag1,daysOfLag2,daysOfLag3,daysOfLag4):         
        self.daysOfLag1=daysOfLag1
        self.daysOfLag2=daysOfLag2
        self.daysOfLag3=daysOfLag3  
        self.daysOfLag4=daysOfLag4  
        self.TheAlphaReturns=self.ProcessData.Returns
        if( ( (daysOfLag1+daysOfLag2+daysOfLag3+daysOfLag4)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (daysOfLag1+daysOfLag2+daysOfLag3+daysOfLag4)*self.TradingFrequency)        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        Value1=0.1*(self.Close.iloc[self.dateIndex-self.daysOfLag1,1:]-2*self.Close.iloc[self.dateIndex-self.daysOfLag2,1:]-self.Close.iloc[self.dateIndex,1:])
        self.Value=0*Value1.copy()
        self.Value.loc[Value1>0.25]=-1
        self.Value.loc[Value1<0]=-1
        self.Value.loc[(Value1>0)&(Value1<0.25)]=-self.Delta(self.Close,self.daysOfLag4)
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value

class Alpha48Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfDelta,self.startDate):
            self.dateIndex=dateIndex
            self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.Delta(self.Close,self.daysOfDelta)            
            self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.Delta(self.Close.shift(1),self.daysOfDelta) 
            self.AuxiliaryAlpha3.iloc[self.dateIndex,1:]=self.Delta(self.Close,self.daysOfDelta)/(self.Delta(self.Close,self.daysOfDelta)).apply(lambda x: x**2)
                
    def SetAlphaParameters(self,daysOfDelta,daysOfLag,daysOfCorrelation,daysOfSum):         
        self.daysOfDelta=daysOfDelta
        self.daysOfLag=daysOfLag
        self.daysOfCorrelation=daysOfCorrelation
        self.daysOfSum=daysOfSum
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2 
        self.AuxiliaryAlpha3=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha3=0*self.AuxiliaryAlpha3   
        if( ( (self.daysOfDelta+self.daysOfLag+self.daysOfCorrelation+self.daysOfSum)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfDelta+self.daysOfLag+self.daysOfCorrelation+self.daysOfSum)*self.TradingFrequency) 
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.Delta(self.Close,self.daysOfDelta)            
        self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.Delta(self.Close.shift(1),self.daysOfDelta) 
        self.AuxiliaryAlpha3.iloc[self.dateIndex,1:]=self.Delta(self.Close,self.daysOfDelta)/(self.Delta(self.Close,self.daysOfDelta)).apply(lambda x: x**2)

        Value1=self.Correl(self.AuxiliaryAlpha1,self.AuxiliaryAlpha2,self.daysOfCorrelation)
        Value2=self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]/self.Close.iloc[self.dateIndex,1:]
        self.Value=Value1*Value2
        self.IndNeut2()
        Value3=self.TSSum(self.AuxiliaryAlpha3,self.daysOfCorrelation)
        self.Value=self.Value*Value3
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        #self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha49Zura(Alpha):
                
    def SetAlphaParameters(self,daysOfLag1,daysOfLag2,daysOfLag3,daysOfLag4): 
        self.TheAlphaReturns=self.ProcessData.Returns        
        self.daysOfLag1=daysOfLag1
        self.daysOfLag2=daysOfLag2
        self.daysOfLag3=daysOfLag3  
        self.daysOfLag4=daysOfLag4  
        if( ( (daysOfLag1+daysOfLag2+daysOfLag3+daysOfLag4)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (daysOfLag1+daysOfLag2+daysOfLag3+daysOfLag4)*self.TradingFrequency)        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        Value1=0.1*(self.Close.iloc[self.dateIndex-self.daysOfLag1,1:]-2*self.Close.iloc[self.dateIndex-self.daysOfLag2,1:]-self.Close.iloc[self.dateIndex,1:])
        self.Value=0*Value1.copy()
        self.Value.loc[Value1<-0.1]=1
        
        self.Value.loc[(Value1>-0.1)]=-self.Delta(self.Close,self.daysOfLag4)
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha51Zura(Alpha):                
    def SetAlphaParameters(self,daysOfLag1,daysOfLag2,daysOfLag3,daysOfLag4):
        self.TheAlphaReturns=self.ProcessData.Returns         
        self.daysOfLag1=daysOfLag1
        self.daysOfLag2=daysOfLag2
        self.daysOfLag3=daysOfLag3  
        self.daysOfLag4=daysOfLag4  
        if( ( (daysOfLag1+daysOfLag2+daysOfLag3+daysOfLag4)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (daysOfLag1+daysOfLag2+daysOfLag3+daysOfLag4)*self.TradingFrequency)        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        Value1=0.1*(self.Close.iloc[self.dateIndex-self.daysOfLag1,1:]-2*self.Close.iloc[self.dateIndex-self.daysOfLag2,1:]-self.Close.iloc[self.dateIndex,1:])
        self.Value=0*Value1.copy()
        self.Value.loc[Value1<-0.05]=1
        
        self.Value.loc[(Value1>-0.05)]=-self.Delta(self.Close,self.daysOfLag4)
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    


class Alpha52Zura(Alpha):
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfDelay,self.startDate):
            self.dateIndex=dateIndex
            if(dateIndex>=self.daysOfSum1):
                self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.TSSum(self.TheAlphaReturns,self.daysOfSum1) 
            if(dateIndex>=self.daysOfSum2):
                self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.TSSum(self.TheAlphaReturns,self.daysOfSum2) 
                
            
    def SetAlphaParameters(self,daysOfTSRank1,daysOfTSRank2,daysOfDelay,daysOfSum1,daysOfSum2):         
        self.daysOfTSRank1=daysOfTSRank1
        self.daysOfTSRank2=daysOfTSRank2
        self.daysOfDelay=daysOfDelay
        self.daysOfSum1=daysOfSum1
        self.daysOfSum2=daysOfSum2
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2 
            
        
        if( ( (self.daysOfTSRank1+self.daysOfTSRank2+self.daysOfDelay+self.daysOfSum1+self.daysOfSum2)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfTSRank1+self.daysOfTSRank2+self.daysOfDelay+self.daysOfSum1+self.daysOfSum2)*self.TradingFrequency)    
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.TSSum(self.TheAlphaReturns,self.daysOfSum1)            
        self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.TSSum(self.TheAlphaReturns,self.daysOfSum2) 

        self.Value=(-self.TSMin(self.Low,self.daysOfTSRank1)+self.TSMin(self.Low,self.daysOfTSRank1).shift(self.daysOfTSRank1))*self.Rank(self.TSSum(self.TheAlphaReturns,self.daysOfSum1)-self.TSSum(self.TheAlphaReturns,self.daysOfSum2))*self.TSRank(self.History(self.daysOfTSRank2,self.Volume))
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        #self.IndNeut2()
        # self.IndSector2()
        return self.Value
    


class Alpha53Zura(Alpha):  
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfDelta,self.startDate):
            self.dateIndex=dateIndex            
            self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=(2*self.Close.iloc[self.dateIndex,1:]-self.Low.iloc[self.dateIndex,1:]-self.High.iloc[self.dateIndex,1:])/(self.Close.iloc[self.dateIndex,1:]-self.Low.iloc[self.dateIndex,1:])
    def SetAlphaParameters(self,daysOfDelta):         
        self.daysOfDelta=daysOfDelta 
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1        
        if( ( (daysOfDelta)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (daysOfDelta)*self.TradingFrequency)  
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=(2*self.Close.iloc[self.dateIndex,1:]-self.Low.iloc[self.dateIndex,1:]-self.High.iloc[self.dateIndex,1:])/(self.Close.iloc[self.dateIndex,1:]-self.Low.iloc[self.dateIndex,1:])        
        self.Value=self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]-self.AuxiliaryAlpha1.iloc[self.dateIndex-self.daysOfDelta,1:]
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha54Zura(Alpha): 
    def SetAlphaParameters(self): 
        self.TheAlphaReturns=self.ProcessData.Returns        
        pass       
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex                
        self.Value=(-(self.Low.iloc[self.dateIndex,1:]-self.Close.iloc[self.dateIndex,1:])*self.Open.iloc[self.dateIndex,1:].apply(lambda x: np.power(x,5)))/((self.Low.iloc[self.dateIndex,1:]-self.High.iloc[self.dateIndex,1:])*self.Close.iloc[self.dateIndex,1:].apply(lambda x: np.power(x,5)) )
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha55Zura(Alpha):  
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfTS,self.startDate):
            self.dateIndex=dateIndex            
            self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.Rank(((self.Close.iloc[self.dateIndex,1:]-self.TSMin(self.Low,self.daysOfTS))/(self.TSMax(self.High,self.daysOfTS) - self.TSMin(self.Low,self.daysOfTS)  )  )   )
            self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.Rank(self.Volume.iloc[self.dateIndex,1:])
    def SetAlphaParameters(self,daysOfTS,daysOfCorrelation): 
        self.daysOfTS=daysOfTS 
        self.daysOfCorrelation=daysOfCorrelation
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1    
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2   
        if( ( (self.daysOfTS+self.daysOfCorrelation)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfTS+self.daysOfCorrelation)*self.TradingFrequency)  
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.Rank(((self.Close.iloc[self.dateIndex,1:]-self.TSMin(self.Low,self.daysOfTS))/(self.TSMax(self.High,self.daysOfTS) - self.TSMin(self.Low,self.daysOfTS)  )  )    ) 
        self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.Rank(self.Volume.iloc[self.dateIndex,1:])
        self.Value=-self.Correl(self.AuxiliaryAlpha1,self.AuxiliaryAlpha2,self.daysOfCorrelation)
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value

class Alpha56Zura(Alpha):  
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfTS,self.startDate):
            self.dateIndex=dateIndex            
            self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.TSSum(self.TheAlphaReturns,self.daysOfTS)/self.TSSum(self.TheAlphaReturns,self.daysOfSum)
            
    def SetAlphaParameters(self,daysOfTS,daysOfSum): 
        self.daysOfTS=daysOfTS 
        self.daysOfSum=daysOfSum
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1    
         
        if( ( (self.daysOfTS+self.daysOfSum)*self.TradingFrequency)<=self.startDate):
            pass
        else:
            self.startDate=( (self.daysOfTS+self.daysOfSum)*self.TradingFrequency)  
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.TSSum(self.TheAlphaReturns,self.daysOfTS)/self.TSSum(self.TheAlphaReturns,self.daysOfSum)
        
        self.Value=-self.Rank(self.AuxiliaryAlpha1.iloc[self.dateIndex,1:])*self.Rank(self.MarketCap.iloc[self.dateIndex,1:]*self.TheAlphaReturns.iloc[self.dateIndex,1:])
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha60Zura(Alpha): 
    def SetAlphaParameters(self,daysTS): 
        self.daysTS=daysTS
        self.TheAlphaReturns=self.ProcessData.Returns        
        pass       
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        if(self.dateIndex<=self.daysTS):
            self.dateIndex=self.daysTS
        self.dateIndex=dateIndex 
        Aux=2*self.Close.iloc[self.dateIndex,1:]- self.Low.iloc[self.dateIndex,1:]-self.High.iloc[self.dateIndex,1:]   
        AuxDenum=- self.Low.iloc[self.dateIndex,1:]+self.High.iloc[self.dateIndex,1:]
        Aux2=-2*self.Scale(self.Rank((Aux/AuxDenum)*self.Volume.iloc[self.dateIndex,1:]))
        Aux3=self.Scale(self.Rank( self.TSArgMax(self.Close,self.daysTS) ))
        self.Value=Aux2+Aux3
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        
        # self.IndSector2()
        return self.Value
    
class Alpha68Zura(Alpha):  
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(self.daysOfLag,self.startDate):
            self.dateIndex=dateIndex            
            self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=-self.Rank((self.w1*self.Close.iloc[dateIndex,1:]+(1-self.w1)*self.Low.iloc[dateIndex,1:])-(self.w1*self.Close.iloc[dateIndex-self.daysOfLag,1:]+(1-self.w1)*self.Low.iloc[dateIndex-self.daysOfLag,1:]) )
            self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.Rank(self.High.iloc[dateIndex,1:])
            if(dateIndex>self.daysOfADV):
                self.AuxiliaryAlpha3.iloc[self.dateIndex,1:]=self.Rank(self.TSMean(self.Volume,self.daysOfADV))
            if(dateIndex>self.daysOfADV+self.daysOfCorrelation+self.daysOfLag):
                self.AuxiliaryAlpha4.iloc[self.dateIndex,1:]=self.Correl(self.AuxiliaryAlpha2,self.AuxiliaryAlpha3,self.daysOfCorrelation)   
                
    def SetAlphaParameters(self,daysOfCorrelation,daysOfADV,daysOfTSRank,daysOfLag,w1): 
        self.daysOfCorrelation=daysOfCorrelation
        self.daysOfADV=daysOfADV
        self.daysOfTSRank=daysOfTSRank
        self.daysOfLag=daysOfLag
        self.w1=w1
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1    
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2  
        self.AuxiliaryAlpha3=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha3=0*self.AuxiliaryAlpha3 
        self.AuxiliaryAlpha4=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha4=0*self.AuxiliaryAlpha4 
         
        if(  (daysOfCorrelation+daysOfADV+daysOfTSRank+daysOfLag)*self.TradingFrequency<=self.startDate):
            pass
        else:
            self.startDate=( (daysOfCorrelation+daysOfADV+daysOfTSRank+daysOfLag)*self.TradingFrequency)  
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=-self.Rank((self.w1*self.Close.iloc[dateIndex,1:]+(1-self.w1)*self.Low.iloc[dateIndex,1:])-(self.w1*self.Close.iloc[dateIndex-self.daysOfLag,1:]+(1-self.w1)*self.Low.iloc[dateIndex-self.daysOfLag,1:]) )
        self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.Rank(self.High.iloc[dateIndex,1:])            
        self.AuxiliaryAlpha3.iloc[self.dateIndex,1:]=self.Rank(self.TSMean(self.Volume,self.daysOfADV))            
        self.AuxiliaryAlpha4.iloc[self.dateIndex,1:]=self.Correl(self.AuxiliaryAlpha2,self.AuxiliaryAlpha3,self.daysOfCorrelation)   
  
        Boolean=self.TSRank(self.History(self.daysOfTSRank,self.AuxiliaryAlpha4))<self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]
        self.Value=Boolean.astype(int).copy()
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha80Zura(Alpha):  
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            self.dateIndex=dateIndex
            self.Value=self.w1*self.Open.iloc[self.dateIndex,1:]+self.w2*self.High.iloc[self.dateIndex,1:] 
            self.IndNeut2()
            self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.Value
            if(dateIndex>self.daysOfLag):
                self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.Rank(self.Sign(self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]-self.AuxiliaryAlpha1.iloc[self.dateIndex-self.daysOfLag,1:]))
            if(dateIndex>self.daysOfADV):  
                self.AuxiliaryAlpha3.iloc[self.dateIndex,1:]=self.TSMean(self.Volume,self.daysOfADV)            
            if(dateIndex>self.daysOfADV+self.daysOfCorrelation):
                self.AuxiliaryAlpha4.iloc[self.dateIndex,1:]=self.Correl(self.AuxiliaryAlpha3,self.High,self.daysOfCorrelation)
                
    def SetAlphaParameters(self,daysOfCorrelation,daysOfADV,daysOfTSRank,daysOfLag,w1,w2): 
        self.daysOfCorrelation=daysOfCorrelation
        self.daysOfADV=daysOfADV
        self.daysOfTSRank=daysOfTSRank
        self.daysOfLag=daysOfLag
        self.w1=w1
        self.w2=w2
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1    
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2  
        self.AuxiliaryAlpha3=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha3=0*self.AuxiliaryAlpha3 
        self.AuxiliaryAlpha4=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha4=0*self.AuxiliaryAlpha4 
         
        if(  (daysOfCorrelation+daysOfADV+daysOfTSRank+daysOfLag)*self.TradingFrequency<=self.startDate):
            pass
        else:
            self.startDate=( (daysOfCorrelation+daysOfADV+daysOfTSRank+daysOfLag)*self.TradingFrequency)  
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        
        self.Value=self.w1*self.Open.iloc[self.dateIndex,1:]+self.w2*self.High.iloc[self.dateIndex,1:] 
        self.IndNeut2()
        self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.Value            
        self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.Rank(self.Sign(self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]-self.AuxiliaryAlpha1.iloc[self.dateIndex-self.daysOfLag,1:]))             
        self.AuxiliaryAlpha3.iloc[self.dateIndex,1:]=self.TSMean(self.Volume,self.daysOfADV)
        self.AuxiliaryAlpha4.iloc[self.dateIndex,1:]=self.Correl(self.AuxiliaryAlpha3,self.High,self.daysOfCorrelation)
  
        self.Value=-self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]**(self.TSRank(self.History(self.daysOfTSRank,self.AuxiliaryAlpha4)))
        self.Value.fillna(value=0,inplace=True)
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value


class Alpha82Zura(Alpha):  
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            self.dateIndex=dateIndex
            self.Value=self.Volume.iloc[self.dateIndex,1:] 
            self.IndSector2()
            self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.Value
            self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.w1*self.Open.iloc[self.dateIndex,1:]+self.w2*self.Close.iloc[self.dateIndex,1:]
            if(dateIndex>self.daysOfCorrelation):
                self.AuxiliaryAlpha3.iloc[self.dateIndex,1:]=self.Correl(self.AuxiliaryAlpha1,self.AuxiliaryAlpha2,self.daysOfCorrelation)
            if(dateIndex>self.daysOfCorrelation+self.daysOfDecayLinear1):  
                self.AuxiliaryAlpha4.iloc[self.dateIndex,1:]=self.TSLinearDecay(self.AuxiliaryAlpha3,self.daysOfDecayLinear1)           
            if(dateIndex>self.daysOfCorrelation+self.daysOfDecayLinear1+self.daysOfTSRank):
                self.AuxiliaryAlpha5.iloc[self.dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank,self.AuxiliaryAlpha4))
            if(dateIndex>self.daysOfDelta):  
                self.AuxiliaryAlpha6.iloc[self.dateIndex,1:]=self.Open.iloc[self.dateIndex,1:]-self.Open.iloc[self.dateIndex-self.daysOfDelta,1:]
            if(dateIndex>self.daysOfDelta+self.daysOfDecayLinear2):
                self.AuxiliaryAlpha7.iloc[self.dateIndex,1:]=self.Rank(self.TSLinearDecay(self.AuxiliaryAlpha6,self.daysOfDecayLinear2))
                
    def SetAlphaParameters(self,daysOfCorrelation,daysOfDecayLinear1,daysOfDecayLinear2,daysOfTSRank,daysOfDelta,w1,w2): 
        self.daysOfCorrelation=daysOfCorrelation
        self.daysOfDecayLinear1=daysOfDecayLinear1
        self.daysOfDecayLinear2=daysOfDecayLinear2
        self.daysOfTSRank=daysOfTSRank
        self.daysOfDelta=daysOfDelta
        self.w1=w1
        self.w2=w2        
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1    
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2  
        self.AuxiliaryAlpha3=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha3=0*self.AuxiliaryAlpha3 
        self.AuxiliaryAlpha4=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha4=0*self.AuxiliaryAlpha4  
        self.AuxiliaryAlpha5=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha5=0*self.AuxiliaryAlpha5
        self.AuxiliaryAlpha6=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha6=0*self.AuxiliaryAlpha6  
        self.AuxiliaryAlpha7=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha7=0*self.AuxiliaryAlpha7
        if(  (daysOfCorrelation+daysOfDecayLinear1+daysOfDecayLinear2+daysOfTSRank+daysOfDelta)*self.TradingFrequency<=self.startDate):
            pass
        else:
            self.startDate=( (daysOfCorrelation+daysOfDecayLinear1+daysOfDecayLinear2+daysOfTSRank+daysOfDelta)*self.TradingFrequency)  
        self.GenerateAuxiliaryAlpha()
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        
        self.Value=self.Volume.iloc[self.dateIndex,1:] 
        self.IndSector2()
        self.AuxiliaryAlpha1.iloc[self.dateIndex,1:]=self.Value
        self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]=self.w1*self.Open.iloc[self.dateIndex,1:]+self.w2*self.Close.iloc[self.dateIndex,1:]
      
        self.AuxiliaryAlpha3.iloc[self.dateIndex,1:]=self.Correl(self.AuxiliaryAlpha1,self.AuxiliaryAlpha2,self.daysOfCorrelation)
              
        self.AuxiliaryAlpha4.iloc[self.dateIndex,1:]=self.TSLinearDecay(self.AuxiliaryAlpha3,self.daysOfDecayLinear1)           
            
        self.AuxiliaryAlpha5.iloc[self.dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank,self.AuxiliaryAlpha4))
            
        self.AuxiliaryAlpha6.iloc[self.dateIndex,1:]=self.Open.iloc[self.dateIndex,1:]-self.Open.iloc[self.dateIndex-self.daysOfDelta,1:]
            
        self.AuxiliaryAlpha7.iloc[self.dateIndex,1:]=self.Rank(self.TSLinearDecay(self.AuxiliaryAlpha6,self.daysOfDecayLinear2))
        Value0=self.AuxiliaryAlpha7.iloc[self.dateIndex,1:]
        Value1=self.AuxiliaryAlpha5.iloc[self.dateIndex,1:]
        Value2=Value0-Value1
        self.Value=0*Value2.copy()
        self.Value.loc[Value2<0]=Value0.loc[Value2<0]
        self.Value.loc[Value2>=0]=Value1.loc[Value2>=0]
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
    
class Alpha85Zura(Alpha):  
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            self.dateIndex=dateIndex
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.w1*self.High.iloc[dateIndex,1:]+self.w2*self.Close.iloc[dateIndex,1:]
            self.AuxiliaryAlpha4.iloc[dateIndex,1:]= 0.5*(self.High.iloc[dateIndex,1:]+self.Low.iloc[dateIndex,1:])
            if(dateIndex>=self.daysOfADV):
                self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.TSMean(self.Volume,self.daysOfADV)
            if(dateIndex>=self.daysOfADV+self.daysOfCorrelation1):
                self.AuxiliaryAlpha3.iloc[dateIndex,1:]=self.Correl(self.AuxiliaryAlpha1,self.AuxiliaryAlpha2,self.daysOfCorrelation1)
            if(dateIndex>=self.daysOfTSRank1):
                self.AuxiliaryAlpha5.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank1,self.AuxiliaryAlpha4))
            if(dateIndex>=self.daysOfTSRank2):
                self.AuxiliaryAlpha6.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank2,self.Volume))
            if(dateIndex>=max(self.daysOfTSRank2,self.daysOfTSRank1)+self.daysOfCorrelation2):
                self.AuxiliaryAlpha7.iloc[dateIndex,1:]=self.Rank(self.Correl(self.AuxiliaryAlpha5,self.AuxiliaryAlpha6,self.daysOfCorrelation2))
                
               
    def SetAlphaParameters(self,daysOfCorrelation1,daysOfCorrelation2,daysOfTSRank1,daysOfTSRank2,daysOfADV,w1,w2): 
        self.daysOfCorrelation1=daysOfCorrelation1
        self.daysOfCorrelation2=daysOfCorrelation2       
        self.daysOfTSRank1=daysOfTSRank1
        self.daysOfTSRank2=daysOfTSRank2
        self.daysOfADV=daysOfADV
        self.w1=w1
        self.w2=w2        
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1    
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2  
        self.AuxiliaryAlpha3=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha3=0*self.AuxiliaryAlpha3 
        self.AuxiliaryAlpha4=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha4=0*self.AuxiliaryAlpha4  
        self.AuxiliaryAlpha5=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha5=0*self.AuxiliaryAlpha5
        self.AuxiliaryAlpha6=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha6=0*self.AuxiliaryAlpha6  
        self.AuxiliaryAlpha7=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha7=0*self.AuxiliaryAlpha7
        if(  (daysOfCorrelation1+daysOfCorrelation1+daysOfTSRank1+daysOfTSRank2+daysOfADV)*self.TradingFrequency<=self.startDate):
            pass
        else:
            self.startDate=( (daysOfCorrelation1+daysOfCorrelation1+daysOfTSRank1+daysOfTSRank2+daysOfADV)*self.TradingFrequency)  
        self.GenerateAuxiliaryAlpha()
        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.w1*self.High.iloc[dateIndex,1:]+self.w2*self.Close.iloc[dateIndex,1:]
        self.AuxiliaryAlpha4.iloc[dateIndex,1:]= 0.5*(self.High.iloc[dateIndex,1:]+self.Low.iloc[dateIndex,1:])            
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.TSMean(self.Volume,self.daysOfADV)            
        self.AuxiliaryAlpha3.iloc[dateIndex,1:]=self.Correl(self.AuxiliaryAlpha1,self.AuxiliaryAlpha2,self.daysOfCorrelation1)            
        self.AuxiliaryAlpha5.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank1,self.AuxiliaryAlpha4))           
        self.AuxiliaryAlpha6.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank2,self.Volume))            
        self.AuxiliaryAlpha7.iloc[dateIndex,1:]=self.Rank(self.Correl(self.AuxiliaryAlpha5,self.AuxiliaryAlpha6,self.daysOfCorrelation2))

        self.Value=(self.AuxiliaryAlpha3.iloc[dateIndex,1:])**(self.AuxiliaryAlpha7.iloc[dateIndex,1:])
        self.Value.fillna(value=0,inplace=True)
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    
class Alpha88Zura(Alpha):  
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            self.dateIndex=dateIndex
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Rank(self.Open.iloc[dateIndex,1:])+self.Rank(self.Low.iloc[dateIndex,1:])-self.Rank(self.High.iloc[dateIndex,1:])-self.Rank(self.Close.iloc[dateIndex,1:])
            if(dateIndex>=self.daysOfDecayLinear1):
                self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Rank(self.TSLinearDecay(self.AuxiliaryAlpha1,self.daysOfDecayLinear1))
            if(dateIndex>=self.daysOfTSRank1):
                self.AuxiliaryAlpha3.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank1,self.Close))
            if(dateIndex>=self.daysOfADV): 
                self.AuxiliaryAlpha4.iloc[dateIndex,1:]=self.TSMean(self.Volume,self.daysOfADV)
            if(dateIndex>=self.daysOfADV+self.daysOfTSRank2): 
                self.AuxiliaryAlpha5.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank2,self.AuxiliaryAlpha4))
            if(dateIndex>=self.daysOfADV+self.daysOfTSRank2+self.daysOfCorrelation): 
                self.AuxiliaryAlpha6.iloc[dateIndex,1:]=self.Correl(self.AuxiliaryAlpha5,self.AuxiliaryAlpha3,self.daysOfCorrelation)
            if(dateIndex>=self.daysOfADV+self.daysOfTSRank2+self.daysOfCorrelation+self.daysOfDecayLinear2): 
                self.AuxiliaryAlpha7.iloc[dateIndex,1:]=self.TSLinearDecay(self.AuxiliaryAlpha6,self.daysOfDecayLinear2)
            if(dateIndex>=self.daysOfADV+self.daysOfTSRank2+self.daysOfCorrelation+self.daysOfDecayLinear2+self.daysOfTSRank3): 
                self.AuxiliaryAlpha8.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank3,self.AuxiliaryAlpha7))
    
                          
               
    def SetAlphaParameters(self,daysOfCorrelation,daysOfDecayLinear1,daysOfDecayLinear2,daysOfTSRank1,daysOfTSRank2,daysOfTSRank3,daysOfADV): 
        self.daysOfCorrelation=daysOfCorrelation
        self.daysOfDecayLinear1=daysOfDecayLinear1  
        self.daysOfDecayLinear2=daysOfDecayLinear2
        self.daysOfTSRank1=daysOfTSRank1
        self.daysOfTSRank2=daysOfTSRank2
        self.daysOfTSRank3=daysOfTSRank3
        self.daysOfADV=daysOfADV
               
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1    
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2  
        self.AuxiliaryAlpha3=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha3=0*self.AuxiliaryAlpha3 
        self.AuxiliaryAlpha4=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha4=0*self.AuxiliaryAlpha4  
        self.AuxiliaryAlpha5=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha5=0*self.AuxiliaryAlpha5
        self.AuxiliaryAlpha6=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha6=0*self.AuxiliaryAlpha6  
        self.AuxiliaryAlpha7=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha7=0*self.AuxiliaryAlpha7
        self.AuxiliaryAlpha8=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha8=0*self.AuxiliaryAlpha8
        if(  (daysOfCorrelation+daysOfDecayLinear1+daysOfDecayLinear2+daysOfTSRank1+daysOfTSRank2+daysOfTSRank3+daysOfADV)*self.TradingFrequency<=self.startDate):
            pass
        else:
            self.startDate=( (daysOfCorrelation+daysOfDecayLinear1+daysOfDecayLinear2+daysOfTSRank1+daysOfTSRank2+daysOfTSRank3+daysOfADV)*self.TradingFrequency)  
        self.GenerateAuxiliaryAlpha()
        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=self.Rank(self.Open.iloc[dateIndex,1:])+self.Rank(self.Low.iloc[dateIndex,1:])-self.Rank(self.High.iloc[dateIndex,1:])-self.Rank(self.Close.iloc[dateIndex,1:])            
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Rank(self.TSLinearDecay(self.AuxiliaryAlpha1,self.daysOfDecayLinear1)  )  
        self.AuxiliaryAlpha3.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank1,self.Close))    
        self.AuxiliaryAlpha4.iloc[dateIndex,1:]=self.TSMean(self.Volume,self.daysOfADV)    
        self.AuxiliaryAlpha5.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank2,self.AuxiliaryAlpha4))    
        self.AuxiliaryAlpha6.iloc[dateIndex,1:]=self.Correl(self.AuxiliaryAlpha5,self.AuxiliaryAlpha3,self.daysOfCorrelation)    
        self.AuxiliaryAlpha7.iloc[dateIndex,1:]=self.TSLinearDecay(self.AuxiliaryAlpha6,self.daysOfDecayLinear2)    
        self.AuxiliaryAlpha8.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank3,self.AuxiliaryAlpha7))
  
        Value0=self.AuxiliaryAlpha8.iloc[self.dateIndex,1:]
        Value1=self.AuxiliaryAlpha2.iloc[self.dateIndex,1:]
        Value2=Value0-Value1
        self.Value=0*Value2.copy()
        self.Value.loc[Value2<0]=Value0.loc[Value2<0]
        self.Value.loc[Value2>=0]=Value1.loc[Value2>=0]
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    

class Alpha90Zura(Alpha):  
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            self.dateIndex=dateIndex
            
            if(dateIndex>=self.daysOfTSMax):
                self.AuxiliaryAlpha1.iloc[dateIndex,1:]=-self.Rank(self.Close.iloc[dateIndex,1:]-self.TSMax(self.Close,self.daysOfTSMax))
               
            if(dateIndex>=self.daysOfADV):
                self.Value=self.TSMean(self.Volume,self.daysOfADV)
                self.IndNeut2()
                self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Value.copy()
                
            if(dateIndex>=self.daysOfADV+self.daysOfCorrelation): 
                self.AuxiliaryAlpha3.iloc[dateIndex,1:]=self.Correl(self.AuxiliaryAlpha2,self.Low,self.daysOfCorrelation)
                
            if(dateIndex>=self.daysOfADV+self.daysOfCorrelation+self.daysOfTSRank): 
                self.AuxiliaryAlpha4.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank,self.AuxiliaryAlpha3))
                
                
                          
               
    def SetAlphaParameters(self,daysOfCorrelation,daysOfTSRank,daysOfTSMax,daysOfADV): 
        self.daysOfCorrelation=daysOfCorrelation        
        self.daysOfTSRank=daysOfTSRank
        self.daysOfTSMax=daysOfTSMax        
        self.daysOfADV=daysOfADV               
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1    
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2  
        self.AuxiliaryAlpha3=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha3=0*self.AuxiliaryAlpha3      
        self.AuxiliaryAlpha4=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha4=0*self.AuxiliaryAlpha4    
        if(  (daysOfCorrelation+daysOfTSRank+daysOfTSMax+daysOfADV)*self.TradingFrequency<=self.startDate):
            pass
        else:
            self.startDate=( (daysOfCorrelation+daysOfTSRank+daysOfTSMax+daysOfADV)*self.TradingFrequency)  
        self.GenerateAuxiliaryAlpha()
        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=-self.Rank(self.Close.iloc[dateIndex,1:]-self.TSMax(self.Close,self.daysOfTSMax))            
            
        self.Value=self.TSMean(self.Volume,self.daysOfADV)
        self.IndNeut2()
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.Value.copy()
        self.AuxiliaryAlpha3.iloc[dateIndex,1:]=self.Correl(self.AuxiliaryAlpha2,self.Low,self.daysOfCorrelation)      
        self.AuxiliaryAlpha4.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank,self.AuxiliaryAlpha3))
        self.Value=(self.AuxiliaryAlpha1.iloc[dateIndex,1:])**(self.AuxiliaryAlpha4.iloc[dateIndex,1:])
        self.Value.fillna(value=0,inplace=True)
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value
    

class Alpha92Zura(Alpha):  
    def GenerateAuxiliaryAlpha(self):
        for dateIndex in range(0,self.startDate):
            print(dateIndex)
            self.dateIndex=dateIndex
            self.AuxiliaryAlpha5.iloc[dateIndex,1:]=self.Rank(self.Low.iloc[dateIndex,1:])
            
            Boolean=(self.Close.iloc[dateIndex,1:]+0.5*self.High.iloc[dateIndex,1:]+0.5*self.Low.iloc[dateIndex,1:])<(self.Low.iloc[dateIndex,1:]+self.Open.iloc[dateIndex,1:])
            self.AuxiliaryAlpha1.iloc[dateIndex,1:]=Boolean.astype(int).copy()
            if(dateIndex>=self.daysOfDecayLinear1):
                self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.TSLinearDecay(self.AuxiliaryAlpha1.iloc[dateIndex,1:],self.daysOfDecayLinear1)
                 
            if(dateIndex>=self.daysOfDecayLinear1+self.daysOfTSRank1):
                self.AuxiliaryAlpha3.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank1,self.AuxiliaryAlpha2))
               
            if(dateIndex>=self.daysOfADV):
                self.AuxiliaryAlpha4.iloc[dateIndex,1:]=self.Rank(self.TSMean(self.Volume,self.daysOfADV))
                 
            if(dateIndex>=self.daysOfADV+self.daysOfCorrelation):
                self.AuxiliaryAlpha6.iloc[dateIndex,1:]=self.Correl(self.AuxiliaryAlpha4,self.AuxiliaryAlpha5,self.daysOfCorrelation)
                
            if(dateIndex>=self.daysOfADV+self.daysOfCorrelation+self.daysOfDecayLinear2): 
                self.AuxiliaryAlpha7.iloc[dateIndex,1:]=self.TSLinearDecay(self.AuxiliaryAlpha6,self.daysOfDecayLinear2)
                 
            if(dateIndex>=self.daysOfADV+self.daysOfCorrelation+self.daysOfDecayLinear2+self.daysOfTSRank2): 
                self.AuxiliaryAlpha8.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank2,self.AuxiliaryAlpha7))
                
                
                          
               
    def SetAlphaParameters(self,daysOfCorrelation,daysOfTSRank1,daysOfTSRank2,daysOfDecayLinear1,daysOfDecayLinear2,daysOfADV): 
        self.daysOfCorrelation=daysOfCorrelation        
        self.daysOfTSRank1=daysOfTSRank1
        self.daysOfTSRank2=daysOfTSRank2
        self.daysOfDecayLinear1=daysOfDecayLinear1
        self.daysOfDecayLinear2=daysOfDecayLinear2        
        self.daysOfADV=daysOfADV               
        self.TheAlphaReturns=self.ProcessData.Returns
        self.AuxiliaryAlpha1=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha1=0*self.AuxiliaryAlpha1    
        self.AuxiliaryAlpha2=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha2=0*self.AuxiliaryAlpha2  
        self.AuxiliaryAlpha3=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha3=0*self.AuxiliaryAlpha3      
        self.AuxiliaryAlpha4=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha4=0*self.AuxiliaryAlpha4    
        self.AuxiliaryAlpha5=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha5=0*self.AuxiliaryAlpha5    
        self.AuxiliaryAlpha6=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha6=0*self.AuxiliaryAlpha6  
        self.AuxiliaryAlpha7=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha7=0*self.AuxiliaryAlpha7      
        self.AuxiliaryAlpha8=self.TheAlphaReturns.copy()
        self.AuxiliaryAlpha8=0*self.AuxiliaryAlpha8    
        if(  (daysOfCorrelation+daysOfTSRank1+daysOfTSRank2+daysOfDecayLinear1+daysOfDecayLinear2+daysOfADV)*self.TradingFrequency<=self.startDate):
            pass
        else:
            self.startDate=( (daysOfCorrelation+daysOfTSRank1+daysOfTSRank2+daysOfDecayLinear1+daysOfDecayLinear2+daysOfADV)*self.TradingFrequency)  
        self.GenerateAuxiliaryAlpha()
        
    def GenerateAlpha(self,dateIndex, TotalAvailable):
        self.dateIndex=dateIndex
        self.AuxiliaryAlpha5.iloc[dateIndex,1:]=self.Rank(self.Low.iloc[dateIndex,1:])
        #print("Manos")
        Boolean=(self.Close.iloc[dateIndex,1:]+0.5*self.High.iloc[dateIndex,1:]+0.5*self.Low.iloc[dateIndex,1:])<(self.Low.iloc[dateIndex,1:]+self.Open.iloc[dateIndex,1:])
        self.AuxiliaryAlpha1.iloc[dateIndex,1:]=Boolean.astype(int).copy()
        self.AuxiliaryAlpha2.iloc[dateIndex,1:]=self.TSLinearDecay(self.AuxiliaryAlpha1.iloc[dateIndex,1:],self.daysOfDecayLinear1)
        #print("Yannos")    
        
        self.AuxiliaryAlpha3.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank1,self.AuxiliaryAlpha2))
           
        
        self.AuxiliaryAlpha4.iloc[dateIndex,1:]=self.Rank(self.TSMean(self.Volume,self.daysOfADV))
             
        
        self.AuxiliaryAlpha6.iloc[dateIndex,1:]=self.Correl(self.AuxiliaryAlpha4,self.AuxiliaryAlpha5,self.daysOfCorrelation)
            
        
        self.AuxiliaryAlpha7.iloc[dateIndex,1:]=self.TSLinearDecay(self.AuxiliaryAlpha6,self.daysOfDecayLinear2)
             
        
        self.AuxiliaryAlpha8.iloc[dateIndex,1:]=self.TSRank(self.History(self.daysOfTSRank2,self.AuxiliaryAlpha7))

        Value0=self.AuxiliaryAlpha8.iloc[self.dateIndex,1:]
        Value1=self.AuxiliaryAlpha3.iloc[self.dateIndex,1:]
        Value2=Value0-Value1
        self.Value=0*Value2.copy()
        self.Value.loc[Value2<0]=Value0.loc[Value2<0]
        self.Value.loc[Value2>=0]=Value1.loc[Value2>=0]
        
        self.PrepareAlpha2Neut(dateIndex, TotalAvailable) 
        # self.IndNeut2()
        # self.IndSector2()
        return self.Value