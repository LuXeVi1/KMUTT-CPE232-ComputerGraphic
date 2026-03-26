"""
Module 1-4: Bresenham's (Midpoint) Circle Algorithm
Based on Lecture 4 - Scan Conversion for Circle Drawing (CPE 381)

Formulas:
  h_init = 1 - r  (where h = d - 1/4, avoids fraction)
  if h < 0: choose U (stay same y), h_new = h + 2*x + 3
  if h >= 0: choose D (decrease y), h_new = h + 2*(x - y) + 5
"""
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt

def bresenham_circle(r, show_formula=True):
    """Compute first octant points. Returns table rows and octant points."""
    x, y = 0, r
    h = 1 - r
    rows = []
    octant_points = []

    if show_formula:
        print(f"\n{'='*60}")
        print(f"  Bresenham's (Midpoint) Circle Algorithm")
        print(f"  Radius r = {r}")
        print(f"{'='*60}")
        print(f"\n  Circle equation: F(x,y) = x² + y² - r²")
        print(f"  Initial point: (0, {r})")
        print(f"\n  Formulas:")
        print(f"  h_init = 1 - r = 1 - {r} = {1 - r}")
        print(f"  (h replaces d to avoid fractions: h = d - 1/4)")
        print(f"\n  At each step (starting from x_i, y_i):")
        print(f"    if h < 0 => choose U (inside circle, keep y)")
        print(f"      h_U = h + 2*x_i + 3")
        print(f"      next: (x_i+1, y_i)")
        print(f"    if h >= 0 => choose D (outside circle, decrease y)")
        print(f"      h_D = h + 2*(x_i - y_i) + 5")
        print(f"      next: (x_i+1, y_i-1)")
        print(f"\n  Stop when x > y (end of first octant)")
        print()

    step = 1
    while x <= y:
        if step == 1:
            rows.append([step, "–", "–", f"({x},{y})"])
            if show_formula:
                print(f"  Step {step}: Plot ({x},{y})  [initial point, h = {h}]")
        else:
            choice = prev_choice
            rows.append([step, prev_h, choice, f"({x},{y})"])
            if show_formula:
                if choice == "U":
                    print(f"  Step {step}: h = {prev_h} < 0 => U, "
                          f"h_new = {prev_h} + 2*{prev_x} + 3 = {prev_h} + {2*prev_x+3} = {h_before_update}, "
                          f"Plot ({x},{y})")
                else:
                    print(f"  Step {step}: h = {prev_h} >= 0 => D, "
                          f"h_new = {prev_h} + 2*({prev_x} - {prev_y}) + 5 = {prev_h} + {2*(prev_x-prev_y)+5} = {h_before_update}, "
                          f"Plot ({x},{y})")
        octant_points.append((x, y))

        prev_h = h
        prev_x = x
        prev_y = y
        if h < 0:
            prev_choice = "U"
            h = h + 2 * x + 3
            h_before_update = h
        else:
            prev_choice = "D"
            h = h + 2 * (x - y) + 5
            h_before_update = h
            y -= 1
        x += 1
        step += 1

    return rows, octant_points

def eight_way_symmetry(x, y, cx=0, cy=0):
    """Generate all 8 symmetric points around center (cx, cy)."""
    return [
        (cx + x, cy + y), (cx + y, cy + x),
        (cx - y, cy + x), (cx - x, cy + y),
        (cx - x, cy - y), (cx - y, cy - x),
        (cx + y, cy - x), (cx + x, cy - y),
    ]

def show_eight_way(octant_points, cx=0, cy=0):
    """Show 8-way symmetry mapping."""
    print(f"\n  Eight-Way Symmetry: (x,y) => 8 points")
    print(f"    P1=(cx+x, cy+y)   P5=(cx-x, cy-y)")
    print(f"    P2=(cx+y, cy+x)   P6=(cx-y, cy-x)")
    print(f"    P3=(cx-y, cy+x)   P7=(cx+y, cy-x)")
    print(f"    P4=(cx-x, cy+y)   P8=(cx+x, cy-y)")
    if cx != 0 or cy != 0:
        print(f"    Center offset: ({cx}, {cy})")
    print()
    for ox, oy in octant_points:
        pts = eight_way_symmetry(ox, oy, cx, cy)
        labels = [f"({p[0]},{p[1]})" for p in pts]
        print(f"    ({ox},{oy}) => {', '.join(labels)}")

def circle_points_in_range(r, cx, cy, start_deg, end_deg):
    """Get circle points within angle range using Bresenham."""
    _, octant = bresenham_circle(r, show_formula=False)
    all_pts = set()
    for ox, oy in octant:
        for px, py in eight_way_symmetry(ox, oy, cx, cy):
            angle = np.degrees(np.arctan2(py - cy, px - cx)) % 360
            if start_deg <= end_deg:
                if start_deg <= angle <= end_deg:
                    all_pts.add((px, py))
            else:
                if angle >= start_deg or angle <= end_deg:
                    all_pts.add((px, py))
    return sorted(all_pts, key=lambda p: np.arctan2(p[1] - cy, p[0] - cx))

def print_circle_table(rows):
    headers = ["No", "h", "U&D", "Point"]
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

def plot_circle(octant_points, r, cx=0, cy=0, title="Bresenham's Circle"):
    fig, ax = plt.subplots(figsize=(8, 8))
    all_pts = []
    for x, y in octant_points:
        all_pts.extend(eight_way_symmetry(x, y, cx, cy))
    all_pts = list(set(all_pts))
    xs = [p[0] for p in all_pts]
    ys = [p[1] for p in all_pts]
    ax.plot(xs, ys, 's', color='dodgerblue', markersize=6)
    ox = [p[0] + cx for p in octant_points]
    oy = [p[1] + cy for p in octant_points]
    ax.plot(ox, oy, 's', color='tomato', markersize=8, label='1st octant')
    theta = np.linspace(0, 2 * np.pi, 200)
    ax.plot(cx + r * np.cos(theta), cy + r * np.sin(theta), '--', color='gray', alpha=0.5)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3); ax.set_aspect('equal'); ax.legend()
    plt.tight_layout(); plt.show()
