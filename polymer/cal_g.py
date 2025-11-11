import numpy as np

# Load the data
rg1 = np.loadtxt('rg_leash.txt')   # columns: step, Rg
rg2 = np.loadtxt('rg_tree.txt')

# Extract columns
steps1, rg_values1 = rg1[:,0], rg1[:,1]
steps2, rg_values2 = rg2[:,0], rg2[:,1]

# Make sure they have the same steps
if not np.array_equal(steps1, steps2):
    raise ValueError("Timestep mismatch between rg1.txt and rg2.txt")

# Compute averages
avg_rg1 = np.mean(rg_values1)
avg_rg2 = np.mean(rg_values2)
s
# Compute per-step difference and mean difference
rg_diff = rg_values2 - rg_values1
mean_diff = np.mean(rg_diff)

print(f"Average Rg (File 1): {avg_rg1:.4f}")
print(f"Average Rg (File 2): {avg_rg2:.4f}")
print(f"Mean difference (Rg2 - Rg1): {mean_diff:.4f}")

g_factor = (((avg_rg1/avg_rg2)**2))*((91/87)**(1.176))
print(f'Contraction factor g(G∞/Gtree∞) : {g_factor}')

# Optional: Save the difference to a new file
np.savetxt("rg_difference.txt", np.column_stack((steps1, rg_diff)),
           header="Step  Rg_diff(Rg2 - Rg1)")
