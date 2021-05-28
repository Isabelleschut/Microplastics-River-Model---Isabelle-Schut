# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 14:28:15 2021

@author: PradoDomercq
"""

#Function to estimate the relative abundance of MPs based on a selected criteria:
# (i.e. compartment type, MP aggregation state, MP size bin) taking the whole river system
import pandas as pd

def Relative_Abundance_calc (ConcFinal_num_m3, Clist,MPforms,riverComp,sizeBin, MPformslabels,compartments,stepSize,dilution_vol_m3,sizeBinLabel,t_span):
    

    #### Function to extract lists from a list by criteria
    def listofindex(criteria,Clist):                                                                                                             
        lista= [[] for x in range(len(criteria))]
        for i in range(len(lista)):
            lista[i] = [n for n in Clist if criteria[i] in n[-3:]]
        return lista
    
    #### Etract lists by MpType, Compartment and sizeBin
    list_of_indexesMpType=listofindex(MPforms,Clist)
    list_of_indexesCompartments=listofindex(riverComp,Clist)
    list_ofindexesSizeBins=listofindex(sizeBin,Clist)
    
    #define time resolution for the results
    numTstep_hour=(60/stepSize)
    Time_months=t_span[::(int(numTstep_hour*24*30))]
    Time_days=t_span[::(int(numTstep_hour*24))]
    Time_halfMonth=t_span[::(int(numTstep_hour*24*15))]
        
    Time_resol=Time_months
    
    #### Distribution of MPs per aggregation state and compartment over time 
    
    MpTypeNum_t=pd.DataFrame(index=range(len(Time_resol)),columns=["Timepoint (min)"]+[m+" (Total number)" for m in MPformslabels]+["Total"])
    RelativeAbun_MPtype_t=pd.DataFrame(0, columns=["Timepoint (days)"]+[m+" (%)" for m in MPformslabels], index=MpTypeNum_t.index)
    compNum_t=pd.DataFrame(index=range(len(Time_resol)),columns=["Timepoint (min)"]+[m+" (Total number)" for m in compartments])
    RelativeAbun_Comp=pd.DataFrame(0, columns=["Timepoint (days)"]+[m+" (%)" for m in compartments], index=MpTypeNum_t.index)
    for t in range(len(Time_resol)):
        #Convert concentration to particle number
        PartNum_timestep=ConcFinal_num_m3.iloc[int(Time_resol[t]/stepSize)]*dilution_vol_m3
        MpTypeNum_t.iloc[t,len(MPforms)+1]=sum(PartNum_timestep)
        PartNum_timestep=PartNum_timestep.to_frame()
        for mp in range(1,1+len(MPforms)):
            MpTypeNum_t.iloc[t,mp]=sum(PartNum_timestep.loc[list_of_indexesMpType[mp-1], :][Time_resol[t]].to_list())
            if MpTypeNum_t.iloc[t,len(MPforms)+1] == 0:
                RelativeAbun_MPtype_t.iloc[t,mp]= 0
            else:
                RelativeAbun_MPtype_t.iloc[t,mp]=round((MpTypeNum_t.iloc[t,mp]/MpTypeNum_t.iloc[t,len(MPforms)+1])*100,2)
        for com in range(1,1+len(compartments)):
            compNum_t.iloc[t,com]=sum(PartNum_timestep.loc[list_of_indexesCompartments[com-1], :][Time_resol[t]].to_list())
            if MpTypeNum_t.iloc[t,len(MPforms)+1]== 0:
                RelativeAbun_Comp.iloc[t,com]=0
            else:
                RelativeAbun_Comp.iloc[t,com]=round((compNum_t.iloc[t,com]/MpTypeNum_t.iloc[t,len(MPforms)+1])*100,2)
        RelativeAbun_MPtype_t.iloc[t,0]=int((Time_resol[t]/stepSize)/24)
        MpTypeNum_t.iloc[t,0]=Time_resol[t]/stepSize
        compNum_t.iloc[t,0]=Time_resol[t]/stepSize
        RelativeAbun_Comp.iloc[t,0]=int((Time_resol[t]/stepSize)/24)
        
    SizeBinNum_t=pd.DataFrame(index=range(len(Time_resol)),columns=[m+" (Total number)" for m in sizeBinLabel]+["Total"])
    for t in range(len(Time_resol)):
        PartNum_timestep=ConcFinal_num_m3.iloc[int(Time_resol[t]/stepSize)]*dilution_vol_m3
        PartNum_timestep=PartNum_timestep.to_frame()
        for size in range(len(sizeBinLabel)):
            SizeBinNum_t.iloc[t,size]=sum(PartNum_timestep.loc[list_ofindexesSizeBins[size], :][Time_resol[t]].to_list())
    for t in range(len(Time_resol)):
        SizeBinNum_t.iloc[t,5]=sum(SizeBinNum_t.iloc[t,:][0:5])
    SizeBinNum_t
    
    RelativeAbun_Size=pd.DataFrame(0, columns=["Timepoint (days)"]+[m+" (%)" for m in sizeBinLabel], index=MpTypeNum_t.index)
    for t in range(len(Time_resol)):
        RelativeAbun_Size.iloc[t,0]=int((Time_resol[t]/stepSize)/24)
        for size in range(1,len(sizeBinLabel)+1):
            if SizeBinNum_t.iloc[t,size-1]==0:
                RelativeAbun_Size.iloc[t,size]=0
            else:
                RelativeAbun_Size.iloc[t,size]=round((SizeBinNum_t.iloc[t,size-1]/SizeBinNum_t.iloc[t,5])*100,2)
    RelativeAbun_Size
    
    return [RelativeAbun_MPtype_t, RelativeAbun_Comp, RelativeAbun_Size]