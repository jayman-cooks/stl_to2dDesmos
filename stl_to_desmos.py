import trimesh
import numpy as np
import matplotlib.pyplot as plt


# Load the STL file
stl_path = "" # insert your path to your stl
rx_deg = -30      # Rotation around X (e.g. tilt forward/backward)
ry_deg = 45     # Rotation around Y (e.g. rotate left/right)
rz_deg = 40       # Rotation around Z (e.g. spin around vertical)
output_file = 'desmos_output.txt'
max_edges = 1000  # Limit number of segments to avoid Desmos slowdown, make sure you use a low poly model

# === FUNCTIONS ===

def rotation_matrix_xyz(rx_deg=0, ry_deg=0, rz_deg=0):
    rx = np.radians(rx_deg)
    ry = np.radians(ry_deg)
    rz = np.radians(rz_deg)

    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(rx), -np.sin(rx)],
        [0, np.sin(rx),  np.cos(rx)]
    ])
    Ry = np.array([
        [np.cos(ry), 0, np.sin(ry)],
        [0, 1, 0],
        [-np.sin(ry), 0, np.cos(ry)]
    ])
    Rz = np.array([
        [np.cos(rz), -np.sin(rz), 0],
        [np.sin(rz),  np.cos(rz), 0],
        [0, 0, 1]
    ])
    return Rz @ Ry @ Rx

# === LOAD & PROCESS MESH ===

# Load STL file
mesh = trimesh.load(stl_path)

# Apply rotation
rotation = rotation_matrix_xyz(rx_deg, ry_deg, rz_deg)
rotated_vertices = mesh.vertices @ rotation.T

# Project to 2D (drop Z)
projected_vertices = rotated_vertices[:, :2]

# Get edges
edges = mesh.edges_unique
projected_edges = [(projected_vertices[e[0]], projected_vertices[e[1]]) for e in edges]

# === OPTIONAL PREVIEW ===
plt.figure(figsize=(6, 6))
for p1, p2 in projected_edges[:max_edges]:
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'k-', linewidth=0.5)
plt.axis('equal')
plt.title("2D Projection Preview")
plt.show()

# === EXPORT TO DESMOS ===
with open(output_file, "w") as f:
    for p1, p2 in projected_edges[:max_edges]:
        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1
        line_expr = f"({x1:.3f} + ({dx:.3f}) * t, {y1:.3f} + ({dy:.3f}) * t) \\left\\{{0 \\le t \\le 1\\right\\}}\n"
        f.write(line_expr)

print(f"\nExported {min(len(projected_edges), max_edges)} segments to '{output_file}'")
