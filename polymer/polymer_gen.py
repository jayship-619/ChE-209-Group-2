#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a LAMMPS data file for a 3-arm polymer where each arm ends in a loop.
Each loop is detached - no shared atom or central atom inside the loop.
"""

import math

def generate_three_arm_loop_polymer(
    atoms_per_arm=3,
    atoms_per_loop=4,
    bond_length=0.5,
    box_size=20.0,
    output_file="three_arm_polymer.data",
    dimension="3D"
):
    """
    Generates a LAMMPS data file for a 3-arm polymer with detached loops.
    Each loop is a ring (no center atom, no bond to the arm).
    """
    assert atoms_per_arm >= 1, "atoms_per_arm must be >=1"
    assert atoms_per_loop >= 3, "atoms_per_loop must be >=3"
    dim3 = (dimension.upper() == "3D")

    atom_lines = []
    bond_lines = []
    atom_id = 0
    bond_id = 0

    # Central junction
    atom_id += 1
    central_id = atom_id
    z0 = 0.1 if dim3 else 0.0
    atom_lines.append((central_id, 1, 1, 0.0, 0.0, z0))

    # Arm directions (120 degrees apart)
    angles = [0.0, 2 * math.pi / 3, 4 * math.pi / 3]

    for arm_idx, theta in enumerate(angles):
        ux = math.cos(theta)
        uy = math.sin(theta)
        prev_id = central_id

        # Linear arm
        for i in range(1, atoms_per_arm + 1):
            atom_id += 1
            x = ux * (i * bond_length)
            y = uy * (i * bond_length)
            z = (0.01 * i if dim3 else 0.0)
            atom_lines.append((atom_id, 1, 1, x, y, z))
            bond_id += 1
            bond_lines.append((bond_id, 1, prev_id, atom_id))
            prev_id = atom_id

        # Detached ring loop
        n = atoms_per_loop
        R = bond_length / (2.0 * math.sin(math.pi / n))

        # Slightly offset loop away from arm
        center_x = (ux * (atoms_per_arm * bond_length)) + R * ux * 1.2
        center_y = (uy * (atoms_per_arm * bond_length)) + R * uy * 1.2
        center_z = z0 if not dim3 else z0 + 0.05 * (arm_idx + 1)

        # Tangent and perpendicular vectors
        u = (ux, uy)
        v = (-uy, ux)
        loop_ids = []

        for k in range(n):
            phi = 2.0 * math.pi * k / n
            x = center_x + R * (math.cos(phi) * u[0] + math.sin(phi) * v[0])
            y = center_y + R * (math.cos(phi) * u[1] + math.sin(phi) * v[1])
            z = center_z + (0.02 * math.sin(phi) if dim3 else 0.0)

            # Only ring atoms (no central atom)
            atom_id += 1
            atom_lines.append((atom_id, 1, 1, x, y, z))
            loop_ids.append(atom_id)

        # Bonds around the ring
        for idx in range(n):
            a1 = loop_ids[idx]
            a2 = loop_ids[(idx + 1) % n]
            bond_id += 1
            bond_lines.append((bond_id, 1, a1, a2))

    # Write LAMMPS data file
    total_atoms = len(atom_lines)
    total_bonds = len(bond_lines)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("LAMMPS data file - 3-arm polymer with detached terminal loops\n\n")
        f.write(f"{total_atoms} atoms\n")
        f.write(f"{total_bonds} bonds\n")
        f.write("0 angles\n0 dihedrals\n0 impropers\n\n")
        f.write("1 atom types\n1 bond types\n\n")
        f.write(f"0.0 {box_size} xlo xhi\n0.0 {box_size} ylo yhi\n0.0 {box_size} zlo zhi\n\n")

        f.write("Masses\n\n1 12.011 # atom type 1 (example)\n\n")
        f.write("Atoms\n\n")

        for a in atom_lines:
            aid, molid, atype, x, y, z = a
            f.write(f"{aid} {molid} {atype} {x:.6f} {y:.6f} {z:.6f}\n")

        f.write("\nBonds\n\n")
        for b in bond_lines:
            bid, btype, i, j = b
            f.write(f"{bid} {btype} {i} {j}\n")

    print("? LAMMPS data file generated successfully!")
    print(f"Filename: {output_file}")
    print(f"Total atoms: {total_atoms}")
    print(f"Total bonds: {total_bonds}")
    print("Structure: 1 central junction, 3 arms, 3 detached ring loops (no bonds or center atoms).")


if __name__ == "__main__":
    generate_three_arm_loop_polymer(
        atoms_per_arm=3,
        atoms_per_loop=4,
        bond_length=0.5,
        box_size=20.0,
        output_file="three_arm_polymer.data",
        dimension="3D"
    )
