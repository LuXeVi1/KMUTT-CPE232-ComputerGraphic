"""
Module 2: 3D Geometric Transformations
Based on Exam Q4 - 3D Transformation (CPE 381)

3D uses 4x4 homogeneous matrices:
  [x']   [           ] [x]
  [y'] = [  4x4 M    ] [y]
  [z']   [           ] [z]
  [1 ]   [           ] [1]
"""
import numpy as np
from tabulate import tabulate

# ============================================================
# Basic 3D Transformation Matrices
# ============================================================

def translation_3d(tx, ty, tz, show=False):
    M = np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ], dtype=float)
    if show:
        print(f"\n  Formula: 3D Translation T({tx}, {ty}, {tz})")
        print(f"  ┌              ┐")
        print(f"  │ 1  0  0  tx  │   tx = {tx}")
        print(f"  │ 0  1  0  ty  │   ty = {ty}")
        print(f"  │ 0  0  1  tz  │   tz = {tz}")
        print(f"  │ 0  0  0   1  │")
        print(f"  └              ┘")
    return M

def scaling_3d(sx, sy, sz, show=False):
    M = np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    if show:
        print(f"\n  Formula: 3D Scaling S({sx}, {sy}, {sz})")
        print(f"  ┌              ┐")
        print(f"  │ sx  0  0  0  │   sx = {sx}")
        print(f"  │ 0  sy  0  0  │   sy = {sy}")
        print(f"  │ 0  0  sz  0  │   sz = {sz}")
        print(f"  │ 0  0  0   1  │")
        print(f"  └              ┘")
    return M

def rotation_x_3d(angle_deg, show=False):
    """Rotation about the x-axis."""
    t = np.radians(angle_deg)
    c, s = np.cos(t), np.sin(t)
    M = np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    if show:
        print(f"\n  Formula: 3D Rotation about X-axis, θ = {angle_deg}°")
        print(f"  ┌                     ┐")
        print(f"  │  1    0      0    0  │")
        print(f"  │  0   cosθ  -sinθ  0  │   cosθ = cos({angle_deg}°) = {c:.6f}")
        print(f"  │  0   sinθ   cosθ  0  │   sinθ = sin({angle_deg}°) = {s:.6f}")
        print(f"  │  0    0      0    1  │")
        print(f"  └                     ┘")
    return M

def rotation_y_3d(angle_deg, show=False):
    """Rotation about the y-axis."""
    t = np.radians(angle_deg)
    c, s = np.cos(t), np.sin(t)
    M = np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    if show:
        print(f"\n  Formula: 3D Rotation about Y-axis, θ = {angle_deg}°")
        print(f"  ┌                     ┐")
        print(f"  │  cosθ  0   sinθ  0  │   cosθ = cos({angle_deg}°) = {c:.6f}")
        print(f"  │   0    1    0    0  │   sinθ = sin({angle_deg}°) = {s:.6f}")
        print(f"  │ -sinθ  0   cosθ  0  │")
        print(f"  │   0    0    0    1  │")
        print(f"  └                     ┘")
        print(f"\n  Note: Ry has sinθ in (0,2) and -sinθ in (2,0)")
    return M

def rotation_z_3d(angle_deg, show=False):
    """Rotation about the z-axis."""
    t = np.radians(angle_deg)
    c, s = np.cos(t), np.sin(t)
    M = np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    if show:
        print(f"\n  Formula: 3D Rotation about Z-axis, θ = {angle_deg}°")
        print(f"  ┌                     ┐")
        print(f"  │  cosθ  -sinθ  0  0  │   cosθ = cos({angle_deg}°) = {c:.6f}")
        print(f"  │  sinθ   cosθ  0  0  │   sinθ = sin({angle_deg}°) = {s:.6f}")
        print(f"  │   0      0    1  0  │")
        print(f"  │   0      0    0  1  │")
        print(f"  └                     ┘")
    return M

# ============================================================
# 3D Composite: Rotation about arbitrary axis through origin
# ============================================================

def rotation_arbitrary_axis(angle_deg, ux, uy, uz, show=False):
    """
    Rotation about an arbitrary axis through the origin defined by
    unit vector (ux, uy, uz). Uses Rodrigues' rotation formula in matrix form.
    """
    t = np.radians(angle_deg)
    c = np.cos(t)
    s = np.sin(t)

    M = np.array([
        [c + ux*ux*(1-c),      ux*uy*(1-c) - uz*s, ux*uz*(1-c) + uy*s, 0],
        [uy*ux*(1-c) + uz*s,   c + uy*uy*(1-c),     uy*uz*(1-c) - ux*s, 0],
        [uz*ux*(1-c) - uy*s,   uz*uy*(1-c) + ux*s,  c + uz*uz*(1-c),    0],
        [0, 0, 0, 1]
    ], dtype=float)

    if show:
        print(f"\n  Rodrigues' Rotation Matrix about axis ({ux:.4f}, {uy:.4f}, {uz:.4f})")
        print(f"  θ = {angle_deg}°, cosθ = {c:.6f}, sinθ = {s:.6f}")
        print(f"\n  R = cosθ·I + (1-cosθ)·(u⊗u) + sinθ·[u]×")
    return M


def rotation_about_arbitrary_line(angle_deg, px, py, pz, vx, vy, vz, show=False):
    """
    Rotation about an arbitrary line passing through point (px,py,pz)
    with direction vector (vx,vy,vz).

    Steps:
    1. Translate so point P is at origin
    2. Rotate to align axis with z-axis (Rx then Ry)
    3. Rotate by θ about z-axis
    4. Inverse of step 2 (Ry^-1 then Rx^-1)
    5. Translate back
    """
    # Normalize direction vector
    length = np.sqrt(vx*vx + vy*vy + vz*vz)
    a, b, c_dir = vx/length, vy/length, vz/length

    if show:
        print(f"\n{'='*60}")
        print(f"  3D Rotation about Arbitrary Line")
        print(f"  Point on line: G = ({px}, {py}, {pz})")
        print(f"  Direction vector: V = ({vx}, {vy}, {vz})")
        print(f"  |V| = sqrt({vx}² + {vy}² + {vz}²) = sqrt({vx*vx + vy*vy + vz*vz}) = {length:.6f}")
        print(f"  Unit vector: u = ({a:.6f}, {b:.6f}, {c_dir:.6f})")
        print(f"  Rotation angle: θ = {angle_deg}°")
        print(f"{'='*60}")

    # Step 1: Translate P to origin
    if show:
        print(f"\n  Step 1: Translate G to origin => T(-{px}, -{py}, -{pz})")
    T1 = translation_3d(-px, -py, -pz, show)

    # Step 2: Rotate to align with z-axis
    # First rotate about x-axis to bring vector into xz-plane
    d = np.sqrt(b*b + c_dir*c_dir)

    if show:
        print(f"\n  Step 2: Align axis with z-axis")
        print(f"  d = sqrt(b² + c²) = sqrt({b:.6f}² + {c_dir:.6f}²) = {d:.6f}")

    if d > 1e-10:
        cos_alpha = c_dir / d
        sin_alpha = b / d
        Rx = np.array([
            [1, 0, 0, 0],
            [0, cos_alpha, -sin_alpha, 0],
            [0, sin_alpha, cos_alpha, 0],
            [0, 0, 0, 1]
        ], dtype=float)
        if show:
            alpha_deg = np.degrees(np.arctan2(b, c_dir))
            print(f"  Rx: rotate about x-axis to bring into xz-plane")
            print(f"    cos(α) = c/d = {c_dir:.6f}/{d:.6f} = {cos_alpha:.6f}")
            print(f"    sin(α) = b/d = {b:.6f}/{d:.6f} = {sin_alpha:.6f}")
            print(f"    α = {alpha_deg:.4f}°")
            print_matrix_4x4(Rx, "Rx")
    else:
        Rx = np.eye(4)
        if show:
            print(f"  d ≈ 0, skip Rx (axis already in xz-plane)")

    # Rotate about y-axis to align with z-axis
    cos_beta = d
    sin_beta = -a  # negative because we rotate to align with +z
    Ry = np.array([
        [cos_beta, 0, sin_beta, 0],
        [0, 1, 0, 0],
        [-sin_beta, 0, cos_beta, 0],
        [0, 0, 0, 1]
    ], dtype=float)
    if show:
        beta_deg = np.degrees(np.arctan2(-a, d))
        print(f"\n  Ry: rotate about y-axis to align with z-axis")
        print(f"    cos(β) = d = {d:.6f}")
        print(f"    sin(β) = -a = {-a:.6f}")
        print(f"    β = {beta_deg:.4f}°")
        print_matrix_4x4(Ry, "Ry")

    # Step 3: Rotate about z-axis by θ
    if show:
        print(f"\n  Step 3: Rotate θ = {angle_deg}° about z-axis")
    Rz = rotation_z_3d(angle_deg, show)

    # Step 4: Inverse rotations
    Ry_inv = Ry.T.copy()
    Ry_inv[0:3, 3] = 0; Ry_inv[3, 0:3] = 0; Ry_inv[3, 3] = 1
    Rx_inv = Rx.T.copy()
    Rx_inv[0:3, 3] = 0; Rx_inv[3, 0:3] = 0; Rx_inv[3, 3] = 1

    if show:
        print(f"\n  Step 4: Undo alignment rotations")
        print_matrix_4x4(Ry_inv, "Ry⁻¹")
        print_matrix_4x4(Rx_inv, "Rx⁻¹")

    # Step 5: Translate back
    if show:
        print(f"\n  Step 5: Translate back => T({px}, {py}, {pz})")
    T2 = translation_3d(px, py, pz, show)

    # Composite: M = T2 · Rx_inv · Ry_inv · Rz · Ry · Rx · T1
    M = T2 @ Rx_inv @ Ry_inv @ Rz @ Ry @ Rx @ T1

    if show:
        print(f"\n  Final: M = T2 · Rx⁻¹ · Ry⁻¹ · Rz(θ) · Ry · Rx · T1")
        print_matrix_4x4(M, "Composite Matrix M")

    return M


# ============================================================
# 3D Perspective Projection
# ============================================================

def perspective_projection(d, show=False):
    """
    Standard perspective projection matrix.
    Projects onto xy-plane with center of projection at (0,0,d).

    x_proj = x * d / (d + z)  [or x / (1 + z/d)]
    y_proj = y * d / (d + z)  [or y / (1 + z/d)]

    In homogeneous coords:
    [x']   [1  0  0    0 ] [x]   [  x  ]       x' = x/(1+z/d) = xd/(d+z)
    [y'] = [0  1  0    0 ] [y] = [  y  ]       y' = y/(1+z/d) = yd/(d+z)
    [z']   [0  0  0    0 ] [z]   [  0  ]
    [w']   [0  0  1/d  1 ] [1]   [z/d+1]
    """
    M = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 1.0/d, 1]
    ], dtype=float)
    if show:
        print(f"\n  Formula: Standard Perspective Projection")
        print(f"  Center of projection on z-axis at distance d = {d}")
        print(f"  Projects onto xy-plane (z = 0)")
        print(f"\n  x_proj = x·d/(d+z) = x/(1 + z/d)")
        print(f"  y_proj = y·d/(d+z) = y/(1 + z/d)")
        print(f"\n  Homogeneous matrix:")
        print(f"  ┌                  ┐")
        print(f"  │ 1   0   0    0   │")
        print(f"  │ 0   1   0    0   │")
        print(f"  │ 0   0   0    0   │")
        print(f"  │ 0   0  1/d   1   │   1/d = 1/{d} = {1.0/d:.6f}")
        print(f"  └                  ┘")
        print(f"\n  After multiplication, divide by w' to get Cartesian coords:")
        print(f"  w' = z/d + 1 = (z + d)/d")
        print(f"  x_proj = x/w',  y_proj = y/w'")
    return M

def apply_perspective(M, points_3d, d, show=False):
    """Apply perspective projection and return 2D projected points."""
    results = []
    if show:
        print(f"\n  Applying projection to each vertex:")
    for name, (x, y, z) in points_3d:
        v = np.array([x, y, z, 1.0])
        r = M @ v
        w = r[3]
        x_proj = r[0] / w
        y_proj = r[1] / w
        if show:
            print(f"\n    {name}({x},{y},{z}):")
            print(f"      [x,y,z,1] = [{x}, {y}, {z}, 1]")
            print(f"      M × v = [{r[0]:.4f}, {r[1]:.4f}, {r[2]:.4f}, {r[3]:.4f}]")
            print(f"      w' = z/d + 1 = {z}/{d} + 1 = {z/d:.4f} + 1 = {w:.4f}")
            print(f"      x_proj = {x}/w' = {x}/{w:.4f} = {x_proj:.4f}")
            print(f"      y_proj = {y}/w' = {y}/{w:.4f} = {y_proj:.4f}")
            print(f"      => {name}'({x_proj:.4f}, {y_proj:.4f})")
        results.append((name, x_proj, y_proj))
    return results

# ============================================================
# Helpers
# ============================================================

def print_matrix_4x4(M, label="Matrix"):
    print(f"\n  {label}:")
    for i in range(4):
        row_str = "  │ " + "  ".join(f"{M[i,j]:10.4f}" for j in range(4)) + "  │"
        if i == 0:
            print("  ┌" + " " * (len(row_str) - 4) + "┐")
        print(row_str)
        if i == 3:
            print("  └" + " " * (len(row_str) - 4) + "┘")

def apply_3d_transform(M, points, show=False):
    """Apply 4x4 matrix to list of (name, x, y, z) points."""
    results = []
    if show:
        print(f"\n  Applying transformation to each vertex:")
    for name, x, y, z in points:
        v = np.array([x, y, z, 1.0])
        r = M @ v
        if show:
            print(f"\n    {name}({x},{y},{z}):")
            print(f"      [{x}, {y}, {z}, 1] × M = [{r[0]:.4f}, {r[1]:.4f}, {r[2]:.4f}, {r[3]:.4f}]")
            print(f"      => {name}'({r[0]:.4f}, {r[1]:.4f}, {r[2]:.4f})")
        results.append((name, r[0], r[1], r[2]))
    return results

def print_3d_results_table(original, transformed):
    """Print before/after table for 3D points."""
    table = []
    for (name, x, y, z), (_, x2, y2, z2) in zip(original, transformed):
        table.append([name, f"({x},{y},{z})", f"({x2:.3f},{y2:.3f},{z2:.3f})"])
    headers = ["Point", "Original", "Transformed"]
    print("\n" + tabulate(table, headers=headers, tablefmt="fancy_grid"))
