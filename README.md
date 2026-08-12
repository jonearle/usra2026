(AI Generated README)

# Summer 2026 NSERC USRA Project
# Dalhousie University

Evaluation of LoRa Mesh Networks in an Urban Environment 

The project investigates the effectiveness and scalability of **LoRa mesh networks in urban environments**, with a particular focus on the open-source [Meshtastic](https://meshtastic.org/) firmware. Real-world experiments were conducted throughout Halifax and on the Dalhousie University campus, alongside simulations of larger networks using a modified version of Meshtasticator.

## Project Overview

LoRa offers long-range, low-power wireless communication without relying on existing Internet or cellular infrastructure. Mesh networking extends this capability by allowing devices to relay messages between one another.

Urban environments, however, introduce significant challenges due to:

* building obstructions
* limited line of sight
* node placement
* interference and packet collisions
* increased network traffic as a mesh grows

This project evaluates these limitations through a combination of **real-world LoRa deployments and network simulation**.

The primary metrics investigated include:

* communication range
* RSSI and SNR
* packet delivery
* message latency
* hop count and routing behaviour
* collision rate
* network reach
* transmission overhead
* airtime utilization
* node density and spacing

## Experiments

### Range Testing

Multiple zero-hop range experiments were performed throughout Halifax to evaluate how distance, building obstructions, elevation, and LoRa configuration affect communication.

Tests included:

* SMU football field and campus range testing
* bike-based range testing around Halifax
* comparison of Meshtastic and MeshCore
* RSSI and SNR mapping

Results demonstrated the large impact that buildings have on LoRa propagation. Reliable zero-hop communication was achieved at approximately **260 m under typical urban conditions**, while communication of approximately **1.1 km** was achieved when nodes were positioned along an adjacent street acting as a propagation corridor.

### Dalhousie Campus Mesh Deployment

A multi-node Meshtastic testbed was deployed across several buildings on the Dalhousie University campus.

The deployment was used to investigate:

* multi-hop communication
* message delivery rate
* message latency
* retransmissions
* routing paths
* traceroutes
* network traffic
* node telemetry

Nodes were placed at locations including the Goldberg Computer Science Building, Life Sciences Centre, Rowe Building, McCain Arts Building, Student Union Building, James Dunn Building, and Dalplex.

### Meshtastic Simulation

Larger networks were evaluated using **Meshtasticator**, with modifications developed during the project to support geographic node generation and additional experimentation.

Simulations examined:

* different network sizes
* random node placement across Halifax
* 3-hop versus 7-hop routing
* node density and spacing
* network reach
* message delay
* collisions
* transmission overhead
* airtime utilization

While the campus deployment demonstrated reliable multi-hop communication at a small scale, simulations indicated significant scalability limitations for a Halifax-wide Meshtastic deployment. Network reach peaked at approximately **54%**, after which congestion and message delay increased substantially.

## Repository Structure

```text
usra2026/
├── Meshtasticator-GeoJSON/     # Modified Meshtasticator simulator (git submodule)
├── data/                       # Experimental and simulation datasets
│   ├── bike_tests/
│   ├── delivery_rate/
│   ├── dynamic_test/
│   ├── latency/
│   ├── simulations/
│   ├── traceroutes/
│   └── ...
│
├── script/
│   ├── maps/                   # Mapping and visualization scripts
│   ├── meshcore/               # MeshCore experiment utilities
│   └── meshtastic/             # Meshtastic experiment and analysis utilities
│
├── USRA 2026 Final Paper/      # Final report, LaTeX source, figures, and bibliography
├── Presentations/              # Research presentations
├── Other/                      # Additional project material
└── README.md
```

## Meshtasticator-GeoJSON

`Meshtasticator-GeoJSON` is included as a Git submodule and contains modifications made to the Meshtasticator simulator during this project.

The modified simulator supports experiments involving geographically constrained node placement, including generating nodes within GeoJSON polygons for simulations of the Halifax peninsula.

To clone this repository with the simulator:

```bash
git clone --recurse-submodules https://github.com/jonearle/usra2026.git
cd usra2026
```

If the repository has already been cloned without its submodules:

```bash
git submodule update --init --recursive
```

The submodule tracks the `research` branch of `Meshtasticator-GeoJSON`.

## Data

Raw and processed experimental data are stored under [`data/`](./data).

The repository contains datasets from range tests, delivery-rate experiments, latency tests, dynamic mesh experiments, traceroutes, and network simulations.

Simulation datasets are primarily located under:

```text
data/simulations/
├── box_1000m/
├── box_2000m/
├── halifax_random_3hop/
├── halifax_random_7hop/
└── ...
```

These directories contain simulation outputs used to calculate and visualize metrics such as network reach, collisions, latency, transmission overhead, and airtime utilization.

## Scripts

Experimental and analysis utilities are stored under [`script/`](./script).

### Meshtastic

[`script/meshtastic/`](./script/meshtastic) contains tools developed for working with the Meshtastic testbed, including utilities for:

* sending and receiving packets
* collecting telemetry
* traceroutes
* dynamic mesh experiments
* retransmission testing
* battery monitoring
* position data
* network monitoring and data collection

### MeshCore

[`script/meshcore/`](./script/meshcore) contains scripts used during the Meshtastic/MeshCore comparison and early MeshCore experiments.

### Mapping

[`script/maps/`](./script/maps) contains Python scripts used to visualize experimental data geographically, including:

* RSSI
* SNR
* latency
* hop count
* retransmissions
* communication range

## Final Report

The complete research report is available in:

[`USRA 2026 Final Paper/`](./USRA%202026%20Final%20Paper)

The directory contains:

* `JE_USRA_2026_Final_Report.pdf`
* `main.tex`
* bibliography
* report figures and images

The report provides detailed descriptions of the experimental methodology, simulation methodology, results, limitations, and conclusions.

## Hardware and Software

The project primarily used:

* LILYGO T-Beam LoRa radios
* LILYGO LoRa32 radios
* Meshtastic
* MeshCore
* Python
* Meshtastic Python API
* Meshtasticator
* Grafana / MeshMonitor
* OpenStreetMap-based visualization tools

Most experiments used the Meshtastic `LONG_FAST` modem preset in the US 915 MHz ISM band.

## Key Findings

Overall, the project found that:

* Buildings significantly reduce LoRa range in urban environments.
* Streets can act as effective propagation corridors and substantially increase communication distance.
* Small Meshtastic deployments can provide reliable multi-hop communication.
* Increasing node density initially improves connectivity but eventually creates substantial network congestion.
* Increasing the permitted hop limit can increase routing opportunities but also increases network traffic and delay.
* Large flooding-based LoRa meshes face significant scalability limitations in dense urban environments.

## Author

**Jonathan Earle**
NSERC USRA 2026
Dalhousie University

## Acknowledgements

This work was completed as part of an **NSERC Undergraduate Student Research Award (USRA)** at Dalhousie University during Summer 2026.

