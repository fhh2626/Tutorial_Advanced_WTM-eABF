import numpy as np
import matplotlib.pyplot as plt

HIST_PMF_FILE = "output/free_energy.abf1.hist.pmf"  # The input hist.pmf file containing pmfs at different time points

def calculate_rmsd(pmf_data):
    """Calculate the RMSD from the given PMF data."""
    return np.sqrt(np.sum(np.array(pmf_data) ** 2) / len(pmf_data))

def read_hist_pmf_file(file_path):
    """Read the PMF data from the given HIST_PMF_FILE and calculate RMSD."""
    rmsd_data = [0]
    pmf_data = []

    with open(file_path, 'r') as hist_file:
        for line in hist_file:
            line = line.strip()
            if not line:
                continue

            if line.startswith('#'):
                splited_line = line.split()
                num_skip_lines = int(splited_line[1])
                for _ in range(num_skip_lines):
                    next(hist_file)  # Skip the specified number of lines

                if pmf_data:
                    rmsd_data.append(calculate_rmsd(pmf_data))
                    pmf_data = []

            else:
                pmf_data.append(float(line.split()[-1]))

        # Handle the last block of PMF data
        if pmf_data:
            rmsd_data.append(calculate_rmsd(pmf_data))

    return rmsd_data

rmsd_data = read_hist_pmf_file(HIST_PMF_FILE)

# Plotting the RMSD data
plt.figure()
plt.plot(rmsd_data, marker='o', linestyle='-', color='b')
plt.title('RMSD Over Time')
plt.xlabel('Time Point Index')
plt.ylabel('RMSD')
plt.grid(True)
plt.show()