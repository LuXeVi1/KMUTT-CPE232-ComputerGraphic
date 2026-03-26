"""
Matrix Calculator - General Purpose
For when the exam gives you raw matrices to work with.

Operations:
  - Enter & display matrices
  - Multiply matrices (step-by-step)
  - Inverse, Determinant, Transpose
  - Multiply matrix × point(s)
  - Composite: chain multiple matrices
"""
import numpy as np
from tabulate import tabulate

def input_matrix(prompt="Enter matrix", rows=None, cols=None):
    """Input a matrix row by row. Auto-detect size or use given dimensions."""
    print(f"\n  {prompt}")
    if rows is None:
        rows = int(input("  Number of rows: ").strip())
    if cols is None:
        cols = int(input("  Number of columns: ").strip())
    print(f"  Enter {rows} rows, each with {cols} values (space-separated):")
    M = []
    for i in range(rows):
        row_str = input(f"    Row {i+1}: ").strip()
        vals = [float(v) for v in row_str.split()]
        if len(vals) != cols:
            raise ValueError(f"Expected {cols} values, got {len(vals)}")
        M.append(vals)
    return np.array(M, dtype=float)

def display_matrix(M, label="Matrix", decimals=4):
    """Pretty-print a matrix with label."""
    fmt = f".{decimals}f"
    print(f"\n  {label} ({M.shape[0]}×{M.shape[1]}):")
    rows = []
    for i in range(M.shape[0]):
        rows.append([f"r{i+1}"] + [f"{v:{fmt}}" for v in M[i]])
    headers = [""] + [f"c{j+1}" for j in range(M.shape[1])]
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

def show_multiply_step(A, B, label_A="A", label_B="B"):
    """Show step-by-step matrix multiplication A × B."""
    if A.shape[1] != B.shape[0]:
        print(f"  [ERROR] Cannot multiply {A.shape} × {B.shape}: inner dimensions don't match!")
        return None

    print(f"\n  {label_A} × {label_B} = C")
    print(f"  ({A.shape[0]}×{A.shape[1]}) × ({B.shape[0]}×{B.shape[1]}) = ({A.shape[0]}×{B.shape[1]})")
    print(f"\n  Formula: C[i,j] = Σ {label_A}[i,k] × {label_B}[k,j]  for k=1..{A.shape[1]}")

    C = np.zeros((A.shape[0], B.shape[1]))
    for i in range(A.shape[0]):
        for j in range(B.shape[1]):
            terms = []
            for k in range(A.shape[1]):
                terms.append(f"({A[i,k]:.4f}×{B[k,j]:.4f})")
            products = [A[i,k] * B[k,j] for k in range(A.shape[1])]
            C[i,j] = sum(products)
            products_str = " + ".join(f"{p:.4f}" for p in products)
            print(f"    C[{i+1},{j+1}] = {' + '.join(terms)}")
            print(f"           = {products_str} = {C[i,j]:.4f}")

    return C

def show_inverse_step(M, label="M"):
    """Show matrix inverse with verification."""
    n = M.shape[0]
    if M.shape[0] != M.shape[1]:
        print(f"  [ERROR] Matrix must be square for inverse! Got {M.shape}")
        return None

    det = np.linalg.det(M)
    print(f"\n  Finding inverse of {label} ({n}×{n})")
    print(f"  det({label}) = {det:.6f}")

    if abs(det) < 1e-10:
        print(f"  [ERROR] Matrix is singular (det ≈ 0), no inverse exists!")
        return None

    M_inv = np.linalg.inv(M)

    if n == 2:
        a, b, c, d = M[0,0], M[0,1], M[1,0], M[1,1]
        print(f"\n  For 2×2 matrix [[a,b],[c,d]]:")
        print(f"  {label}⁻¹ = (1/det) × [[d, -b], [-c, a]]")
        print(f"       = (1/{det:.4f}) × [[{d:.4f}, {-b:.4f}], [{-c:.4f}, {a:.4f}]]")
    elif n == 3:
        print(f"\n  For 3×3 matrix, using cofactor method:")
        print(f"  {label}⁻¹ = (1/det) × adj({label})")
        print(f"  det = {det:.6f}")

        # Show cofactor matrix
        cofactor = np.zeros((3,3))
        for i in range(3):
            for j in range(3):
                minor = np.delete(np.delete(M, i, axis=0), j, axis=1)
                cofactor[i,j] = ((-1)**(i+j)) * np.linalg.det(minor)
        display_matrix(cofactor, f"Cofactor matrix of {label}")
        adj = cofactor.T
        display_matrix(adj, f"Adjugate (transpose of cofactor)")

    print(f"\n  Verification: {label} × {label}⁻¹ = I")
    verify = M @ M_inv
    # Round near-zero values
    verify = np.where(np.abs(verify) < 1e-10, 0, verify)
    display_matrix(verify, f"{label} × {label}⁻¹")

    return M_inv

def show_determinant_step(M, label="M"):
    """Show determinant calculation."""
    n = M.shape[0]
    if n != M.shape[1]:
        print(f"  [ERROR] Matrix must be square! Got {M.shape}")
        return None

    if n == 2:
        a, b, c, d = M[0,0], M[0,1], M[1,0], M[1,1]
        det = a*d - b*c
        print(f"\n  det({label}) for 2×2:")
        print(f"  det = a·d - b·c")
        print(f"      = {a:.4f}×{d:.4f} - {b:.4f}×{c:.4f}")
        print(f"      = {a*d:.4f} - {b*c:.4f}")
        print(f"      = {det:.4f}")
        return det

    elif n == 3:
        print(f"\n  det({label}) for 3×3 using cofactor expansion along row 1:")
        det = 0
        for j in range(3):
            minor = np.delete(np.delete(M, 0, axis=0), j, axis=1)
            minor_det = minor[0,0]*minor[1,1] - minor[0,1]*minor[1,0]
            sign = (-1)**j
            cofactor = sign * M[0,j] * minor_det
            sign_str = "+" if sign > 0 else "-"
            print(f"    {sign_str} a[1,{j+1}] × M{j+1} = {sign_str} {M[0,j]:.4f} × det({minor.tolist()}) = {sign_str} {M[0,j]:.4f} × {minor_det:.4f} = {cofactor:.4f}")
            det += cofactor
        print(f"  det = {det:.4f}")
        return det

    else:
        det = np.linalg.det(M)
        print(f"\n  det({label}) for {n}×{n} = {det:.6f}")
        return det

def show_matrix_power(M, label="M"):
    """Find eigenvalues of a matrix."""
    if M.shape[0] != M.shape[1]:
        print(f"  [ERROR] Must be square!")
        return
    eigenvalues = np.linalg.eigvals(M)
    print(f"\n  Eigenvalues of {label}:")
    for i, ev in enumerate(eigenvalues):
        if np.isreal(ev):
            print(f"    λ{i+1} = {ev.real:.6f}")
        else:
            print(f"    λ{i+1} = {ev:.6f}")

def matrix_calculator_menu():
    """Interactive matrix calculator."""
    stored = {}  # Store matrices by name

    while True:
        print(f"\n  --- Matrix Calculator ---")
        print(f"  Stored matrices: {list(stored.keys()) if stored else 'none'}")
        print(f"  (1) Enter/store a matrix")
        print(f"  (2) Multiply two matrices (A × B) with steps")
        print(f"  (3) Multiply matrix × point(s)")
        print(f"  (4) Find inverse (with steps)")
        print(f"  (5) Find determinant (with steps)")
        print(f"  (6) Transpose")
        print(f"  (7) Chain multiply multiple matrices")
        print(f"  (8) Scalar operations (add/subtract/scale)")
        print(f"  (9) Display a stored matrix")
        print(f"  (0) Back to main menu")
        ch = input("\n  Choose: ").strip()

        if ch == '0':
            break

        elif ch == '1':
            name = input("  Matrix name (e.g. A, B, M1): ").strip().upper()
            M = input_matrix(f"Enter matrix {name}")
            stored[name] = M
            display_matrix(M, name)

        elif ch == '2':
            a_name = input("  First matrix name (or 'new'): ").strip().upper()
            if a_name == 'NEW':
                A = input_matrix("Enter first matrix")
                a_name = "A"
            elif a_name in stored:
                A = stored[a_name]
                display_matrix(A, a_name)
            else:
                print(f"  Matrix '{a_name}' not found. Enter it:")
                A = input_matrix(f"Enter matrix {a_name}")
                stored[a_name] = A

            b_name = input("  Second matrix name (or 'new'): ").strip().upper()
            if b_name == 'NEW':
                B = input_matrix("Enter second matrix")
                b_name = "B"
            elif b_name in stored:
                B = stored[b_name]
                display_matrix(B, b_name)
            else:
                print(f"  Matrix '{b_name}' not found. Enter it:")
                B = input_matrix(f"Enter matrix {b_name}")
                stored[b_name] = B

            C = show_multiply_step(A, B, a_name, b_name)
            if C is not None:
                display_matrix(C, f"{a_name} × {b_name}")
                save = input(f"  Save result as? (name or Enter to skip): ").strip().upper()
                if save:
                    stored[save] = C

        elif ch == '3':
            m_name = input("  Matrix name (or 'new'): ").strip().upper()
            if m_name == 'NEW':
                M = input_matrix("Enter matrix")
                m_name = "M"
            elif m_name in stored:
                M = stored[m_name]
                display_matrix(M, m_name)
            else:
                M = input_matrix(f"Enter matrix {m_name}")
                stored[m_name] = M

            n_pts = int(input("  Number of points: ").strip())
            print(f"  Enter points ({M.shape[1]} values each, space-separated):")
            for i in range(n_pts):
                pt_str = input(f"    Point {i+1}: ").strip()
                vals = [float(v) for v in pt_str.split()]
                # Auto-add homogeneous coordinate if needed
                if len(vals) == M.shape[1] - 1:
                    vals.append(1.0)
                    print(f"    (auto-added homogeneous 1) => {vals}")
                P = np.array(vals)
                print(f"\n    {m_name} × P{i+1}:")
                R = M @ P
                for r in range(M.shape[0]):
                    terms = " + ".join(f"({M[r,k]:.4f}×{P[k]:.4f})" for k in range(M.shape[1]))
                    print(f"      row{r+1}: {terms} = {R[r]:.4f}")
                if len(R) >= 3 and abs(R[-1]) > 1e-10 and abs(R[-1] - 1.0) > 1e-10:
                    # Homogeneous: divide by last coord
                    w = R[-1]
                    cartesian = R[:-1] / w
                    print(f"      w = {w:.4f}")
                    print(f"      Cartesian: {[f'{v:.4f}' for v in cartesian]}")
                print(f"      Result: {[f'{v:.4f}' for v in R]}")

        elif ch == '4':
            m_name = input("  Matrix name (or 'new'): ").strip().upper()
            if m_name == 'NEW':
                M = input_matrix("Enter matrix")
                m_name = "M"
            elif m_name in stored:
                M = stored[m_name]
                display_matrix(M, m_name)
            else:
                M = input_matrix(f"Enter matrix {m_name}")
                stored[m_name] = M

            M_inv = show_inverse_step(M, m_name)
            if M_inv is not None:
                display_matrix(M_inv, f"{m_name}⁻¹")
                stored[f"{m_name}_INV"] = M_inv

        elif ch == '5':
            m_name = input("  Matrix name (or 'new'): ").strip().upper()
            if m_name == 'NEW':
                M = input_matrix("Enter matrix")
                m_name = "M"
            elif m_name in stored:
                M = stored[m_name]
                display_matrix(M, m_name)
            else:
                M = input_matrix(f"Enter matrix {m_name}")
                stored[m_name] = M

            show_determinant_step(M, m_name)

        elif ch == '6':
            m_name = input("  Matrix name (or 'new'): ").strip().upper()
            if m_name == 'NEW':
                M = input_matrix("Enter matrix")
                m_name = "M"
            elif m_name in stored:
                M = stored[m_name]
            else:
                M = input_matrix(f"Enter matrix {m_name}")
                stored[m_name] = M

            display_matrix(M, f"{m_name}")
            T = M.T
            display_matrix(T, f"{m_name}ᵀ (transpose)")
            stored[f"{m_name}T"] = T

        elif ch == '7':
            n = int(input("  How many matrices to chain multiply? ").strip())
            matrices = []
            names = []
            for i in range(n):
                name = input(f"  Matrix {i+1} name (or 'new'): ").strip().upper()
                if name == 'NEW':
                    M = input_matrix(f"Enter matrix {i+1}")
                    name = f"M{i+1}"
                elif name in stored:
                    M = stored[name]
                else:
                    M = input_matrix(f"Enter matrix {name}")
                    stored[name] = M
                matrices.append(M)
                names.append(name)
                display_matrix(M, name)

            print(f"\n  Computing: {' × '.join(names)}")
            result = matrices[0]
            for i in range(1, len(matrices)):
                label = f"({' × '.join(names[:i+1])})"
                print(f"\n  Step {i}: {' × '.join(names[:i])} × {names[i]}")
                result = show_multiply_step(result, matrices[i],
                    f"{'×'.join(names[:i])}", names[i])
                if result is None:
                    print("  [ERROR] Multiplication failed!")
                    break
                display_matrix(result, label)

            if result is not None:
                display_matrix(result, f"Final: {' × '.join(names)}")
                save = input(f"  Save result as? (name or Enter to skip): ").strip().upper()
                if save:
                    stored[save] = result

        elif ch == '8':
            print("  (a) Add A + B")
            print("  (b) Subtract A - B")
            print("  (c) Scalar multiply k × A")
            op = input("  Choose: ").strip().lower()

            if op in ('a', 'b'):
                a_name = input("  First matrix name (or 'new'): ").strip().upper()
                A = stored.get(a_name) if a_name in stored else input_matrix(f"Enter {a_name}")
                b_name = input("  Second matrix name (or 'new'): ").strip().upper()
                B = stored.get(b_name) if b_name in stored else input_matrix(f"Enter {b_name}")

                if A.shape != B.shape:
                    print(f"  [ERROR] Shapes don't match: {A.shape} vs {B.shape}")
                else:
                    if op == 'a':
                        C = A + B
                        display_matrix(A, a_name)
                        display_matrix(B, b_name)
                        print(f"\n  Element-wise: C[i,j] = {a_name}[i,j] + {b_name}[i,j]")
                        display_matrix(C, f"{a_name} + {b_name}")
                    else:
                        C = A - B
                        display_matrix(A, a_name)
                        display_matrix(B, b_name)
                        print(f"\n  Element-wise: C[i,j] = {a_name}[i,j] - {b_name}[i,j]")
                        display_matrix(C, f"{a_name} - {b_name}")

            elif op == 'c':
                k = float(input("  Scalar k = ").strip())
                m_name = input("  Matrix name (or 'new'): ").strip().upper()
                M = stored.get(m_name) if m_name in stored else input_matrix(f"Enter {m_name}")
                display_matrix(M, m_name)
                C = k * M
                print(f"\n  Every element multiplied by {k}")
                display_matrix(C, f"{k} × {m_name}")

        elif ch == '9':
            if not stored:
                print("  No matrices stored yet.")
            else:
                for name, M in stored.items():
                    display_matrix(M, name)
