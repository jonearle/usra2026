import pandas as pd
import matplotlib.pyplot as plt
import math
from itertools import combinations

def get_summary_metrics():
    df_summary = pd.read_csv("/Users/Jon/usra2026/data/simulations/test/summary.csv")

    summary_metrics = [
        {
            "column": "node_reach",
            "title": "Network Reach",
            "ylabel": "Node reach (%)",
            "scale": 100,
        },
        {
            "column": "mean_delay_ms",
            "title": "Mean Message Delay",
            "ylabel": "Mean delay (ms)",
            "scale": 1,
        },
        {
            "column": "collision_rate",
            "title": "Collision Rate",
            "ylabel": "Collision rate (%)",
            "scale": 100,
        },
        {
            "column": "tx_air_utilization_rate",
            "title": "TX Airtime Utilization",
            "ylabel": "Airtime utilization (%)",
            "scale": 100,
        },
        {
            "column": "transmissions_per_message",
            "title": "Transmission Overhead",
            "ylabel": "Transmissions per message",
            "scale": 1,
        },
        {
            "column": "usefulness",
            "title": "Reception Usefulness",
            "ylabel": "Useful receptions (%)",
            "scale": 100,
        },
    ]

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 8), sharex=True,)

    axes = axes.flatten()

    for ax, metric in zip(axes, summary_metrics):
        column = metric["column"]
        scale = metric["scale"]

        grouped = (df_summary.groupby("number_of_nodes")[column].mean().reset_index().sort_values("number_of_nodes"))

        x = grouped["number_of_nodes"]
        y = grouped[column] * scale

        ax.plot(x, y, marker="o", linestyle="-")

        ax.set_title(metric["title"])
        ax.set_ylabel(metric["ylabel"])
        ax.set_xticks(x)
        ax.tick_params(axis="x", labelbottom=True)
        ax.grid(alpha=0.3)

    fig.supxlabel("Number of nodes")

    fig.suptitle(
        "Mesh Network Performance by Number of Nodes",
        fontsize=16,
    )

    fig.tight_layout(rect=[0, 0, 1, 0.97])

    plt.show()

def get_min_node_distance():
    df_summary = pd.read_csv("/Users/Jon/usra2026/data/simulations/test/summary.csv")
    df_nodes = pd.read_csv("/Users/Jon/usra2026/data/simulations/test/nodes.csv", skip_blank_lines=False)

    results = []

    ### Get avg distance metrics from nodes.csv ###
    for sim_id, group in df_nodes.groupby("simulation_id"):
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

    df_distances = pd.DataFrame(results)

    min_distance_grouped = (df_distances
                .groupby("number_of_nodes", as_index=False)
                .agg(mean_distance_m=("mean_min_distance", "mean"), number_of_simulations=("sim_id", "count"),)
                .sort_values("number_of_nodes")
                )

    node_reach_grouped = (
        df_summary
        .groupby("number_of_nodes", as_index=False)
        .agg(
            mean_node_reach=("node_reach", "mean"),
        )
        .sort_values("number_of_nodes")
    )

    graph_data = node_reach_grouped.merge(min_distance_grouped, on="number_of_nodes", how="inner",)
    
    ### Now, graph the metrics ###   
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(13, 5), sharex=True)

    x = graph_data["number_of_nodes"]

    # Left graph: network reach
    axes[0].plot(x, graph_data["mean_node_reach"] * 100, marker="o", linestyle="-")
    axes[0].set_title("Network Reach")
    axes[0].set_xlabel("Number of nodes")
    axes[0].set_ylabel("Node reach (%)")
    axes[0].set_xticks(x)
    axes[0].grid(alpha=0.3)

    # Right graph: average distance
    axes[1].plot(x, graph_data["mean_distance_m"], marker="o", linestyle="-",)
    axes[1].set_title("Average Distance Between Nodes")
    axes[1].set_xlabel("Number of nodes")
    axes[1].set_ylabel("Average distance (m)")
    axes[1].set_xticks(x)
    axes[1].grid(alpha=0.3)

    fig.suptitle(
        "Network Reach and Node Distance by Network Size",
        fontsize=14,
    )

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    plt.show()

get_summary_metrics()
get_min_node_distance()