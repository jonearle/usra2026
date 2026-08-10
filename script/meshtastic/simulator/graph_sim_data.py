import csv
import pandas as pd
import matplotlib.pyplot as plt
import math
from pathlib import Path

def set_node_count(summary_path):
    with open(summary_path, "r", encoding='utf-8', newline="") as file:
        rows = list(csv.reader(file))

    num_nodes_list = [5, 7, 10, 12, 14, 17, 22, 32, 52, 77, 102] 
    repeitions = 20
    header = rows[0]

    if header[0] == "num_nodes":
        return
    
    with open(summary_path, "w", encoding='utf-8', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["number_of_nodes"] + header)

        for i, row in enumerate(rows[1:]):
            idx = i // 20
            writer.writerow([num_nodes_list[idx]] + row)

def set_simulation_id(nodes_path):
    with open(nodes_path, "r", encoding='utf-8', newline="") as file:
        rows = list(csv.reader(file))

    sim_id = 0
    header = rows[0]

    if header[0] == "simulation_id":
        return
    
    with open(nodes_path, "w", encoding='utf-8', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["simulation_id"] + header)

        for row in rows[1:]:
            if not row or all(not value.strip() for value in row):
                writer.writerow([])
                sim_id += 1
            else:
                writer.writerow([sim_id] + row)

def graph_metrics(*file_paths, df_distances=None):
    metrics = [
        {
            "column": "node_reach",
            "title": "Network Reach",
            "ylabel": "Node reach (%)",
            "scale": 100,
            "source": "summary"
        },
        {
            "column": "mean_delay_ms",
            "title": "Mean Message Delay",
            "ylabel": "Mean delay (ms)",
            "scale": 1,
            "source": "summary"
        },
        {
            "column": "collision_rate",
            "title": "Collision Rate",
            "ylabel": "Collision rate (%)",
            "scale": 100,
            "source": "summary"
        },
        {
            "column": "tx_air_utilization_rate",
            "title": "TX Airtime Utilization",
            "ylabel": "Airtime utilization (%)",
            "scale": 100,
            "source": "summary"
        },
        {
            "column": "transmissions_per_message",
            "title": "Transmission Overhead",
            "ylabel": "Transmissions per message",
            "scale": 1,
            "source": "summary"
        },
        {
            "column": "usefulness",
            "title": "Reception Usefulness",
            "ylabel": "Useful receptions (%)",
            "scale": 100,
            "source": "summary"
        }
    ]

    df_list = []
    labels = []
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        df_list.append(df)
        labels.append(Path(file_path).parent.name)

    if df_distances is not None:
        metrics.append(
            {
                "column": "mean_distance_m",
                "title": "Mean Minimum Node Distance",
                "ylabel": "Mean minimum distance (m)",
                "scale": 1,
                "source": "distance"
            }
        )
        nrows, ncols = 3, 3
    else:
        nrows, ncols = 2, 3

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 8), sharex=True,)
    axes = axes.flatten()

    for ax, metric in zip(axes, metrics):
        column = metric["column"]
        scale = metric["scale"]

        if metric["source"] == "summary":
            for df, label in zip(df_list, labels):
                grouped = (df.groupby("number_of_nodes")[column].mean().reset_index().sort_values("number_of_nodes"))

                x = grouped["number_of_nodes"]
                y = grouped[column] * scale

                ax.plot(x, y, marker="o", linestyle="-", label=label)

        elif metric["source"] == "distance":
            for df in df_distances:
                x = df["number_of_nodes"]
                y = df["mean_distance_m"]
                ax.plot(x, y, marker="o", linestyle="-")

        ax.set_title(metric["title"])
        ax.set_ylabel(metric["ylabel"])
        ax.set_xticks(x)
        ax.tick_params(axis="x", labelbottom=True)
        ax.grid(alpha=0.3)

    if df_distances is not None:
        handles, labels = axes[0].get_legend_handles_labels()
        axes[7].axis("off")
        axes[7].legend(
            handles,
            labels,
            loc="center",
            title="Legend",
            frameon=False,
        )
        axes[8].set_visible(False)

    fig.supxlabel("Number of nodes")
    fig.suptitle(
        "Mesh Network Performance by Number of Nodes",
        fontsize=16,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.97])

    plt.show()

# Input: nodes.csv file
# Output: pandas dataframe with the mean minimum distance between nodes grouped by the number of nodes in the sim.
def get_min_node_distance(*node_paths):
    df_list_nodes = []
    df_list_distances = []
    df_list_distances_grouped = []

    for node_path in node_paths:
        df_list_nodes.append(pd.read_csv(node_path))

    ### Get avg distance metrics from nodes.csv ###
    for df in df_list_nodes:
        results = []

        for sim_id, group in df.groupby("simulation_id"):
            coords = list(zip(group["node_id"], group["x_position_m"], group["y_position_m"]))
            number_of_nodes = len(coords)
            
            min_distances = []
            for node_id, x, y in coords:
                node_distances = []
                for other_id, x_other, y_other in coords:
                    if node_id == other_id:
                        continue
                    distance = math.hypot(x_other - x, y_other - y)
                    node_distances.append(distance)
                min_distances.append(min(node_distances))

            mean_min_distance = sum(min_distances) / len(min_distances)
            results.append({
                "sim_id": sim_id,
                "number_of_nodes": number_of_nodes,
                "mean_min_distance": mean_min_distance
            })

        df_list_distances.append(pd.DataFrame(results))

    for df in df_list_distances:
        df_list_distances_grouped.append(df
                                .groupby("number_of_nodes", as_index=False)
                                .agg(mean_distance_m=("mean_min_distance", "mean"), number_of_simulations=("sim_id", "count"),)
                                .sort_values("number_of_nodes")
                                )

    print(df_list_distances_grouped)
    return df_list_distances_grouped

#set_node_count("/Users/Jon/usra2026/data/simulations/default_config/summary.csv")
#set_simulation_id("/Users/Jon/usra2026/data/simulations/default_config/nodes.csv")

df_distances = get_min_node_distance(
    "/Users/Jon/usra2026/data/simulations/halifax_random_3hop/nodes.csv",
    "/Users/Jon/usra2026/data/simulations/halifax_random_7hop/nodes.csv"
)
graph_metrics(
    "/Users/Jon/usra2026/data/simulations/halifax_random_3hop/summary.csv",
    "/Users/Jon/usra2026/data/simulations/halifax_random_7hop/summary.csv" ,
    df_distances=df_distances
)