# AI generated code

import pandas as pd
import matplotlib.pyplot as plt


def get_average_tx_airtime(file_path):
    df = pd.read_csv(
        file_path,
        skip_blank_lines=True
    )

    # Total TX airtime across all nodes in each simulation
    simulation_results = (
        df.groupby("simulation_id")
        .agg(
            number_of_nodes=("node_id", "count"),
            total_tx_airtime_ms=("tx_airtime_ms", "sum")
        )
        .reset_index()
    )

    # Average total TX airtime for each node count
    summary = (
        simulation_results
        .groupby("number_of_nodes")["total_tx_airtime_ms"]
        .mean()
        .reset_index(name="average_tx_airtime_ms")
        .sort_values("number_of_nodes")
    )

    return summary


# CSV files
file_3hop = "/Users/Jon/usra2026/data/simulations/halifax_random_3hop/nodes.csv"
file_7hop = "/Users/Jon/usra2026/data/simulations/halifax_random_7hop/nodes.csv"

# Calculate averages
summary_3hop = get_average_tx_airtime(file_3hop)
summary_7hop = get_average_tx_airtime(file_7hop)


# Graph
plt.figure(figsize=(10, 6))

plt.plot(
    summary_3hop["number_of_nodes"],
    summary_3hop["average_tx_airtime_ms"],
    marker="o",
    label="3 hop"
)

plt.plot(
    summary_7hop["number_of_nodes"],
    summary_7hop["average_tx_airtime_ms"],
    marker="o",
    label="7 hop"
)

plt.title("Average Total TX Airtime by Number of Nodes")
plt.xlabel("Number of Nodes")
plt.ylabel("Average Total TX Airtime per Simulation (ms)")

# Include all node counts from either file
all_node_counts = sorted(
    set(summary_3hop["number_of_nodes"])
    | set(summary_7hop["number_of_nodes"])
)

plt.xticks(all_node_counts)

plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()


print("3 hop:")
print(summary_3hop)

print("\n7 hop:")
print(summary_7hop)