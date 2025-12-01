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

def hash_field(x: F) -> F:
    """
    Toy hash function in our field:
        hash(x) = x^3 + 5
    """
    t1 = x * x
    t2 = t1 * x
    h = t2 + F(5)
    return h

def prove_hash_preimage(x_int: int):
    """
    Prover side:
    - Takes a secret integer x_int.
    - Computes all intermediate witness values.
    - Constructs the residual polynomial P(x).
    - Returns:
        - public output H
        - a Proof object (no raw witness exposed).
    """
    x = F(x_int)  # secret

    # internal witness values
    t1 = x * x
    t2 = t1 * x
    h  = t2 + F(5)

    H = h  # public value

    # residuals
    r1 = t1 - x * x
    r2 = t2 - t1 * x
    r3 = h  - (t2 + F(5))
    r4 = h  - H          # uses H the prover is claiming publicly

    points = [
        (F(1), r1),
        (F(2), r2),
        (F(3), r3),
        (F(4), r4),
    ]
    P = lagrange_interpolate(points)

    # Build proof from H and P(x)
    proof = Proof(H, P.coeffs)

    witness = {
        "x": x,
        "t1": t1,
        "t2": t2,
        "h": h,
    }
    print("witness: ", witness)

    # (Optionally you could still return witness separately for debugging, but
    #  the verifier should never see it.)
    return H, proof


def verify_hash_preimage(H: F, proof: Proof) -> bool:
    """
    Verifier side (toy, SNARK-like):
    - Sees only:
        * public input H
        * proof object
    - Does NOT see x, t1, t2, h.
    - Checks:
        1. The proof's embedded H matches the public H.
        2. The polynomial P(x) is divisible by Z(x).
    """
    # 1. Ensure the prover's claimed H matches the public H
    if proof.H_public != H:
        print("Public H mismatch.")
        return False

    # Rebuild P(x) from proof
    P = Polynomial(proof.P_coeffs)

    # Vanishing polynomial for 4 constraints
    Z = vanishing_poly(4)

    # Check divisibility: P(x) = Q(x) * Z(x)   <=> remainder == 0
    Q, R = poly_divmod(P, Z)
    print("Divisibility check: remainder =", R)

    is_zero = all(c == F(0) for c in R.coeffs)
    return is_zero

if __name__ == "__main__":
    # prover picks secret x
    x_secret = 4

    # prover computes public H and witness
    H, proof = prove_hash_preimage(x_secret)

    print("Public H =", H)
    print("Proof    =", proof)

    # verifier checks constraints
    ok = verify_hash_preimage(H, proof)
    print("verification result:", ok)


