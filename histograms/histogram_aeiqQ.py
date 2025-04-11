import sys
import matplotlib.pyplot as plt

def load_data(filename):
    data = {'a': [], 'e': [], 'i': [], 'q': [], 'Q': []}
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            data['a'].append(float(parts[0]))
            data['e'].append(float(parts[1]))
            data['i'].append(float(parts[2]))
            data['q'].append(float(parts[3]))
            data['Q'].append(float(parts[4]))
    return data

def connect_quit_event(fig):
    def on_key(event):
        if event.key == 'q':
            plt.close('all')
            sys.exit(0)
    fig.canvas.mpl_connect('key_press_event', on_key)

def plot_single(data, key, min_val=None, max_val=None, bins=100):
    values = data[key]
    if min_val is not None and max_val is not None:
        values = [v for v in values if min_val <= v <= max_val]
    elif min_val is not None:
        values = [v for v in values if v >= min_val]
    elif max_val is not None:
        values = [v for v in values if v <= max_val]

    fig = plt.figure()
    plt.hist(values, bins=bins, edgecolor='black')
    plt.title(f"Histogram of {key}")
    plt.xlabel(key)
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.legend([f"Objects: {len(values)}"])
    plt.tight_layout()
    connect_quit_event(fig)
    plt.show()

def plot_all(data):
    for key in data:
        plot_single(data, key)

def print_usage():
    print("Usage:")
    print("  python plot_histograms.py [key] [min] [max] [bins]")
    print()
    print("Arguments:")
    print("  key     Orbital element to plot: a, e, i, q, Q")
    print("  min     Optional minimum value for filtering")
    print("  max     Optional maximum value for filtering")
    print("  bins    Optional number of histogram bins (default: 100)")
    print()
    print("Examples:")
    print("  python plot_histograms.py                  # Plot all elements")
    print("  python plot_histograms.py a                # Plot semi-major axis")
    print("  python plot_histograms.py e 0.001 0.02 40  # Plot eccentricity in range")
    print("  python plot_histograms.py q 300            # Plot perigee > 300 km")
    print()
    print("Flags:")
    print("  -h, --help      Show this help message and exit")
    print()
    print("Shortcuts:")
    print("  Press 'q' while viewing a plot to exit the script")
    sys.exit(0)

if __name__ == '__main__':
    filename = 'aeiqq_from_tle.txt'
    data = load_data(filename)

    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print_usage()

    key = None
    min_val = None
    max_val = None
    bins = 100

    if len(sys.argv) >= 2:
        key = sys.argv[1]
        if key not in data:
            print(f"Invalid key '{key}'. Use one of: a, e, i, q, Q")
            sys.exit(1)
    if len(sys.argv) >= 3:
        min_val = float(sys.argv[2])
    if len(sys.argv) >= 4:
        max_val = float(sys.argv[3])
    if len(sys.argv) >= 5:
        bins = int(sys.argv[4])

    if key:
        plot_single(data, key, min_val, max_val, bins)
    else:
        plot_all(data)
