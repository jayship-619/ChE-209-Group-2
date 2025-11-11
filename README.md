# 🧬 Polymer Simulation Project

## 📁 Project Structure
```
Latest/
├── alpha_polymer.in              # LAMMPS input script for polymer simulation
├── compute.py                    # Python script for analyzing simulation data
├── gyration.txt                  # Output file containing radius of gyration or related data
├── log.lammps                    # LAMMPS log file with simulation details
├── polymer_gen.py                # Script for generating polymer structures
├── run_simulation.sh             # Shell script to run the simulation
├── three_arm_4247.err            # Error log from simulation
├── three_arm_4247.out            # Output log from simulation
├── three_arm_polymer.data        # LAMMPS data file defining the polymer
└── trajectory_three_arm.lammpstrj # LAMMPS trajectory file for visualization
```

## 🧠 Project Overview
This repository contains input files, scripts, and output data for simulating a **three-arm polymer** using **LAMMPS**.
The goal of the project is to:
- Generate a branched polymer structure.
- Run molecular dynamics simulations.
- Analyze structural properties such as **radius of gyration (Rg)** and the **G factor**.

## ⚙️ How to Run the Simulation
1. **Generate the polymer structure:**
   ```bash
   python polymer_gen.py
   ```

2. **Run the simulation in LAMMPS:**
   ```bash
   bash run_simulation.sh
   ```
   or manually:
   ```bash
   lmp_serial < alpha_polymer.in
   ```

3. **Analyze the results:**
   ```bash
   python compute.py
   ```

## 📊 Output Files
- **trajectory_three_arm.lammpstrj** — Atomistic trajectory from LAMMPS (for visualization in OVITO or VMD).
- **gyration.txt** — Contains computed values of the radius of gyration or related metrics.
- **three_arm_4247.out / .err** — Log files for debugging and verifying simulation runs.

## 🧩 Dependencies
- [LAMMPS](https://www.lammps.org/)
- Python 3.x
  - numpy
  - matplotlib (optional for visualization)

