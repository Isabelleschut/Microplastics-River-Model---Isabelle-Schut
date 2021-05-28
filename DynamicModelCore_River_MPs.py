# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 15:11:20 2020

@author: PradoDomercq
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def solverPrado(Concentrations_t0, interactions_df,inflow_vector, tmax, timesteps,t_days):
    
    
    def dCdt(C,t):
         Conc_row = C
         
         I= inflow_vector.to_numpy(dtype="float")
         I= np.resize(I, (1,len(I)))    
         ktransf = interactions_df.to_numpy()
         sol= np.dot(Conc_row,ktransf)+I
         
         return np.squeeze(sol)
     
    #Initial conditions
    Conc0 = Concentrations_t0
    # for p in range(len(Conc0)):
    #     Conc0.iloc[p][0]= 0
    # Conc0.loc["C_02Ae_0"] = 100
    conc0_col= Conc0.to_numpy(dtype="float")
    conc0=np.resize(conc0_col,(1,len(conc0_col)))
    conc0 = np.squeeze(conc0) #to solve ValueError: Initial condition y0 must be one-dimensional we use squeeze!
    t_span = np.linspace(0, tmax, int(timesteps)+1, dtype=int)
    
    Results= odeint(dCdt, conc0 , t_days, col_deriv=True)
    
    #Generate data frame to store final concentrations of each species-compartment-RS -->   concatenate results to results from previous run(s) ??
    Concentrations_finalRiver2 = pd.DataFrame(data = Results, index=t_days , columns= Concentrations_t0.index)        
        
    
    return Concentrations_finalRiver2, Results  

