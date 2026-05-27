import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

attributes = ["rssi", "snr", "latency", "deliveryRate"]

# Data
data = {
    "elevated_short_turbo": pd.read_csv("/Users/Jon/USRA2026/data/wickwire_inside_elevated/short_turbo.csv"),

    "elevated_long_fast": pd.read_csv("/Users/Jon/USRA2026/data/wickwire_inside_elevated/long_fast.csv"),

    "noelevation_short_turbo": pd.read_csv("/Users/Jon/USRA2026/data/wickwire_inside_noelevation/short_turbo.csv"),

    "noelevation_long_fast": pd.read_csv("/Users/Jon/USRA2026/data/wickwire_inside_noelevation/long_fast.csv"),

    "outside_short_turbo": pd.read_csv("/Users/Jon/USRA2026/data/wickwire_outside/short_turbo.csv"),

    "outside_long_fast": pd.read_csv("/Users/Jon/USRA2026/data/wickwire_outside/long_fast.csv")
}

for attribute in attributes:
    plt.figure()

    for name, df in data.items():
        x = np.arange(len(df[attribute]))
        y = df[attribute]

        # Polynomial fit
        coefficients = np.polyfit(x, y, 3)
        curve = np.poly1d(coefficients)

        # Original data
        plt.plot(x, y, alpha=0.6)

        # Plot curve
        plt.plot(x, curve(x), label=name, linewidth=2)

    plt.xlabel("Time")
    plt.ylabel(attribute)
    plt.title(f"Measured {attribute}")
    plt.legend()
    plt.tight_layout()
    plt.show()





