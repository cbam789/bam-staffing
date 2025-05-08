import matplotlib.pyplot as plt


def plot_supply_demand(supply, demand, output_path):
    hours = list(range(24))

    plt.figure(figsize=(12, 6))
    plt.plot(
        hours,
        demand,
        marker="o",
        label="Average Hourly Demand",
        color="skyblue",
        linewidth=2,
    )
    plt.plot(
        hours,
        supply,
        marker="s",
        label="Recommended Supply",
        color="orange",
        linewidth=2,
    )

    plt.xticks(hours)
    plt.xlabel("Hour of Day")
    plt.ylabel("Count")
    plt.title("Hourly Demand vs Recommended Supply")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()
