# packages
import pandas as pd
import numpy as np
from glob import glob
import os 


#### 0. Function to combine daily flows
def allowDictionary(proj, dict_name, loc):
    files = [f for f in sorted(glob('../../Timeseries/%s/%s*' % (loc,proj)))  ]
    allQ = pd.DataFrame()
    for f in files:
        df = pd.read_csv(f)
        allQ["P" + f.split("_")[2]] = df['flow']
    allQ.index = pd.to_datetime(df.date)
    dict_name[proj] = allQ
    return dict_name
    
#### 1. Set Up

# Define Filepaths
fpath_dps = '../../Timeseries/DPS_MEF'
# fpath_uc = '../../Timeseries/UC'
fpath_d = '../../Extremes/DPS_MEF'
# fpath_u = '../Extremes/Uncontrolled'

# List of Projections
projections = np.unique([f.split("_")[0] for f in os.listdir(fpath_dps)])
print(projections)
print(len(projections), " # of projections")


# Initialize Empty Dictionaries
DPS = dict.fromkeys(projections)
DPS_7Q = dict.fromkeys(projections)
DPS_AMS = dict.fromkeys(projections)
# UC = dict.fromkeys(projections)
# UC_7Q = dict.fromkeys(projections)
# UC_AMS = dict.fromkeys(projections)


# Populate / Initialize Dictionaries
for proj in projections:
    try:
        DPS[proj] = pd.read_csv(os.path.join(fpath_d, f'{proj}_DailyFlows.csv'), parse_dates=True, index_col = 'date')
    except:
        DPS = allowDictionary(proj, DPS, "DPS_MEF")
        DPS[proj].to_csv(os.path.join(fpath_d, f'{proj}_DailyFlows.csv'))
        # UC = allowDictionary(proj, UC, "Uncontrolled") 
    DPS_7Q[proj] = pd.DataFrame()
    
    # UC[proj] = pd.read_csv(os.path.join(fpath_u,'%s_DailyFlows.csv' % proj), parse_dates=True, index_col = 'date')
    # UC_7Q[proj] = pd.DataFrame()


#### 2. Low Flow and High Flows 
def sevenQ(df, col, endYear):
    """Seven day low flow calculator"""
    df['Year'] = df.index.year
    nyears = endYear - df['Year'][0]
    years = np.arange(df['Year'][0], df['Year'][0] + nyears, 1) 
    min7dayQ = np.zeros(nyears)
    for i,year in enumerate(years):
        yearlyFlows = df[col][np.where(df['Year']==year)[0]]
        sevenDayQ = np.zeros(len(yearlyFlows)-7+1)
        for j in range(len(sevenDayQ)):
            sevenDayQ[j] = np.sum(yearlyFlows[j:(j+7)])
        min7dayQ[i] = np.min(sevenDayQ)
    return min7dayQ

# loop through projections
for proj in  projections:
    # find annual maxima for each policy
    DPS_AMS[proj] = DPS[proj].resample("Y").max()
    DPS_AMS[proj].to_csv(os.path.join(fpath_d, f'{proj}_AMS.csv'))
    print(proj)
    # calculate seven day low flow for each policy
    for col in DPS[proj].columns:
        DPS_7Q[proj][col] = sevenQ(DPS[proj], col, 2100)
    # format dataframe and save to csv
    DPS_7Q[proj].index = range(2019, 2100)
    DPS_7Q[proj].to_csv(os.path.join(fpath_d, f'{proj}_7Q.csv'))


# UNCONTROLLEd

# Define Filepaths
fpath_uc = '../../Timeseries/RedoUncontrolled'
fpath_u = '../../Extremes/RedoUncontrolled'

# List of Projections
projections = np.unique([f.split("_")[0] for f in os.listdir(fpath_uc)])
print(projections)
print(len(projections), " # of projections")


# Initialize Empty Dictionaries
UC = dict.fromkeys(projections)
UC_7Q = dict.fromkeys(projections)
UC_AMS = dict.fromkeys(projections)


# Populate / Initialize Dictionaries
for proj in projections:
    try:
        UC[proj] = pd.read_csv(os.path.join(fpath_u,'%s_DailyFlows.csv' % proj), parse_dates=True, index_col = 'date')  
    except:
        UC = allowDictionary(proj, UC, "Uncontrolled") 
    UC_7Q[proj] = pd.DataFrame()


# loop through projections
for proj in  projections:
    # find annual maxima for each policy
    UC_AMS[proj] = UC[proj].resample("Y").max()
    UC_AMS[proj].to_csv(os.path.join(fpath_u, f'{proj}_AMS.csv'))
    print(proj)
    # calculate seven day low flow for each policy
    for col in UC[proj].columns:
        UC_7Q[proj][col] = sevenQ(UC[proj], col, 2100)
    # format dataframe and save to csv
    UC_7Q[proj].index = range(2019, 2100)
    UC_7Q[proj].to_csv(os.path.join(fpath_u, f'{proj}_7Q.csv'))





