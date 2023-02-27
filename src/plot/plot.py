from .fetch import fetch_rankings_delta
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

history_indices, history_values = None, None

def animate_iteration(idx: int):
    global history_indices, history_values
    rankings = fetch_rankings_delta()
    if rankings is None: return

    if history_indices is None:
        history_indices = [idx]
        history_values = [[value[1]] for value in rankings]
    else:
        history_indices.append(idx)
        for history, value in zip(history_values, rankings):
            history.append(value[1])

    plt.cla()
    data_point_count = min(60, len(history_indices))
    for idx, (value, (name, _)) in enumerate(zip(history_values, rankings)):
        print(name, value)
        plt.plot(history_indices[-data_point_count:],
                 value[-data_point_count:],
                 label=name, color=plt.cm.tab20(idx), linewidth=1.5)
    plt.legend(loc='upper left')
    plt.tight_layout()

def start():
    plt.figure(figsize = (20, 8))
    plt.style.use('fivethirtyeight')
    ani = FuncAnimation(plt.gcf(), animate_iteration, interval=1000)
    plt.tight_layout()
    plt.get_current_fig_manager().full_screen_toggle()
    plt.show()
