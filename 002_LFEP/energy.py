import numpy as np
import matplotlib.pyplot as plt

ENERGY_FILE = "free_energy.abf1.czar.energy"  # The input energy file containing energies along LFEP

energy_data = np.loadtxt("free_energy.abf1.czar.energy")
x = np.linspace(0, 1, len(energy_data))

# Plotting the RMSD data
plt.figure()
plt.plot(x, energy_data, marker='o', linestyle='-', color='b')
plt.title('free-energy change along LFEP')
plt.xlabel('s')
plt.ylabel('energy (kcal/mol)')
plt.grid(True)
plt.show()