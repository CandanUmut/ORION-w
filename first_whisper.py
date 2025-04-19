import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants for water and simulation
density = 1000       # kg/m^3
gravity = 9.81       # m/s^2
N = 100              # grid size
dx = 0.01            # spatial step
dt = 0.001           # time step
time_steps = 500     # total simulation steps

# Material interface - simulate via surface tension variations
# e.g., center = glass (0.072), outer = metal (0.09), edge = wood (0.05)
surface_tension_map = np.ones((N, N)) * 0.072
surface_tension_map[:N//3, :] = 0.05
surface_tension_map[N//3:2*N//3, :] = 0.072
surface_tension_map[2*N//3:, :] = 0.09

# Initialize wave state and velocity
z = np.zeros((N, N))
v = np.zeros((N, N))

# Embedded geometry: hexagon-like pulse pattern
for i in range(N):
    for j in range(N):
        if abs(i - N//2) + abs(j - N//2) < 15:  # diamond approximation of a hexagon
            z[i, j] = 0.005 * np.sin(np.sqrt((i - N//2)**2 + (j - N//2)**2))

# Laplacian operator
def laplacian(Z):
    return (
        -4 * Z
        + np.roll(Z, 1, axis=0)
        + np.roll(Z, -1, axis=0)
        + np.roll(Z, 1, axis=1)
        + np.roll(Z, -1, axis=1)
    ) / dx**2

# Feedback loop modifier function
def adjust_pulse(v, threshold=0.001):
    energy = np.mean(np.abs(v))
    modulation = np.clip(energy * 10, 0.5, 1.5)
    return modulation

# Store animation frames
frames = []

# Simulate with feedback and material effects
for t in range(time_steps):
    mod_factor = adjust_pulse(v)
    local_surface_tension = surface_tension_map * mod_factor
    force = local_surface_tension * laplacian(z) - density * gravity * z
    v += dt * force / density
    z += dt * v
    frames.append(z.copy())

# Animate the result
fig, ax = plt.subplots()
im = ax.imshow(frames[0], cmap='coolwarm', animated=True, vmin=-0.01, vmax=0.01)
ax.set_title("Water Resonance: Geometry + Material + Feedback")

def update(frame):
    im.set_array(frame)
    return [im]

ani = FuncAnimation(fig, update, frames=frames, interval=30, blit=True)
plt.close()

ani
