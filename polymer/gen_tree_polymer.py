import numpy as np
import os
import sys

# -----------------------------
# Check command-line arguments
# -----------------------------
if len(sys.argv) < 2:
    print("\nUsage: star.py [output_folder]\n")
    sys.exit(0)

# Output directory
output_folder = sys.argv[1]

# -----------------------------
# PARAMETERS
# -----------------------------
num_primary_arms = 3      # number of arms from core
arm_length = 10            # beads per primary arm
branch_arms = 2           # number of secondary arms per end
branch_length = 10         # beads per secondary arm
initial_spacing = 1.1     # spacing between beads
angle_primary = 2 * np.pi / num_primary_arms
angle_branch = 2 * np.pi / (branch_arms + 1)
box_size = 50.0           # simulation box size

# -----------------------------
# GENERATE ATOMS AND BONDS
# -----------------------------
positions = [np.array([0.0, 0.0, 0.0])]  # Core
atom_types = [1]
bonds = []
atom_id = 1

# Primary arms
for i in range(num_primary_arms):
    angle = i * angle_primary
    prev_id = 1  # Core atom ID
    for j in range(arm_length):
        x = (j + 1) * initial_spacing * np.cos(angle)
        y = (j + 1) * initial_spacing * np.sin(angle)
        z = 0.0
        positions.append(np.array([x, y, z]))
        if j == arm_length - 1  : 
         atom_types.append(1)
        else : 
         atom_types.append(2)
        atom_id += 1
        bonds.append([1, prev_id, atom_id])  # bond type 1 for main arm
        prev_id = atom_id

    # Secondary branches from end of primary arm
    end_id = prev_id
    end_pos = positions[end_id - 1]
    for k in range(branch_arms):
        branch_angle = k * angle_branch - (angle_branch / 2)
        prev_branch_id = end_id
        for b in range(branch_length):
            x_b = end_pos[0] + (b + 1) * initial_spacing * np.cos(angle + branch_angle)
            y_b = end_pos[1] + (b + 1) * initial_spacing * np.sin(angle + branch_angle)
            z_b = (b + 1) * 0.5 * initial_spacing  # small z offset
            positions.append(np.array([x_b, y_b, z_b]))
            if b == branch_length - 1:
                atom_types.append(1)
            else: 
               atom_types.append(2)
               
            atom_id += 1

            # Bond type 2 for secondary arms
            bonds.append([2, prev_branch_id, atom_id])
            prev_branch_id = atom_id

# -----------------------------
# WRITE LAMMPS DATA FILE
# -----------------------------
natoms = len(positions)
nbonds = len(bonds)
atom_types_unique = len(set(atom_types))
bond_types_unique = len(set([b[0] for b in bonds]))

with open("tree.data", "w") as f:
    # Header
    f.write("LAMMPS data file for branched Tree polymer\n\n")
    f.write(f"{natoms} atoms\n")
    f.write(f"{nbonds} bonds\n")
    f.write(f"{atom_types_unique} atom types\n")
    f.write(f"{bond_types_unique} bond types\n\n")

    # Box dimensions
    f.write(f"0.0 {box_size:.3f} xlo xhi\n")
    f.write(f"0.0 {box_size:.3f} ylo yhi\n")
    f.write(f"0.0 {box_size:.3f} zlo zhi\n\n")

    # Atoms section
    f.write("Atoms\n\n")
    for i, pos in enumerate(positions, start=1):
        # Format: atom-ID molecule-ID atom-type x y z
        f.write(f"{i} 1 {atom_types[i-1]} {pos[0]+box_size/2:.4f} {pos[1]+box_size/2:.4f} {pos[2]+box_size/2:.4f}\n")

    # Bonds section
    f.write("\nBonds\n\n")
    for i, bond in enumerate(bonds, start=1):
        bond_type, a1, a2 = bond
        f.write(f"{i} {bond_type} {a1} {a2}\n")

print(f"Generated 'tree.data' successfully .")