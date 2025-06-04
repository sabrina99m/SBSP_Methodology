import matplotlib.pyplot as plt

# Shared setup
percent_changes = [-60, -50, -40, -30, -20, 0, 20, 30, 40, 50, 60]
hours_per_year = 8677.56
system_lifetime = 30
system_capacity_MW = 2000
baseline_cf = 0.9

# Monte Carlo mean emissions (g CO₂e/kWh)
mc_means = {
    "Si": {
        "Starship": 8.10,
        "Falcon 9": 11.28
    },
    "GaAs": {
        "Starship": 7.45,
        "Falcon 9": 9.68
    }
}

colors = {
    "Starship": "blue",
    "Falcon 9": "red"
}

def compute_cf_sensitivity(monte_carlo_mean):
    baseline_energy_output = (
        system_capacity_MW * 1e3 *
        hours_per_year *
        system_lifetime *
        baseline_cf
    )
    total_emissions = monte_carlo_mean * baseline_energy_output / 1000  # kg
    results = []
    for pct in percent_changes:
        new_cf = baseline_cf * (1 + pct / 100)
        energy_output = (
            system_capacity_MW * 1e3 *
            hours_per_year *
            system_lifetime *
            new_cf
        )
        gco2e_per_kwh = (total_emissions / energy_output) * 1000
        results.append(gco2e_per_kwh)
    return results

# side-by-side subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

# Plot for Silicon system
ax = axes[0]
for vehicle in ["Starship", "Falcon 9"]:
    results = compute_cf_sensitivity(mc_means["Si"][vehicle])
    ax.plot(
        percent_changes, results, marker='o',
        label=f"{vehicle} (mean = {mc_means['Si'][vehicle]:.2f})",
        color=colors[vehicle]
    )
    for pct, val in zip(percent_changes, results):
        if pct % 20 == 0:
            ax.annotate(f"{val:.2f}", (pct, val), textcoords="offset points",
                        xytext=(0, 8), ha='center', fontsize=8)

ax.set_title("a) Silicon System")
ax.set_xlabel("Capacity Factor Change (%)")
ax.set_ylabel("g CO₂e per kWh")
ax.grid(True)
ax.legend()

# Plot for GaAs system
ax = axes[1]
for vehicle in ["Starship", "Falcon 9"]:
    results = compute_cf_sensitivity(mc_means["GaAs"][vehicle])
    ax.plot(
        percent_changes, results, marker='o',
        label=f"{vehicle} (mean = {mc_means['GaAs'][vehicle]:.2f})",
        color=colors[vehicle]
    )
    for pct, val in zip(percent_changes, results):
        if pct % 20 == 0:
            ax.annotate(f"{val:.2f}", (pct, val), textcoords="offset points",
                        xytext=(0, 8), ha='center', fontsize=8)

ax.set_title("b) Gallium Arsenide System")
ax.set_xlabel("Capacity Factor Change (%)")
ax.grid(True)
ax.legend()


fig.suptitle("Emissions Sensitivity to Capacity Factor", fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
