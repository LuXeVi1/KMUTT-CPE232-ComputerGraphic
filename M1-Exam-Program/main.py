"""
CPE 381 Computer Graphics - Exam Calculator
============================================
Interactive tool covering all Past Exam topics:
  1. 2D Geometric Transformation (Basic)
  2. 2D Composite Geometric Transformation
  3. Cohen-Sutherland Line Clipping
  4. Polygon Clipping (Sutherland-Hodgman)
  5. Inverse Geometric Transformation
  6. Application - Transform Points with Matrix
  7. Bresenham's Line Algorithm (Parameter Selection)
  8. Bresenham's Line Algorithm (Full Table)
  9. Bresenham's Circle Algorithm
  10. Bresenham's Circle with Center & Angle Range
  11. Midpoint Ellipse Algorithm
  12. 3D Geometric Transformation (Basic)
  13. 3D Composite Transformation (Arbitrary Axis)
  14. 3D Perspective Projection
"""
import numpy as np
from tabulate import tabulate
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from transformations import *
from clipping import *
from line_drawing import *
from circle_drawing import *
from ellipse_drawing import *
from transformations_3d import *
from matrix_calc import *

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║      CPE 381 - Computer Graphics Exam Calculator             ║
║      Based on Lecture Modules 1-1 to 1-5                     ║
╚══════════════════════════════════════════════════════════════╝
"""

MENU = """
┌──────────────────────────────────────────────────────────────┐
│  Module 1-1: 2D Transformations                              │
│    [1]  Basic Transformation Matrix                          │
│    [2]  Composite Transformation Matrix                      │
│    [5]  Inverse Geometric Transformation                     │
│    [6]  Apply Transformation to Points                       │
│                                                              │
│  Module 1-2: 2D Viewing & Clipping                           │
│    [3]  Cohen-Sutherland Line Clipping                       │
│    [4]  Sutherland-Hodgman Polygon Clipping                  │
│                                                              │
│  Module 1-3: Line Drawing                                    │
│    [7]  Bresenham Parameter Selection                        │
│    [8]  Bresenham Line Algorithm (Full Table)                │
│                                                              │
│  Module 1-4: Circle Drawing                                  │
│    [9]  Bresenham Circle Algorithm (Full Table)              │
│    [10] Circle with Center & Angle Range                     │
│                                                              │
│  Module 1-5: Ellipse Drawing                                 │
│    [11] Midpoint Ellipse Algorithm (Full Table)              │
│                                                              │
│  Module 2: 3D Transformations & Projection                   │
│    [12] 3D Basic Transformation (Rx, Ry, Rz)                 │
│    [13] 3D Rotation about Arbitrary Line                     │
│    [14] 3D Perspective Projection                            │
│                                                              │
│  Tools                                                       │
│    [15] Matrix Calculator (enter & compute raw matrices)     │
│                                                              │
│    [0]  Exit                                                 │
└──────────────────────────────────────────────────────────────┘
"""

def input_int(prompt, default=None):
    s = input(prompt).strip()
    if s == "" and default is not None: return default
    return int(s)

def input_float(prompt, default=None):
    s = input(prompt).strip()
    if s == "" and default is not None: return default
    return float(s)

def input_points(prompt="Enter points as x1,y1 x2,y2 ... : "):
    s = input(prompt).strip()
    pts = []
    for p in s.split():
        x, y = p.split(',')
        pts.append((float(x), float(y)))
    return pts

# ============================================================
# Option 1: Basic Transformation Matrix (Exam Q1 Solver)
# ============================================================
def _pick_transform():
    """Let user pick a transform and return (M, description)."""
    print("\n  Transform types:")
    print("    (a) Translation        (b) Scaling (origin)")
    print("    (c) Rotation (origin)  (d) Reflection x-axis")
    print("    (e) Reflection y-axis  (f) Reflection origin")
    print("    (g) Reflection y=x     (h) Reflection y=-x")
    print("    (i) Reflection x=val   (j) Reflection y=val")
    print("    (k) Reflection y=mx    (l) Shearing")
    ch = input("  Choose (a-l): ").strip().lower()

    if ch == 'a':
        tx = input_float("  tx = ")
        ty = input_float("  ty = ")
        M = translation_matrix(tx, ty, show=True)
        return M, f"Translation T({tx},{ty})"
    elif ch == 'b':
        sx = input_float("  sx = ")
        sy = input_float("  sy = ")
        M = scaling_matrix(sx, sy, show=True)
        return M, f"Scaling S({sx},{sy})"
    elif ch == 'c':
        angle = input_float("  Angle (degrees) = ")
        M = rotation_matrix(angle, show=True)
        return M, f"Rotation R({angle}°)"
    elif ch == 'd':
        M = reflection_x_axis(show=True)
        return M, "Reflection across x-axis"
    elif ch == 'e':
        M = reflection_y_axis(show=True)
        return M, "Reflection across y-axis"
    elif ch == 'f':
        M = reflection_origin(show=True)
        return M, "Reflection across origin"
    elif ch == 'g':
        M = reflection_y_eq_x(show=True)
        return M, "Reflection across y=x"
    elif ch == 'h':
        M = reflection_y_eq_neg_x(show=True)
        return M, "Reflection across y=-x"
    elif ch == 'i':
        val = input_float("  x = ")
        M = reflection_line_x_eq(val, show=True)
        return M, f"Reflection across x={val}"
    elif ch == 'j':
        val = input_float("  y = ")
        M = reflection_line_y_eq(val, show=True)
        return M, f"Reflection across y={val}"
    elif ch == 'k':
        m = input_float("  slope m (y=mx): ")
        M = reflection_y_eq_mx(m, show=True)
        return M, f"Reflection across y={m}x"
    elif ch == 'l':
        shx = input_float("  shx = ")
        shy = input_float("  shy = ")
        M = shearing_matrix(shx, shy, show=True)
        return M, f"Shearing shx={shx}, shy={shy}"
    else:
        return None, None

def option_basic_transform():
    print("\n" + "="*60)
    print("  Q1: Basic 2D Transformation (Exam Solver)")
    print("="*60)

    # --- Step 1: Input points ---
    n = input_int("  Number of points: ")
    names = []
    points = []
    for i in range(n):
        name = input(f"  Point {i+1} name (e.g. A): ").strip()
        x = input_float(f"  {name} x = ")
        y = input_float(f"  {name} y = ")
        names.append(name)
        points.append((x, y))

    print(f"\n  Points entered:")
    for name, (x, y) in zip(names, points):
        print(f"    {name}({x}, {y})")

    # --- Step 2: Loop through sub-questions ---
    sub_q = 1
    while True:
        print(f"\n{'─'*60}")
        print(f"  Sub-question {sub_q}:  (type 'done' to finish)")
        ch = input(f"  Press Enter to continue or 'done': ").strip().lower()
        if ch == 'done':
            break

        result = _pick_transform()
        if result[0] is None:
            print("  Invalid choice, try again.")
            continue
        M, desc = result

        # Show the matrix
        print_matrix(M, f"Q1.{sub_q}: {desc}")

        # Apply to each point with step-by-step
        print(f"\n  Applying {desc} to each point:")
        transformed = []
        for name, (x, y) in zip(names, points):
            P = np.array([x, y, 1.0])
            print(f"\n    {name}({x}, {y}):")
            r = show_matrix_multiply(M, P, "M", f"[{x},{y},1]")
            transformed.append((r[0], r[1]))
            print(f"    => {name}'({r[0]:.4f}, {r[1]:.4f})")

        # Results table
        table = []
        for name, (ox, oy), (tx, ty) in zip(names, points, transformed):
            table.append([name, f"({ox},{oy})", f"({tx:.3f},{ty:.3f})"])
        print(f"\n  Results for Q1.{sub_q}: {desc}")
        print(tabulate(table, headers=["Point", "Original", "Transformed"],
                       tablefmt="fancy_grid"))

        show_plot = input("\n  Show plot? (y/n): ").strip().lower()
        if show_plot == 'y':
            plot_transform(points, transformed, title=f"Q1.{sub_q}: {desc}")

        sub_q += 1

# ============================================================
# Option 2: Composite Transformation Matrix
# ============================================================
def _pick_composite_transform():
    """Let user pick a composite transform and return (M, description)."""
    print("\n  Composite transform types:")
    print("    (a) Reflection across y = mx + b")
    print("    (b) Rotation about point (cx, cy)")
    print("    (c) Scaling about point (cx, cy)")
    print("    (d) Custom sequence of transforms")
    ch = input("  Choose (a-d): ").strip().lower()

    if ch == 'a':
        m = input_float("  slope m = ")
        b = input_float("  intercept b = ")
        M = reflection_y_eq_mx_plus_b(m, b, show=True)
        return M, f"Reflection across y = {m}x + {b}"
    elif ch == 'b':
        angle = input_float("  Angle (degrees) = ")
        cx = input_float("  cx = ")
        cy = input_float("  cy = ")
        M = rotation_about_point(angle, cx, cy, show=True)
        return M, f"Rotation {angle}° about ({cx},{cy})"
    elif ch == 'c':
        sx = input_float("  sx = ")
        sy = input_float("  sy = ")
        cx = input_float("  cx = ")
        cy = input_float("  cy = ")
        M = scaling_about_point(sx, sy, cx, cy, show=True)
        return M, f"Scaling ({sx},{sy}) about ({cx},{cy})"
    elif ch == 'd':
        n_t = input_int("  How many transforms? ")
        M = np.eye(3)
        desc_parts = []
        for i in range(n_t):
            print(f"\n  Transform {i+1}:")
            print("    (t)ranslation (s)caling (r)otation (ref)lection")
            t = input("    Type: ").strip().lower()
            if t == 't':
                tx = input_float("    tx = ")
                ty = input_float("    ty = ")
                T = translation_matrix(tx, ty, show=True)
                print_matrix(T, f"T({tx},{ty})")
                M = T @ M
                desc_parts.append(f"T({tx},{ty})")
            elif t == 's':
                sx = input_float("    sx = ")
                sy = input_float("    sy = ")
                S = scaling_matrix(sx, sy, show=True)
                print_matrix(S, f"S({sx},{sy})")
                M = S @ M
                desc_parts.append(f"S({sx},{sy})")
            elif t == 'r':
                angle = input_float("    Angle = ")
                R = rotation_matrix(angle, show=True)
                print_matrix(R, f"R({angle}°)")
                M = R @ M
                desc_parts.append(f"R({angle}°)")
            elif t == 'ref':
                print("    (x) x-axis (y) y-axis (o) origin (yx) y=x (ynx) y=-x")
                rc = input("    Axis: ").strip().lower()
                if rc == 'x': Ref = reflection_x_axis(show=True)
                elif rc == 'y': Ref = reflection_y_axis(show=True)
                elif rc == 'o': Ref = reflection_origin(show=True)
                elif rc == 'yx': Ref = reflection_y_eq_x(show=True)
                elif rc == 'ynx': Ref = reflection_y_eq_neg_x(show=True)
                else: Ref = np.eye(3)
                print_matrix(Ref, "Reflection")
                M = Ref @ M
                desc_parts.append(f"Ref({rc})")
        return M, " · ".join(desc_parts)
    else:
        return None, None

def option_composite_transform():
    print("\n" + "="*60)
    print("  Q2: Composite 2D Transformation (Exam Solver)")
    print("="*60)

    # --- Step 1: Input points ---
    n = input_int("  Number of points: ")
    names = []
    points = []
    for i in range(n):
        name = input(f"  Point {i+1} name (e.g. A): ").strip()
        x = input_float(f"  {name} x = ")
        y = input_float(f"  {name} y = ")
        names.append(name)
        points.append((x, y))

    print(f"\n  Points entered:")
    for name, (x, y) in zip(names, points):
        print(f"    {name}({x}, {y})")

    # --- Step 2: Loop through sub-questions ---
    sub_q = 1
    while True:
        print(f"\n{'─'*60}")
        print(f"  Sub-question {sub_q}:  (type 'done' to finish)")
        ch = input(f"  Press Enter to continue or 'done': ").strip().lower()
        if ch == 'done':
            break

        result = _pick_composite_transform()
        if result[0] is None:
            print("  Invalid choice, try again.")
            continue
        M, desc = result

        # Show the composite matrix
        print_matrix(M, f"Q2.{sub_q}: {desc}")

        # Apply to each point with step-by-step
        print(f"\n  Applying {desc} to each point:")
        transformed = []
        for name, (x, y) in zip(names, points):
            P = np.array([x, y, 1.0])
            print(f"\n    {name}({x}, {y}):")
            r = show_matrix_multiply(M, P, "M", f"[{x},{y},1]")
            transformed.append((r[0], r[1]))
            print(f"    => {name}'({r[0]:.4f}, {r[1]:.4f})")

        # Results table
        table = []
        for name, (ox, oy), (tx, ty) in zip(names, points, transformed):
            table.append([name, f"({ox},{oy})", f"({tx:.3f},{ty:.3f})"])
        print(f"\n  Results for Q2.{sub_q}: {desc}")
        print(tabulate(table, headers=["Point", "Original", "Transformed"],
                       tablefmt="fancy_grid"))

        show_plot = input("\n  Show plot? (y/n): ").strip().lower()
        if show_plot == 'y':
            plot_transform(points, transformed, title=f"Q2.{sub_q}: {desc}")

        sub_q += 1

# ============================================================
# Option 3: Line Clipping
# ============================================================
def option_line_clipping():
    print("\n--- Cohen-Sutherland Line Clipping ---")
    print("  (a) Clip individual lines")
    print("  (b) Clip polygon edges (exam Q3 mode)")
    mode = input("Choose (a/b): ").strip().lower()

    print("\nEnter window coordinates:")
    xmin = input_float("  Lower-left  x (xmin) = ")
    ymin = input_float("  Lower-left  y (ymin) = ")
    xmax = input_float("  Upper-right x (xmax) = ")
    ymax = input_float("  Upper-right y (ymax) = ")
    print(f"\n  Window: ({xmin},{ymin}) to ({xmax},{ymax})")

    if mode == 'b':
        # --- Polygon edge mode ---
        n = input_int("\nNumber of polygon vertices: ")
        vert_names = []
        vertices = []
        for i in range(n):
            name = input(f"  Vertex {i+1} name (e.g. A): ").strip()
            x = input_float(f"  {name} x = ")
            y = input_float(f"  {name} y = ")
            vert_names.append(name)
            vertices.append((x, y))

        # Step 1: Region codes for ALL vertices
        print(f"\n{'='*60}")
        print(f"  Step 1: Region codes for all vertices")
        print(f"{'='*60}")
        codes = []
        code_table = []
        for name, (x, y) in zip(vert_names, vertices):
            code = compute_code(x, y, xmin, ymin, xmax, ymax)
            codes.append(code)
            code_str = code_to_str(code)
            above = 1 if y > ymax else 0
            below = 1 if y < ymin else 0
            right = 1 if x > xmax else 0
            left  = 1 if x < xmin else 0
            print(f"\n  {name}({x},{y}):")
            print(f"    Bit1(above): y={y} > ymax={ymax}? {'Yes' if above else 'No'} => {above}")
            print(f"    Bit2(below): y={y} < ymin={ymin}? {'Yes' if below else 'No'} => {below}")
            print(f"    Bit3(right): x={x} > xmax={xmax}? {'Yes' if right else 'No'} => {right}")
            print(f"    Bit4(left):  x={x} < xmin={xmin}? {'Yes' if left else 'No'} => {left}")
            print(f"    => Code = {code_str}")
            code_table.append([name, f"({x},{y})", code_str])

        print(f"\n  Region Code Summary:")
        print(tabulate(code_table, headers=["Vertex", "Coords", "Code"], tablefmt="fancy_grid"))

        # Step 2: Edge categories
        edges = []
        for i in range(n):
            j = (i + 1) % n
            edges.append((vert_names[i], vert_names[j], vertices[i], vertices[j], codes[i], codes[j]))

        print(f"\n{'='*60}")
        print(f"  Step 2: Edge categories")
        print(f"{'='*60}")
        edge_cat_table = []
        for v1n, v2n, (x1,y1), (x2,y2), c1, c2 in edges:
            c1s = code_to_str(c1)
            c2s = code_to_str(c2)
            if c1 == 0 and c2 == 0:
                cat = "Visible (both 0000)"
            elif c1 & c2 != 0:
                cat = "Invisible (AND != 0)"
            else:
                cat = "Clipping Candidate"
            edge_cat_table.append([f"{v1n}{v2n}", f"({x1},{y1})", f"({x2},{y2})", c1s, c2s, cat])
        print(tabulate(edge_cat_table,
                       headers=["Edge", "P1", "P2", "Code1", "Code2", "Category"],
                       tablefmt="fancy_grid"))

        # Step 3: Clip each edge
        print(f"\n{'='*60}")
        print(f"  Step 3: Clipping (order: Below, Right, Above, Left)")
        print(f"{'='*60}")
        int_label = ord('P')
        all_intersections = []
        visible_segments = []
        results_table = []
        plot_data = []

        for v1n, v2n, (x1,y1), (x2,y2), c1, c2 in edges:
            ename = f"{v1n}{v2n}"
            print(f"\n  --- Edge {ename}: ({x1},{y1}) to ({x2},{y2}) ---")

            init_cat, final_cat, vp1, vp2, steps = cohen_sutherland_clip(
                x1, y1, x2, y2, xmin, ymin, xmax, ymax)
            for s in steps:
                print(f"    {s}")

            if vp1 and vp2:
                if abs(vp1[0]-x1) > 0.001 or abs(vp1[1]-y1) > 0.001:
                    iname = chr(int_label)
                    int_label += 1
                    all_intersections.append((iname, vp1[0], vp1[1], ename))
                    print(f"    => Intersection {iname} = ({vp1[0]:.4f}, {vp1[1]:.4f})")
                if abs(vp2[0]-x2) > 0.001 or abs(vp2[1]-y2) > 0.001:
                    iname = chr(int_label)
                    int_label += 1
                    all_intersections.append((iname, vp2[0], vp2[1], ename))
                    print(f"    => Intersection {iname} = ({vp2[0]:.4f}, {vp2[1]:.4f})")
                visible_segments.append((ename, vp1, vp2))

            vp1_str = f"({vp1[0]:.4f},{vp1[1]:.4f})" if vp1 else "-"
            vp2_str = f"({vp2[0]:.4f},{vp2[1]:.4f})" if vp2 else "-"
            results_table.append([ename, f"({x1},{y1})", f"({x2},{y2})",
                                  code_to_str(c1), code_to_str(c2), final_cat, vp1_str, vp2_str])
            plot_data.append((init_cat, final_cat, vp1, vp2, (x1,y1), (x2,y2)))

        # Summary
        print(f"\n{'='*60}")
        print(f"  Results Summary")
        print(f"{'='*60}")
        headers = ["Edge", "P1", "P2", "Code1", "Code2", "Category", "Vis P1", "Vis P2"]
        print(tabulate(results_table, headers=headers, tablefmt="fancy_grid"))

        if all_intersections:
            print(f"\n  Intersection Points:")
            int_table = [[nm, f"({x:.4f}, {y:.4f})", e] for nm, x, y, e in all_intersections]
            print(tabulate(int_table, headers=["Label", "Coords", "Edge"], tablefmt="fancy_grid"))

        print(f"\n  Visible Segments after clipping:")
        if visible_segments:
            for ename, p1, p2 in visible_segments:
                print(f"    {ename}: ({p1[0]:.4f},{p1[1]:.4f}) to ({p2[0]:.4f},{p2[1]:.4f})")
        else:
            print(f"    None")

        # Clipped polygon vertices
        print(f"\n  Clipped Polygon Vertices (in order):")
        clipped_verts = []
        for ename, p1, p2 in visible_segments:
            if not clipped_verts or (abs(clipped_verts[-1][0]-p1[0]) > 0.001 or abs(clipped_verts[-1][1]-p1[1]) > 0.001):
                clipped_verts.append(p1)
            clipped_verts.append(p2)
        for i, (x, y) in enumerate(clipped_verts):
            label = f"V{i+1}"
            for iname, ix, iy, _ in all_intersections:
                if abs(ix-x) < 0.001 and abs(iy-y) < 0.001:
                    label = iname; break
            for vn, (vx, vy) in zip(vert_names, vertices):
                if abs(vx-x) < 0.001 and abs(vy-y) < 0.001:
                    label = vn; break
            print(f"    {label}({x:.4f}, {y:.4f})")

        show = input("\nShow plot? (y/n): ").strip().lower()
        if show == 'y':
            plot_clipping(plot_data, xmin, ymin, xmax, ymax)

    else:
        # --- Individual lines mode (original) ---
        n = input_int("Number of lines = ")
        results_table = []
        plot_data = []
        for i in range(n):
            print(f"\n  Line {i+1}:")
            x1 = input_float("    P1 x = ")
            y1 = input_float("    P1 y = ")
            x2 = input_float("    P2 x = ")
            y2 = input_float("    P2 y = ")
            c1 = compute_code(x1, y1, xmin, ymin, xmax, ymax)
            c2 = compute_code(x2, y2, xmin, ymin, xmax, ymax)
            init_cat, final_cat, vp1, vp2, steps = cohen_sutherland_clip(
                x1, y1, x2, y2, xmin, ymin, xmax, ymax)
            vp1_str = f"({vp1[0]},{vp1[1]})" if vp1 else "-"
            vp2_str = f"({vp2[0]},{vp2[1]})" if vp2 else "-"
            results_table.append([
                f"{i+1}", f"({x1},{y1})", f"({x2},{y2})",
                code_to_str(c1), code_to_str(c2),
                final_cat, vp1_str, vp2_str
            ])
            plot_data.append((init_cat, final_cat, vp1, vp2, (x1, y1), (x2, y2)))
            for s in steps:
                print(f"    {s}")

        headers = ["Line", "Point 1", "Point 2", "Code P1", "Code P2", "Category", "Vis P1", "Vis P2"]
        print("\n" + tabulate(results_table, headers=headers, tablefmt="fancy_grid"))
        show = input("\nShow plot? (y/n): ").strip().lower()
        if show == 'y':
            plot_clipping(plot_data, xmin, ymin, xmax, ymax)

# ============================================================
# Option 4: Polygon Clipping (Sutherland-Hodgman)
# ============================================================
def line_intersect(p1, p2, edge_start, edge_end):
    x1, y1 = p1; x2, y2 = p2
    x3, y3 = edge_start; x4, y4 = edge_end
    denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if abs(denom) < 1e-10: return p1
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / denom
    return (x1 + t*(x2-x1), y1 + t*(y2-y1))

def is_inside(p, edge_start, edge_end):
    return (edge_end[0]-edge_start[0])*(p[1]-edge_start[1]) - \
           (edge_end[1]-edge_start[1])*(p[0]-edge_start[0]) >= 0

def sutherland_hodgman(polygon, clip_rect):
    xmin, ymin, xmax, ymax = clip_rect
    clip_edges = [
        ((xmin, ymin), (xmax, ymin)),  # bottom
        ((xmax, ymin), (xmax, ymax)),  # right
        ((xmax, ymax), (xmin, ymax)),  # top
        ((xmin, ymax), (xmin, ymin)),  # left
    ]
    output = list(polygon)
    all_steps = []
    edge_names = ["Bottom (y=ymin)", "Right (x=xmax)", "Top (y=ymax)", "Left (x=xmin)"]
    for idx, (es, ee) in enumerate(clip_edges):
        if not output: break
        inp = output
        output = []
        step_info = {"edge": edge_names[idx], "input": list(inp), "output": []}
        for i in range(len(inp)):
            curr = inp[i]
            prev = inp[i - 1]
            curr_inside = is_inside(curr, es, ee)
            prev_inside = is_inside(prev, es, ee)
            if curr_inside:
                if not prev_inside:
                    inter = line_intersect(prev, curr, es, ee)
                    output.append(inter)
                output.append(curr)
            elif prev_inside:
                inter = line_intersect(prev, curr, es, ee)
                output.append(inter)
        step_info["output"] = list(output)
        all_steps.append(step_info)

    return output, all_steps

def option_polygon_clipping():
    print("\n--- Sutherland-Hodgman Polygon Clipping ---")
    xmin = input_float("Window xmin = ")
    ymin = input_float("Window ymin = ")
    xmax = input_float("Window xmax = ")
    ymax = input_float("Window ymax = ")
    pts = input_points("Enter polygon vertices (x1,y1 x2,y2 ...): ")
    clipped, steps = sutherland_hodgman(pts, (xmin, ymin, xmax, ymax))

    for s in steps:
        print(f"\n  Clip against {s['edge']}:")
        print(f"    Input:  {[f'({p[0]:.1f},{p[1]:.1f})' for p in s['input']]}")
        print(f"    Output: {[f'({p[0]:.1f},{p[1]:.1f})' for p in s['output']]}")

    print(f"\nFinal clipped polygon ({len(clipped)} vertices):")
    for i, p in enumerate(clipped):
        print(f"  V{i+1}: ({p[0]:.4f}, {p[1]:.4f})")

    show = input("\nShow plot? (y/n): ").strip().lower()
    if show == 'y':
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        # Original
        ox = [p[0] for p in pts] + [pts[0][0]]
        oy = [p[1] for p in pts] + [pts[0][1]]
        ax1.fill(ox, oy, alpha=0.3, color='dodgerblue')
        ax1.plot(ox, oy, 'o-', color='dodgerblue')
        rect = mpatches.Rectangle((xmin, ymin), xmax-xmin, ymax-ymin,
                                   linewidth=2, edgecolor='green', facecolor='lightgreen', alpha=0.2)
        ax1.add_patch(rect)
        ax1.set_title("Original"); ax1.grid(True, alpha=0.3); ax1.set_aspect('equal')
        # Clipped
        if clipped:
            cx = [p[0] for p in clipped] + [clipped[0][0]]
            cy = [p[1] for p in clipped] + [clipped[0][1]]
            ax2.fill(cx, cy, alpha=0.3, color='tomato')
            ax2.plot(cx, cy, 'o-', color='tomato')
        rect2 = mpatches.Rectangle((xmin, ymin), xmax-xmin, ymax-ymin,
                                    linewidth=2, edgecolor='green', facecolor='lightgreen', alpha=0.2)
        ax2.add_patch(rect2)
        ax2.set_title("Clipped"); ax2.grid(True, alpha=0.3); ax2.set_aspect('equal')
        fig.suptitle("Sutherland-Hodgman Polygon Clipping", fontweight='bold')
        plt.tight_layout(); plt.show()

# ============================================================
# Option 5: Inverse Transformation
# ============================================================
def option_inverse():
    print("\n--- Inverse Geometric Transformation ---")
    print("  (a) General: Result = M × Original => M = Result × inv(Original)")
    print("  (b) Unit square exam: given result 2×4, find [[A,C],[B,D]] and (x,y)")
    mode = input("Choose (a/b): ").strip().lower()

    if mode == 'b':
        # User-defined vertex pattern
        print("\n  The original shape has vertices defined in terms of (x,y).")
        print("  Enter the offsets (dx,dy) for each point relative to (x,y).")
        print("  Common: Unit square => (0,0) (1,0) (1,1) (0,1)")
        print("  Example: P1=(x,y) => offsets: 0 0")
        print("           P2=(x+1,y) => offsets: 1 0")
        print("           P3=(x+1,y+1) => offsets: 1 1")
        print("           P4=(x,y+1) => offsets: 0 1")
        print("  Transformed by M = [[A,C],[B,D]]")

        n_pts = input_int("\n  Number of points: ")
        offsets = []
        pnames = []
        for i in range(n_pts):
            nm = input(f"  Point {i+1} name (e.g. P{i+1}): ").strip()
            off_str = input(f"  {nm} offsets (dx dy): ").strip().split()
            dx, dy = float(off_str[0]), float(off_str[1])
            offsets.append((dx, dy))
            pnames.append(nm)

        print(f"\n  Vertex pattern:")
        for nm, (dx, dy) in zip(pnames, offsets):
            xs = f"x+{dx:g}" if dx != 0 else "x"
            ys = f"y+{dy:g}" if dy != 0 else "y"
            print(f"    {nm} = ({xs}, {ys})")

        print(f"\n  Enter result matrix (2 rows × {n_pts} columns):")
        r1 = input("  Row 1 (x' values, space-separated): ").strip().split()
        r2 = input("  Row 2 (y' values, space-separated): ").strip().split()
        rx = [float(v) for v in r1]
        ry = [float(v) for v in r2]

        print(f"\n  Result points:")
        for i in range(n_pts):
            print(f"    {pnames[i]}' = ({rx[i]}, {ry[i]})")

        # Set up equations
        print(f"\n{'='*60}")
        print(f"  Setting up equations:  M × [x+dx, y+dy]^T = [x', y']^T")
        print(f"{'='*60}")
        eq_num = 1
        for i in range(n_pts):
            dx, dy = offsets[i]
            xs = f"x+{dx:g}" if dx != 0 else "x"
            ys = f"y+{dy:g}" if dy != 0 else "y"
            print(f"  {pnames[i]}: A·({xs}) + C·({ys}) = {rx[i]}   ... ({eq_num})")
            eq_num += 1
            print(f"      B·({xs}) + D·({ys}) = {ry[i]}   ... ({eq_num})")
            eq_num += 1

        # Solve for A,B,C,D
        print(f"\n{'='*60}")
        print(f"  Solving for A, B, C, D:")
        print(f"{'='*60}")
        A = B = C = D = None
        # Find A,B: two points with same dy offset but different dx
        for i in range(n_pts):
            for j in range(i+1, n_pts):
                dxi, dyi = offsets[i]; dxj, dyj = offsets[j]
                if abs(dyi - dyj) < 1e-10 and abs(dxi - dxj) > 1e-10:
                    ddx = dxj - dxi
                    A = (rx[j] - rx[i]) / ddx
                    B = (ry[j] - ry[i]) / ddx
                    print(f"  {pnames[j]}-{pnames[i]}: dy same, dx diff={ddx:g}")
                    print(f"    A·{ddx:g} = {rx[j]}-{rx[i]} = {rx[j]-rx[i]}  =>  A = {A}")
                    print(f"    B·{ddx:g} = {ry[j]}-{ry[i]} = {ry[j]-ry[i]}  =>  B = {B}")
                    break
            if A is not None: break
        # Find C,D: two points with same dx offset but different dy
        for i in range(n_pts):
            for j in range(i+1, n_pts):
                dxi, dyi = offsets[i]; dxj, dyj = offsets[j]
                if abs(dxi - dxj) < 1e-10 and abs(dyi - dyj) > 1e-10:
                    ddy = dyj - dyi
                    C = (rx[j] - rx[i]) / ddy
                    D = (ry[j] - ry[i]) / ddy
                    print(f"  {pnames[j]}-{pnames[i]}: dx same, dy diff={ddy:g}")
                    print(f"    C·{ddy:g} = {rx[j]}-{rx[i]} = {rx[j]-rx[i]}  =>  C = {C}")
                    print(f"    D·{ddy:g} = {ry[j]}-{ry[i]} = {ry[j]-ry[i]}  =>  D = {D}")
                    break
            if C is not None: break

        if A is None or C is None:
            # Fallback: general solve using first 3 points
            print("  Using general solve (3 points)...")
            d0 = offsets[0]; d1 = offsets[1]; d2 = offsets[2]
            ddx1 = d1[0]-d0[0]; ddy1 = d1[1]-d0[1]
            ddx2 = d2[0]-d0[0]; ddy2 = d2[1]-d0[1]
            det_s = ddx1*ddy2 - ddy1*ddx2
            if abs(det_s) > 1e-10:
                A = ((rx[1]-rx[0])*ddy2 - ddy1*(rx[2]-rx[0])) / det_s
                C = (ddx1*(rx[2]-rx[0]) - (rx[1]-rx[0])*ddx2) / det_s
                B = ((ry[1]-ry[0])*ddy2 - ddy1*(ry[2]-ry[0])) / det_s
                D = (ddx1*(ry[2]-ry[0]) - (ry[1]-ry[0])*ddx2) / det_s
                print(f"    A = {A}, B = {B}, C = {C}, D = {D}")

        if A is not None and C is not None:
            # Solve for x, y from first point: A(x+dx0) + C(y+dy0) = rx[0]
            dx0, dy0 = offsets[0]
            rhs1 = rx[0] - A*dx0 - C*dy0
            rhs2 = ry[0] - B*dx0 - D*dy0

            print(f"\n{'='*60}")
            print(f"  Solving for x, y:")
            print(f"{'='*60}")
            print(f"  {A}·x + {C}·y = {rx[0]} - {A}×{dx0:g} - {C}×{dy0:g} = {rhs1}")
            print(f"  {B}·x + {D}·y = {ry[0]} - {B}×{dx0:g} - {D}×{dy0:g} = {rhs2}")

            det = A*D - C*B
            print(f"\n  det = A·D - C·B = {A}×{D} - {C}×{B} = {det}")

            if abs(det) < 1e-10:
                print(f"  det = 0 => cannot solve uniquely")
            else:
                x_val = (rhs1*D - C*rhs2) / det
                y_val = (A*rhs2 - rhs1*B) / det
                print(f"  x = ({rhs1}×{D} - {C}×{rhs2}) / {det} = {x_val}")
                print(f"  y = ({A}×{rhs2} - {rhs1}×{B}) / {det} = {y_val}")

                print(f"\n{'='*60}")
                print(f"  Original vertices:")
                print(f"{'='*60}")
                orig = [(x_val+dx, y_val+dy) for dx, dy in offsets]
                for nm, (ox, oy) in zip(pnames, orig):
                    print(f"    {nm} = ({ox:.4f}, {oy:.4f})")

            M = np.array([[A, C], [B, D]])
            print(f"\n{'='*60}")
            print(f"  Transformation Matrix M = [[A,C],[B,D]]:")
            print(f"{'='*60}")
            print(f"    = [[{A}, {C}], [{B}, {D}]]")
            print(tabulate(M, tablefmt="fancy_grid", floatfmt=".4f"))

            if abs(det) >= 1e-10:
                print(f"\n{'='*60}")
                print(f"  Verification: M × Original = Result")
                print(f"{'='*60}")
                vtable = []
                for i, (nm, (ox, oy)) in enumerate(zip(pnames, orig)):
                    r = M @ np.array([ox, oy])
                    ok = abs(r[0]-rx[i])<0.001 and abs(r[1]-ry[i])<0.001
                    print(f"    M×{nm}({ox:.4f},{oy:.4f}) = ({r[0]:.4f},{r[1]:.4f}) expected ({rx[i]},{ry[i]}) {'✓' if ok else '✗'}")
                    vtable.append([nm, f"({ox:.4f},{oy:.4f})", f"({r[0]:.4f},{r[1]:.4f})", f"({rx[i]},{ry[i]})"])
                print()
                print(tabulate(vtable, headers=["Point","Original","Computed","Expected"], tablefmt="fancy_grid"))

    else:
        # General mode
        print("\n  Result = M × Original => M = Result × inv(Original)")
        rows = input_int("  Matrix size (rows) = ")
        cols = input_int("  Matrix size (cols) = ")
        print(f"\n  Enter the Result matrix ({rows}×{cols}):")
        r = []
        for i in range(rows):
            row = input(f"    Row {i+1} (space-separated): ").strip().split()
            r.append([float(v) for v in row])
        R = np.array(r)
        print(f"\n  Enter the Original matrix ({rows}×{cols}):")
        o = []
        for i in range(rows):
            row = input(f"    Row {i+1} (space-separated): ").strip().split()
            o.append([float(v) for v in row])
        O = np.array(o)
        print("\n  Original Matrix:")
        print(tabulate(O, tablefmt="fancy_grid", floatfmt=".4f"))
        det_val = np.linalg.det(O)
        print(f"\n  det(Original) = {det_val:.6f}")
        if abs(det_val) < 1e-10:
            print("  [ERROR] Singular matrix!"); return
        O_inv = np.linalg.inv(O)
        print("\n  inv(Original):")
        print(tabulate(O_inv, tablefmt="fancy_grid", floatfmt=".4f"))
        print("\n  Result Matrix:")
        print(tabulate(R, tablefmt="fancy_grid", floatfmt=".4f"))
        M = R @ O_inv
        print("\n  M = Result × inv(Original):")
        print(tabulate(M, tablefmt="fancy_grid", floatfmt=".4f"))
        verify = M @ O
        print("\n  Verification: M × Original =")
        print(tabulate(verify, tablefmt="fancy_grid", floatfmt=".4f"))
        print(f"  Match? {'✓' if np.allclose(verify, R) else '✗'}")

# ============================================================
# Option 6: Apply Transform to Points
# ============================================================
def option_apply_transform():
    print("\n--- Apply Transformation to Points ---")
    pts = input_points("Enter points (x1,y1 x2,y2 ...): ")
    print("Build transform sequence:")
    n = input_int("Number of transforms: ")
    M = np.eye(3)
    for i in range(n):
        print(f"\n  Transform {i+1}:")
        print(f"    [t]   Translation (tx, ty)")
        print(f"    [s]   Scaling (sx, sy)")
        print(f"    [r]   Rotation (angle)")
        print(f"    [rx]  Reflection across x-axis")
        print(f"    [ry]  Reflection across y-axis")
        print(f"    [ro]  Reflection across origin")
        print(f"    [ryx] Reflection across y=x")
        print(f"    [rynx] Reflection across y=-x")
        print(f"    [rxv] Reflection across x=val")
        print(f"    [ryv] Reflection across y=val")
        print(f"    [rmx] Reflection across y=mx")
        print(f"    [sh]  Shearing (shx, shy)")
        t = input("  Type: ").strip().lower()
        if t == 't':
            tx, ty = input_float("  tx="), input_float("  ty=")
            M = translation_matrix(tx, ty, show=True) @ M
        elif t == 's':
            sx, sy = input_float("  sx="), input_float("  sy=")
            M = scaling_matrix(sx, sy, show=True) @ M
        elif t == 'r':
            a = input_float("  angle(deg)=")
            M = rotation_matrix(a, show=True) @ M
        elif t == 'rx': M = reflection_x_axis(show=True) @ M
        elif t == 'ry': M = reflection_y_axis(show=True) @ M
        elif t == 'ro': M = reflection_origin(show=True) @ M
        elif t == 'ryx': M = reflection_y_eq_x(show=True) @ M
        elif t == 'rynx': M = reflection_y_eq_neg_x(show=True) @ M
        elif t == 'rxv':
            val = input_float("  x=")
            M = reflection_line_x_eq(val, show=True) @ M
        elif t == 'ryv':
            val = input_float("  y=")
            M = reflection_line_y_eq(val, show=True) @ M
        elif t == 'rmx':
            m = input_float("  slope m (y=mx)=")
            M = reflection_y_eq_mx(m, show=True) @ M
        elif t == 'sh':
            shx, shy = input_float("  shx="), input_float("  shy=")
            M = shearing_matrix(shx, shy, show=True) @ M
        else:
            print("  [!] Unknown type, skipping.")
    print_matrix(M, "Composite Matrix")
    # Apply to points as column matrix
    pts_arr = np.array([[x, y] for x, y in pts]).T  # 2xN
    ones = np.ones((1, len(pts)))
    P = np.vstack([pts_arr, ones])  # 3xN
    R = M @ P
    print("\nOriginal Points Matrix:")
    print(tabulate(P, tablefmt="fancy_grid", floatfmt=".4f"))
    print("\nStep-by-step M × each point:")
    transformed = []
    for i in range(len(pts)):
        pi = np.array([pts[i][0], pts[i][1], 1])
        print(f"\n  P{i+1} = ({pts[i][0]}, {pts[i][1]}):")
        result = show_matrix_multiply(M, pi, "M", f"P{i+1}")
        transformed.append((result[0], result[1]))
    print("\nTransformed Points Matrix (M × P):")
    print(tabulate(R, tablefmt="fancy_grid", floatfmt=".4f"))
    table = [[f"P{i+1}", f"({pts[i][0]},{pts[i][1]})",
              f"({transformed[i][0]:.4f},{transformed[i][1]:.4f})"]
             for i in range(len(pts))]
    print(tabulate(table, headers=["Point", "Original", "Transformed"], tablefmt="fancy_grid"))
    show = input("\nShow plot? (y/n): ").strip().lower()
    if show == 'y':
        plot_transform(pts, transformed, "Applied Transformation")

# ============================================================
# Option 7: Bresenham Parameter Selection
# ============================================================
def option_bresenham_params():
    print("\n--- Bresenham Parameter Selection ---")
    print("Options: (a) Bresenham(x1,y1,x2,y2)  (b) Bresenham(y1,x1,y2,x2)")
    print("         (c) Bresenham(x1,-y1,x2,-y2) (d) Bresenham(-y1,x1,-y2,x2)")
    n = input_int("Number of lines: ")
    results = []
    for i in range(n):
        x1 = input_int(f"  P1 x = ")
        y1 = input_int(f"  P1 y = ")
        x2 = input_int(f"  P2 x = ")
        y2 = input_int(f"  P2 y = ")
        answers = determine_bresenham_params(x1, y1, x2, y2)
        ans_str = ", ".join(f"({a})" for a in answers) if answers else "None found"
        results.append([f"{i+1}", f"({x1},{y1})", f"({x2},{y2})", ans_str])
    print(tabulate(results, headers=["#", "P1", "P2", "Answer"], tablefmt="fancy_grid"))

# ============================================================
# Option 8: Bresenham Line Full Table
# ============================================================
def option_bresenham_line():
    print("\n--- Bresenham's Line Algorithm ---")
    x1 = input_int("Start x1 = ")
    y1 = input_int("Start y1 = ")
    x2 = input_int("End x2 = ")
    y2 = input_int("End y2 = ")
    rows, points = bresenham_line(x1, y1, x2, y2)
    dx, dy = abs(x2-x1), abs(y2-y1)
    print(f"\ndx = {dx}, dy = {dy}")
    print(f"d1 = 2*dy - dx = {2*dy - dx}" if dx >= dy else f"d1 = 2*dx - dy = {2*dx - dy}")
    print_bresenham_table(rows)
    show = input("\nShow plot? (y/n): ").strip().lower()
    if show == 'y':
        plot_bresenham_line(points, f"Bresenham Line ({x1},{y1})->({x2},{y2})")

# ============================================================
# Option 9: Bresenham Circle Full Table
# ============================================================
def option_bresenham_circle():
    print("\n--- Bresenham's Circle Algorithm ---")
    r = input_int("Radius r = ")
    rows, octant = bresenham_circle(r)
    print(f"\nh_initial = 1 - r = {1 - r}")
    print_circle_table(rows)
    print(f"\nFirst octant points: {len(octant)}")
    all_pts = []
    for x, y in octant:
        sym = eight_way_symmetry(x, y)
        all_pts.extend(sym)
    all_pts = sorted(set(all_pts))
    print(f"Total circle points (8-way symmetry): {len(all_pts)}")
    show = input("\nShow plot? (y/n): ").strip().lower()
    if show == 'y':
        plot_circle(octant, r, title=f"Bresenham Circle r={r}")

# ============================================================
# Option 10: Circle with Center & Angle Range
# ============================================================
def option_circle_range():
    print("\n--- Circle with Center & Angle Range ---")
    r = input_int("Radius = ")
    cx = input_int("Center x = ")
    cy = input_int("Center y = ")
    start = input_float("Start angle (deg) = ")
    end = input_float("End angle (deg) = ")
    rows, _ = bresenham_circle(r)
    print(f"\nBresenham table (first octant, r={r}):")
    print_circle_table(rows)
    pts = circle_points_in_range(r, cx, cy, start, end)
    print(f"\nPoints in range {start}° to {end}° with center ({cx},{cy}):")
    table = [[i+1, f"({p[0]},{p[1]})"] for i, p in enumerate(pts)]
    print(tabulate(table, headers=["No", "Point"], tablefmt="fancy_grid"))

# ============================================================
# Option 11: Midpoint Ellipse
# ============================================================
def option_ellipse():
    print("\n--- Midpoint Ellipse Algorithm ---")
    a = input_int("Semi-major axis a = ")
    b = input_int("Semi-minor axis b = ")
    rows, quad = midpoint_ellipse(a, b)
    print_ellipse_table(rows)
    print(f"\nFirst quadrant points: {len(quad)}")
    show = input("\nShow plot? (y/n): ").strip().lower()
    if show == 'y':
        plot_ellipse(quad, a, b, title=f"Midpoint Ellipse a={a}, b={b}")

# ============================================================
# Option 12: 3D Basic Transformation
# ============================================================
def option_3d_basic():
    print("\n--- 3D Geometric Transformation ---")
    print("  (a) Rotation about x-axis")
    print("  (b) Rotation about y-axis")
    print("  (c) Rotation about z-axis")
    print("  (d) Translation")
    print("  (e) Scaling")
    ch = input("Choose (a-e): ").strip().lower()

    if ch == 'a':
        angle = input_float("Angle (degrees) = ")
        M = rotation_x_3d(angle, show=True)
    elif ch == 'b':
        angle = input_float("Angle (degrees) = ")
        M = rotation_y_3d(angle, show=True)
    elif ch == 'c':
        angle = input_float("Angle (degrees) = ")
        M = rotation_z_3d(angle, show=True)
    elif ch == 'd':
        tx = input_float("tx = ")
        ty = input_float("ty = ")
        tz = input_float("tz = ")
        M = translation_3d(tx, ty, tz, show=True)
    elif ch == 'e':
        sx = input_float("sx = ")
        sy = input_float("sy = ")
        sz = input_float("sz = ")
        M = scaling_3d(sx, sy, sz, show=True)
    else:
        print("Invalid choice.")
        return

    print_matrix_4x4(M, "Transformation Matrix")

    apply = input("\nApply to a set of 3D points? (y/n): ").strip().lower()
    if apply == 'y':
        n = input_int("Number of points: ")
        points = []
        for i in range(n):
            name = input(f"  Point {i+1} name (e.g. P): ").strip()
            x = input_float(f"  {name} x = ")
            y = input_float(f"  {name} y = ")
            z = input_float(f"  {name} z = ")
            points.append((name, x, y, z))
        transformed = apply_3d_transform(M, points, show=True)
        print_3d_results_table(points, transformed)

# ============================================================
# Option 13: 3D Rotation about Arbitrary Line
# ============================================================
def option_3d_arbitrary_rotation():
    print("\n--- 3D Rotation about Arbitrary Line ---")
    print("  Line L passes through point G and has direction vector V")
    angle = input_float("Rotation angle (degrees) = ")
    print("  Point G on the line:")
    gx = input_float("    Gx = ")
    gy = input_float("    Gy = ")
    gz = input_float("    Gz = ")
    print("  Direction vector V:")
    vx = input_float("    Vx = ")
    vy = input_float("    Vy = ")
    vz = input_float("    Vz = ")

    M = rotation_about_arbitrary_line(angle, gx, gy, gz, vx, vy, vz, show=True)

    apply = input("\nApply to a set of 3D points? (y/n): ").strip().lower()
    if apply == 'y':
        n = input_int("Number of points: ")
        points = []
        for i in range(n):
            name = input(f"  Point {i+1} name (e.g. A): ").strip()
            x = input_float(f"  {name} x = ")
            y = input_float(f"  {name} y = ")
            z = input_float(f"  {name} z = ")
            points.append((name, x, y, z))
        transformed = apply_3d_transform(M, points, show=True)
        print_3d_results_table(points, transformed)

# ============================================================
# Option 14: 3D Perspective Projection
# ============================================================
def option_3d_projection():
    print("\n--- 3D Perspective Projection ---")
    print("  Standard perspective projection onto xy-plane")
    d = input_float("Distance d (from view plane) = ")
    M = perspective_projection(d, show=True)
    print_matrix_4x4(M, "Perspective Projection Matrix")

    n = input_int("\nNumber of 3D points to project: ")
    points_3d = []
    for i in range(n):
        name = input(f"  Point {i+1} name (e.g. A): ").strip()
        x = input_float(f"  {name} x = ")
        y = input_float(f"  {name} y = ")
        z = input_float(f"  {name} z = ")
        points_3d.append((name, (x, y, z)))

    projected = apply_perspective(M, points_3d, d, show=True)

    print("\nProjected 2D coordinates:")
    table = [[name, f"({x:.3f}, {y:.3f})"] for name, x, y in projected]
    print(tabulate(table, headers=["Point", "(x', y')"], tablefmt="fancy_grid"))

    show = input("\nShow plot? (y/n): ").strip().lower()
    if show == 'y':
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 8))
        xs = [p[1] for p in projected]
        ys = [p[2] for p in projected]
        ax.plot(xs, ys, 'o', color='tomato', markersize=8)
        for name, x, y in projected:
            ax.annotate(f"{name}'({x:.2f},{y:.2f})", (x, y), fontsize=8,
                       textcoords="offset points", xytext=(5, 5))
        # Draw edges for cube if 8 points
        if len(projected) == 8:
            # Assume standard unit cube ordering: A-H
            edges = [(0,1),(1,2),(2,3),(3,0),  # front face
                     (4,5),(5,6),(6,7),(7,4),  # back face
                     (0,4),(1,5),(2,6),(3,7)]  # connecting
            for i, j in edges:
                ax.plot([projected[i][1], projected[j][1]],
                       [projected[i][2], projected[j][2]], '-', color='dodgerblue', linewidth=1.5)
        ax.set_title(f"Perspective Projection (d={d})", fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3); ax.set_aspect('equal')
        plt.tight_layout(); plt.show()

# ============================================================
# Main
# ============================================================
def main():
    print(BANNER)
    while True:
        print(MENU)
        choice = input("Select option: ").strip()
        try:
            if choice == '0':
                print("Goodbye!")
                break
            elif choice == '1': option_basic_transform()
            elif choice == '2': option_composite_transform()
            elif choice == '3': option_line_clipping()
            elif choice == '4': option_polygon_clipping()
            elif choice == '5': option_inverse()
            elif choice == '6': option_apply_transform()
            elif choice == '7': option_bresenham_params()
            elif choice == '8': option_bresenham_line()
            elif choice == '9': option_bresenham_circle()
            elif choice == '10': option_circle_range()
            elif choice == '11': option_ellipse()
            elif choice == '12': option_3d_basic()
            elif choice == '13': option_3d_arbitrary_rotation()
            elif choice == '14': option_3d_projection()
            elif choice == '15': matrix_calculator_menu()
            else:
                print("Invalid option. Please try again.")
        except Exception as e:
            print(f"\n[Error] {e}")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
