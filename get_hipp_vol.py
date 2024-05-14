import os
import pandas as pd 
import subprocess
import numpy as np
import sys

local_path = '/Users/williamstanford/Workspace/Lab/Projects/Neuroscience/'
cluster_path = '/proj/dayanelab/users/William/'

def get_correct_path(local_path, cluster_path):
    if os.path.exists(local_path):
        return local_path
    if os.path.exists(cluster_path):
        return cluster_path
    
path = get_correct_path(local_path, cluster_path)

sub_df = pd.read_csv(path + 'HCP-Aging/02_Raw_Data/03_Imaging/02_ppMRI/02_PreProcessed/batch_organization.csv')

labels = ['17 Left-Hippocampus 30','53 Right-Hippocampus 30']

#labels = ['17 Left-Hippocampus 30', '53 Right-Hippocampus 30']

if os.path.exists(path + '/HCP-Aging-dMRI/02_Analysis/vol_raw_df.csv'):
    vol_df = pd.read_csv(path + '/HCP-Aging-dMRI/02_Analysis/vol_raw_df.csv', index_col='SubID')
else:
    vol_df = pd.DataFrame(index=sub_df['SubID'], columns=labels)

   
for subid in vol_df.index:
    
    filepath = path + 'HCP-Aging-dMRI/00_Data/04_volume2/'+ subid + '_all_fast_firstseg'
     
    if os.path.exists(filepath +'.nii.gz'):
        print('   path exists')
        
        for label in labels:
        
            ind = label.split(' ')[0]
            ind1 = float(ind) - 0.5
            ind2 = float(ind) + 0.5
          
            comm_cmd = f"fslstats {filepath} -l {ind1} -u {ind2} -V"          
            result = subprocess.check_output(comm_cmd, shell=True)
            print(result)
          
            vol_df.loc[vol_df.index==subid, label] = str(result).split(' ')[1]
            vol_df.to_csv(path + '/HCP-Aging-dMRI/02_Analysis/vol_raw_df.csv', index='SubID')

vol_df.to_csv(path + '/HCP-Aging-dMRI/02_Analysis/vol_raw_df.csv', index='SubID')

sys.exit()
