MODULUS = 101

class FieldElement:
    def __init__(self, value: int):
        self.value = value % MODULUS
    
    def __repr__(self):
        return f"F({self.value})"
    
    def __eq__(self, other):
        if isinstance(other, FieldElement):
            return self.value == other.value
        return self.value == (other % MODULUS)
    
    def __add__(self, other):
        if isinstance(other, FieldElement):
            other = other.value
        return FieldElement(self.value + other)
    
    def __sub__(self, other):
        if isinstance(other, FieldElement):
            other = other.value
        return FieldElement(self.value - other)
    
    def __mul__(self, other):
        if isinstance(other, FieldElement):
            other = other.value
        return FieldElement(self.value * other)
    
    def __neg__(self):
        return FieldElement(-self.value)
    
    def __pow__(self, exponent: int):
        return FieldElement(pow(self.value, exponent, MODULUS))
    
    def inv(self):
        if self.value == 0:
            raise ZeroDivisionError("No inverse for 0 in a field.")
        # Fermat's little theorem: a^(p-2) ≡ a^{-1} (mod p)
        return self ** (MODULUS - 2)
    
    def __truediv__(self, other):
        if isinstance(other, FieldElement):
            other = other.value
        other_fe = FieldElement(other)
        return self * other_fe.inv()
    

if __name__ == "__main__":
    a = FieldElement(3)
    b = FieldElement(7)

    print("a =", a)           # F(3)
    print("b =", b)           # F(7)
    print("a + b =", a + b)   # F(10)
    print("a * b =", a * b)   # F(21)

    # test wrap-around
    c = FieldElement(100)
    print("c + 5 =", c + 5)   # should wrap: 100 + 5 = 105 -> 105 mod 101 = 4 => F(4)

    # test inverse
    inv_a = a.inv()
    print("a^{-1} =", inv_a)
    print("a * a^{-1} =", a * inv_a)  # should be F(1)

    # test division
    print("b / a =", b / a)   # check it runs and gives some F(x)