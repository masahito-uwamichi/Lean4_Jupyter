"""
lean4_viz.py - Visualization helper for Lean4 expressions in JupyterLab notebooks.

Usage:
    import lean4_viz
    lean4_viz.show_latex(r"\forall x \in \mathbb{N}, x + 0 = x")
    lean4_viz.show_expr("Nat.add_zero")
"""

from IPython.display import display, Math


def show_latex(latex_str: str) -> None:
    """Render a LaTeX string using MathJax in JupyterLab.

    Args:
        latex_str: A valid LaTeX math expression string.
    """
    try:
        if not isinstance(latex_str, str) or not latex_str.strip():
            raise ValueError("latex_str must be a non-empty string")
        display(Math(latex_str))
    except Exception as e:
        print(f"[lean4_viz] Could not render LaTeX: {e}\nRaw: {latex_str}")


def show_expr(lean_expr_str: str) -> None:
    """Display a Lean4 expression as LaTeX-style notation in JupyterLab.

    Converts a Lean4 identifier or expression string into a LaTeX-friendly
    representation using \\text{} so it renders in MathJax.

    Args:
        lean_expr_str: A Lean4 expression or identifier string.
    """
    try:
        if not isinstance(lean_expr_str, str) or not lean_expr_str.strip():
            raise ValueError("lean_expr_str must be a non-empty string")
        # Wrap in \text{} so MathJax renders it as math-mode text
        latex = r"\text{" + lean_expr_str.strip() + r"}"
        display(Math(latex))
    except Exception as e:
        print(f"[lean4_viz] Could not render expression: {e}\nRaw: {lean_expr_str}")
