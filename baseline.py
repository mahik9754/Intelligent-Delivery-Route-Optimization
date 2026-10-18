
from evaluation import evaluate_route


def nearest_neighbor(data):
    # constructing and evaluating a route using the Nearest Neighbor heuristic

    n = data["n_customers"]
    distance = data["distance"]

    current_node = 0
    unvisited = set(range(1, n + 1))
    route = [0]

    # visiting the nearest unvisited customer at each step
    while unvisited:
        next_customer = min(
            unvisited, key=lambda customer: distance[current_node, customer])

        route.append(next_customer)
        unvisited.remove(next_customer)
        current_node = next_customer

    # returning to the depot and evaluating the completed route
    route.append(0)
    metrics = evaluate_route(route, data)

    return route, metrics


if __name__ == "__main__":
    from network import generate_network

    data = generate_network(n_customers=12, seed=42)
    route, metrics = nearest_neighbor(data)

    print("\nNearest neighbour baseline: ")
    print("Route:", route)

    for metric, value in metrics.items():
        print(f"{metric}: {value:.3f}")
