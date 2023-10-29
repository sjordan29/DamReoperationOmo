import pandas as pd
import os 
    


def print_dict(dict_name):
    '''
    sorts keys by their values  
    '''
    dict1 = {x: dict_name[x] for x in dict_name if x not in ['Year']}
    sorted_dict = {}
    sorted_keys = sorted(dict1, key=dict1.get, reverse=False)  # [1, 3, 2]

    for w in sorted_keys:
        sorted_dict[w] = dict1[w]
        
    keys = [f for f in sorted_dict.keys()]

    return keys


def sort_dry_to_wet(projections, fpath_ts= '../../Timeseries/Uncontrolled'):
    '''
    sorts projections from wet to dry 
    '''
    UC_ts = dict.fromkeys(projections)
    for proj in projections:
        UC_ts[proj] = pd.read_csv(os.path.join(fpath_ts, '%s_UC_Flow.csv' % proj), index_col = 'Unnamed: 0')
    
    UC_mean = dict.fromkeys(projections)
    for proj in projections:
        UC_mean[proj] = UC_ts[proj]['flow'].mean()

    sorted_projs = print_dict(UC_mean)

    return sorted_projs


