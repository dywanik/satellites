from vpython import sphere, rate, vector, textures, scene, keysdown, color, box
import time
import math

# Scene setup
scene.title = "Real-Time Rotating Earth with Satellite"
scene.width = 1000
scene.height = 700
scene.autoscale = False
scene.center = vector(0, 0, 0)
scene.background = color.black

# Earth model
earth = sphere(
    pos=vector(0, 0, 0),
    radius=5,
    texture=textures.earth,
    shininess=0
)

# Satellite model
orbit_radius = 6.5
satellite = box(
    pos=vector(orbit_radius, 0, 0),
    size=vector(0.1, 0.05, 0.05),
    color=color.red,
    make_trail=True,
    trail_type="points",
    interval=10,
    retain=100
)

# Constants
rotation_period = 86400  # seconds for Earth rotation (1 day)
earth_angular_speed = (2 * math.pi) / rotation_period  # radians/sec
satellite_orbit_period = 5400  # e.g. 90 minutes
satellite_angular_speed = (2 * math.pi) / satellite_orbit_period

# Time control
time_scale = 3600  # speed up time: 1s real = 1h simulated
paused = False
prev_time = time.time()

# Instructions
print("Controls:")
print("  ↑ Arrow = increase time speed")
print("  ↓ Arrow = decrease time speed")
print("  Spacebar = pause/resume simulation")

# Main loop
while True:
    rate(100)
    now = time.time()
    delta_real = now - prev_time
    prev_time = now

    if not paused:
        delta_sim = delta_real * time_scale

        # Rotate Earth
        earth.rotate(angle=earth_angular_speed * delta_sim, axis=vector(0, 1, 0))

        # Move satellite in circular orbit
        angle = satellite_angular_speed * delta_sim
        x = orbit_radius * math.cos(angle)
        z = orbit_radius * math.sin(angle)
        satellite.pos = vector(x, 0, z)

    # Handle key input
    keys = keysdown()
    if "up" in keys:
        time_scale *= 2
        print(f"Time scale increased to {time_scale}x")
        time.sleep(0.2)
    elif "down" in keys:
        time_scale = max(1, time_scale // 2)
        print(f"Time scale decreased to {time_scale}x")
        time.sleep(0.2)
    elif " " in keys:
        paused = not paused
        print("Paused" if paused else "Resumed")
        time.sleep(0.3)
