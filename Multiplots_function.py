# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 20:12:50 2020

@author: PradoDomercq
"""
#Script to generate multiplot graphs to visualize modelled data

"""Plot multigraphs"""

# libraries
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib as mpl
from cycler import cycler


def Multiplots (ConcFinal_num_m3,t0, tmax, timesteps, results_path, composition, compartments, MPforms, MPformslabels, sizeBin, sizeBinLabel, RS_cumLength_m):

    ##plot straigth from Solution   
    #select time span units
    t_span_min = np.linspace(t0, tmax, int(timesteps)+1, dtype=int)
    t_span_h = t_span_min/60
    t_span_days = t_span_h/24
    
    
    #create folder to store the figures for the day if it doesnt already exists
    
    os.chdir(results_path)
    Fig_folder= "/Figures"
    os.path.isdir(results_path+Fig_folder)
    
    new_path = os.path.isdir(results_path+Fig_folder)
    if not new_path:
        os.mkdir("Figures")
        print("Created Folder : ", Fig_folder)
    else:
        print(Fig_folder, "folder already exists.")
    
    results_figures_path= results_path+Fig_folder
    
    ####PLOT PARTICLES DISTRIBUTION

      
    RS= ["0","1"] #Select the rivers sections to plot
    
    
    # create a color palette
    palette = plt.get_cmap('Set2')
    #Choose style
    plt.style.use('seaborn-white')

    
    ###Concentration of MPs (num/m3) vs time of size Bins (one graph per MPform)
    for p in range(len(MPforms)):
        fig, axs = plt.subplots(len(compartments),len(RS), figsize=(30, 15),sharex='col')
        fig.suptitle("Concentration of "+ composition +" " + MPformslabels[p]+ " MPs (Num/$m^3$) over time", fontsize=30)
        for i in range(len(RS)):
            for j in range(len(compartments)):
               for k in range(len(sizeBin)):
                   
                   axs[j,i].plot(t_span_days, ConcFinal_num_m3.loc[:,"C_"+RS[i]+str(j+1)+MPforms[p]+ sizeBin[k]], label= sizeBinLabel[k], color=palette(k), linewidth=3);
                   axs[j,i].set_yscale("log")
                   axs[j,i].set_ylim(1e-13,1e7)
                   if RS[i] == "0":
                       axs[j,i].set_title(compartments[j]+"\n 0-" + str(int(RS_cumLength_m[int(RS[i])]/1000))+" km distance ", y=1.0)
                   else:               
                       axs[j,i].set_title(compartments[j]+"\n "+str(int(RS_cumLength_m[int(RS[i])-1]/1000))+ "-" + str(int(RS_cumLength_m[int(RS[i])]/1000))+" km distance ", y=1.0)
                   
                   axs[j,i].set_yscale('log')
                   axs[j,i].legend()
                   # if RS==6:
                   #     axs[j,i].text(1.1, 0.5, compartments[j])   
         
        # Axis titles
        plt.text(0.1, 0.5, "Concentration of particles (Num/$m^3$)", fontsize=18, transform=plt.gcf().transFigure, rotation='vertical',ha='center', va='center')
        plt.text(0.5, 0.1, "time (days)", fontsize=18, transform=plt.gcf().transFigure, ha='center', va='center')
           
        png_label = 'figures/'+ "Concentration_Num_m3_Multiplot_sizeBins_"+ MPformslabels[p] +"_" +composition+'.png'    
        fig.savefig(png_label) #or pdf   
        
    ###Concentration of MPs (num/m3) vs time MP types (one per size bin)
    # create a color palette
    palette2 = plt.get_cmap('Paired')
    for o in range(len(sizeBin)):
        fig, axs = plt.subplots(len(compartments),len(RS), figsize=(30, 15),sharex='col')
        
        fig.suptitle("Concentration of " + composition +" particles of size fraction "+sizeBinLabel[o]+ " in (Num/$m^3$) per RS and compartment over time", fontsize=30)
        
        for i in range(len(RS)):
            for j in range(len(compartments)):
                for z in range(len(MPforms)):
                    axs[j,i].plot(t_span_days, ConcFinal_num_m3.loc[:, "C_"+RS[i]+str(j+1)+ MPforms[z]+ sizeBin[o]], label= MPformslabels[z], color=palette2(z), linewidth=3);
                    axs[j,i].set_yscale("log")
                    axs[j,i].set_ylim(1e-13,10)
                    if RS[i] == "0":
                       axs[j,i].set_title(compartments[j]+"\n 0-" + str(int(RS_cumLength_m[int(RS[i])]/1000))+" km distance ", y=1.0)
                    else:               
                       axs[j,i].set_title(compartments[j]+"\n "+str(int(RS_cumLength_m[int(RS[i])-1]/1000))+ "-" + str(int(RS_cumLength_m[int(RS[i])]/1000))+" km distance ", y=1.0)
                 
                    #axs[j,i].set_yscale('log')
                    axs[j,i].legend()         
       # Axis titles
        plt.text(0.1, 0.5, "Concentration of particles (Num/$m^3$)", fontsize=18, transform=plt.gcf().transFigure, rotation='vertical',ha='center', va='center')
        plt.text(0.5, 0.1, "time (days)", fontsize=18, transform=plt.gcf().transFigure, ha='center', va='center')
            
        png_label2 = 'figures/'+ "Concentration_Num_m3__aggState_"+ sizeBinLabel[o] +"_" +composition+'.png'    
        fig.savefig(png_label2) #or pdf  
            
        
        
