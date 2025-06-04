import matplotlib.pyplot as plt

#  Setup 
percent_changes = [-60, -50, -40, -30, -20, 0, 20, 30, 40, 50, 60]
hours_per_year = 8677.56
system_lifetime = 30
system_capacity_MW = 2000
capacity_factor = 0.9

baseline_energy_output = (
    system_capacity_MW * 1e3 *
    hours_per_year *
    system_lifetime *
    capacity_factor
)

#  Fixed Emissions 
launch_emissions = {
    "Starship": {
        "Si": 779_976_500,
        "GaAs": 522_160_000
    },
    "Falcon 9": {
        "Si": 2_200_916_551,
        "GaAs": 1_473_844_037
    }
}

satellite_emissions = {
    "Si": 222_878_364,
    "GaAs": 221_113_832
}

rectenna_emissions = 2_473_433_488

# Monte Carlo Means 
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

#  Total Emissions 
def compute_total_emissions(tech, system):
    return (
        launch_emissions[system][tech] +
        satellite_emissions[tech] +
        rectenna_emissions
    )

#  Sensitivity Function 
def compute_energy_sensitivity(tech, system):
    baseline_total = compute_total_emissions(tech, system)
    baseline_gco2e = (baseline_total / baseline_energy_output) * 1000
    scale_factor = mc_means[tech][system] / baseline_gco2e

    results = []
    for pct in percent_changes:
        varied_energy_output = baseline_energy_output * (1 + pct / 100)
        gco2e_per_kwh = (baseline_total * scale_factor / varied_energy_output) * 1000
        results.append(gco2e_per_kwh)
    return results


colors = {
    "Starship": {"Si": "blue", "GaAs": "red"},
    "Falcon 9": {"Si": "red", "GaAs": "blue"}
}

# Annotation settings 
annotation_points = [-60, -40, -20, 20, 40, 60]

#  side-by-side subplots 
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)
fig.suptitle("Emissions Sensitivity to Total Energy Produced", fontsize=14)

# Subplot a): Silicon
ax = axes[0]
for system in ["Starship", "Falcon 9"]:
    results = compute_energy_sensitivity("Si", system)
    ax.plot(percent_changes, results, marker='o', color=colors[system]["Si"],
            label=f"{system} (mean = {mc_means['Si'][system]:.2f})")
    
    for pct in annotation_points:
        val = results[percent_changes.index(pct)]
        x_offset = 8 if pct < 0 else 0
        ha = 'left' if pct < 0 else 'center'
        y_offset = 6 if pct == -60 else 12 

        ax.annotate(f"{val:.2f}", (pct, val), textcoords="offset points",
                    xytext=(x_offset, y_offset), ha=ha, fontsize=9, color='black')

ax.set_title("a) Silicon System")
ax.set_xlabel("Energy Output Change (%)")
ax.set_ylabel("g CO₂e per kWh")
ax.grid(True)
ax.legend()

#  Subplot b): GaAs
ax = axes[1]
for system in ["Starship", "Falcon 9"]:
    results = compute_energy_sensitivity("GaAs", system)
    ax.plot(percent_changes, results, marker='o', color=colors[system]["GaAs"],
            label=f"{system} (mean = {mc_means['GaAs'][system]:.2f})")
    
    for pct in annotation_points:
        val = results[percent_changes.index(pct)]
        x_offset = 8 if pct < 0 else 0
        ha = 'left' if pct < 0 else 'center'

        if system == "Falcon 9" and pct == -60:
            y_offset = 6
        elif system == "Starship" and pct in [20, 40, 60]:
            y_offset = -12  
        else:
            y_offset = 12

        ax.annotate(f"{val:.2f}", (pct, val), textcoords="offset points",
                    xytext=(x_offset, y_offset), ha=ha, fontsize=9, color='black')

ax.set_title("b) Gallium Arsenide System")
ax.set_xlabel("Energy Output Change (%)")
ax.grid(True)
ax.legend()



plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
