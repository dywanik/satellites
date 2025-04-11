import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

MU = 398600.4418  # km^3/s^2
EARTH_RADIUS = 6371  # km

# === TLE parsing ===
def parse_tle(lines):
    name = lines[0].strip()
    line2 = lines[2].strip()
    if not name.upper().startswith("STARLINK"):
        return None

    i_deg = float(line2[8:16])
    e = float(f"0.{line2[26:33]}")
    n = float(line2[52:63])  # rev/day

    i = math.radians(i_deg)
    n_rad_s = n * 2 * math.pi / 86400
    a = (MU / (n_rad_s ** 2)) ** (1/3)

    return {
        'name': name,
        'a': a,
        'e': e,
        'i': i,
        'n_rad_s': n_rad_s,
    }

# === Orbit position ===
def generate_position(sat, time_s):
    M = sat['n_rad_s'] * time_s
    theta = M % (2 * math.pi)
    r = sat['a'] * (1 - sat['e'] ** 2) / (1 + sat['e'] * math.cos(theta))

    x_orb = r * math.cos(theta)
    y_orb = r * math.sin(theta)
    z_orb = 0

    x = x_orb
    y = y_orb * math.cos(sat['i'])
    z = y_orb * math.sin(sat['i'])

    return x, y, z

# === Ground track utilities ===
def to_latlon(x, y, z):
    r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    lat = math.asin(z / r)
    lon = math.atan2(y, x)
    return math.degrees(lat), math.degrees(lon)

def latlon_to_ecef(lat, lon, t=0, radius=EARTH_RADIUS):
    # Apply Earth rotation (inertial frame → rotating Earth)
    omega_deg_per_sec = 360 / 86164
    lon_rotated = lon - omega_deg_per_sec * t
    lon_rad = math.radians(lon_rotated)
    lat_rad = math.radians(lat)

    x = radius * math.cos(lat_rad) * math.cos(lon_rad)
    y = radius * math.cos(lat_rad) * math.sin(lon_rad)
    z = radius * math.sin(lat_rad)
    return x, y, z

# === Earth sphere ===
def plot_earth(ax):
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x = EARTH_RADIUS * np.outer(np.cos(u), np.sin(v))
    y = EARTH_RADIUS * np.outer(np.sin(u), np.sin(v))
    z = EARTH_RADIUS * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='blue', alpha=0.3)

# === Animate! ===
def animate_starlink_orbits(tle_file, hours=1, step_minutes=1):
    with open(tle_file, 'r') as f:
        lines = f.readlines()

    sats = []
    for i in range(0, len(lines), 3):
        if i + 2 >= len(lines):
            continue
        sat = parse_tle(lines[i:i + 3])
        if sat:
            sats.append(sat)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    plot_earth(ax)

    scatters = [ax.plot([], [], [], 'o', markersize=2)[0] for _ in sats]
    trails = [ax.plot([], [], [], '-', linewidth=0.5, color='orange')[0] for _ in sats]
    trail_history = [[] for _ in sats]
    state = {
        'trail_enabled': True,
        'speed_multiplier': 1.0
    }

    max_a = max(s['a'] for s in sats)
    ax.set_xlim([-max_a, max_a])
    ax.set_ylim([-max_a, max_a])
    ax.set_zlim([-max_a, max_a])
    ax.set_box_aspect([1, 1, 1])
    ax.set_title("Starlink Coverage (press 'T' to toggle trails, ↑↓ to change speed)")

    times = np.arange(0, hours * 3600, step_minutes * 60)

    def update(frame_idx):
        t = times[frame_idx] * state['speed_multiplier']
        for j, sat in enumerate(sats):
            x, y, z = generate_position(sat, t)
            scatters[j].set_data([x], [y])
            scatters[j].set_3d_properties([z])

            lat, lon = to_latlon(x, y, z)
            gx, gy, gz = latlon_to_ecef(lat, lon, t=t)
            trail_history[j].append((gx, gy, gz))
            if len(trail_history[j]) > 100:
                trail_history[j] = trail_history[j][-100:]

            if state['trail_enabled']:
                tx, ty, tz = zip(*trail_history[j])
                trails[j].set_data(tx, ty)
                trails[j].set_3d_properties(tz)
            else:
                trails[j].set_data([], [])
                trails[j].set_3d_properties([])

        ax.set_title(f"Time = {t / 3600:.2f} hrs  |  Speed x{state['speed_multiplier']:.1f}  |  T = toggle trails, ↑↓ = speed")
        return scatters + trails

    ani = FuncAnimation(fig, update, frames=len(times), interval=100)

    def on_key(event):
        if event.key.lower() == 't':
            state['trail_enabled'] = not state['trail_enabled']
            print(f"Trails {'enabled' if state['trail_enabled'] else 'disabled'}")
        elif event.key == 'up':
            state['speed_multiplier'] *= 2
            print(f"Speed increased to x{state['speed_multiplier']:.1f}")
        elif event.key == 'down':
            state['speed_multiplier'] /= 2
            if state['speed_multiplier'] < 0.1:
                state['speed_multiplier'] = 0.1
            print(f"Speed decreased to x{state['speed_multiplier']:.1f}")

    fig.canvas.mpl_connect('key_press_event', on_key)
    plt.show()

# === Run it ===
animate_starlink_orbits("tle.txt", hours=1, step_minutes=1)