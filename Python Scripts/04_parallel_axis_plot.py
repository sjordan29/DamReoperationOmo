# -*- coding: utf-8 -*-
"""
Created 6/21/2021, modified 1/26/2023 for paper

@author: Sarah Jordan, Julianne Quinn

Make parallel axis of DPS reservoir operating policies 
"""

# packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from utilities import ROBUST_POLICY_LIST


# read in UC and DPS
uc = pd.read_csv('files/Uncontrolled_Historical.obj', sep=' ', names =  ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'])
uc['source'] = 'Uncontrolled'
dps = pd.read_csv('files/DPS_ReferenceSet.reference', sep=' ', names =  ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'])
dps['source'] = 'Optimized'

uc_dps_all = pd.concat([dps, uc])

def FindBetterPolicies(uc_dps_all, uc):
    pols = []
    for i in range(len(uc_dps_all.index)):
        better = True
        for col in uc_dps_all.columns.tolist():
            if uc_dps_all[col].iloc[i] > uc[col].iloc[0]:
                better = False
                break
        if better == True:
            pols.append(i)
            
    return pols  

better_pols = FindBetterPolicies(uc_dps_all, uc)

print(better_pols)

def PAP(ax, df, better_pols, title, lgd, cmap, brushed=True):
    
    cmap = matplotlib.cm.get_cmap(cmap)

    table = df[['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton']]

    # Scale the data to minimum and maximum values 
    scaled = table.copy()
    for column in table.columns:
        if column != 'Source':
            mm = df[column].min()
            mx = df[column].max()
            scaled[column] = (table[column] - mm) / (mx - mm)
    
    # Plot all of the policies 
    d = 0
    u = 0
    for i,solution in enumerate(scaled.iterrows()):
        ys = solution[1]
        xs = range(len(ys - 1))
        if df['source'].iloc[i]=='Optimized':
            d +=1
            col = cmap(ys[1]) # shade by environmental objective
            ls = "solid"
            if d == 1:
                lbl = 'Optimized'
            else:
                lbl = ""
        else:
            u += 1
            col = 'black'
            ls = "dashed"
            if u == 1:
                lbl = 'Uncontrolled'
            else:
                lbl = ""
            
        if brushed == True:
            if i in better_pols:
                ax.plot(xs, ys, c=col, linewidth = 2, linestyle=ls, label=lbl)
            else:
                ax.plot(xs, ys, c=col, linewidth = 1, linestyle=ls, label=lbl, alpha=0.3)
        else:
            ax.plot(xs, ys, c=col, linewidth = 2, linestyle=ls, label=lbl)

    # Format the figure

    ax.annotate('', xy=(-0.14, 0.15), xycoords='axes fraction', xytext=(-0.14, 0.85),
        arrowprops=dict(arrowstyle="->", color='black'))

    ax.set_xticks(np.arange(0,np.shape(table)[1],1))
    ax.set_xlim([0,np.shape(table)[1]-1])
    ax.set_ylim([0,1])

    ax.set_ylabel("Scaled Objective Values",fontsize=16)
    # ax.set_xticks([0,1,2,3,4])
    ax.set_xticklabels(["Hydropower", "Environment", "Recession", "Sugar", "Cotton"],fontsize=16)

    ax.tick_params(labelsize=14)
    ax.tick_params(axis='y',which='both',labelleft='off',left='off',right='off')
    ax.tick_params(axis='x',which='both',top='off',bottom='off')

    #cbar = fig.colorbar()
    #cbar.ax.set_xticklabels(['10','15','20','25','30'])
    #fig.axes[-1].set_xlabel('Scaled Environmental Flows Objective',fontsize=14)
    
    # make subplot frames invisible
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    # draw in axes
    for i in np.arange(0,np.shape(table)[1],1):
        ax.plot([i,i],[0,1],c='k')

    # ax.set_title("Policy Source", size=18)
    ax.set_title(title)
    if lgd == True:
        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=2)


fpath = './'



# find sources of combined Pareto Set 

sns.set(style="white")
fig, (ax1) = plt.subplots(1, 1)
fig.set_size_inches([8, 5])

PAP(ax1, uc_dps_all, better_pols, "", True, "RdYlGn_r")

fig.savefig("Figures/testing/BrushedSet.png")
plt.clf()

sns.set(style="white")
fig, (ax1) = plt.subplots(1, 1)
fig.set_size_inches([8, 5])

PAP(ax1, uc_dps_all, better_pols, "", True, "RdYlGn_r", False)

fig.savefig("Figures/testing/UnbrushedSet.png")
plt.clf()