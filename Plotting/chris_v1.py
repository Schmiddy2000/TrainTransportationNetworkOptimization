import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def plot_simple_timetable(num_trains, num_blocks, time_horizon, x, is_station, track_blueprint=None, train_schedules=None):

    fig = plt.figure(figsize=(18, 10))

    ax1 = plt.subplot(1, 5, (1, 4))
    ax2 = plt.subplot(1, 5, 5)

    high_contrast_colors = [
        (1.0, 0.0, 0.0),      #Rot
        (0.0, 0.0, 1.0),      #Blau
        (0.0, 0.7, 0.0),      #Grün
        (1.0, 0.6, 0.0),      #Orange
    ]

    colors = [high_contrast_colors[i % len(high_contrast_colors)] for i in range(num_trains)]

    station_blocks = [j for j in range(num_blocks) if is_station[j]]
    station_block_indices = station_blocks

    station_names = {}
    for station_idx, block_idx in enumerate(station_blocks):
        station_names[block_idx] = station_idx

    station_positions = []
    block_to_x = {}
    block_idx = 0
    current_x = 0

    if track_blueprint is not None:
        for item in track_blueprint:
            if item["type"] == "station":
                station_positions.append(current_x)
                block_to_x[block_idx] = current_x
                block_idx += 1
                current_x += 1
            elif item["type"] == "segment":
                for seg_pos in range(item["length"]):
                    block_to_x[block_idx] = current_x
                    block_idx += 1
                    current_x += 1
    else:
        for j in range(num_blocks):
            block_to_x[j] = j
        station_positions = station_blocks

    train_paths = defaultdict(lambda: {'time': [], 'x_pos': [], 'block': []})

    for i in range(num_trains):
        for k in range(time_horizon):
            for j in range(num_blocks):
                if x[i, j, k].X > 0.5:
                    train_paths[i]['time'].append(k)
                    train_paths[i]['x_pos'].append(block_to_x[j])
                    train_paths[i]['block'].append(j)

    train_delays = {}
    if train_schedules is not None:
        for i in range(num_trains):
            train_delays[i] = []

            for station_id, schedule in train_schedules[i].items():
                if "arrival" in schedule:
                    scheduled_arrival = schedule["arrival"]
                    station_block = station_block_indices[station_id]

                    actual_arrival = None
                    for k in range(time_horizon):
                        if x[i, station_block, k].X > 0.5:
                            actual_arrival = k
                            break

                    if actual_arrival is not None:
                        delay = actual_arrival - scheduled_arrival
                        if delay > 0:
                            train_delays[i].append({
                                'station': station_id,
                                'scheduled': scheduled_arrival,
                                'actual': actual_arrival,
                                'delay': delay
                            })

    # Plot paths
    for train_id, path in train_paths.items():
        times = path['time']
        x_positions = path['x_pos']
        blocks = path['block']

        if len(times) == 0:
            continue

        sorted_data = sorted(zip(times, x_positions, blocks))
        times_sorted, x_sorted, blocks_sorted = zip(*sorted_data)

        ax1.plot(x_sorted, times_sorted,
                color=colors[train_id % len(colors)],
                linewidth=3,
                label=f'Zug {train_id}',
                alpha=0.8)

        for idx in range(1, len(times_sorted)):
            if blocks_sorted[idx] != blocks_sorted[idx-1]:
                ax1.scatter(x_sorted[idx], times_sorted[idx],
                          color=colors[train_id % len(colors)],
                          marker='>',
                          s=100, alpha=0.8)

    for station_block, station_x in zip(station_blocks, station_positions):
        ax1.axvline(x=station_x, color='gray', linestyle='--',
                   alpha=0.6, linewidth=2)

    ax1.set_ylabel('Time', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Track Segment', fontsize=12, fontweight='bold')
    ax1.set_title('Optimal Timetable', fontsize=15, fontweight='bold')

    station_labels = [f'Station {station_names[block]}' for block in station_blocks]
    ax1.set_xticks(station_positions)
    ax1.set_xticklabels(station_labels, fontsize=10)


    ax1.set_ylim(time_horizon + 0.5, -0.5)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right')


    # Rechter Bar chart
    bar_width = 0.7

    ax2.set_xlim(-0.5, num_trains - 0.5)
    ax2.set_ylim(time_horizon + 0.5, -0.5)
    ax2.set_xticks(range(num_trains))
    ax2.set_xticklabels([f'Zug {i}' for i in range(num_trains)], fontsize=10)
    ax2.set_ylabel('Delay', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Train', fontsize=12, fontweight='bold')
    ax2.set_title('Delay Overview', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    if train_schedules is not None:
        for train_id in range(num_trains):
            if train_id in train_delays and train_delays[train_id]:
                # Filter only positive delays
                positive_delays = [d for d in train_delays[train_id] if d['delay'] > 0]

                if positive_delays:

                    for delay_idx, delay_info in enumerate(positive_delays):
                        x_pos = train_id
                        scheduled = delay_info['scheduled']
                        actual = delay_info['actual']

                        rect = plt.Rectangle((x_pos - bar_width/2, scheduled),
                                            bar_width, actual - scheduled,
                                            facecolor=colors[train_id % len(colors)],
                                            alpha=0.5,
                                            edgecolor='black',
                                            linewidth=1)
                        ax2.add_patch(rect)

                        ax2.text(x_pos, delay_info['scheduled'] + delay_info['delay'] / 2,
                                f'+{delay_info["delay"]}',
                                ha='center', va='center', fontsize=7, fontweight='bold',
                                rotation=90)

    plt.tight_layout(pad=3)
    plt.show()

    return fig, (ax1, ax2)