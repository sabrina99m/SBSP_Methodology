import matplotlib.pyplot as plt

# Setup 
percent_changes = [-60, -50, -40, -30, -20, 0, 20, 30, 40, 50, 60]
hours_per_year = 8677.56
system_lifetime = 30
system_capacity_MW = 2000
capacity_factor = 0.9

energy_output = (
    system_capacity_MW * 1e3 *
    hours_per_year *
    system_lifetime *
    capacity_factor
)

#  Fixed Launch and Satellite Emissions 
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
    "Si": 380_486_488,
    "GaAs": 563_543_885
}

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

# Baseline Rectenna Emissions 
baseline_rectenna_emissions = 2_473_433_488

# Sensitivity Function for Rectenna Emissions 
def compute_rectenna_sensitivity(tech, system):
    baseline_total = (
        launch_emissions[system][tech] +
        satellite_emissions[tech] +
        baseline_rectenna_emissions
    )
    baseline_gco2e = (baseline_total / energy_output) * 1000
    scale_factor = mc_means[tech][system] / baseline_gco2e

    results = []
    for pct in percent_changes:
        varied_rectenna = baseline_rectenna_emissions * (1 + pct / 100)
        total_emissions = (
            launch_emissions[system][tech] +
            satellite_emissions[tech] +
            varied_rectenna
        ) * scale_factor
        gco2e_per_kwh = (total_emissions / energy_output) * 1000
        results.append(gco2e_per_kwh)
    return results


colors = {
    "Starship": {"Si": "blue", "GaAs": "blue"},
    "Falcon 9": {"Si": "red", "GaAs": "red"}
}

# Annotation points to show 
annotation_points = [-60, -40, -20, 20, 40, 60]

# Create side-by-side subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)
fig.suptitle("Sensitivity to Rectenna Emissions", fontsize=14)

#  Plot Silicon System 
ax = axes[0]
for system in ["Starship", "Falcon 9"]:
    results = compute_rectenna_sensitivity("Si", system)
    ax.plot(percent_changes, results, marker='o', color=colors[system]["Si"],
            label=f"{system} (mean = {mc_means['Si'][system]:.2f})")

    for pct in annotation_points:
        val = results[percent_changes.index(pct)]
        x_offset = 8 if pct < 0 else 0
        ha = 'left' if pct < 0 else 'center'
        y_offset = 10
        ax.annotate(f"{val:.2f}", (pct, val), textcoords="offset points",
                    xytext=(x_offset, y_offset), ha=ha, fontsize=9, color='black')

ax.set_title("a) Silicon System")
ax.set_xlabel("Rectenna Emissions Change (%)")
ax.set_ylabel("g CO₂e per kWh")
ax.grid(True)
ax.set_ylim(4, 16)
ax.legend()

#  Plot GaAs System 
ax = axes[1]
for system in ["Starship", "Falcon 9"]:
    results = compute_rectenna_sensitivity("GaAs", system)
    ax.plot(percent_changes, results, marker='o', color=colors[system]["GaAs"],
            label=f"{system} (mean = {mc_means['GaAs'][system]:.2f})")

    for pct in annotation_points:
        val = results[percent_changes.index(pct)]
        x_offset = 8 if pct < 0 else 0
        ha = 'left' if pct < 0 else 'center'
        y_offset = 10
        ax.annotate(f"{val:.2f}", (pct, val), textcoords="offset points",
                    xytext=(x_offset, y_offset), ha=ha, fontsize=9, color='black')

ax.set_title("b) Gallium Arsenide System")
ax.set_xlabel("Rectenna Emissions Change (%)")
ax.grid(True)
ax.set_ylim(4, 16)
ax.legend()


plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
