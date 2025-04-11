import numpy as np
import matplotlib.pyplot as plt
from sgp4.api import Satrec
from sgp4.conveniences import sat_epoch_datetime
import math
import sys

def read_tles(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    sats = []
    for i in range(0, len(lines) - 2, 3):
        name = lines[i].strip()
        line1 = lines[i + 1].strip()
        line2 = lines[i + 2].strip()
        try:
            sat = Satrec.twoline2rv(line1, line2)
            sats.append((name, sat))
        except Exception as e:
            print(f"Error parsing TLE: {name} - {e}")
    return sats

def extract_parameter(sat, param):
    mu = 398600.4418  # Earth's gravitational parameter, km^3/s^2
    if param == 'e':
        return sat.ecco
    elif param == 'i':
        return math.degrees(sat.inclo)
    elif param == 'a':
        try:
            # Compute semi-major axis (km) from mean motion (rev/day)
            mean_motion = sat.no_kozai  # rad/min
            n = mean_motion * 60  # rad/hour
            a = (mu / (n * math.pi / 180 / 3600) ** 2) ** (1 / 3)
            return a
        except Exception as e:
            return None
    return None

def plot_histogram(values, param):
    param_labels = {
        'a': 'Semi-Major Axis (km)',
        'e': 'Eccentricity',
        'i': 'Inclination (degrees)'
    }

    plt.figure(figsize=(10, 6))
    plt.hist(values, bins=100, edgecolor='black')
    plt.title(f"Histogram of {param_labels.get(param, param)}")
    plt.xlabel(param_labels.get(param, param))
    plt.ylabel("Number of Objects")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Draw histogram from TLE catalog.")
    parser.add_argument("tle_file", help="Path to the TLE file")
    parser.add_argument("param", choices=["a", "e", "i"], help="Parameter to plot: a (semi-major axis), e (eccentricity), i (inclination)")
    args = parser.parse_args()

    sats = read_tles(args.tle_file)
    values = [extract_parameter(sat, args.param) for name, sat in sats]
    values = [v for v in values if v is not None]
    
    if not values:
        print("No valid satellite data found for the selected parameter.")
        return

    plot_histogram(values, args.param)

if __name__ == "__main__":
    main()
