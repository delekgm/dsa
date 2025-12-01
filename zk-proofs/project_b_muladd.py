from field import FieldElement as F
from poly import Polynomial, vanishing_poly, lagrange_interpolate, poly_divmod

class Proof:
    def __init__(self, H_public: F, P_coeffs):
        # Public value the prover used when building the constraints
        self.H_public = H_public
        # Coefficients of P(x) in the field
        self.P_coeffs = [c if isinstance(c, F) else F(c) for c in P_coeffs]

    def __repr__(self):
        return f"Proof(H={self.H_public}, P_coeffs={self.P_coeffs})"

def prove_relation(x_int: int):
    x = F(x_int)

    t1 = x + 3
    t2 = x * t1
    y_public = t2

    # residuals
    r1 = t1 - (x + 3)
    r2 = t2 - (x * t1)
    r3 = y_public - t2

    points = [
        (F(1), r1),
        (F(2), r2),
        (F(3), r3),
    ]
    P = lagrange_interpolate(points)

    # Build proof from H and P(x)
    proof = Proof(y_public, P.coeffs)

    return y_public, proof

def verify_relation(y_public: F, proof: Proof) -> bool:
    # 1. public input consistency
    if proof.H_public != y_public:
        print("Public value mismatch.")
        return False
    
    # 2. rebuild P(x)
    P = Polynomial(proof.P_coeffs)

    # 3. Z(x) for 3 constraints
    Z = vanishing_poly(3)

    # 4. check divisibility
    Q, R = poly_divmod(P, Z)
    print("Divisibility check: remainder =", R)

    # remainder must be zero polynomial
    is_zero = all(c == F(0) for c in R.coeffs)
    return is_zero

if __name__ == "__main__":
    x_secret = 1213444776239
    y_public, proof = prove_relation(x_secret)

    print("x_secret:", x_secret)
    print("y_public:", y_public)
    print("proof:", proof)

    ok = verify_relation(y_public, proof)
    print("Verification result:", ok)