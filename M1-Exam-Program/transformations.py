"""
Module 1-1: 2D Geometric Transformations
Based on Lecture 1 - 2D Transformations (CPE 381)
"""
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt

# ============================================================
# Basic Transformation Matrices (with formula display)
# ============================================================

def translation_matrix(tx, ty, show=False):
    M = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]], dtype=float)
    if show:
        print(f"\n  Formula: Translation T(tx, ty)")
        print(f"  ┌           ┐")
        print(f"  │ 1   0  tx │   tx = {tx}")
        print(f"  │ 0   1  ty │   ty = {ty}")
        print(f"  │ 0   0   1 │")
        print(f"  └           ┘")
    return M

def scaling_matrix(sx, sy, show=False):
    M = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]], dtype=float)
    if show:
        print(f"\n  Formula: Scaling S(sx, sy)")
        print(f"  ┌           ┐")
        print(f"  │ sx  0   0 │   sx = {sx}")
        print(f"  │ 0   sy  0 │   sy = {sy}")
        print(f"  │ 0   0   1 │")
        print(f"  └           ┘")
    return M

def rotation_matrix(angle_deg, show=False):
    theta = np.radians(angle_deg)
    c, s = np.cos(theta), np.sin(theta)
    M = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)
    if show:
        print(f"\n  Formula: Rotation R(θ) counterclockwise")
        print(f"  ┌                  ┐")
        print(f"  │ cosθ  -sinθ   0  │   θ = {angle_deg}°")
        print(f"  │ sinθ   cosθ   0  │   cosθ = cos({angle_deg}°) = {c:.6f}")
        print(f"  │  0      0     1  │   sinθ = sin({angle_deg}°) = {s:.6f}")
        print(f"  └                  ┘")
    return M

def reflection_x_axis(show=False):
    M = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]], dtype=float)
    if show:
        print(f"\n  Formula: Reflection across x-axis")
        print(f"  x' = x,  y' = -y")
        print(f"  ┌            ┐")
        print(f"  │  1   0   0 │")
        print(f"  │  0  -1   0 │")
        print(f"  │  0   0   1 │")
        print(f"  └            ┘")
    return M

def reflection_y_axis(show=False):
    M = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=float)
    if show:
        print(f"\n  Formula: Reflection across y-axis")
        print(f"  x' = -x,  y' = y")
        print(f"  ┌            ┐")
        print(f"  │ -1   0   0 │")
        print(f"  │  0   1   0 │")
        print(f"  │  0   0   1 │")
        print(f"  └            ┘")
    return M

def reflection_origin(show=False):
    M = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]], dtype=float)
    if show:
        print(f"\n  Formula: Reflection across origin")
        print(f"  x' = -x,  y' = -y")
        print(f"  ┌            ┐")
        print(f"  │ -1   0   0 │")
        print(f"  │  0  -1   0 │")
        print(f"  │  0   0   1 │")
        print(f"  └            ┘")
    return M

def reflection_y_eq_x(show=False):
    M = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
    if show:
        print(f"\n  Formula: Reflection across y = x")
        print(f"  x' = y,  y' = x")
        print(f"  ┌           ┐")
        print(f"  │  0  1   0 │")
        print(f"  │  1  0   0 │")
        print(f"  │  0  0   1 │")
        print(f"  └           ┘")
    return M

def reflection_y_eq_neg_x(show=False):
    M = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, 1]], dtype=float)
    if show:
        print(f"\n  Formula: Reflection across y = -x")
        print(f"  x' = -y,  y' = -x")
        print(f"  ┌            ┐")
        print(f"  │  0  -1   0 │")
        print(f"  │ -1   0   0 │")
        print(f"  │  0   0   1 │")
        print(f"  └            ┘")
    return M

def reflection_line_x_eq(val, show=False):
    """Reflect across vertical line x = val."""
    if show:
        print(f"\n  Formula: Reflection across x = {val}")
        print(f"  Composite: T({val},0) · Ref_y · T(-{val},0)")
        print(f"  Step 1: Translate x={val} to origin => T(-{val}, 0)")
        print(f"  Step 2: Reflect across y-axis")
        print(f"  Step 3: Translate back => T({val}, 0)")
    T1 = translation_matrix(-val, 0, show)
    Ref = reflection_y_axis(show)
    T2 = translation_matrix(val, 0, show)
    return T2 @ Ref @ T1

def reflection_line_y_eq(val, show=False):
    """Reflect across horizontal line y = val."""
    if show:
        print(f"\n  Formula: Reflection across y = {val}")
        print(f"  Composite: T(0,{val}) · Ref_x · T(0,-{val})")
        print(f"  Step 1: Translate y={val} to origin => T(0, -{val})")
        print(f"  Step 2: Reflect across x-axis")
        print(f"  Step 3: Translate back => T(0, {val})")
    T1 = translation_matrix(0, -val, show)
    Ref = reflection_x_axis(show)
    T2 = translation_matrix(0, val, show)
    return T2 @ Ref @ T1

def reflection_y_eq_mx(m, show=False):
    """Reflect across line y = mx (through origin)."""
    theta = np.degrees(np.arctan(m))
    if show:
        print(f"\n  Formula: Reflection across y = {m}x")
        print(f"  θ = arctan(m) = arctan({m}) = {theta:.4f}°")
        print(f"  Composite: R(θ) · Ref_x · R(-θ)")
        print(f"  Step 1: Rotate by -θ = -{theta:.4f}° to align with x-axis")
        print(f"  Step 2: Reflect across x-axis")
        print(f"  Step 3: Rotate back by θ = {theta:.4f}°")
    R1 = rotation_matrix(-theta, show)
    Ref = reflection_x_axis(show)
    R2 = rotation_matrix(theta, show)
    return R2 @ Ref @ R1

def reflection_y_eq_mx_plus_b(m, b, show=False):
    """Reflect across line y = mx + b."""
    theta = np.degrees(np.arctan(m))
    if show:
        print(f"\n  Formula: Reflection across y = {m}x + {b}")
        print(f"  θ = arctan(m) = arctan({m}) = {theta:.4f}°")
        print(f"  Composite: T(0,b) · R(θ) · Ref_x · R(-θ) · T(0,-b)")
        print(f"  Step 1: Translate by T(0, -{b}) to move line to origin")
    T1 = translation_matrix(0, -b, show)
    if show:
        print(f"  Step 2: Rotate by -{theta:.4f}° to align with x-axis")
    R1 = rotation_matrix(-theta, show)
    if show:
        print(f"  Step 3: Reflect across x-axis")
    Ref = reflection_x_axis(show)
    if show:
        print(f"  Step 4: Rotate back by {theta:.4f}°")
    R2 = rotation_matrix(theta, show)
    if show:
        print(f"  Step 5: Translate back by T(0, {b})")
    T2 = translation_matrix(0, b, show)
    return T2 @ R2 @ Ref @ R1 @ T1

def shearing_matrix(shx, shy, show=False):
    M = np.array([[1, shx, 0], [shy, 1, 0], [0, 0, 1]], dtype=float)
    if show:
        print(f"\n  Formula: Shearing")
        print(f"  x' = x + shx·y,  y' = shy·x + y")
        print(f"  ┌              ┐")
        print(f"  │  1   shx   0 │   shx = {shx}")
        print(f"  │ shy   1   0 │   shy = {shy}")
        print(f"  │  0    0   1 │")
        print(f"  └              ┘")
    return M

# ============================================================
# Composite Transformations (with formula display)
# ============================================================

def scaling_about_point(sx, sy, cx, cy, show=False):
    if show:
        print(f"\n  Formula: Scaling S({sx},{sy}) about point ({cx},{cy})")
        print(f"  M = T(cx,cy) · S(sx,sy) · T(-cx,-cy)")
        print(f"  Step 1: Translate ({cx},{cy}) to origin")
    T1 = translation_matrix(-cx, -cy, show)
    if show:
        print(f"  Step 2: Scale by ({sx},{sy})")
    S = scaling_matrix(sx, sy, show)
    if show:
        print(f"  Step 3: Translate back to ({cx},{cy})")
    T2 = translation_matrix(cx, cy, show)
    M = T2 @ S @ T1
    if show:
        print(f"\n  Result matrix = T({cx},{cy}) × S({sx},{sy}) × T(-{cx},-{cy})")
    return M

def rotation_about_point(angle_deg, cx, cy, show=False):
    if show:
        print(f"\n  Formula: Rotation R({angle_deg}°) about point ({cx},{cy})")
        print(f"  M = T(cx,cy) · R(θ) · T(-cx,-cy)")
        print(f"  Step 1: Translate ({cx},{cy}) to origin")
    T1 = translation_matrix(-cx, -cy, show)
    if show:
        print(f"  Step 2: Rotate by {angle_deg}°")
    R = rotation_matrix(angle_deg, show)
    if show:
        print(f"  Step 3: Translate back to ({cx},{cy})")
    T2 = translation_matrix(cx, cy, show)
    M = T2 @ R @ T1
    if show:
        print(f"\n  Result matrix = T({cx},{cy}) × R({angle_deg}°) × T(-{cx},-{cy})")
    return M

# ============================================================
# Helpers
# ============================================================

def apply_matrix(M, points):
    result = []
    for x, y in points:
        v = M @ np.array([x, y, 1])
        result.append((v[0], v[1]))
    return result

def print_matrix(M, label="Matrix"):
    print(f"\n{label}:")
    headers = ["", "col1", "col2", "col3"]
    rows = []
    for i, row in enumerate(M):
        rows.append([f"row{i+1}"] + [f"{v:.4f}" for v in row])
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

def show_matrix_multiply(M, P, label_M="M", label_P="P"):
    """Show step-by-step matrix × point multiplication."""
    result = M @ P
    print(f"\n  {label_M} × {label_P} =")
    for i in range(M.shape[0]):
        terms = []
        for j in range(M.shape[1]):
            terms.append(f"({M[i,j]:.4f} × {P[j]:.4f})")
        calc = " + ".join(terms)
        val = result[i]
        print(f"    row{i+1}: {calc} = {val:.4f}")
    return result

def plot_transform(original_pts, transformed_pts, title="2D Transformation"):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ox = [p[0] for p in original_pts] + [original_pts[0][0]]
    oy = [p[1] for p in original_pts] + [original_pts[0][1]]
    ax1.fill(ox, oy, alpha=0.3, color='dodgerblue')
    ax1.plot(ox, oy, 'o-', color='dodgerblue', linewidth=2)
    for i, (x, y) in enumerate(original_pts):
        ax1.annotate(f'P{i+1}({x:.1f},{y:.1f})', (x, y), fontsize=8,
                     textcoords="offset points", xytext=(5, 5))
    ax1.set_title("Original", fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3); ax1.set_aspect('equal')
    ax1.axhline(0, color='k', lw=0.5); ax1.axvline(0, color='k', lw=0.5)

    tx = [p[0] for p in transformed_pts] + [transformed_pts[0][0]]
    ty = [p[1] for p in transformed_pts] + [transformed_pts[0][1]]
    ax2.fill(tx, ty, alpha=0.3, color='tomato')
    ax2.plot(tx, ty, 'o-', color='tomato', linewidth=2)
    for i, (x, y) in enumerate(transformed_pts):
        ax2.annotate(f"P{i+1}'({x:.1f},{y:.1f})", (x, y), fontsize=8,
                     textcoords="offset points", xytext=(5, 5))
    ax2.set_title("Transformed", fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3); ax2.set_aspect('equal')
    ax2.axhline(0, color='k', lw=0.5); ax2.axvline(0, color='k', lw=0.5)

    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout(); plt.show()
