from vpython import sphere, rate, vector, textures, scene
import time

# Configure the 3D scene
scene.title = "Real-Time Rotating Earth"
scene.width = 800
scene.height = 600
scene.autoscale = False
scene.center = vector(0, 0, 0)

# Create Earth with texture
earth = sphere(
    pos=vector(0, 0, 0),
    radius=5,
    texture=textures.earth,
    make_trail=False
)

# Constants
rotation_period_seconds = 86400  # One full rotation = 86400 seconds (24h)
time_scale = 3600  # Speed-up time (e.g., 3600 = 1 second real-time = 1 hour simulated)

# Angular speed in radians per second (scaled)
angular_speed = (2 * 3.141592653589793) / rotation_period_seconds  # rad/s

# Rotation loop
prev_time = time.time()

while True:
    rate(100)  # Refresh rate (fps limit)
    
    # Calculate delta time
    current_time = time.time()
    delta_time = current_time - prev_time
    prev_time = current_time

    # Rotate Earth (scaled time)
    earth.rotate(angle=angular_speed * delta_time * time_scale, axis=vector(0, 1, 0))
