import numpy as np
import re

# -------- Read Group 2 simulation data (this polymer) --------
gyration_file = "gyration.txt"
data = np.loadtxt(gyration_file, comments="#")
rg_values = data[:, 1]

mean_rg2_polymer = np.mean(rg_values ** 2)
mean_rg_polymer = np.mean(rg_values)

# -------- Read Group 1 reference results from RESULTS_SUMMARY.txt --------
summary_file = "RESULTS_SUMMARY.txt"
with open(summary_file, "r") as f:
    text = f.read()

# Extract Mean Rg² and Mean Rg from the reference group using regex
ref_rg2_match = re.search(r"Mean Rg²\s*=\s*([\d.]+)", text)
ref_rg_match = re.search(r"Mean Rg\s*=\s*([\d.]+)", text)

if ref_rg2_match:
    mean_rg2_ref = float(ref_rg2_match.group(1))
else:
    raise ValueError("Couldn't find Mean Rg² in RESULTS_SUMMARY.txt")

if ref_rg_match:
    mean_rg_ref = float(ref_rg_match.group(1))
else:
    raise ValueError("Couldn't find Mean Rg in RESULTS_SUMMARY.txt")

# -------- Calculate g-factor --------
g_factor = mean_rg2_polymer / mean_rg2_ref

# -------- Display results --------
print("=== G-Factor Calculation ===")
print(f"Mean Rg (this polymer): {mean_rg_polymer:.4f}")
print(f"Mean ⟨Rg²⟩ (this polymer): {mean_rg2_polymer:.4f}")
print(f"Reference ⟨Rg²⟩: {mean_rg2_ref:.4f}")
print(f"\nContraction Factor g = ⟨Rg²⟩_polymer / ⟨Rg²⟩_reference = {g_factor:.4f}")

if g_factor < 1:
    print("→ The polymer is more compact than the reference (g < 1).")
else:
    print("→ The polymer is more expanded than the reference (g > 1).")
