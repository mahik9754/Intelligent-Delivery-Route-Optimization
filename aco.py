
import numpy as np
from evaluation import evaluate_route


def ant_colony_optimization(
    data,
    n_ants=20,
    n_iterations=100,
    alpha=1.0,
    beta=2.0,
    rho=0.3,
    Q=1.0,
    seed=42
):
    n = data["n_customers"]
    distance = data["distance"]
    travel_time = data["travel_time"]
    congestion = data["congestion"]
    weights = data["weights"]
    scales = data["normalization"]

    rng = np.random.default_rng(seed)

    pheromone = np.ones((n + 1, n + 1), dtype=float)
    heuristic = np.zeros((n + 1, n + 1), dtype=float)

    for i in range(n + 1):
        for j in range(n + 1):
            if i == j:
                continue

            edge_cost = (
                weights["distance"] * distance[i, j] / scales["distance"]
                + weights["travel_time"] * travel_time[i, j] / scales["travel_time"]
                + weights["congestion"] * (
                    travel_time[i, j] * congestion[i, j]
                ) / scales["congestion"]
            )

            heuristic[i, j] = 1.0 / (1e-12 + edge_cost)

    def construct_route():
        route = [0]
        unvisited = set(range(1, n + 1))
        current = 0

        while unvisited:
            candidates = sorted(unvisited)

            desirability = np.array([
                (pheromone[current, customer] ** alpha)
                * (heuristic[current, customer] ** beta)
                for customer in candidates
            ], dtype=float)

            total = desirability.sum()

            if not np.isfinite(total) or total <= 0:
                probabilities = np.full(
                    len(candidates), 1.0 / len(candidates)
                )
            else:
                probabilities = desirability / total

            next_customer = int(
                rng.choice(candidates, p=probabilities)
            )

            route.append(next_customer)
            unvisited.remove(next_customer)
            current = next_customer

        route.append(0)
        return route

    best_route = None
    best_metrics = None
    best_objective = float("inf")
    convergence_history = []

    for _ in range(n_iterations):
        ant_results = []

        for _ in range(n_ants):
            route = construct_route()
            metrics = evaluate_route(route, data)

            ant_results.append((route, metrics))

            if metrics["objective"] < best_objective:
                best_route = route.copy()
                best_metrics = metrics.copy()
                best_objective = metrics["objective"]

        pheromone *= (1.0 - rho)

        # Reinforce routes with lower objective values.
        for route, metrics in ant_results:
            deposit = Q / max(metrics["objective"], 1e-12)

            for k in range(len(route) - 1):
                i = route[k]
                j = route[k + 1]

                pheromone[i, j] += deposit
                pheromone[j, i] += deposit

        convergence_history.append(best_objective)

    return best_route, best_metrics, convergence_history


if __name__ == "__main__":
    from network import generate_network

    data = generate_network(n_customers=12, seed=42)

    route, metrics, history = ant_colony_optimization(data)

    print("ACO route:", route)
    print("\nACO metrics:")

    for metric, value in metrics.items():
        print(f"{metric}: {value:.3f}")

    print("\nInitial best objective:", history[0])
    print("Final best objective:", history[-1])
