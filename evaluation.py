
def validate_route(route, data):
    # validating the route structure and customer visits

    n = data["n_customers"]

    if not isinstance(route, (list, tuple)):
        raise TypeError("Route must be a list or tuple.")

    if len(route) != n + 2:
        raise ValueError(
            "Route must contain all customers and both depot visits.")

    if route[0] != 0 or route[-1] != 0:
        raise ValueError("Route must start and end at depot 0.")

    customers = list(route[1:-1])

    if any(
        not isinstance(node, int) or isinstance(node, bool)
        for node in customers
    ):
        raise ValueError("Customer node IDs must be integers.")

    if sorted(customers) != list(range(1, n + 1)):
        raise ValueError("Each customer must be visited exactly once.")


def evaluate_route(route, data):
    # calculating route metrics and the normalized objective

    validate_route(route, data)

    distance_matrix = data["distance"]
    travel_time_matrix = data["travel_time"]
    congestion_matrix = data["congestion"]
    time_windows = data["time_windows"]
    service_time = data["service_time"]

    # calculaing distance, travel time, and congestion exposure
    total_distance = 0.0
    total_travel_time = 0.0
    congestion_exposure = 0.0

    for k in range(len(route) - 1):
        i = route[k]
        j = route[k + 1]

        total_distance += distance_matrix[i, j]
        total_travel_time += travel_time_matrix[i, j]
        congestion_exposure += (
            travel_time_matrix[i, j] * congestion_matrix[i, j]
        )

    # simulating customer arrivals, waiting, and service
    current_time = 0.0
    total_waiting_time = 0.0
    total_lateness = 0.0
    on_time_deliveries = 0

    for k in range(1, len(route) - 1):
        previous_node = route[k - 1]
        customer = route[k]

        arrival_time = (
            current_time + travel_time_matrix[previous_node, customer])

        earliest, latest = time_windows[customer]

        waiting = max(0.0, earliest - arrival_time)
        lateness = max(0.0, arrival_time - latest)

        total_waiting_time += waiting
        total_lateness += lateness

        if arrival_time <= latest:
            on_time_deliveries += 1

        service_start = max(arrival_time, earliest)
        current_time = service_start + service_time[customer]

    # normalizing metrics using the shared reference scales
    weights = data["weights"]
    scales = data["normalization"]

    distance_normalized = total_distance / scales["distance"]
    time_normalized = total_travel_time / scales["travel_time"]
    congestion_normalized = congestion_exposure / scales["congestion"]
    lateness_normalized = total_lateness / scales["lateness"]

    # calculating the weighted route objective
    objective = (weights["distance"] * distance_normalized + weights["travel_time"] * time_normalized +
                 weights["congestion"] * congestion_normalized + weights["lateness"] * lateness_normalized)

    return {
        "distance": float(total_distance),
        "travel_time": float(total_travel_time),
        "congestion_exposure": float(congestion_exposure),
        "waiting_time": float(total_waiting_time),
        "lateness": float(total_lateness),
        "on_time_deliveries": int(on_time_deliveries),
        "objective": float(objective)
    }
