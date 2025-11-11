#!/bin/bash
#SBATCH --job-name=three_arm_md
#SBATCH --output=three_arm_%j.out
#SBATCH --error=three_arm_%j.err
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --partition=phd_student
#SBATCH --qos=phd_student

module purge
module load openmpi-4.1.5
module load lammps-openmpi
module load anaconda3

echo "Starting 3-Arm Polymer Simulation"
echo "LAMMPS path: $(which lmp)"
echo "Date: $(date)"
echo "=========================================="

# ? use absolute path to LAMMPS binary
mpirun -np 1 /apps/codes/lammps-29Aug2024/bin/lmp -in alpha_polymer.in

if [ $? -eq 0 ]; then
    echo "SUCCESS: LAMMPS simulation completed!"
else
    echo "ERROR: LAMMPS simulation failed!"
fi

echo "Job completed at: $(date)"
