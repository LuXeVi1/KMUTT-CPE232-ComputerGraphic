"""
Module 1-2: Cohen-Sutherland Line Clipping
Based on Lecture 2 - 2D Viewing (CPE 381)

Region codes (4-bit): bit1=above, bit2=below, bit3=right, bit4=left
  Bit 1 = sign(y - ymax)     -> above
  Bit 2 = sign(ymin - y)     -> below
  Bit 3 = sign(x - xmax)     -> right
  Bit 4 = sign(xmin - x)     -> left
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tabulate import tabulate

def compute_code(x, y, xmin, ymin, xmax, ymax):
    code = 0
    if y > ymax: code |= 8   # bit1 (above)
    if y < ymin: code |= 4   # bit2 (below)
    if x > xmax: code |= 2   # bit3 (right)
    if x < xmin: code |= 1   # bit4 (left)
    return code

def code_to_str(code):
    return f"{code:04b}"

def explain_code(x, y, xmin, ymin, xmax, ymax):
    """Return explanation string of how code is computed."""
    bits = []
    bits.append(f"Bit1(above): y={y} > ymax={ymax}? {'Yes=>1' if y > ymax else 'No=>0'}")
    bits.append(f"Bit2(below): y={y} < ymin={ymin}? {'Yes=>1' if y < ymin else 'No=>0'}")
    bits.append(f"Bit3(right): x={x} > xmax={xmax}? {'Yes=>1' if x > xmax else 'No=>0'}")
    bits.append(f"Bit4(left):  x={x} < xmin={xmin}? {'Yes=>1' if x < xmin else 'No=>0'}")
    code = compute_code(x, y, xmin, ymin, xmax, ymax)
    return bits, code

def cohen_sutherland_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    """
    Returns (initial_category, final_category, visible_p1, visible_p2, steps).
    """
    steps = []

    # --- Step 1: Compute region codes ---
    steps.append("=" * 50)
    steps.append("Step 1: Compute Region Codes")
    steps.append(f"  Window: xmin={xmin}, ymin={ymin}, xmax={xmax}, ymax={ymax}")
    steps.append(f"  Code format: [Bit1:above | Bit2:below | Bit3:right | Bit4:left]")

    bits1, code1 = explain_code(x1, y1, xmin, ymin, xmax, ymax)
    steps.append(f"\n  P1({x1}, {y1}):")
    for b in bits1:
        steps.append(f"    {b}")
    steps.append(f"    => Code P1 = {code_to_str(code1)}")

    bits2, code2 = explain_code(x2, y2, xmin, ymin, xmax, ymax)
    steps.append(f"\n  P2({x2}, {y2}):")
    for b in bits2:
        steps.append(f"    {b}")
    steps.append(f"    => Code P2 = {code_to_str(code2)}")

    # --- Step 2: Determine category ---
    steps.append(f"\nStep 2: Determine Category")
    steps.append(f"  Code P1 AND Code P2 = {code_to_str(code1)} & {code_to_str(code2)} = {code_to_str(code1 & code2)}")

    # Case 1: Visible
    if code1 == 0 and code2 == 0:
        steps.append(f"  Both codes = 0000 => VISIBLE")
        steps.append(f"  Visible segment: ({x1},{y1}) to ({x2},{y2})")
        return "Visible", "Visible", (x1, y1), (x2, y2), steps

    # Case 2: Invisible
    if (code1 & code2) != 0:
        steps.append(f"  AND = {code_to_str(code1 & code2)} ≠ 0000 => INVISIBLE (trivially rejected)")
        return "Invisible", "Invisible", None, None, steps

    # Case 3: Clipping Candidate
    steps.append(f"  AND = 0000 but not both 0000 => CLIPPING CANDIDATE")
    steps.append(f"\nStep 3: Perform Clipping")
    steps.append(f"  Line equation: y - y1 = m(x - x1)")
    dx_orig = x2 - x1
    dy_orig = y2 - y1
    if dx_orig != 0:
        m = dy_orig / dx_orig
        steps.append(f"  m = (y2-y1)/(x2-x1) = ({y2}-{y1})/({x2}-{x1}) = {dy_orig}/{dx_orig} = {m:.6f}")
    else:
        m = float('inf')
        steps.append(f"  m = (y2-y1)/(x2-x1) = vertical line (m = ∞)")

    cx1, cy1, cx2, cy2 = float(x1), float(y1), float(x2), float(y2)
    max_iter = 20
    clip_round = 0

    for iteration in range(max_iter):
        c1 = compute_code(cx1, cy1, xmin, ymin, xmax, ymax)
        c2 = compute_code(cx2, cy2, xmin, ymin, xmax, ymax)

        if c1 == 0 and c2 == 0:
            break

        if (c1 & c2) != 0:
            steps.append(f"\n  After clipping:")
            steps.append(f"    P1'({cx1:.4f},{cy1:.4f}) code={code_to_str(c1)}")
            steps.append(f"    P2'({cx2:.4f},{cy2:.4f}) code={code_to_str(c2)}")
            steps.append(f"    AND = {code_to_str(c1 & c2)} ≠ 0000 => INVISIBLE after clipping")
            return "Clipping Candidate", "Clipping Candidate (Invisible)", None, None, steps

        code_out = c1 if c1 != 0 else c2
        which = "P1" if code_out == c1 else "P2"
        clip_round += 1
        dx = cx2 - cx1
        dy = cy2 - cy1

        steps.append(f"\n  --- Clip round {clip_round}: {which} (code={code_to_str(code_out)}) ---")

        if code_out & 8:  # above
            steps.append(f"    Bit1=1 => {which} is ABOVE window, clip against y = ymax = {ymax}")
            if dy != 0:
                x_int = cx1 + dx * (ymax - cy1) / dy
                steps.append(f"    Formula: x = x1 + dx*(ymax - y1)/dy")
                steps.append(f"           = {cx1:.4f} + {dx:.4f}*({ymax} - {cy1:.4f})/{dy:.4f}")
                steps.append(f"           = {cx1:.4f} + {dx:.4f}*{ymax - cy1:.4f}/{dy:.4f}")
                steps.append(f"           = {cx1:.4f} + {dx*(ymax - cy1)/dy:.4f}")
                steps.append(f"           = {x_int:.4f}")
            else:
                x_int = cx1
            y_int = ymax
            steps.append(f"    y = ymax = {ymax}")
            steps.append(f"    => Intersection: ({x_int:.4f}, {y_int:.4f})")

        elif code_out & 4:  # below
            steps.append(f"    Bit2=1 => {which} is BELOW window, clip against y = ymin = {ymin}")
            if dy != 0:
                x_int = cx1 + dx * (ymin - cy1) / dy
                steps.append(f"    Formula: x = x1 + dx*(ymin - y1)/dy")
                steps.append(f"           = {cx1:.4f} + {dx:.4f}*({ymin} - {cy1:.4f})/{dy:.4f}")
                steps.append(f"           = {cx1:.4f} + {dx:.4f}*{ymin - cy1:.4f}/{dy:.4f}")
                steps.append(f"           = {cx1:.4f} + {dx*(ymin - cy1)/dy:.4f}")
                steps.append(f"           = {x_int:.4f}")
            else:
                x_int = cx1
            y_int = ymin
            steps.append(f"    y = ymin = {ymin}")
            steps.append(f"    => Intersection: ({x_int:.4f}, {y_int:.4f})")

        elif code_out & 2:  # right
            steps.append(f"    Bit3=1 => {which} is RIGHT of window, clip against x = xmax = {xmax}")
            if dx != 0:
                y_int = cy1 + dy * (xmax - cx1) / dx
                steps.append(f"    Formula: y = y1 + dy*(xmax - x1)/dx")
                steps.append(f"           = {cy1:.4f} + {dy:.4f}*({xmax} - {cx1:.4f})/{dx:.4f}")
                steps.append(f"           = {cy1:.4f} + {dy:.4f}*{xmax - cx1:.4f}/{dx:.4f}")
                steps.append(f"           = {cy1:.4f} + {dy*(xmax - cx1)/dx:.4f}")
                steps.append(f"           = {y_int:.4f}")
            else:
                y_int = cy1
            x_int = xmax
            steps.append(f"    x = xmax = {xmax}")
            steps.append(f"    => Intersection: ({x_int:.4f}, {y_int:.4f})")

        elif code_out & 1:  # left
            steps.append(f"    Bit4=1 => {which} is LEFT of window, clip against x = xmin = {xmin}")
            if dx != 0:
                y_int = cy1 + dy * (xmin - cx1) / dx
                steps.append(f"    Formula: y = y1 + dy*(xmin - x1)/dx")
                steps.append(f"           = {cy1:.4f} + {dy:.4f}*({xmin} - {cx1:.4f})/{dx:.4f}")
                steps.append(f"           = {cy1:.4f} + {dy:.4f}*{xmin - cx1:.4f}/{dx:.4f}")
                steps.append(f"           = {cy1:.4f} + {dy*(xmin - cx1)/dx:.4f}")
                steps.append(f"           = {y_int:.4f}")
            else:
                y_int = cy1
            x_int = xmin
            steps.append(f"    x = xmin = {xmin}")
            steps.append(f"    => Intersection: ({x_int:.4f}, {y_int:.4f})")

        new_code = compute_code(x_int, y_int, xmin, ymin, xmax, ymax)
        steps.append(f"    New {which}' = ({x_int:.4f}, {y_int:.4f}), code = {code_to_str(new_code)}")

        if code_out == c1:
            cx1, cy1 = x_int, y_int
        else:
            cx2, cy2 = x_int, y_int

    vp1 = (round(cx1, 4), round(cy1, 4))
    vp2 = (round(cx2, 4), round(cy2, 4))
    steps.append(f"\nResult: VISIBLE segment")
    steps.append(f"  From ({vp1[0]}, {vp1[1]}) to ({vp2[0]}, {vp2[1]})")
    return "Clipping Candidate", "Clipping Candidate (Visible)", vp1, vp2, steps

def plot_clipping(lines_data, xmin, ymin, xmax, ymax):
    fig, ax = plt.subplots(figsize=(10, 8))
    rect = patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                              linewidth=2, edgecolor='green', facecolor='lightgreen', alpha=0.3,
                              label=f'Window [{xmin},{ymin}]x[{xmax},{ymax}]')
    ax.add_patch(rect)
    colors = ['blue', 'red', 'purple', 'orange', 'brown', 'teal', 'magenta']
    for i, (init_cat, final_cat, p1, p2, op1, op2) in enumerate(lines_data):
        c = colors[i % len(colors)]
        ax.plot([op1[0], op2[0]], [op1[1], op2[1]], '--', color=c, alpha=0.4, linewidth=1)
        ax.plot([op1[0]], [op1[1]], 'o', color=c, markersize=4)
        ax.plot([op2[0]], [op2[1]], 'o', color=c, markersize=4)
        if p1 and p2:
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], '-', color=c, linewidth=2.5,
                    label=f'Line {i+1}: {final_cat}')
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'o', color=c, markersize=6)
        else:
            ax.plot([], [], '-', color=c, label=f'Line {i+1}: {final_cat}')
    ax.set_title("Cohen-Sutherland Line Clipping", fontsize=14, fontweight='bold')
    ax.legend(fontsize=8, loc='upper left')
    ax.grid(True, alpha=0.3); ax.set_aspect('equal')
    plt.tight_layout(); plt.show()
