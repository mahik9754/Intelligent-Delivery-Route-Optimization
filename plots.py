
"""Generate plots for delivery-route optimization experiments."""

import os
import matplotlib.pyplot as plt


def plot_results(results):
    output_dir = results.get("plot_dir", "plots")
    os.makedirs(output_dir, exist_ok=True)

    saved_paths = {}

    data = results["data"]

    # 1. Route comparison
    fig, ax = plt.subplots(figsize=(9, 7))

    coordinates = data["coordinates"]

    routes = {
        "Nearest Neighbor": results["nearest_neighbor"]["route"],
        "ACO": results["aco"]["route"],
        "ACO + 2-opt": results["aco_2opt"]["route"]
    }

    for name, route in routes.items():
        x = [coordinates[node][0] for node in route]
        y = [coordinates[node][1] for node in route]
        ax.plot(x, y, marker="o", linewidth=1.8, label=name)

    ax.scatter(
        coordinates[0][0],
        coordinates[0][1],
        marker="s",
        s=150,
        label="Depot",
        zorder=5
    )

    ax.set_title("Delivery Route Comparison")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    path = os.path.join(output_dir, "route_comparison.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    saved_paths["route_comparison"] = path

    # 2. ACO convergence
    fig, ax = plt.subplots(figsize=(9, 5))

    history = results["aco"]["history"]

    if isinstance(history, dict):
        values = history.get(
            "best_objective",
            history.get("best_cost", history.get("objective", []))
        )
    else:
        values = history

    ax.plot(range(1, len(values) + 1), values, linewidth=2)
    ax.set_title("ACO Convergence")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Best Objective")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    path = os.path.join(output_dir, "aco_convergence.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    saved_paths["aco_convergence"] = path

    # 3. Metric comparison
    metric_names = [
        "distance",
        "travel_time",
        "congestion_exposure",
        "waiting_time",
        "lateness",
        "objective"
    ]

    method_names = [
        "Nearest Neighbor",
        "ACO",
        "ACO + 2-opt"
    ]

    metric_data = [
        results["nearest_neighbor"]["metrics"],
        results["aco"]["metrics"],
        results["aco_2opt"]["metrics"]
    ]

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()

    for ax, metric in zip(axes, metric_names):
        values = [metrics[metric] for metrics in metric_data]

        ax.bar(method_names, values)
        ax.set_title(metric.replace("_", " ").title())
        ax.tick_params(axis="x", rotation=20)
        ax.grid(axis="y", alpha=0.3)

    fig.suptitle("Optimization Metric Comparison")
    fig.tight_layout()

    path = os.path.join(output_dir, "metric_comparison.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    saved_paths["metric_comparison"] = path

    # 4. Performance under traffic disruption
    traffic = results["traffic"]

    traffic_methods = [
        "Original route\nunder traffic",
        "Reoptimized\nunder traffic"
    ]

    traffic_metrics = [
        traffic["original_route_metrics"],
        traffic["reoptimized_metrics"]
    ]

    values = [m["objective"] for m in traffic_metrics]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(traffic_methods, values)
    ax.set_title("Objective Under Traffic Disruption")
    ax.set_ylabel("Objective")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    path = os.path.join(output_dir, "traffic_comparison.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    saved_paths["traffic_comparison"] = path

    return saved_paths
