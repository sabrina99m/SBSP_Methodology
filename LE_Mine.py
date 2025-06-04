import matplotlib.pyplot as plt

# Setup 
percent_changes = [-60, -50, -40, -30, -20, 0, 20, 30, 40, 50, 60]
energy_output = 469_588_240_000  # kWh

# Baseline emissions  (kg CO2e) 
configs = {
    "Si": {
        "Starship": {
            "launch": 779_976_500,
            "satellite": 222_878_364,
            "rectenna": 2_473_433_488
        },
        "Falcon 9": {
            "launch": 2_200_916_551,
            "satellite": 222_878_364,
            "rectenna": 2_473_433_488
        }
    },
    "GaAs": {
        "Starship": {
            "launch": 522_160_000,
            "satellite": 221_113_832,
            "rectenna": 2_473_433_488
        },
        "Falcon 9": {
            "launch": 1_473_844_037,
            "satellite": 221_113_832,
            "rectenna": 2_473_433_488
        }
    }
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


colors = {
    "Starship": {"Si": "blue", "GaAs": "blue"},
    "Falcon 9": {"Si": "red", "GaAs": "red"}
}

#  Sensitivity Function 
def compute_sensitivity(launch_emissions, satellite_emissions, rectenna_emissions, mc_mean):
    base_total = launch_emissions + satellite_emissions + rectenna_emissions
    baseline_g_per_kwh = (base_total / energy_output) * 1000
    scale = mc_mean / baseline_g_per_kwh

    results = []
    for pct in percent_changes:
        launch_adj = launch_emissions * (1 + pct / 100)
        total = (launch_adj + satellite_emissions + rectenna_emissions) * scale
        g_per_kwh = (total / energy_output) * 1000
        results.append(g_per_kwh)
    return results

#  Annotation points
annotation_points = [-60, -40, -20, 20, 40, 60]

#  Create side-by-side subplots 
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)
fig.suptitle("Emissions Sensitivity to Launch Emissions", fontsize=14)

# Subplot a): Silicon 
ax = axes[0]
for system in ["Starship", "Falcon 9"]:
    emissions = configs["Si"][system]
    results = compute_sensitivity(
        emissions["launch"], emissions["satellite"], emissions["rectenna"],
        mc_means["Si"][system]
    )
    ax.plot(percent_changes, results, marker='o', color=colors[system]["Si"],
            label=f"{system} (mean = {mc_means['Si'][system]:.2f})")
    
    for pct in annotation_points:
        val = results[percent_changes.index(pct)]
        x_offset = 8 if pct < 0 else 0
        ha = 'left' if pct < 0 else 'center'
        y_offset = 12

        ax.annotate(f"{val:.2f}", (pct, val), textcoords="offset points",
                    xytext=(x_offset, y_offset), ha=ha, fontsize=9, color='black')

ax.set_title("a) Silicon System")
ax.set_xlabel("Launch Emissions Change (%)")
ax.set_ylabel("g CO₂e per kWh")
ax.set_ylim(6, 15)
ax.grid(True)
ax.legend()

# === Subplot b): Gallium Arsenide (GaAs) ===
ax = axes[1]
for system in ["Starship", "Falcon 9"]:
    emissions = configs["GaAs"][system]
    results = compute_sensitivity(
        emissions["launch"], emissions["satellite"], emissions["rectenna"],
        mc_means["GaAs"][system]
    )

    ax.plot(percent_changes, results, marker='o', color=colors[system]["GaAs"],
            label=f"{system} (mean = {mc_means['GaAs'][system]:.2f})")
    
    
    for pct in annotation_points:
        val = results[percent_changes.index(pct)]
        x_offset = 8 if pct < 0 else 0
        ha = 'left' if pct < 0 else 'center'
        y_offset = 12

        ax.annotate(f"{val:.2f}", (pct, val), textcoords="offset points",
                    xytext=(x_offset, y_offset), ha=ha, fontsize=9, color='black')
  
ax.set_title("b) Gallium Arsenide System")
ax.set_xlabel("Launch Emissions Change (%)")
ax.grid(True)
ax.set_ylim(6, 15)
ax.legend()


plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

