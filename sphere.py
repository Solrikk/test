import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

def create_sphere(r=1.0, num_points=50):
    u = np.linspace(0, 2*np.pi, num_points)
    v = np.linspace(0, np.pi, num_points)
    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    z = r * np.outer(np.ones_like(u), np.cos(v))
    return x, y, z

def create_cube(min_coord=-1.0, max_coord=1.0):
    points = [
        [min_coord, min_coord, min_coord],
        [min_coord, min_coord, max_coord],
        [min_coord, max_coord, min_coord],
        [min_coord, max_coord, max_coord],
        [max_coord, min_coord, min_coord],
        [max_coord, min_coord, max_coord],
        [max_coord, max_coord, min_coord],
        [max_coord, max_coord, max_coord],
    ]
    return np.array(points)

def get_cube_edges(points):
    edges_indices = [
        (0,1), (0,2), (0,4),
        (3,1), (3,2), (3,7),
        (5,1), (5,4), (5,7),
        (6,2), (6,4), (6,7)
    ]
    edges = []
    for e in edges_indices:
        p1, p2 = points[e[0]], points[e[1]]
        edges.append((p1, p2))
    return edges

def deform_sphere(X, Y, Z, cube_limits):
    x_min, x_max, y_min, y_max, z_min, z_max = cube_limits
    X_deformed = np.where(X > x_max, x_max, X)
    X_deformed = np.where(X_deformed < x_min, x_min, X_deformed)
    Y_deformed = np.where(Y > y_max, y_max, Y)
    Y_deformed = np.where(Y_deformed < y_min, y_min, Y_deformed)
    Z_deformed = np.where(Z > z_max, z_max, Z)
    Z_deformed = np.where(Z_deformed < z_min, z_min, Z_deformed)
    return X_deformed, Y_deformed, Z_deformed

frames = 2000
interval_ms = 50

def update(frame, ax, sphere_container, cube_limits):
    r = 0.3 + (frame * 0.005)
    X, Y, Z = create_sphere(r, num_points=50)
    X, Y, Z = deform_sphere(X, Y, Z, cube_limits)
    if sphere_container[0] is not None:
        sphere_container[0].remove()
    sphere_container[0] = ax.plot_surface(X, Y, Z, color='lightblue', alpha=0.6, edgecolor='none')
    return sphere_container

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d', facecolor='black')
cube_coords = create_cube(-1.0, 1.0)
edges = get_cube_edges(cube_coords)
for (p1, p2) in edges:
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='white', linewidth=1, alpha=0.6)
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_zlim(-1.2, 1.2)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
for spine in (ax.xaxis, ax.yaxis, ax.zaxis):
    spine.pane.fill = False
    spine.pane.set_edgecolor('black')
sphere_container = [None]
cube_limits = [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0]
ani = animation.FuncAnimation(
    fig,
    func=update,
    fargs=(ax, sphere_container, cube_limits),
    frames=frames,
    interval=interval_ms,
    repeat=True,
    blit=False
)
plt.show()
