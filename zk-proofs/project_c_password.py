from field import FieldElement as F
from poly import Polynomial, vanishing_poly, lagrange_interpolate, poly_divmod


class Proof:
    def __init__(self, H_public: F, s_public: F, P_coeffs):
        self.H_public = H_public
        self.s_public = s_public
        self.P_coeffs = [c if isinstance(c, F) else F(c) for c in P_coeffs]

    def __repr__(self):
        return f"Proof(H={self.H_public}, s={self.s_public}, P_coeffs={self.P_coeffs})"

def prove_password(x_int: int, s_int: int):
    x = F(x_int)       # secret password (as a field element)
    s = F(s_int)       # public salt (also treated as field element)

    # Circuit
    t1 = x + s
    t2 = t1 * t1
    t3 = t2 * t1
    h  = t3 + F(7)
    H  = h  # public hash

    # Residuals
    r1 = t1 - (x + s)
    r2 = t2 - t1 * t1
    r3 = t3 - t2 * t1
    r4 = h  - (t3 + 7)
    r5 = H  - h

    points = [
        (F(1), r1),
        (F(2), r2),
        (F(3), r3),
        (F(4), r4),
        (F(5), r5),
    ]
    P = lagrange_interpolate(points)

    proof = Proof(H, s, P.coeffs)
    return H, s, proof

def verify_password(H_public: F, s_public: F, proof: Proof) -> bool:
    # 1. public input consistency
    if proof.H_public != H_public:
        print("Public H value mismatch.")
        return False
    
    if proof.s_public != s_public:
        print("Public s value mismatch.")
        return False
    
    # 2. rebuild P(x)
    P = Polynomial(proof.P_coeffs)

    # 3. Z(x) for 5 constraints
    Z = vanishing_poly(5)

    # 4. check divisibility
    Q, R = poly_divmod(P, Z)
    print("Divisibility check: remainder =", R)

    # remainder must be zero polynomial
    is_zero = all(c == F(0) for c in R.coeffs)
    return is_zero

if __name__ == "__main__":
    x_secret = 5
    s_public_int = 42

    # Prover side
    H, s, proof = prove_password(x_secret, s_public_int)

    print("x_secret:", x_secret)
    print("s_public:", s)
    print("H_public:", H)
    print("proof:", proof)

    # Verifier side (correct inputs)
    ok = verify_password(H, s, proof)
    print("Verification result (correct):", ok)

    # Tamper test 1: wrong hash
    ok_wrong_H = verify_password(H + F(1), s, proof)
    print("Verification result (wrong H):", ok_wrong_H)

    # Tamper test 2: wrong salt
    ok_wrong_s = verify_password(H, s + F(1), proof)
    print("Verification result (wrong s):", ok_wrong_s)

