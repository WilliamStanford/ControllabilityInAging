import os
import pandas as pd

local_path = '/Users/williamstanford/Workspace/Lab/Projects/Neuroscience/'
cluster_path = '/proj/dayanelab/users/William/'

def get_correct_path(local_path, cluster_path):
    if os.path.exists(local_path):
        return local_path
    if os.path.exists(cluster_path):
        return cluster_path
    
path = get_correct_path(local_path, cluster_path)

sub_df = pd.read_csv(path + 'HCP-Aging/02_Raw_Data/03_Imaging/02_ppMRI/02_PreProcessed/batch_organization.csv')

#for sub in range(720):
for sub in range(0, 710):
    
    subid = sub_df.loc[sub, 'SubID']
    
    filepath = path + 'William/HCP-Aging/02_Raw_Data/03_Imaging/01_T1w/imagingcollection01/'+subid+'_V1_MR/unprocessed/T1w_MPR_vNav_4e_e1e2_mean/'+subid+'_V1_MR_T1w_MPR_vNav_4e_e1e2_mean.nii.gz'

    o = path + 'HCP-Aging-dMRI/00_Data/04_volume2/'+ subid 
    
    if os.path.exists(o + '_all_fast_firstseg.nii.gz') == False:

        comm_cmd = f'sh fs.sh {filepath} {o}'
        print('Outputing to system the command: ' + comm_cmd)
        os.system(comm_cmd)   

# cd /proj/dayanelab/users/William//HCP-Aging-dMRI/01_Scripts/04_FS/
# sbatch -p general -N 1 -n 1 -t 02-00:00:00 --mem=5g --wrap="python fs_parallel_raw.py -logfile collect_data.out"


# fslstats '/proj/dayanelab/users/William/HCP-Aging/02_Raw_Data/03_Imaging/02_ppMRI/02_PreProcessed/subject_000/T1w_restore_brain_all_fast_firstseg' -l 16.5 -u 17.5 -V