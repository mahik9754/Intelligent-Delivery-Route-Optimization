
import numpy as np


def generate_network(n_customers=12, seed=42):
    # generating a synthetic delivery network and its associated data

    rng = np.random.default_rng(seed)
    n_nodes = n_customers + 1

    # generating depot and customer coordinates
    coordinates = rng.uniform(0, 10, size=(n_nodes, 2))

    # calculating Euclidean distances
    distance = np.zeros((n_nodes, n_nodes), dtype=float)

    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            dx = coordinates[i, 0] - coordinates[j, 0]
            dy = coordinates[i, 1] - coordinates[j, 1]
            d = max(np.sqrt(dx**2 + dy**2), 0.1)

            distance[i, j] = d
            distance[j, i] = d

    # generating symmetric congestion scores
    congestion = np.zeros((n_nodes, n_nodes), dtype=float)

    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            score = rng.uniform(0.0, 1.0)
            congestion[i, j] = score
            congestion[j, i] = score

    # calculating travel times using distance and congestion
    travel_time = np.zeros((n_nodes, n_nodes), dtype=float)
    base_speed_kmph = 30.0
    congestion_factor = 0.5

    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            base_time = (distance[i, j] / base_speed_kmph) * 60
            time = base_time * (
                1 + congestion_factor * congestion[i, j]
            )

            travel_time[i, j] = time
            travel_time[j, i] = time

    # assigning delivery time windows to customers

    # depot node (last to be returned back to)
    time_windows = {0: (0.0, 9999.0)}

    for customer in range(1, n_nodes):
        earliest = float(rng.integers(15, 91))
        width = float(rng.integers(25, 61))
        time_windows[customer] = (earliest, earliest + width)

    # assigning 3-10 minutes of service time per customer
    service_time = np.zeros(n_nodes, dtype=float)
    service_time[1:] = rng.integers(3, 11, size=n_customers)

    # defining the weighted route objective
    weights = {"distance": 0.30, "travel_time": 0.30,
               "congestion": 0.15, "lateness": 0.25}

    # calculating fixed normalization scales from a reference route
    reference_route = [0] + list(range(1, n_nodes)) + [0]

    ref_distance = sum(
        distance[reference_route[k], reference_route[k + 1]]
        for k in range(len(reference_route) - 1)
    )

    ref_travel_time = sum(
        travel_time[reference_route[k], reference_route[k + 1]]
        for k in range(len(reference_route) - 1)
    )

    ref_congestion = sum(
        travel_time[reference_route[k], reference_route[k + 1]]
        * congestion[reference_route[k], reference_route[k + 1]]
        for k in range(len(reference_route) - 1)
    )

    ref_lateness = max(60.0, 0.5 * ref_travel_time)

    normalization = {"distance": max(ref_distance, 1e-9), "travel_time": max(
        ref_travel_time, 1e-9), "congestion": max(ref_congestion, 1e-9), "lateness": max(ref_lateness, 1e-9)}

    # packaging the data for use by all project modules
    data = {"n_customers": n_customers, "coordinates": coordinates, "distance": distance, "travel_time": travel_time,
            "congestion": congestion, "time_windows": time_windows, "service_time": service_time, "weights": weights, "normalization": normalization}

    return data


if __name__ == "__main__":
    data = generate_network()

    print("Network generated successfully.")
    print("Customers:", data["n_customers"])
    print("Matrix shape:", data["distance"].shape)
    print("Distance normalization:", data["normalization"]["distance"])
    print("Time windows:")

    for customer, window in data["time_windows"].items():
        print(f"Node {customer}: {window}")
