# AI generated code

import pandas as pd
import matplotlib.pyplot as plt


def get_packet_summary(file_path):
    df = pd.read_csv(file_path, skip_blank_lines=True)

    simulations = (
        df.groupby("simulation_id")
        .agg(
            number_of_nodes=("node_id", "count"),
            messages_created=("messages_created", "sum"),
            packets_sent=("packets_sent", "sum")
        )
        .reset_index()
    )

    summary = (
        simulations
        .groupby("number_of_nodes")
        .agg(
            average_messages_created=("messages_created", "mean"),
            average_packets_sent=("packets_sent", "mean")
        )
        .reset_index()
        .sort_values("number_of_nodes")
    )

    return summary


file_3hop = "/Users/Jon/usra2026/data/simulations/halifax_random_3hop/nodes.csv"
file_7hop = "/Users/Jon/usra2026/data/simulations/halifax_random_7hop/nodes.csv"

summary_3hop = get_packet_summary(file_3hop)
summary_7hop = get_packet_summary(file_7hop)

summary_3hop["packets_per_message"] = (
    summary_3hop["average_packets_sent"]
    / summary_3hop["average_messages_created"]
)

summary_7hop["packets_per_message"] = (
    summary_7hop["average_packets_sent"]
    / summary_7hop["average_messages_created"]
)

plt.figure(figsize=(10, 6))

plt.plot(
    summary_3hop["number_of_nodes"],
    summary_3hop["packets_per_message"],
    marker="o",
    label="3 hop"
)

plt.plot(
    summary_7hop["number_of_nodes"],
    summary_7hop["packets_per_message"],
    marker="o",
    label="7 hop"
)

plt.xlabel("Number of Nodes")
plt.ylabel("Packets Transmitted per Message Created")
plt.title("Packets Sent per Messages Created")
plt.xticks(summary_3hop["number_of_nodes"])
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()