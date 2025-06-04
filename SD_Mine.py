import matplotlib.pyplot as plt

# === Constants ===
percent_changes = [-60, -50, -40, -30, -20, 0, 20, 30, 40, 50, 60]
baseline_energy_output = 469_588_240_000  # kWh 

# === Emissions (kg CO2e)
configs = {
    "Si": {
        "Starship": {
            "monte_carlo_mean": 8.10,
            "color": "blue"
        },
        "Falcon 9": {
            "monte_carlo_mean": 11.28,
            "color": "red"
        }
    },
    "GaAs": {
        "Starship": {
            "monte_carlo_mean": 7.45,
            "color": "blue"
        },
        "Falcon 9": {
            "monte_carlo_mean": 9.68,
            "color": "red"
        }
    }
}

# === Compute sensitivity function
def compute_sensitivity(monte_carlo_mean):
    total_emissions = monte_carlo_mean * baseline_energy_output / 1000  # kg CO₂e
    return [
        (total_emissions / (baseline_energy_output * (1 + pct / 100))) * 1000
        for pct in percent_changes
    ]

# === Plot setup
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)
fig.suptitle("Emissions Sensitivity to System Delivery", fontsize=14)

# === Annotate only these points
annotation_points = [-60, -40, -20, 20, 40, 60]

# === Subplot (a): Silicon
ax = axes[0]
for vehicle, params in configs["Si"].items():
    results = compute_sensitivity(params["monte_carlo_mean"])
    ax.plot(percent_changes, results, marker='o',
            label=f"{vehicle} (mean = {params['monte_carlo_mean']:.2f})",
            color=params["color"])

    for pct in annotation_points:
        if pct in percent_changes:
            val = results[percent_changes.index(pct)]
            x_offset = 8 if pct < 0 else 0
            ha = 'left' if pct < 0 else 'center'

            
            if pct == -60:
                y_offset = 6
            else:
                y_offset = 12

            ax.annotate(f"{val:.2f}", (pct, val),
                        textcoords="offset points",
                        xytext=(x_offset, y_offset),
                        ha=ha, fontsize=9, color='black')

ax.set_title("a) Silicon System")
ax.set_xlabel("System Delivery Change (%)")
ax.set_ylabel("g CO₂e per kWh")
ax.grid(True)
ax.legend()

# === Subplot (b): GaAs
ax = axes[1]
for vehicle, params in configs["GaAs"].items():
    results = compute_sensitivity(params["monte_carlo_mean"])
    ax.plot(percent_changes, results, marker='o',
            label=f"{vehicle} (mean = {params['monte_carlo_mean']:.2f})",
            color=params["color"])

    for pct in annotation_points:
        if pct in percent_changes:
            val = results[percent_changes.index(pct)]
            x_offset = 8 if pct < 0 else 0
            ha = 'left' if pct < 0 else 'center'

            
            if vehicle == "Starship" and pct in [20, 40, 60]:
                y_offset = -12
            elif pct == -60:
                y_offset = 6
            else:
                y_offset = 12

            ax.annotate(f"{val:.2f}", (pct, val),
                        textcoords="offset points",
                        xytext=(x_offset, y_offset),
                        ha=ha, fontsize=9, color='black')

ax.set_title("b) Gallium Arsenide System")
ax.set_xlabel("System Delivery Change (%)")
ax.grid(True)
ax.legend()


plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
