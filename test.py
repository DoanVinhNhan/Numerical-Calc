import numpy as np
from backend.numerical_methods.honner_table.synthetic_division import synthetic_division
if __name__ == "__main__":
    # --- Ví dụ 1: Chia Horner ---
    print("="*70)
    print("1. VÍ DỤ VỀ PHÉP CHIA HORNER (synthetic_division)")
    print("="*70)
    a1 = [-46, -5, 4, -3, 2, 1]  # p(x) = x^5 + 2x^4 - 3x^3 + 4x^2 - 5x - 46
    c1 = 2
    result1 = synthetic_division(a1, c1)
    print(f"Hệ số đa thức: {a1}")
    print(f"Nghiệm chia: {c1}")
    print("Bảng chia Horner:")
    for row in result1['division_table']:
        print(row)
    print(f"Hệ số đa thức thương: {result1['quotient_coeffs']}")
    print(f"giá trị tại {c1}: {result1['value']}")
    print("\n")