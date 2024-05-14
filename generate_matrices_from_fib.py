import subprocess #allows us to run the shell 
import glob #for dir searching
import os

import scipy.io as sio
import pandas as pd
import numpy as np
from scipy.io import savemat


local_path = '/Users/williamstanford/Workspace/Lab/Projects/Neuroscience/HCP-Aging-dMRI/'
cluster_path = '/proj/dayanelab/users/William/HCP-Aging-dMRI/'

def get_correct_path(local_path, cluster_path):
    if os.path.exists(local_path):
        return local_path    
    if os.path.exists(cluster_path):        
        return cluster_path
    
path  = get_correct_path(local_path, cluster_path)
data_path = path + "00_Data/HCP_A720_fib/"
analysis_path = path + "02_Analysis/"
sc_path = path + "00_Data/00_structural_connectomes/"

# Find files in current directory
srcFiberFiles=glob.glob(data_path+"*.fib.gz") 

atlas = 'schaefer'
norm = 'count'
fib = 'pass'


# Perform fiber tracking and generate connectivity matrices, network stats, and connectogram
for ind, file in enumerate(srcFiberFiles):
    
    if ind % 50 == 0:
        print('Processing subject: ' +str(ind))
       
    # if len(glob.glob(data_path+'*' + atlas + "." + norm + "." + fib + "*.mat")) == 0:
    
    # Output in shell
    TrackingCallInfo = "\
       /Applications/dsi_studio.app/Contents/MacOS/dsi_studio --action='trk' --source="+file+"\
       --seed_count=5000000 --connectivity_type="+fib+"\
       --connectivity_threshold=0.0001 --connectivity_value="+norm+"\
       --connectivity="+atlas+" --output='no_file'"
           
        # Call shell 
    subprocess.call(TrackingCallInfo, shell=True) 


# Find matrices
matFiles=glob.glob(data_path+'*' + atlas + "." + norm + "." + fib + "*.mat")
matFiles.sort()

mat = sio.loadmat(matFiles[0])['connectivity']
file = matFiles[0]



subs = []
sub_dict = {}
group_mat = np.zeros(((len(matFiles), mat.shape[0], mat.shape[1])))

for ind, file in enumerate(matFiles):
    subs.append(file.split('/')[-1].split('.')[0])
    mat = sio.loadmat(file)['connectivity']
    group_mat[ind, :,:] = mat
 
mat_dict = {
    'subs':subs,
    'group_matrix':group_mat}

# Saves with naming convention HCP + atlas + edge weighting + edges considered + type 
np.save(sc_path + 'HCP_'+file.split('tt.gz.')[1].replace(".", "_")+".npy", mat_dict)


savemat(sc_path + 'HCP_'+file.split('tt.gz.')[1].replace(".", "_")+".mat", mat_dict)

    
  
