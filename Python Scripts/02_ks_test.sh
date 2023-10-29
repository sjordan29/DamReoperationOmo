#!/bin/bash
#SBATCH -D /scratch/smj5vup/omoScenarios/BestPolicyEachObjCC/PythonScripts/MEF # working directory
#SBATCH -o /scratch/smj5vup/omoScenarios/BestPolicyEachObjCC/PythonScripts/MEF/output/ks-test.out   # Name of the output file (eg. myMPI.oJobID)
#SBATCH -N 1
#SBATCH --ntasks-per-node 1
#SBATCH -p dev          				# Queue name "dev"
#SBATCH -A quinnlab_paid       					# allocation name
#SBATCH -t 1:00:00       					# Run time (hh:mm:ss) - up to 36 hours // 1 hr for dev queue 
#SBATCH --mail-user=smjordan329@gmail.com      # address for email notification
#SBATCH --mail-type=ALL                  	# email at Begin and End of job


module load gcc
module load anaconda

srun python 02_KS_test.py