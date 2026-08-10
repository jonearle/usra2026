import pandas as pd
import matplotlib.pyplot as plt


def get_neighbor_summary(file_path):
    df = pd.read_csv(file_path, skip_blank_lines=True)

    # Average direct neighbours within each simulation
    simulations = (
        df.groupby("simulation_id")
        .agg(
            number_of_nodes=("node_id", "count"),
            average_neighbors=("direct_neighbor_count", "mean")
        )
        .reset_index()
    )

    # Average across repeated simulations of the same node count
    summary = (
        simulations
        .groupby("number_of_nodes")["average_neighbors"]
        .mean()
        .reset_index()
        .sort_values("number_of_nodes")
    )

    return summary


file_1000m = "/Users/Jon/usra2026/data/simulations/box_1000m/nodes.csv"
file_2000m = "/Users/Jon/usra2026/data/simulations/box_2000m/nodes.csv"

summary_1000m = get_neighbor_summary(file_1000m)
summary_2000m = get_neighbor_summary(file_2000m)


plt.figure(figsize=(10, 6))

plt.plot(
    summary_1000m["number_of_nodes"],
    summary_1000m["average_neighbors"],
    marker="o",
    label="1000 m"
)

plt.plot(
    summary_2000m["number_of_nodes"],
    summary_2000m["average_neighbors"],
    marker="o",
    label="2000 m"
)

plt.xlabel("Number of Nodes")
plt.ylabel("Average Number of Direct Neighbours")
plt.title("Average Direct Neighbours by Network Size")
plt.xticks(summary_1000m["number_of_nodes"])
plt.grid(alpha=0.3)
plt.legend()

plt.tight_layout()
plt.show()