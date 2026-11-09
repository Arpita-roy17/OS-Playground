
import matplotlib.pyplot as plt


def plot_gantt(intervals):

    # Create the chart
    fig, ax = plt.subplots(figsize=(12, 3.5))

    # Different colors for different processes
    colors = {
        "P1": "#3B82F6",
        "P2": "#10B981",
        "P3": "#F59E0B",
        "P4": "#A855F7",
        "IDLE": "#64748B"
    }

    # Draw each process as a horizontal bar
    for pid, start, end in intervals:

        duration = end - start

        ax.barh(
            y=0,
            width=duration,
            left=start,
            height=0.55,
            color=colors.get(pid, "#EC4899"),
            edgecolor="white"
        )

        # Display process name inside the bar
        ax.text(
            start + duration / 2,
            0,
            pid,
            ha="center",
            va="center",
            color="white",
            fontweight="bold",
            fontsize=11
        )

        # Display start and end times
        ax.text(
            start,
            -0.42,
            str(start),
            ha="center",
            fontsize=10
        )

        ax.text(
            end,
            -0.42,
            str(end),
            ha="center",
            fontsize=10
        )

    # Chart styling
    ax.set_title(
        "CPU Scheduling Gantt Chart",
        fontsize=16,
        fontweight="bold",
        pad=20
    )

    ax.set_xlabel("Time Units", fontsize=11)

    ax.set_yticks([])
    ax.set_ylim(-0.65, 0.65)

    ax.grid(axis="x", linestyle="--", alpha=0.3)

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()

    return fig
