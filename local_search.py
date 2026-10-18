
from evaluation import evaluate_route


def two_opt(route, data, max_passes=50):
    best_route = list(route)
    best_metrics = evaluate_route(best_route, data)

    n = data["n_customers"]

    for _ in range(max_passes):
        improved = False

        for i in range(1, n):
            for j in range(i + 1, n + 1):
                candidate = (
                    best_route[:i]
                    + best_route[i:j + 1][::-1]
                    + best_route[j + 1:]
                )

                candidate_metrics = evaluate_route(candidate, data)

                if (
                    candidate_metrics["objective"]
                    < best_metrics["objective"] - 1e-12
                ):
                    best_route = candidate
                    best_metrics = candidate_metrics
                    improved = True
                    break

            if improved:
                break

        if not improved:
            break

    return best_route, best_metrics


if __name__ == "__main__":
    from network import generate_network
    from aco import ant_colony_optimization

    data = generate_network(n_customers=12, seed=42)

    route, metrics, _ = ant_colony_optimization(data)
    improved_route, improved_metrics = two_opt(route, data)

    print("ACO route:", route)
    print("\nACO metrics:")

    for metric, value in metrics.items():
        print(f"{metric}: {value:.3f}")

    print("\nRoute after 2-opt:", improved_route)
    print("\nMetrics after 2-opt:")

    for metric, value in improved_metrics.items():
        print(f"{metric}: {value:.3f}")

    improvement = (
        (metrics["objective"] - improved_metrics["objective"])
        / metrics["objective"] * 100
    )

    print(f"\nObjective improvement: {improvement:.2f}%")
