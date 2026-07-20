import matplotlib.pyplot as plt


def plot_timetable(x, station_block_indices, train_schedules):
    """
    Plots a Marey Chart (Time-Space Diagram) and a Delay Bar Chart.
    """

    # 0. Get tensor dimensions and save as variables instead of passing them as arguments
    num_trains, num_blocks, time_horizon = [max(indices) + 1 for indices in zip(*x.keys())]

    # 1. Setup Figure using subplots for cleaner ratio management
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), gridspec_kw={'width_ratios': [4, 1]})
    colors = ['red', 'blue', 'green', 'orange']

    # 2. Extract Data
    # By looping 'k' on the outside, the lists naturally sort chronologically
    train_paths = {i: {'time': [], 'block': []} for i in range(num_trains)}

    for k in range(time_horizon):
        for i in range(num_trains):
            for j in range(num_blocks):
                # .X > 0.5 accounts for floating point solver tolerances
                if x[i, j, k].X > 0.5:
                    train_paths[i]['time'].append(k)
                    train_paths[i]['block'].append(j)

    # 3. Plot Timetable (Left Axis)
    for i, path in train_paths.items():
        if not path['time']:
            continue

        color = colors[i % len(colors)]

        # Plot the main trajectory line
        ax1.plot(path['block'], path['time'], color=color, linewidth=3, label=f'Train {i}', alpha=0.8)

        # Overlay triangles to show movement (only plot when the block index changes)
        for idx in range(1, len(path['time'])):
            if path['block'][idx] != path['block'][idx - 1]:
                ax1.scatter(path['block'][idx], path['time'][idx], color=color, marker='>', s=100, alpha=0.8)

    # Format Timetable Axis
    ax1.set_ylim(time_horizon, 0)  # Invert Y-axis so time flows downward
    ax1.set_xlim(-0.5, num_blocks - 0.5)
    ax1.set_ylabel('Time Step', fontweight='bold')
    ax1.set_xlabel('Track Block', fontweight='bold')
    ax1.set_title('Optimal Timetable (Marey Chart)', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Add vertical lines and labels for the stations
    ax1.set_xticks(station_block_indices)
    ax1.set_xticklabels([f'Station {idx}' for idx in range(len(station_block_indices))])
    for j in station_block_indices:
        ax1.axvline(x=j, color='gray', linestyle='--', alpha=0.6, linewidth=2)

    # 4. Calculate and Plot Delays (Right Axis)
    for i in range(num_trains):
        for station_id, schedule in train_schedules[i].items():

            if "arrival" in schedule:
                target_time = schedule["arrival"]
                station_block = station_block_indices[station_id]

                # Find actual arrival (the first time 'k' the train occupies 'station_block')
                actual_arrival = next((t for t, b in zip(train_paths[i]['time'], train_paths[i]['block'])
                                       if b == station_block), None)

                if actual_arrival is not None:
                    delay = actual_arrival - target_time

                    if delay > 0:
                        # Use ax.bar with the 'bottom' argument instead of drawing raw Rectangles
                        ax2.bar(i, delay, bottom=target_time, width=0.6,
                                color=colors[i % len(colors)], alpha=0.5, edgecolor='black')

                        # Add the "+X" text label in the middle of the bar
                        ax2.text(i, target_time + (delay / 2), f'+{delay}',
                                 ha='center', va='center', fontsize=9, fontweight='bold')

    # Format Delay Axis
    ax2.set_ylim(time_horizon, 0)  # Match inverted Y-axis of the timetable
    ax2.set_xlim(-0.5, num_trains - 0.5)
    ax2.set_xticks(range(num_trains))
    ax2.set_xticklabels([f'Train {i}' for i in range(num_trains)])
    ax2.set_title('Delays', fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.show()