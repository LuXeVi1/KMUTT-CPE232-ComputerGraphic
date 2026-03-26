"""
Module 1-5: Midpoint Ellipse Drawing Algorithm
Based on Lecture 5 - Ellipse Drawing Algorithm (CPE 381)

Formulas:
  h(x,y) = 4*b²*x² + 4*a²*y² - 4*a²*b² (multiplied by 4a²b² to avoid fractions)
  
  Region 1: |slope| < 1 (b²*x < a²*y), increment x
    h_init = 4*b² + a²*(1 - 4*b)
    d1_init = 12*b²
    d2_init = -8*a²*(b - 1)
    if h < 0 => U: h += d1, d1 += 8*b²
    if h >= 0 => D: h += d1+d2, d1 += 8*b², d2 += 8*a², y--
    
  Region 2: |slope| >= 1, decrement y
"""
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt

def midpoint_ellipse(a, b, show_formula=True):
    """Draw first-quadrant ellipse points. Returns rows and points."""
    rows = []
    points = []
    x, y = 0, b

    if show_formula:
        print(f"\n{'='*60}")
        print(f"  Midpoint Ellipse Algorithm")
        print(f"  a = {a} (semi-major), b = {b} (semi-minor)")
        print(f"{'='*60}")
        print(f"\n  Ellipse equation: x²/a² + y²/b² = 1")
        print(f"  Implicit form: h(x,y) = b²x² + a²y² - a²b²")
        print(f"  Scaled by 4: h(x,y) = 4·b²·x² + 4·a²·y² - 4·a²·b²")
        print(f"    a² = {a**2}, b² = {b**2}, 4·a²·b² = {4*a**2*b**2}")
        print(f"\n  Slope: dy/dx = -b²x / (a²y)")
        print(f"  Region 1: |slope| < 1  =>  b²·x < a²·y  (increment x)")
        print(f"  Region 2: |slope| >= 1  (decrement y)")

    # Region 1
    h = 4 * b * b + a * a * (1 - 4 * b)
    d1 = 12 * b * b
    d2 = -8 * a * a * (b - 1)

    if show_formula:
        print(f"\n  ── Region 1 ──")
        print(f"  Initial point: ({x}, {y})")
        print(f"  h_init = 4·b² + a²·(1 - 4b)")
        print(f"         = 4·{b**2} + {a**2}·(1 - 4·{b})")
        print(f"         = {4*b**2} + {a**2}·{1-4*b}")
        print(f"         = {4*b**2} + {a**2*(1-4*b)} = {h}")
        print(f"  d1_init = 12·b² = 12·{b**2} = {d1}")
        print(f"  d2_init = -8·a²·(b-1) = -8·{a**2}·{b-1} = {d2}")
        print(f"\n  Rules:")
        print(f"    if h < 0 (inside) => U: h += d1, d1 += 8b²={8*b**2}")
        print(f"    if h >= 0 (outside) => D: h += d1+d2, d1 += 8b²={8*b**2}, d2 += 8a²={8*a**2}, y--")
        print(f"  Continue while b²·(x+1) < a²·(y-0.5)")
        print()

    step = 1
    rows.append([step, h, d1, d2, "–", f"({x},{y})"])
    points.append((x, y))
    if show_formula:
        print(f"  Step {step}: ({x},{y})  h={h}, d1={d1}, d2={d2}  [initial]")

    while b * b * (x + 1) < a * a * (y - 0.5):
        prev_h = h
        if h < 0:
            choice = "U"
            h += d1
            if show_formula:
                print(f"  Step {step+1}: h={prev_h} < 0 => U")
                print(f"    h_new = {prev_h} + d1({d1}) = {h}")
            d1 += 8 * b * b
            if show_formula:
                print(f"    d1_new = d1 + 8b² = {d1-8*b**2} + {8*b**2} = {d1}")
        else:
            choice = "D"
            h += d1 + d2
            if show_formula:
                print(f"  Step {step+1}: h={prev_h} >= 0 => D")
                print(f"    h_new = {prev_h} + d1({d1}) + d2({d2}) = {h}")
            d1 += 8 * b * b
            d2 += 8 * a * a
            if show_formula:
                print(f"    d1_new = {d1-8*b**2} + {8*b**2} = {d1}")
                print(f"    d2_new = {d2-8*a**2} + {8*a**2} = {d2}")
            y -= 1
        x += 1
        step += 1
        rows.append([step, h, d1, d2, choice, f"({x},{y})"])
        points.append((x, y))
        if show_formula:
            check = f"b²·(x+1)={b**2*(x+1)}, a²·(y-0.5)={a**2*(y-0.5)}"
            print(f"    Plot ({x},{y})  [{check}]")

    # Region 2
    if show_formula:
        print(f"\n  ── Region 2 (b²·(x+1) >= a²·(y-0.5)) ──")
        print(f"  Switch: now decrement y, conditionally increment x")
        print(f"  h recalculated at boundary point ({x},{y})")

    h = b * b * (2 * x + 1) ** 2 + 4 * a * a * (y - 1) ** 2 - 4 * a * a * b * b

    if show_formula:
        print(f"  h = b²·(2x+1)² + 4·a²·(y-1)² - 4·a²·b²")
        print(f"    = {b**2}·{(2*x+1)**2} + 4·{a**2}·{(y-1)**2} - {4*a**2*b**2}")
        print(f"    = {b**2*(2*x+1)**2} + {4*a**2*(y-1)**2} - {4*a**2*b**2} = {h}")
        print(f"\n  Rules:")
        print(f"    if h > 0 (outside) => U: only y--, no x change")
        print(f"    if h <= 0 (inside) => D: x++, y--")
        print()

    while y > 0:
        prev_h = h
        if h > 0:
            choice = "U"
            h += -8 * a * a * (y - 1) + 4 * a * a
            if show_formula:
                print(f"  Step {step+1}: h={prev_h} > 0 => U (y only)")
                print(f"    h_new = {prev_h} + (-8a²(y-1) + 4a²) = {prev_h} + {-8*a**2*(y-1) + 4*a**2} = {h}")
        else:
            choice = "D"
            x += 1
            h += 8 * b * b * x + 4 * b * b - 8 * a * a * (y - 1) + 4 * a * a
            if show_formula:
                incr = 8*b**2*x + 4*b**2 - 8*a**2*(y-1) + 4*a**2
                print(f"  Step {step+1}: h={prev_h} <= 0 => D (x++ and y--)")
                print(f"    h_new = {prev_h} + (8b²x + 4b² - 8a²(y-1) + 4a²) = {prev_h} + {incr} = {h}")
        y -= 1
        step += 1
        rows.append([step, h, "–", "–", choice, f"({x},{y})"])
        points.append((x, y))
        if show_formula:
            print(f"    Plot ({x},{y})")

    return rows, points

def four_way_symmetry(x, y, cx=0, cy=0):
    return [(cx+x, cy+y), (cx-x, cy+y), (cx+x, cy-y), (cx-x, cy-y)]

def print_ellipse_table(rows):
    headers = ["No", "h", "d1", "d2", "U&D", "Point"]
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

def plot_ellipse(quad_points, a, b, cx=0, cy=0, title="Midpoint Ellipse"):
    fig, ax = plt.subplots(figsize=(10, 8))
    all_pts = []
    for x, y in quad_points:
        all_pts.extend(four_way_symmetry(x, y, cx, cy))
    all_pts = list(set(all_pts))
    xs = [p[0] for p in all_pts]
    ys = [p[1] for p in all_pts]
    ax.plot(xs, ys, 's', color='dodgerblue', markersize=5)
    theta = np.linspace(0, 2*np.pi, 200)
    ax.plot(cx + a*np.cos(theta), cy + b*np.sin(theta), '--', color='gray', alpha=0.5)
    qx = [p[0]+cx for p in quad_points]
    qy = [p[1]+cy for p in quad_points]
    ax.plot(qx, qy, 's', color='tomato', markersize=7, label='1st quadrant')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3); ax.set_aspect('equal'); ax.legend()
    plt.tight_layout(); plt.show()
