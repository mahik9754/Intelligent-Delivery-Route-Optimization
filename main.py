
"""Run the complete delivery-route optimization experiment."""

from network import generate_network
from evaluation import evaluate_route
from baseline import nearest_neighbor
from aco import ant_colony_optimization
from local_search import two_opt
from traffic import simulate_traffic
from plots import plot_results


def calculate_improvement(before, after):
    """Calculate percentage reduction in objective."""
    if before == 0:
        return None
    return ((before - after) / before) * 100


def run_experiment(data):
    # 1. Nearest Neighbor baseline
    nn_route, nn_metrics = nearest_neighbor(data)

    # 2. Ant Colony Optimization
    aco_route, aco_metrics, history = (
        ant_colony_optimization(data, seed=42)
    )

    # 3. Improve the ACO route using 2-opt
    improved_route, improved_metrics = two_opt(
        aco_route, data, max_passes=50
    )

    # 4. Simulate traffic disruptions
    affected_edges = [
         (improved_route[i], improved_route[i + 1])
    for i in range(len(improved_route) - 1)
    if improved_route[i] != improved_route[i + 1]
    ]

    disrupted_data = simulate_traffic(
        data,
        affected_edges=affected_edges,
        time_multiplier=2.5,
        congestion_increase=0.4,
        seed=42
    )

    # 5. Evaluate the original optimized route under traffic
    original_route_metrics = evaluate_route(
        improved_route, disrupted_data
    )

    # Diagnostic: check whether disrupted edges are used
    print("\nTRAFFIC DISRUPTION CHECK")

    for i, j in affected_edges:
        used = any(
            (
                improved_route[k] == i
                and improved_route[k + 1] == j
            )
            or (
                improved_route[k] == j
                and improved_route[k + 1] == i
            )
            for k in range(len(improved_route) - 1)
        )

        print(
            f"Edge ({i}, {j}): "
            f"original time = {data['travel_time'][i, j]:.2f}, "
            f"disrupted time = "
            f"{disrupted_data['travel_time'][i, j]:.2f}, "
            f"used in route = {used}"
        )

    # 6. Reoptimize under disrupted traffic
    traffic_aco_route, traffic_aco_metrics, traffic_history = (
        ant_colony_optimization(disrupted_data, seed=43)
    )

    traffic_route, traffic_metrics = two_opt(
        traffic_aco_route,
        disrupted_data,
        max_passes=50
    )

    # 7. Calculate objective improvements
    improvements = {
        "ACO vs Nearest Neighbor": calculate_improvement(
            nn_metrics["objective"],
            aco_metrics["objective"]
        ),
        "ACO + 2-opt vs ACO": calculate_improvement(
            aco_metrics["objective"],
            improved_metrics["objective"]
        ),
        "Reoptimization under traffic": calculate_improvement(
            original_route_metrics["objective"],
            traffic_metrics["objective"]
        )
    }

    return {
        "data": data,
        "nearest_neighbor": {
            "route": nn_route,
            "metrics": nn_metrics
        },
        "aco": {
            "route": aco_route,
            "metrics": aco_metrics,
            "history": history
        },
        "aco_2opt": {
            "route": improved_route,
            "metrics": improved_metrics
        },
        "traffic": {
            "data": disrupted_data,
            "affected_edges": affected_edges,
            "original_route": improved_route,
            "original_route_metrics": original_route_metrics,
            "aco_route": traffic_aco_route,
            "aco_metrics": traffic_aco_metrics,
            "aco_history": traffic_history,
            "reoptimized_route": traffic_route,
            "reoptimized_metrics": traffic_metrics
        },
        "improvements_percent": improvements,
        "plot_dir": "plots"
    }


def print_summary(results):
    methods = [
        ("Nearest Neighbor",
         results["nearest_neighbor"]["metrics"]),
        ("ACO",
         results["aco"]["metrics"]),
        ("ACO + 2-opt",
         results["aco_2opt"]["metrics"]),
        ("Original route under traffic",
         results["traffic"]["original_route_metrics"]),
        ("Reoptimized under traffic",
         results["traffic"]["reoptimized_metrics"])
    ]

    columns = [
        "distance",
        "travel_time",
        "congestion_exposure",
        "waiting_time",
        "lateness",
        "on_time_deliveries",
        "objective"
    ]

    print("\nMETRIC COMPARISON")
    print("-" * 145)
    print(f"{'Method':35s}", end="")

    for column in columns:
        print(f"{column:>18s}", end="")

    print()
    print("-" * 145)

    for name, metrics in methods:
        print(f"{name:35s}", end="")

        for column in columns:
            value = metrics[column]

            if column == "on_time_deliveries":
                print(f"{value:18.0f}", end="")
            else:
                print(f"{value:18.3f}", end="")

        print()

    print("\nPERCENTAGE IMPROVEMENTS")

    for name, value in results["improvements_percent"].items():
        if value is None:
            print(f"{name}: undefined (starting objective is zero)")
        else:
            print(f"{name}: {value:.2f}%")


def main():
    # Generate one reproducible network
    data = generate_network(n_customers=12, seed=42)

    # Run the experiments
    results = run_experiment(data)

    # Display metrics
    print_summary(results)

    # Generate graphs
    plot_paths = plot_results(results)

    print("\nGraphs saved:")

    for name, path in plot_paths.items():
        print(f"{name}: {path}")

    print("\nExperiment completed successfully.")


if __name__ == "__main__":
    main()
