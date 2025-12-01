from field import FieldElement as F

class Polynomial:
    """
    Polynomial over the field F, with coefficients:
        coeffs[0] + coeffs[1] * x + coeffs[2] * x^2 + ...
    """
    def __init__(self, coeffs):
        # coeffs is a list of FieldElement or ints
        self.coeffs = [c if isinstance(c, F) else F(c) for c in coeffs]
        self._trim()

    def _trim(self):
        # remove trailing zeros so degree is correct
        while len(self.coeffs) > 1 and self.coeffs[-1] == F(0):
            self.coeffs.pop()

    def __repr__(self):
        return f"Poly({self.coeffs})"

    def degree(self):
        return len(self.coeffs) - 1

    def __add__(self, other):
        max_len = max(len(self.coeffs), len(other.coeffs))
        result = []
        for i in range(max_len):
            a = self.coeffs[i] if i < len(self.coeffs) else F(0)
            b = other.coeffs[i] if i < len(other.coeffs) else F(0)
            result.append(a + b)
        return Polynomial(result)

    def __sub__(self, other):
        max_len = max(len(self.coeffs), len(other.coeffs))
        result = []
        for i in range(max_len):
            a = self.coeffs[i] if i < len(self.coeffs) else F(0)
            b = other.coeffs[i] if i < len(other.coeffs) else F(0)
            result.append(a - b)
        return Polynomial(result)

    def __mul__(self, other):
        # naive O(n^2) multiplication
        result = [F(0)] * (len(self.coeffs) + len(other.coeffs) - 1)
        for i, a in enumerate(self.coeffs):
            for j, b in enumerate(other.coeffs):
                result[i + j] = result[i + j] + (a * b)
        return Polynomial(result)

    def eval(self, x: F) -> F:
        # Horner's rule
        result = F(0)
        power = F(1)
        for coeff in self.coeffs:
            result = result + coeff * power
            power = power * x
        return result
    

def vanishing_poly(n: int) -> Polynomial:
    """
    Z(x) = (x - 1)(x - 2)...(x - n)
    Vanishes exactly at x = 1, 2, ..., n.
    """
    # Start with the constant polynomial 1
    Z = Polynomial([1])
    for i in range(1, n + 1):
        # (x - i) = -i + 1*x  => coeffs: [ -i, 1 ]
        Z = Z * Polynomial([-i, 1])
    return Z

def lagrange_interpolate(points):
    """
    Given a list of (x_i, y_i) with x_i, y_i in the field,
    return the unique polynomial P(x) such that P(x_i) = y_i for all i.

    points: list of tuples (F, F)
    """
    # P(x) = sum_i y_i * L_i(x)
    # where L_i(x) = product_{j != i} (x - x_j) / (x_i - x_j)

    from field import FieldElement as F  # already imported above, but fine

    P = Polynomial([0])  # start with zero polynomial

    for i, (xi, yi) in enumerate(points):
        # Build L_i(x)
        numerator = Polynomial([1])   # 1
        denominator = F(1)

        for j, (xj, yj) in enumerate(points):
            if i == j:
                continue
            # (x - xj)
            numerator = numerator * Polynomial([-xj.value, 1])
            # (xi - xj)
            denominator = denominator * (xi - xj)

        Li = numerator * Polynomial([yi / denominator])
        P = P + Li

    P._trim()
    return P

def poly_divmod(P: Polynomial, Q: Polynomial):
    """
    Return (quotient, remainder) of P(x) / Q(x) over field F.
    Simple long division.
    """
    # copy to avoid mutation
    dividend = P.coeffs[:]  
    divisor  = Q.coeffs[:]

    # normalize
    Ddeg = len(divisor) - 1
    dde  = divisor[-1]  # leading term of divisor

    # quotient initially zero
    quotient = [F(0)] * (len(dividend) - len(divisor) + 1)

    while len(dividend) >= len(divisor):
        # leading terms
        scale = dividend[-1] / dde
        shift = len(dividend) - len(divisor)

        quotient[shift] = scale

        # subtract (scale * divisor * x^shift) from dividend
        for i in range(len(divisor)):
            dividend[shift + i] = dividend[shift + i] - scale * divisor[i]

        # trim trailing zero
        if dividend[-1] == F(0):
            dividend.pop()

        if len(dividend) == 0:
            dividend = [F(0)]
            break

    return Polynomial(quotient), Polynomial(dividend)


if __name__ == "__main__":
    # p(x) = 3 + 2x + x^2
    P = Polynomial([3, 2, 1])
    x = F(5)

    print("p(x) =", P.eval(x))  # should be 3 + 2*5 + 1*25 = 3 + 10 + 25 = 38 -> F(38)

    # Vanishing polynomial for n = 4
    Z = vanishing_poly(4)
    for i in range(1, 5):
        xi = F(i)
        Zi = Z.eval(xi)
        print(f"Z({i}) =", Zi)

    print("\nTesting division:")
    R, rem = poly_divmod(P, P)  # P/P
    print("P/P quotient:", R)
    print("P/P remainder:", rem)
    