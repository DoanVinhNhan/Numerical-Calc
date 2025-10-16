from backend.numerical_methods.horner_table.reverse_horner import reverse_horner
import numpy as np
from backend.numerical_methods.horner_table.synthetic_division import synthetic_division
if __name__ == "__main__":
    # --- Ví dụ 1: Chia Horner ---
    print("="*70)
    print("1. VÍ DỤ VỀ PHÉP CHIA HORNER (synthetic_division)")
    print("="*70)
    a1 = [-46, -5, 4, -3, 2, 1]
    c1 = 2
    result1 = reverse_horner(a1, c1)
    print(f"Hệ số đa thức: {a1}")
    print(f"Nghiệm nhân: {c1}")
    print("Bảng nhân Horner:")
    for row in result1['reverse_table']:
        print(row)
    print(f"Hệ số đa thức tích: {result1['coeffs']}")
    print("\n")