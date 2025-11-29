import hashlib
from math import ceil, log2

def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def next_pow2(n: int) -> int:
    return 1 if n <= 1 else 1 << (n-1).bit_length()

def build_zero_hashes(height: int) -> list[bytes]:
    """ZERO[h] is the hash of an empty subtree of height h (leaves at h=0)."""
    zero = [sha256(b"")]
    for _ in range(height):
        zero.append(sha256(zero[-1] + zero[-1])) # -1 gets you the last value in the list
    return zero

zero_hash_list = build_zero_hashes(4)

class MerkleTree:
    def __init__(self, leaves: list[bytes]):
        self.n = len(leaves)
        if self.n == 0:
            self.height = 0
            self.levels = [[sha256(b"")]]
            self.zero = [sha256(b"")]
            return
        elif self.n == 1:
            self.height = 0
            self.levels = [[sha256(leaves[0])]]
            self.zero = [sha256(b"")]
            return

        pow_two = next_pow2(self.n)
        self.height = (pow_two.bit_length() - 1)
        self.zero = build_zero_hashes(self.height)

        # Level 0 hash leaves and pad with zero hashes
        level0 = [sha256(x) for x in leaves] + [self.zero[0]] * (pow_two - self.n)

        levels = [level0]
        cur = level0
        for _ in range(0, len(cur), 2):
            nxt = [sha256(cur[i] + cur[i+1]) for i in range(0, len(cur), 2)]
            levels.append(nxt)
            cur = nxt
        self.levels = levels

    def root(self) -> bytes:
        return self.levels[-1][0]

    def proof(self, index: int) -> list[tuple[bytes, str]]:
        if not (0 <= index < self.n):
            raise IndexError("leaf index out of range")
        
        proof: list[tuple[bytes, str]] = []
        i = index
        for h in range(self.height):
            sib = i ^ 1 # XOR with 1 flips the farthest right bit which moves by 1 up if even, and down by 1 if odd
            # 0011 = 3 | 0011 ^ 0001 = 0010 = 2
            sibling = self.levels[h][sib]
            direction = 'R' if (i % 2 == 0) else 'L'
            proof.append((sibling, direction))
            i >>= 1 # shift right by 1 bit equivalent to integer division by 2 gets the right parent i in that level
        return proof

    def update(self, index: int, new_leaf: bytes) -> None:
        if not (0 <= index < self.n):
            raise IndexError("leaf index out of range")
        
        # set new leaf hash
        self.levels[0][index] = sha256(new_leaf)
        
        # climb up and recompute
        i = index
        for h in range(self.height):
            parent_idx = i >> 1
            left_idx = i & ~1 # gets even sibling ~1 Bitwise not of 1 0001 -> 1110 then AND takes 0101 = 5 and 1110 -> 0100 = 4
            right_idx = left_idx + 1
            left_hash = self.levels[h][left_idx]
            right_hash = self.levels[h][right_idx]
            self.levels[h+1][parent_idx] = sha256(left_hash + right_hash)
            i = parent_idx

def verify(leaf: bytes, proof: list[tuple[bytes, str]], root: bytes) -> bool:
    accum = sha256(leaf)
    for sibling, direction in proof:
        if direction == 'R':
            accum = sha256(accum + sibling)
        elif direction == 'L':
            accum = sha256(sibling + accum)
        else:
            return False
    return accum == root

def verify_indexed(leaf: bytes, proof: list[bytes], index: int, root: bytes) -> bool:
    accum = sha256(leaf)
    for h, sib in enumerate(proof):
        bit = (index >> h) & 1
        accum = sha256(sib + accum) if bit else sha256(accum + sib)
    return accum == root

t1 = MerkleTree([b"a", b"b", b"c"])
t2 = MerkleTree([b"a", b"b", b"d"])
assert t1.root() != t2.root()
print(t1.root().hex(), t2.root().hex())

# 2) proofs verify for each real leaf
leaves = [b"a", b"b", b"c"]
t = MerkleTree(leaves)
for i, leaf in enumerate(leaves):
    p = t.proof(i)
    assert verify(leaf, p, t.root())

# 3) tamper detection
p_bad = list(t.proof(0))
p_bad[0] = (sha256(b"not-the-sibling"), p_bad[0][1])
assert not verify(leaves[0], p_bad, t.root())

# 4) updates change root and still verify
root_before = t.root()
t.update(1, b"B")
root_after = t.root()
assert root_after != root_before
assert verify(b"B", t.proof(1), root_after)

# 5) edge cases: 0 or 1 leaf
t_empty = MerkleTree([])
t_one = MerkleTree([b"solo"])
assert t_empty.root() == sha256(b"")
assert verify(b"solo", t_one.proof(0), t_one.root())

class MerkleImplicit:
    def __init__(self, leaves: list[bytes]):
        self.leaves = leaves # store raw leaves
        self.n = len(leaves)
        cap = next_pow2(max(1, self.n)) # at least 1
        self.height = (cap.bit_length() - 1)
        self.zero = build_zero_hashes(self.height)
        self._cache: dict[tuple[int, int], bytes] = {}

    def _hash_leaf(self, i: int) -> bytes:
        if i >= self.n:
            return self.zero[0]
        return sha256(self.leaves[i])

    def node_hash(self, start: int, h: int) -> bytes:
        key = (start, h)
        if key in self._cache:
            return self._cache[key]

        if start >= self.n:
            return self.zero[h]
        elif h == 0:
            return self._hash_leaf(start)
        else:
            half = 1 << (h-1)
            L = self.node_hash(start, h-1)
            R = self.node_hash(start + half, h-1)
            out = sha256(L + R)

        self._cache[key] = out
        return out

    def root(self) -> bytes:
        return self.node_hash(0, self.height)

    def update(self, i: int, new_leaf: bytes) -> None:
        if not (0 <= i < self.n):
            raise IndexError("leaf index out of range")
        self.leaves[i] = new_leaf
        self._cache.clear()

    def append(self, new_leaf: bytes) -> None:
        self.leaves.append(new_leaf)
        self.n += 1
        
        old_cap = 1 << self.height # pow 2
        if self.n > old_cap:
            new_cap = next_pow2(self.n)
            new_height = new_cap.bit_length() - 1 # bit length of 4 has 3 levels because first level is id 0
            while len(self.zero) <= new_height:
                z = self.zero[-1]
                self.zero.append(sha256(z + z))
            self.height = new_height
        self._cache.clear()

    def proof(self, i: int) -> list[tuple[bytes, str]]:
        if not (0 <= i < self.n):
            raise IndexError("leaf index out of range")
        proof = []
        for h in range(self.height):
            width = 1 << h
            block = (i // (2 * width)) * (2 * width)
            left_start = block
            right_start = block + width
            if i < right_start:
                # leaf is in left half; sibling is right half
                sib_start, direction = right_start, 'R'
            else:
                sib_start, direction = left_start, 'L'
            proof.append((self.node_hash(sib_start, h), direction))
        return proof
    
    def proof_indexed(self, index: int) -> list[bytes]:
        if not (0 <= index < self.n):
            raise IndexError("leaf index out of range")
        proof: list[bytes] = []
        for h in range(self.height):
            width = 1 << h
            parent_block = (index >> (h + 1)) << (h + 1)   # start of the 2^(h+1)-sized block
            bit = (index >> h) & 1 # 0101 & 0001 = 1 1010 & 0001 = 0
            sib_start = parent_block + (width if bit == 0 else 0)              # flip left/right half
            proof.append(self.node_hash(sib_start, h))
        return proof
    
    def recompute_root_with(self, index: int, leaf: bytes) -> bytes:
        acc = sha256(leaf)
        for h in range(self.height):
            width  = 1 << h
            parent = (index >> (h + 1)) << (h + 1)  # start of the 2^(h+1) block
            bit = (index >> h) & 1               # 0=left child, 1=right child

            sib_start = parent + (width if bit == 0 else 0)

            sib_hash = self.node_hash(sib_start, h)
            acc = sha256(sib_hash + acc) if bit else sha256(acc + sib_hash)
        return acc

m = MerkleImplicit([b'a', b'b', b'c'])
print(m.root().hex())
print(m.proof(1))

# implicit
mi = MerkleImplicit([b'a', b'b', b'c'])
assert verify(b'b', mi.proof(1), mi.root())

# cross-check with explicit tree
mt = MerkleTree([b'a', b'b', b'c'])
assert mi.root() == mt.root()
for i, leaf in enumerate([b'a', b'b', b'c']):
    assert verify(leaf, mi.proof(i), mi.root())

old_root = mi.root()
mi.update(1, b'B')
new_root = mi.root()
assert new_root != old_root
assert verify(b'B', mi.proof(1), new_root)

r1 = mi.root()
mi.append(b'd')
mi.append(b'i')             # crosses from capacity 4? (n=3→4) height stays same; still fine
r2 = mi.root()
assert r2 != r1
assert verify(b'd', mi.proof(3), r2)

mi2 = MerkleImplicit([b'a', b'b', b'c'])
r2 = mi2.root()
for i, leaf in enumerate(mi2.leaves):
    p = mi2.proof_indexed(i)
    assert verify_indexed(leaf, p, i, r2)

r0 = mi2.root()

# Preview the root if we changed index 1 from b'b' -> b'B' (without mutating the tree)
r_preview = mi2.recompute_root_with(1, b'B')

# Now actually apply the update and compare
mi2.update(1, b'B')
r1 = mi2.root()

assert r_preview == r1   # should be true