import os
import pandas as pd 
import sys
import subprocess


subj_id=sys.argv[1]

# comm_cmd = "module add fsl/6.0.5"
# subprocess.call(comm_cmd, shell=True) 

# comm_cmd = f"subj_id=${subj_id}"
# subprocess.call(comm_cmd, shell=True) 

T_brain='/nas/longleaf/apps/fsl/6.0.5/fsl/data/standard/MNI152_T1_1mm_brain'

# comm_cmd = "T_brain=${FSLDIR}/data/standard/MNI152_T1_1mm_brain"
# subprocess.call(comm_cmd, shell=True) 

SUBJECTS_DIR='/proj/dayanelab/users/William/HCP-Aging/02_Raw_Data/03_Imaging/01_T1w_all'

# comm_cmd = f"SUBJECTS_DIR=/proj/dayanelab/users/William/HCP-Aging/02_Raw_Data/03_Imaging/01_T1w_all"
# subprocess.call(comm_cmd, shell=True) 

# -f fractional intensity threshold
comm_cmd = f"bet {SUBJECTS_DIR}/{subj_id}_V1_MR_T1w_MPR_vNav_4e_e1e2_mean.nii.gz {SUBJECTS_DIR}/{subj_id}_braintmp -f 0.2"
subprocess.call(comm_cmd, shell=True) 

comm_cmd = f"fast -b --nopve {SUBJECTS_DIR}/{subj_id}_braintmp"
subprocess.call(comm_cmd, shell=True) 

comm_cmd = f"fslmaths {SUBJECTS_DIR}/{subj_id}_V1_MR_T1w_MPR_vNav_4e_e1e2_mean.nii.gz -div {SUBJECTS_DIR}/{subj_id}_braintmp_bias {SUBJECTS_DIR}/{subj_id}_biascorrected"
subprocess.call(comm_cmd, shell=True) 

comm_cmd = f"bet {SUBJECTS_DIR}/{subj_id}_biascorrected {SUBJECTS_DIR}/{subj_id}_brain -f 0.3"
subprocess.call(comm_cmd, shell=True) 

comm_cmd = f"flirt -in {SUBJECTS_DIR}/{subj_id}_brain -ref {T_brain} -omat {SUBJECTS_DIR}/{subj_id}_brain_to_T_brain.mat"
subprocess.call(comm_cmd, shell=True) 

comm_cmd = f"fast {SUBJECTS_DIR}/{subj_id}_brain"
subprocess.call(comm_cmd, shell=True) 


sys.exit()