import matplotlib.pyplot as plt

# Shared setup
percent_changes = [-60, -50, -40, -30, -20, 0, 20, 30, 40, 50, 60]

# System parameters for energy output calculation
system_capacity_MW = 2000       
hours_per_year = 8677.56        
system_lifetime = 30            
baseline_cf = 0.9               

# Baseline emissions (kg CO2e)
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

# Monte Carlo mean emissions (g CO2e/kWh)
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

def compute_energy_output(cf):
    """Calculate total energy output over system lifetime in kWh."""
    return system_capacity_MW * 1e3 * hours_per_year * system_lifetime * cf

def compute_satellite_sensitivity(launch, satellite, rectenna, mc_mean):
    # Calculate baseline energy output using baseline capacity factor
    baseline_energy_output = compute_energy_output(baseline_cf)
    
    # Baseline total emissions in kg CO2e
    baseline_total_emissions = launch + satellite + rectenna
    
    # Calculate baseline gCO2e/kWh
    baseline_gco2e = (baseline_total_emissions / baseline_energy_output) * 1000
    
    # Scale factor to match MC mean emissions
    scale_factor = mc_mean / baseline_gco2e
    
    results = []
    for pct in percent_changes:
        # Vary satellite emissions only
        varied_satellite = satellite * (1 + pct / 100)
        
        # Total emissions after scaling
        total_emissions = (launch + varied_satellite + rectenna) * scale_factor
        
        # gCO2e per kWh with fixed energy output
        gco2e_per_kwh = (total_emissions / baseline_energy_output) * 1000
        results.append(gco2e_per_kwh)
    return results

# Create side-by-side subplots with shared y-axis
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

# Plot for Silicon system
ax = axes[0]
for vehicle in ["Starship", "Falcon 9"]:
    emissions = configs["Si"][vehicle]
    results = compute_satellite_sensitivity(
        emissions["launch"], emissions["satellite"], emissions["rectenna"],
        mc_means["Si"][vehicle]
    )
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
ax.set_xlabel("Satellite Emissions Change (%)")
ax.set_ylabel("g CO₂e per kWh")
ax.set_ylim(6, 13)
ax.grid(True)
ax.legend()

# Plot for GaAs system
ax = axes[1]
for vehicle in ["Starship", "Falcon 9"]:
    emissions = configs["GaAs"][vehicle]
    results = compute_satellite_sensitivity(
        emissions["launch"], emissions["satellite"], emissions["rectenna"],
        mc_means["GaAs"][vehicle]
    )
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
ax.set_xlabel("Satellite Emissions Change (%)")
ax.set_ylim(6, 13)
ax.grid(True)
ax.legend()


fig.suptitle("Emissions Sensitivity to Satellite Emissions", fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

