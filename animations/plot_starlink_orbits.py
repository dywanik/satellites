import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

MU = 398600.4418  # km^3/s^2

def parse_tle(lines):
    name = lines[0].strip()
    line2 = lines[2].strip()
    
    if not name.upper().startswith("STARLINK"):
        return None
    
    inclination = float(line2[8:16])  # degrees
    eccentricity = float(f"0.{line2[26:33]}")
    mean_motion = float(line2[52:63])  # revs per day

    # calculate semi-major axis
    n_rad_s = mean_motion * 2 * math.pi / 86400
    a = (MU / (n_rad_s ** 2)) ** (1/3)
    
    return {
        'name': name,
        'a': a,
        'e': eccentricity,
        'i': math.radians(inclination)
    }

def generate_orbit(sat, num_points=100):
    a = sat['a']
    e = sat['e']
    i = sat['i']
    
    # Parametrize orbit in its orbital plane
    theta = [2 * math.pi * t / num_points for t in range(num_points)]
    r = [a * (1 - e**2) / (1 + e * math.cos(t)) for t in theta]

    x_orb = [r[j] * math.cos(theta[j]) for j in range(num_points)]
    y_orb = [r[j] * math.sin(theta[j]) for j in range(num_points)]
    z_orb = [0 for _ in range(num_points)]

    # Rotate by inclination (around x-axis)
    x, y, z = [], [], []
    for j in range(num_points):
        xj = x_orb[j]
        yj = y_orb[j] * math.cos(i)
        zj = y_orb[j] * math.sin(i)
        x.append(xj)
        y.append(yj)
        z.append(zj)

    return x, y, z

def plot_earth(ax, radius=6371):
    # Sphere for Earth
    u = np.linspace(0, 2 * math.pi, 50)
    v = np.linspace(0, math.pi, 50)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, rstride=1, cstride=1, color='blue', alpha=0.3)

def plot_starlink_orbits(tle_file):
    with open(tle_file, 'r') as f:
        lines = f.readlines()

    sats = []
    for i in range(0, len(lines), 3):
        if i + 2 >= len(lines):
            continue
        sat = parse_tle(lines[i:i+3])
        if sat:
            sats.append(sat)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    plot_earth(ax)

    for sat in sats:
        x, y, z = generate_orbit(sat)
        ax.plot(x, y, z, linewidth=0.5)

    ax.set_title("Starlink Satellite Orbits Around Earth")
    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.set_zlabel("Z (km)")
    ax.set_box_aspect([1,1,1])
    plt.tight_layout()
    plt.show()

# -----
# Add this to the top:
import numpy as np

# Run it like this:
plot_starlink_orbits("tle.txt")
