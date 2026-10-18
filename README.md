# Intelligent Delivery Route Optimization Using Hybrid Ant Colony Optimization with Time Windows and Dynamic Traffic

## Project Overview

This project focuses on optimizing delivery routes using intelligent optimization techniques. The objective is to find a delivery route that balances distance, travel time, traffic congestion, and delivery time-window violations.

The project uses a hybrid approach combining **Ant Colony Optimization (ACO)** with **2-opt local search**. A nearest-neighbour algorithm is also implemented as a baseline to compare the performance of the optimization approach.

The system currently operates on a synthetically generated delivery network with one depot and 12 customers. It is designed to demonstrate how intelligent optimization techniques can improve delivery planning under time-window constraints.

## Problem Statement

Traditional route planning methods often focus on minimizing distance alone. However, a practical delivery route must also consider travel time, traffic congestion, customer delivery time windows, waiting time, and late deliveries.

The aim of this project is to develop an intelligent route optimization system that minimizes a combined objective function incorporating these factors.

## Objectives

- Generate a synthetic delivery network with a depot and multiple customers.
- Calculate distances, travel times, and congestion levels between locations.
- Implement a nearest-neighbour baseline for route planning.
- Apply Ant Colony Optimization to search for better delivery routes.
- Improve the generated route using 2-opt local search.
- Evaluate and compare routes using a common objective function.
- Study the effect of route optimization on lateness and on-time deliveries.

## Technologies Used

- **Python** — implementation of the optimization algorithms.
- **NumPy** — numerical calculations, matrices, and random data generation.
- **Matplotlib** — planned for visualizing routes and optimization results.

## Methodology

### 1. Synthetic Network Generation

The delivery network is generated programmatically rather than using live map data. It contains one depot, represented by node `0`, and 12 customer locations.

The network generation module creates:

- Coordinates for the depot and customers.
- A distance matrix representing distances between locations.
- A travel-time matrix that accounts for distance and congestion.
- Congestion values for travel between locations.
- Delivery time windows and customer service times.

A fixed random seed is used during testing to make the generated network reproducible.

### 2. Route Evaluation

A common route evaluation function is used to evaluate the performance of different algorithms under the same conditions.

For each route, it calculates:

- Total travel distance.
- Total travel time.
- Congestion exposure.
- Waiting time.
- Total delivery lateness.
- Number of on-time deliveries.
- Overall objective value.

The route must start and end at the depot and visit every customer exactly once.

### 3. Nearest-Neighbour Baseline

The nearest-neighbour algorithm is implemented as a baseline. Starting from the depot, it repeatedly selects the nearest unvisited customer until all customers have been visited, then returns to the depot.

This provides a reference for evaluating whether the optimization algorithms improve delivery performance.

### 4. Ant Colony Optimization

Ant Colony Optimization is a population-based optimization technique inspired by the foraging behaviour of ants.

In this project, multiple artificial ants construct delivery routes. The algorithm uses pheromone values and heuristic information to guide route construction.

- **Pheromone values** represent the learned preference for selecting particular edges.
- **Heuristic information** favours edges with lower estimated travel-related costs.
- **Pheromone evaporation** reduces the influence of previous route choices over time.
- **Pheromone updates** reinforce edges used by the constructed routes, with better-performing routes receiving larger deposits.

Each generated route is evaluated using the shared route evaluation function. The best route found during the iterations is retained.

### 5. 2-opt Local Search

The 2-opt algorithm is applied to improve the route obtained from ACO.

It works by reversing sections of a route to explore alternative customer visiting orders. Each candidate route is evaluated using the same objective function, and a change is accepted only if it reduces the objective value.

This allows the system to refine an existing route without changing the set of customers being visited.

## Objective Function

The system uses a weighted objective function:

\[
J(R)=0.30D_n+0.30T_n+0.15C_n+0.25L_n
\]

Where:

- \(D_n\) = normalized total distance.
- \(T_n\) = normalized total travel time.
- \(C_n\) = normalized congestion exposure.
- \(L_n\) = normalized delivery lateness.
- \(R\) = delivery route being evaluated.

The weights prioritize distance, travel time, congestion, and lateness according to the project's agreed specification. Lower objective values indicate better overall performance under this scoring function.

Normalization scales are established from a reference route and reused across algorithm comparisons so that the metrics are evaluated consistently.

## Experimental Results

The following results were obtained from the current implementation using the same synthetic network and random seed.

| Metric | Nearest Neighbour | ACO | ACO + 2-opt |
|---|---:|---:|---:|
| Distance | 33.099 | 40.746 | 41.097 |
| Travel time | 76.323 | 88.762 | 100.232 |
| Congestion exposure | 25.725 | 17.138 | 46.094 |
| Waiting time | 74.121 | 19.802 | 3.628 |
| Lateness | 708.559 | 288.224 | 230.620 |
| On-time deliveries | 2 | 4 | 7 |
| Objective value | 2.655 | 1.333 | 1.246 |

*Distance is measured in kilometres and time-related values are measured in minutes. Congestion exposure is a derived metric. The objective value is a weighted, normalized score.*

## Results and Observations

- The ACO route achieved a lower objective value than the nearest-neighbour baseline.
- The objective value decreased from **2.655** for nearest neighbour to **1.333** for ACO, a reduction of approximately **49.79%**.
- Applying 2-opt further reduced the objective value from **1.333** to **1.246**, an additional improvement of approximately **6.55%**.
- The number of on-time deliveries increased from 2 with nearest neighbour to 4 with ACO and 7 with ACO followed by 2-opt.
- Total lateness decreased from 708.559 minutes with nearest neighbour to 230.620 minutes after applying 2-opt to the ACO route.
- The 2-opt route has higher distance, travel time, and congestion exposure than the initial ACO route. This demonstrates that optimizing a weighted objective does not necessarily minimize every individual metric.

These results are from one synthetic test network. Further testing across multiple random seeds and network configurations is needed before drawing broader conclusions.

## Project Structure

```text
Intelligent-Delivery-Route-Optimization/
│
├── network.py
├── evaluation.py
├── baseline.py
├── aco.py
├── local_search.py
├── traffic.py
├── plots.py
├── main.py
└── README.md
```

## How to Run

### 1. Install the dependency

```bash
python -m pip install numpy
```

### 2. Run the nearest-neighbour baseline

```bash
python baseline.py
```

### 3. Run Ant Colony Optimization

```bash
python aco.py
```

### 4. Run ACO followed by 2-opt local search

```bash
python local_search.py
```

Run these commands from the project directory. The required Python files should be in the same directory.

## Current Progress

The following components have been implemented and tested individually:

- Synthetic delivery network generation.
- Route evaluation and objective calculation.
- Nearest-neighbour baseline.
- Ant Colony Optimization.
- 2-opt local search.
- Initial performance comparison using the same test network.

The integration of the complete system, dynamic traffic handling, and visualization of the final results are to be added as the remaining work is completed.

## Limitations

- The delivery network is synthetically generated and does not use live map or traffic data.
- The current experiment uses one depot, one vehicle, and 12 customers.
- Traffic congestion is represented through generated congestion values.
- The reported results are based on one test configuration and may vary with different network settings.
- The current objective function uses fixed weights and normalization scales.

## Conclusion

The current implementation demonstrates how Ant Colony Optimization and 2-opt local search can be combined to improve delivery route planning under a multi-factor objective.

Compared with the nearest-neighbour baseline, ACO achieved a lower objective value, while the addition of 2-opt further improved the overall score and increased the number of on-time deliveries in the tested network.

The current results provide a foundation for completing and evaluating the integrated delivery route optimization system.
