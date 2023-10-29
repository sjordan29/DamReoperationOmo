import pandas as pd
import numpy as np
import os
import json 
from projection_utilities import sort_dry_to_wet

### Define Paths 

# Timeseries - Projected Uncontrolled and Res Ops
fpath_dps = '../../Timeseries/DPS_MEF/'
fpath_uc = '../../Timeseries/UC'

# Extremes - Projected Uncontrolled and Res Ops
fpath_d = '../../Extremes/DPS_MEF/'
fpath_u = '../../Extremes/Uncontrolled'

# Historical Uncontrolled
HUC_7Q = pd.read_csv('../../../Historical/Extremes/UC_7Q.csv', index_col = 'Unnamed: 0')
HUC_AMS = pd.read_csv('../../../Historical/Extremes/Uncontrolled_AMS.csv', index_col = 'date')
HUC_historical = pd.read_csv('../../../Historical/Timeseries/Uncontrolled/Historical_00_Flow.csv', parse_dates=True, index_col = 'date')



# Projections
PROJECTIONS = np.unique([f.split("_")[0] for f in os.listdir(fpath_dps)])
SORTED_PROJECTIONS = sort_dry_to_wet(PROJECTIONS)
PROJECTION_COLOR_DICTIONARY = {}
for projection,i in zip(SORTED_PROJECTIONS, range(len(PROJECTIONS))):
    PROJECTION_COLOR_DICTIONARY[projection] = i/47

# Colors
COLOR_DICTIONARY = {
    "High Flow Policy": 0.75,
    "Low Flow Policy": 0.25,
    "Compromise Policy": 0.5,
}

with open('results/robust-policies.json') as json_file:
    ROBUST_POLICIES = json.load(json_file)
    
with open('results/all_robust_policies.json') as json_file:
    ALL_ROBUST_POLICIES = json.load(json_file)
    
with open('results/low_flow_projections.json') as json_file:
    LOW_FLOW_PROJECTIONS = json.load(json_file)
    
with open('results/high_flow_projections.json') as json_file:
    HIGH_FLOW_PROJECTIONS = json.load(json_file)
    
    
with open('results/low_flow_trends.json') as json_file:
    LOW_FLOW_TRENDS = json.load(json_file)
    
with open('results/high_flow_trends.json') as json_file:
    HIGH_FLOW_TRENDS = json.load(json_file)

ROBUST_POLICY_LIST = [ROBUST_POLICIES[f] for f in ROBUST_POLICIES.keys()]
# Flows Class

class Flows:
    def __init__(self, scenario_string, index_col, historical_uncontrolled_timeseries, time_period="Mid", extremes=True):
        # policies 
        self.all_flows = dict.fromkeys(PROJECTIONS)
        self.flows = dict.fromkeys(PROJECTIONS)

        # uncontrolled
        self.historical_uncontrolled_timeseries = historical_uncontrolled_timeseries
        if extremes == True:
                self.historical_uncontrolled_timeseries.index = pd.date_range(start='1/1/1989', end='1/01/2018', freq='AS')
        else:
                self.historical_uncontrolled_timeseries.index = pd.date_range(start='1/1/1989', end='12/31/2018')
            
        self.puc_all_flows = dict.fromkeys(PROJECTIONS)
        self.puc_flows = dict.fromkeys(PROJECTIONS)
        
        # policies + uncontrolled
        self.all_flow_scenarios = dict.fromkeys(PROJECTIONS)

        # all scenario dataframe
        self.scenarios = dict.fromkeys(PROJECTIONS)

        # define dataframe for given time period
        if time_period == "Mid":
            start = 2040
            end = 2070
        else:
            start = 2070 
            end = 2100        
        for proj in PROJECTIONS:
            # read data
            self.all_flows[proj] = pd.read_csv(os.path.join(fpath_d, f'{proj}_{scenario_string}.csv'), parse_dates=True, index_col = index_col)
            self.puc_all_flows[proj] = pd.read_csv(os.path.join(fpath_u, f'{proj}_{scenario_string}.csv'), parse_dates=True, index_col = index_col)

            # limit timeframe
            self.flows[proj] = self._limit_flows(self.all_flows, proj, start, end)
            self.puc_flows[proj] = self._limit_flows(self.puc_all_flows, proj, start, end)

            self.scenarios[proj] = pd.concat([self.flows[proj], self.puc_flows[proj]], axis=1)
            self.all_flow_scenarios[proj] = pd.concat([self.all_flows[proj], self.puc_all_flows[proj]], axis=1)
            

    def _limit_flows(self, df, proj, start, end):
        return df[proj][(df[proj].index.year >= start) & (df[proj].index.year <= end-1)]




### 5. Control Policy
class ControlPolicy:
    projections = PROJECTIONS
    
    def __init__(self, fpath_extremes):
        self.sevenQ = Scenario(self.projections, fpath_extremes, "7Q", 'Unnamed: 0', HUC_7Q, 0.25, "Low Flows")
        self.ams =  Scenario(self.projections, fpath_extremes, "AMS", 'date', HUC_AMS, 0.75, "High Flows")
        self.policies = [f for f in self.sevenQ.all_flows['ACCESS1-0.rcp45'].columns if f != 'Year']
        self.compromise = Compromise(self.policies, 0.5, "Compromise")
        
        
## Other Functions 
def ecdf(data):
    """ Compute ECDF """
    x = np.sort(data)
    n = x.size
    y = np.arange(1, n+1) / n
    return(x,y)