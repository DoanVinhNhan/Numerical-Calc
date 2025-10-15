#backend/numerical_methods/interpolation/chebyshev_nodes.py
import numpy as np

def chebyshev_nodes(a: float, b: float, n: int) -> np.ndarray:
    """
    Calculate Chebyshev nodes (optimal interpolation points) in the interval [a,b]
    
    Parameters:
        a (float): Left endpoint of the interval
        b (float): Right endpoint of the interval
        n (int): Number of points - 1 (total points will be n+1)
    
    Returns:
        np.ndarray: Array of n+1 Chebyshev nodes in ascending order
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("a and b must be numeric values")
    if a >= b:
        raise ValueError("a must be less than b")

    # Calculate points using vectorized operations
    i = np.arange(n + 1)
    chebyshev = np.cos((2*i + 1) * np.pi / (2*(n + 1)))
    
    # Scale from [-1, 1] to [a, b]
    nodes = ((b + a) / 2) + ((b - a) / 2) * chebyshev
    
    # Sort nodes in ascending order
    return {"nodes": np.sort(nodes)}