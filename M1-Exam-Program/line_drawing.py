"""
Module 1-3: Bresenham's Line Algorithm (Midpoint Line)
Based on Lecture 3 - Line Drawing Algorithm (CPE 381)

Formulas:
  d_init = 2*dy - dx
  if d >= 0: choose U (go diagonal), d_new = d + 2*(dy - dx)   [dU]
  if d < 0:  choose D (go horizontal), d_new = d + 2*dy        [dD]
"""
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt

def bresenham_line(x1, y1, x2, y2, show_formula=True):
    """Full Bresenham supporting all octants. Returns table rows and plotted points."""
    points = []
    rows = []

    if show_formula:
        print(f"\n{'='*60}")
        print(f"  Bresenham's Line Algorithm")
        print(f"  From ({x1},{y1}) to ({x2},{y2})")
        print(f"{'='*60}")

    dx_orig = x2 - x1
    dy_orig = y2 - y1
    steep = abs(dy_orig) > abs(dx_orig)

    if show_formula:
        print(f"\n  Original: dx = {x2}-{x1} = {dx_orig}, dy = {y2}-{y1} = {dy_orig}")
        print(f"  |dy| > |dx|? {abs(dy_orig)} > {abs(dx_orig)}? {'Yes => STEEP (swap x,y)' if steep else 'No => Normal'}")

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        if show_formula:
            print(f"  After swap: ({x1},{y1}) to ({x2},{y2})")

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        if show_formula:
            print(f"  Ensure left-to-right: ({x1},{y1}) to ({x2},{y2})")

    dx = x2 - x1
    dy = abs(y2 - y1)
    y_step = 1 if y1 < y2 else -1

    if show_formula:
        print(f"\n  Algorithm parameters:")
        print(f"  dx = {dx}, dy = {dy}")
        print(f"  y_step = {'+1' if y_step == 1 else '-1'}")
        print(f"\n  Formulas:")
        print(f"  d_init = 2*dy - dx = 2*{dy} - {dx} = {2*dy - dx}")
        print(f"  dU (when d >= 0): d_new = d + 2*(dy - dx) = d + 2*({dy} - {dx}) = d + {2*(dy-dx)}")
        print(f"  dD (when d < 0):  d_new = d + 2*dy = d + 2*{dy} = d + {2*dy}")
        print(f"\n  Rule: if d >= 0 => choose U (move x+1, y+step), apply dU")
        print(f"        if d < 0  => choose D (move x+1, y same), apply dD")
        print()

    d = 2 * dy - dx
    y = y1

    for i, x in enumerate(range(x1, x2 + 1)):
        px, py = (y, x) if steep else (x, y)
        if i == 0:
            rows.append([i + 1, "–", "–", f"({px},{py})"])
            if show_formula:
                print(f"  Step {i+1}: Plot ({px},{py})  [initial point]")
        else:
            choice = "U" if prev_d >= 0 else "D"
            d_formula = f"{prev_d} + {2*(dy-dx)} = {prev_d + 2*(dy-dx)}" if choice == "U" else f"{prev_d} + {2*dy} = {prev_d + 2*dy}"
            rows.append([i + 1, prev_d, choice, f"({px},{py})"])
            if show_formula:
                print(f"  Step {i+1}: d = {prev_d} {'≥' if prev_d >= 0 else '<'} 0 => {choice}, "
                      f"d_new = {d_formula}, Plot ({px},{py})")
        points.append((px, py))
        prev_d = d
        if d >= 0:
            y += y_step
            d += 2 * (dy - dx)
        else:
            d += 2 * dy

    return rows, points

def determine_bresenham_params(x1, y1, x2, y2, show_formula=True):
    """
    Determine which Bresenham parameter call is needed.
    Standard Bresenham works for 0 <= slope <= 1, dx > 0.
    """
    if show_formula:
        print(f"\n  Original line: ({x1},{y1}) to ({x2},{y2})")
        print(f"  dx = {x2-x1}, dy = {y2-y1}")
        if (x2-x1) != 0:
            print(f"  slope m = dy/dx = {y2-y1}/{x2-x1} = {(y2-y1)/(x2-x1):.4f}")
        else:
            print(f"  slope m = dy/dx = vertical line")
        print(f"\n  Bresenham works for: dx > 0 AND 0 ≤ m ≤ 1")
        print(f"  Options transform the line to meet this condition:")
        print(f"    (a) Bresenham(x1, y1, x2, y2)    - original")
        print(f"    (b) Bresenham(y1, x1, y2, x2)    - swap x,y")
        print(f"    (c) Bresenham(x1, -y1, x2, -y2)  - negate y")
        print(f"    (d) Bresenham(-y1, x1, -y2, x2)  - swap x,y then negate y")

    options = {
        'a': (x1, y1, x2, y2),
        'b': (y1, x1, y2, x2),
        'c': (x1, -y1, x2, -y2),
        'd': (-y1, x1, -y2, x2),
    }
    results = []
    for key, (a, b, c, d_val) in options.items():
        ddx = c - a
        ddy = d_val - b
        # Bresenham swaps endpoints if dx < 0 (ensures left-to-right)
        if ddx < 0:
            ddx = -ddx
            ddy = -ddy
        if ddx != 0:
            m = ddy / ddx
        else:
            m = float('inf')
        valid = ddx > 0 and 0 <= m <= 1
        if show_formula:
            m_str = f"{m:.4f}" if m != float('inf') else "inf"
            print(f"\n    ({key}): ({a},{b}) to ({c},{d_val})")
            if (c - a) < 0:
                print(f"         dx'={c-a} => swap endpoints => dx'={ddx}, dy'={ddy}")
            else:
                print(f"         dx'={ddx}, dy'={ddy}")
            print(f"         m'={m_str}")
            print(f"         dx'>0? {'Yes' if ddx > 0 else 'No'}, 0≤m'≤1? {'Yes' if 0 <= m <= 1 else 'No'}")
            print(f"         => {'✓ VALID' if valid else '✗ invalid'}")
        if valid:
            results.append(key)
    return results

def print_bresenham_table(rows):
    headers = ["No", "d", "U&D", "Point"]
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

def plot_bresenham_line(points, title="Bresenham's Line"):
    fig, ax = plt.subplots(figsize=(10, 8))
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, 's-', color='dodgerblue', markersize=10, markerfacecolor='tomato', linewidth=2)
    for i, (x, y) in enumerate(points):
        ax.annotate(f'({x},{y})', (x, y), fontsize=7, textcoords="offset points", xytext=(5, 5))
    ax.set_xticks(range(min(xs) - 1, max(xs) + 2))
    ax.set_yticks(range(min(ys) - 1, max(ys) + 2))
    ax.grid(True, alpha=0.3); ax.set_aspect('equal')
    ax.set_title(title, fontsize=14, fontweight='bold')
    plt.tight_layout(); plt.show()
