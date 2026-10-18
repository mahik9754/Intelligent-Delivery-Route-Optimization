
"""Reproducible traffic-disruption scenarios."""

from copy import deepcopy
import numpy as np


def simulate_traffic(
    data,
    affected_edges=None,
    time_multiplier=2.5,
    congestion_increase=0.4,
    seed=42
):
    """Return a modified copy of the network with traffic disruptions."""

    if time_multiplier < 1:
        raise ValueError("time_multiplier must be at least 1.")

    if congestion_increase < 0:
        raise ValueError("congestion_increase cannot be negative.")

    disrupted = deepcopy(data)
    n = data["n_customers"]
    rng = np.random.default_rng(seed)

    # Select roads reproducibly if none are specified.
    if affected_edges is None:
        all_edges = [
            (i, j)
            for i in range(n + 1)
            for j in range(i + 1, n + 1)
        ]

        count = min(max(1, round(len(all_edges) * 0.15)),
                    len(all_edges))

        indices = rng.choice(
            len(all_edges), size=count, replace=False
        )

        edges = [all_edges[int(i)] for i in indices]
    else:
        edges = list(affected_edges)

    processed_edges = set()

    for edge in edges:
        if len(edge) != 2:
            raise ValueError(f"Invalid edge: {edge}")

        i, j = map(int, edge)

        if i == j or not (0 <= i <= n and 0 <= j <= n):
            raise ValueError(f"Invalid edge: {(i, j)}")

        key = (min(i, j), max(i, j))

        if key in processed_edges:
            continue

        processed_edges.add(key)

        # Increase travel time in both directions.
        disrupted["travel_time"][i, j] *= time_multiplier
        disrupted["travel_time"][j, i] *= time_multiplier

        # Increase congestion, capped at 1.0.
        new_congestion = min(
            1.0,
            disrupted["congestion"][i, j]
            + congestion_increase
        )

        disrupted["congestion"][i, j] = new_congestion
        disrupted["congestion"][j, i] = new_congestion

    # Distance, time windows, service times and normalization
    # remain unchanged.
    return disrupted
