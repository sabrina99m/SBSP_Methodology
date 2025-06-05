import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
import seaborn as sns
import sys

print(sys.executable)
np.random.seed(42)

# Monte Carlo Sampling Function using truncated normal 
def sample_trunc_normal(mean, std_frac=0.25, size=10000):
    std_dev = mean * std_frac
    lower, upper = 1, np.inf
    a, b = (lower - mean) / std_dev, (upper - mean) / std_dev
    samples = truncnorm.rvs(a, b, loc=mean, scale=std_dev, size=size)
    return samples

#  Input Parameters for Si and GaAs Configurations 
starship_si = {
    "energy_output": 469_588_240_000,
    "launch_emissions": 779_976_500,
    "satellite_emissions": 222_878_364,
    "rectenna_emissions": 2_473_433_488
}

starship_gaas = starship_si.copy()
starship_gaas["launch_emissions"] = 522_160_000
starship_gaas["satellite_emissions"] = 221_113_832

falcon9_si = {
    "energy_output": 469_588_240_000,
    "launch_emissions": 2_200_916_551,
    "satellite_emissions": 222_878_364,
    "rectenna_emissions": 2_473_433_488
}

falcon9_gaas = falcon9_si.copy()
falcon9_gaas["launch_emissions"] = 1_473_844_037
falcon9_gaas["satellite_emissions"] = 221_113_832

# Monte Carlo Simulation Function 
def run_monte_carlo(params):
    energy_samples = sample_trunc_normal(params["energy_output"])
    launch_emissions_samples = sample_trunc_normal(params["launch_emissions"])
    satellite_emissions_samples = sample_trunc_normal(params["satellite_emissions"])
    rectenna_emissions_samples = sample_trunc_normal(params["rectenna_emissions"])

    total_emissions_samples = (
        launch_emissions_samples +
        satellite_emissions_samples +
        rectenna_emissions_samples
    )

    emissions_g_per_kWh = (total_emissions_samples / energy_samples) * 1000
    return emissions_g_per_kWh

#  Summary Statistics Function 
def summarize(data):
    return {
        "mean": np.mean(data),
        "median": np.median(data),
        "5th_percentile": np.percentile(data, 5),
        "95th_percentile": np.percentile(data, 95),
        "std": np.std(data)
    }

# Run Simulations 
results = {
    "Starship (Si)": run_monte_carlo(starship_si),
    "Starship (GaAs)": run_monte_carlo(starship_gaas),
    "Falcon9 (Si)": run_monte_carlo(falcon9_si),
    "Falcon9 (GaAs)": run_monte_carlo(falcon9_gaas)
}

summaries = {k: summarize(v) for k, v in results.items()}

# Print Results 
for name, summary in summaries.items():
    print(f"\n{name} Monte Carlo: Emissions per kWh (g CO₂e)")
    for k, v in summary.items():
        print(f"  {k.replace('_', ' ').capitalize()}: {v:.2f}")

# Plotting: STARSHIP 
fig_starship, axs = plt.subplots(1, 2, figsize=(14, 5))
colors = ['skyblue', 'navy']
starship_keys = ["Starship (Si)", "Starship (GaAs)"]

for i, key in enumerate(starship_keys):
    sns.histplot(results[key], bins='auto', kde=True, color=colors[i], ax=axs[i])
    axs[i].axvline(summaries[key]["mean"], color='red', linestyle='dashed', linewidth=2,
                   label=f'Mean = {summaries[key]["mean"]:.2f}')
    axs[i].set_title(f"{key}: Emissions per kWh")
    axs[i].set_xlabel("g CO₂e per kWh")
    axs[i].set_ylabel("Frequency")
    axs[i].set_xlim(0, 60)
    axs[i].grid(True)
    axs[i].legend()

fig_starship.suptitle("Starship Monte Carlo Simulations", fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

#  Plotting: FALCON 9 
fig_falcon9, axs = plt.subplots(1, 2, figsize=(14, 5))
colors = ['orange', 'darkred']
falcon_keys = ["Falcon9 (Si)", "Falcon9 (GaAs)"]

for i, key in enumerate(falcon_keys):
    sns.histplot(results[key], bins='auto', kde=True, color=colors[i], ax=axs[i])
    axs[i].axvline(summaries[key]["mean"], color='red', linestyle='dashed', linewidth=2,
                   label=f'Mean = {summaries[key]["mean"]:.2f}')
    axs[i].set_title(f"{key}: Emissions per kWh")
    axs[i].set_xlabel("g CO₂e per kWh")
    axs[i].set_ylabel("Frequency")
    axs[i].set_xlim(0, 60)
    axs[i].grid(True)
    axs[i].legend()

fig_falcon9.suptitle("Falcon 9 Monte Carlo Simulations", fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# Save the plot to the desktop
plt.savefig("Falcon 9 Monte Carlo Simulations.png")
