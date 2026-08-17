import matplotlib.pyplot as plt
from analytics import load_crash_values


def create_crash_chart(limit=100):

    values = load_crash_values()

    if not values:
        return None

    values = values[-limit:]

    rounds = list(range(1, len(values) + 1))

    plt.figure(figsize=(10, 5))

    plt.plot(
        rounds,
        values,
        marker="o",
        linewidth=1
    )

    plt.title("Aviator Crash Trend - Last 100 Rounds")
    plt.xlabel("Round")
    plt.ylabel("Crash Value (x)")

    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    file_path = "crash_trend.png"

    plt.savefig(
        file_path,
        dpi=150
    )

    plt.close()

    return file_path