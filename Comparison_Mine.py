import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Data
sources = [
    "Starship (Si)",
    "Starship (GaAs)",
    "Falcon 9 (Si)",
    "Falcon 9 (GaAs)",
    "Coal",
    "Natural Gas",
    "Solar PV",
    "Wind",
    "Hydropower",
    "Nuclear"
]

# Updated: Use median values instead of means
medians = [
    7.47,  # Starship (Si)
    6.87,  # Starship (GaAs)
    10.42, # Falcon 9 (Si) 
    8.93,  # Falcon 9 (GaAs) 
    820,
    490,
    48,
    11,
    24,
    12
]

# Standard deviations or error bars
errors = [
    5.26,
    4.05,
    4.55,
    3.99,
    100,
    50,
    20,
    10,
    10,
    5
]


bar_colors = ['tab:red', 'tab:red', 'tab:green', 'tab:green'] + ['grey'] * 6

# Sort by emission values
sorted_data = sorted(zip(medians, errors, sources, bar_colors), key=lambda x: x[0])
sorted_medians, sorted_errors, sorted_sources, sorted_colors = zip(*sorted_data)

# Plotting
plt.figure(figsize=(14, 6))
bars = plt.bar(sorted_sources, sorted_medians, yerr=sorted_errors, capsize=5, color=sorted_colors)
plt.ylabel("Median g CO₂e / kWh")
plt.title("Emissions Comparison (Sorted by Median Emissions)")
plt.xticks(rotation=45)

# Annotate each bar with median value
for bar, median, err in zip(bars, sorted_medians, sorted_errors):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + err + 5,
        f"{median:.2f}",
        ha='center', va='bottom', fontsize=9
    )

# Add legend explaining annotations
median_patch = mpatches.Patch(color='none', label='Numbers shown are median emission values')
plt.legend(handles=[median_patch], loc='upper left')

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
