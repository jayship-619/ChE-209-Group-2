#!/usr/bin/env python3
"""
Three-Arm Polymer with Terminal Loops - G-Factor Analysis
Based on Cantarella et al. (2022)
For comparison between theoretical and simulated structures
"""

import numpy as np
import matplotlib.pyplot as plt

# === MODIFY THIS VALUE if needed ===
# Total number of atoms from your LAMMPS data file
NUM_ATOMS = 120

# Theoretical g-factor obtained from your graph analysis script
EXPECTED_G_FACTOR = 0.877   # <-- updated to the value you provided

def analyze_gyration_data(filename="gyration_three_arm.txt", num_atoms=NUM_ATOMS):
    """Analyze radius of gyration data for the 3-arm polymer with loops."""
    
    print("=" * 65)
    print("3-ARM POLYMER WITH TERMINAL LOOPS — G-FACTOR ANALYSIS")
    print(f"Analyzing polymer with {num_atoms} atoms.")
    print(f"Theoretical g-factor (graph model): {EXPECTED_G_FACTOR}")
    print("=" * 65)
    
    try:
        # --- Load Rg data ---
        data = np.loadtxt(filename)
        timesteps = data[:, 0]
        rg_values = data[:, 1]

        # --- Equilibrated average (last 50% of data) ---
        start_idx = len(rg_values) // 2
        eq_rg = rg_values[start_idx:]
        avg_rg = np.mean(eq_rg)
        std_rg = np.std(eq_rg)

        print(f"Simulation timesteps: {int(timesteps[-1])}")
        print(f"Total points: {len(rg_values)}, Equilibrated region: {len(eq_rg)} points")
        print("-" * 60)

        # --- G-factor calculation ---
        rg_sq_sim = avg_rg ** 2

        # theoretical mean-square Rg for a linear chain of same length (Cantarella et al.)
        v = float(num_atoms)
        d = 3.0
        rg_sq_linear = (d * v / 6.0) * ((v + 1.0) / (v - 1.0))

        actual_g = rg_sq_sim / rg_sq_linear
        diff = abs(actual_g - EXPECTED_G_FACTOR)

        # --- Output results ---
        print("RESULTS")
        print(f"Average Rg (sim):        {avg_rg:.3f} ± {std_rg:.3f}")
        print(f"<Rg²> (sim):             {rg_sq_sim:.3f}")
        print(f"<Rg²> (linear chain):    {rg_sq_linear:.3f}")
        print(f"Calculated g-factor:     {actual_g:.3f}")
        print(f"Theoretical g-factor:    {EXPECTED_G_FACTOR:.3f}")
        print(f"Difference:              {diff:.3f}")

        if diff < 0.05:
            print("✅ Excellent: matches theoretical prediction.")
        elif diff < 0.10:
            print("✅ Good: close to expected value.")
        else:
            print("⚠️  Needs review: significant deviation.")
        print("-" * 60)

        # --- Plot results ---
        plt.figure(figsize=(12, 8))

        # Rg vs time
        plt.subplot(2, 1, 1)
        plt.plot(timesteps, rg_values, 'b-', alpha=0.7, label='Rg vs Time')
        plt.axhline(avg_rg, color='r', ls='--', lw=2, label=f'Avg Rg = {avg_rg:.3f}')
        plt.axvline(timesteps[start_idx], color='g', ls=':', label='Equilibration Start')
        plt.xlabel('Timestep')
        plt.ylabel('Radius of Gyration')
        plt.title('3-Arm Polymer with Loops: Radius of Gyration vs Time')
        plt.legend()
        plt.grid(alpha=0.3)

        # Histogram
        plt.subplot(2, 1, 2)
        plt.hist(eq_rg, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        plt.axvline(avg_rg, color='r', ls='--', lw=2, label=f'Mean = {avg_rg:.3f}')
        plt.xlabel('Radius of Gyration')
        plt.ylabel('Frequency')
        plt.title('Distribution of Equilibrated Rg Values')
        plt.legend()
        plt.grid(alpha=0.3)

        plt.tight_layout()
        plt.savefig('three_arm_rg_analysis.png', dpi=300)
        print("Plot saved as: three_arm_rg_analysis.png")

        # --- Save summary ---
        with open('three_arm_g_factor_results.txt', 'w') as f:
            f.write(f"3-ARM POLYMER WITH LOOPS G-FACTOR ANALYSIS ({num_atoms} atoms)\n")
            f.write("=" * 55 + "\n")
            f.write(f"Average Rg (simulated):   {avg_rg:.6f} ± {std_rg:.6f}\n")
            f.write(f"Calculated g-factor:      {actual_g:.6f}\n")
            f.write(f"Theoretical g-factor:     {EXPECTED_G_FACTOR:.6f}\n")
            f.write(f"Difference:               {diff:.6f}\n")
            f.write(f"Simulation timesteps:     {int(timesteps[-1])}\n")
            f.write(f"Data points analyzed:     {len(eq_rg)}\n")

        print("Summary saved as: three_arm_g_factor_results.txt")

        return actual_g, avg_rg, std_rg

    except FileNotFoundError:
        print(f"❌ ERROR: {filename} not found! Ensure LAMMPS simulation output exists.")
        return None, None, None
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return None, None, None

# ==========================================================
if __name__ == "__main__":
    g_factor, avg_rg, std_rg = analyze_gyration_data()

    if g_factor is not None:
        print("\n" + "=" * 60)
        print("3-ARM POLYMER WITH LOOPS — ANALYSIS COMPLETE ✅")
        print(f"Final g-factor: {g_factor:.3f}  (Theory: {EXPECTED_G_FACTOR:.3f})")
        print("=" * 60)
