import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Simulation constants
N = 100
dx = 0.01
dt = 0.001
steps = 500

# Flow field initialization (2D vector field representing the fluid)
flow_x = np.zeros((N, N))
flow_y = np.zeros((N, N))

# Simulate a natural flow environment (river-like)
for i in range(N):
    flow_x[:, i] = 0.02 * np.sin(np.pi * i / N)  # soft directional flow
    flow_y[:, i] = 0.005 * np.cos(np.pi * i / N)  # minor turbulence

# Vehicle state
vehicle_pos = np.array([N//2, N//3], dtype=float)
path_controlled = [vehicle_pos.copy()]
steering_angle = 0.0  # radians

# Resonance with directional steering
def apply_resonance_with_steering(pos, step, angle):
    x, y = int(pos[0]), int(pos[1])
    radius = 5
    dx_steer = np.cos(angle)
    dy_steer = np.sin(angle)
    for i in range(-radius, radius+1):
        for j in range(-radius, radius+1):
            xi, yj = x+i, y+j
            if 0 <= xi < N and 0 <= yj < N:
                dist = np.sqrt(i**2 + j**2)
                if dist < radius:
                    steer_bias = (i * dx_steer + j * dy_steer) / (dist + 1e-5)
                    mod = 0.002 * np.sin(step / 10) * (1 - dist / radius) * steer_bias
                    flow_x[xi, yj] += mod
                    flow_y[xi, yj] += mod * 0.5

# Simulate with steering
for t in range(steps):
    steering_angle = np.sin(t / 50) * 0.5  # oscillating path
    apply_resonance_with_steering(vehicle_pos, t, steering_angle)
    x, y = int(vehicle_pos[0]), int(vehicle_pos[1])
    if 0 <= x < N and 0 <= y < N:
        vehicle_pos[0] += flow_x[x, y] * 50
        vehicle_pos[1] += flow_y[x, y] * 50
    path_controlled.append(vehicle_pos.copy())

# Animate controlled path
fig, ax = plt.subplots()
ax.set_xlim(0, N)
ax.set_ylim(0, N)
line, = ax.plot([], [], 'g-', label='Controlled Vehicle Path')
point, = ax.plot([], [], 'go')
ax.set_title("Resonant Vehicle with Directional Control")
ax.legend()

def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

def update(frame):
    data = np.array(path_controlled[:frame])
    line.set_data(data[:, 1], data[:, 0])
    point.set_data(data[-1, 1], data[-1, 0])
    return line, point

ani = FuncAnimation(fig, update, frames=len(path_controlled), init_func=init, interval=30, blit=True)
plt.show()
