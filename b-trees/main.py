class Node:
    def __init__(self, is_leaf: bool):
        self.keys = []
        self.children = []
        self.leaf = is_leaf
    
    @property
    def k(self):
        return len(self.keys)
    
    def __repr__(self):
        return f"""Node\nkeys:{self.keys}
\nchildren: {self.children}
\nleaf: {self.leaf}
\nk: {self.k}"""


class BTree:
    def __init__(self, t):
        self.root = Node(is_leaf=True)
        self.t = t
    
    def search_node(self, node, key):
        i = 0
        k = node.k
        while i < k and key > node.keys[i]:
            i += 1
        
        if i < k and key == node.keys[i]:
            return (node, i)
        
        if node.leaf:
            return None
        
        return self.search_node(node.children[i], key)

    def search(self, key):
        return self.search_node(self.root, key)

    def split_child(self, x: Node, i: int): # x is the parent i is the child index to split on
        t = self.t
        y = x.children[i] # this is a node
        mid_key = y.keys[t-1] # -1 because 0 count 0, 1, 2, 3, 4 is 5 keys if t = 3 grab idx 2
        z = Node(is_leaf=y.leaf) # because y and z are siblings
        z.keys = y.keys[t:]
        y.keys = y.keys[:t-1]
        # move the children
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t] # up to t because the middle one isn't removed
        x.children.insert(i + 1, z)
        x.keys.insert(i, mid_key)

    def _insert_nonfull(self, x: Node, key: int):
        if x.leaf:
            i = x.k - 1 # last index
            x.keys.append(None) # make room for loop
            while i >= 0 and key < x.keys[i]:
                x.keys[i+1] = x.keys[i]
                i -= 1
            x.keys[i+1] = key
            return
        else:
            i = x.k - 1 # the last key index
            
            while i >= 0 and key < x.keys[i]:
                i -= 1
            i += 1 # child index

            if x.children[i].k == 2 * self.t - 1:
                self.split_child(x, i)
                
                # after split decide to go left or right of the new key
                if key > x.keys[i]:
                    i += 1

            self._insert_nonfull(x.children[i], key)
        
    def insert(self, key: int):
        r = self.root
        if r.k == 2 * self.t - 1:
            s = Node(is_leaf=False)
            s.children.append(r)
            self.root = s
            self.split_child(s, 0)
            self._insert_nonfull(s, key)
        else:
            self._insert_nonfull(r, key)

    def _traverse_node(self, x: Node, out: list):
        # print(x.keys)
        if x.leaf:
            out.extend(x.keys)
        else:
            for i, key in enumerate(x.keys):
                self._traverse_node(x.children[i], out)
                out.append(key)
            self._traverse_node(x.children[x.k], out)

    def inorder_keys(self):
        out = []
        self._traverse_node(self.root, out)
        return out

    def delete(self, key):
        if self.root.k == 0:
            return # nothing to delete
        
        self._delete_from_node(self.root, key)

        if self.root.k == 0 and not self.root.leaf:
            self.root = self.root.children[0]
    
    def _delete_from_node(self, x: Node, key: int):
        i = 0
        while i < x.k and key > x.keys[i]:
            i += 1
        
        if i < x.k and x.keys[i] == key:
            if x.leaf:
                x.keys.pop(i)
            else:
                self._delete_from_internal(x, i)
            return
        if x.leaf:
            return
        
        child_index = i
        
        if x.children[child_index].k == self.t -1:
            self._fill_child(x, child_index)
            # After _fill_child, structure may have changed.
            # If we merged child with its left sibling, our target might shift:
            if child_index > x.k:
                child_index -= 1
        self._delete_from_node(x.children[child_index], key)

    def _delete_from_internal(self, x: Node, idx: int):
        key = x.keys[idx]
        left = x.children[idx]
        right = x.children[idx+1]

        # left child has >= t keys
        if left.k >= self.t:
            pred = self._get_predecessor(x, idx)
            x.keys[idx] = pred
            self._delete_from_node(left, pred)
            return
        
        if right.k >= self.t:
            succ = self._get_successor(x, idx)
            x.keys[idx] = succ
            self._delete_from_node(right, succ)
            return
        
        # both children have only t-1 keys
        self._merge_children(x, idx)
        self._delete_from_node(left, key)

    def _fill_child(self, x: Node, idx: int):
        # ensure child x.children[idx] has at least t keys before descending
        if idx > 0 and x.children[idx - 1].k >= self.t:
            self._borrow_from_prev(x, idx)
        elif idx < x.k and x.children[idx + 1].k >= self.t:
            self._borrow_from_next(x, idx)
        else:
            if idx < x.k:
                # merge child[idx] with child[idx + 1]
                self._merge_children(x, idx)
            else:
                # idx == x.k, rightmost child: merge with left sibling
                self._merge_children(x, idx - 1)


    def _get_predecessor(self, x: Node, idx: int) -> int:
        cur = x.children[idx] # left child is same as id because lc id: 0 key id: 0 rc id: 1
        while not cur.leaf:
            cur = cur.children[cur.k] # it's k because children is one longer than keys
        return cur.keys[cur.k - 1] # last key in the leaf

    def _get_successor(self, x: Node, idx: int) -> int:
        cur = x.children[idx + 1]
        while not cur.leaf:
            cur = cur.children[0]
        return cur.keys[0]

    def _borrow_from_prev(self, x: Node, idx: int):
        child = x.children[idx]
        sibling = x.children[idx-1] # -1 cause prev

        child.keys.insert(0, x.keys[idx-1])

        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        
        x.keys[idx-1] = sibling.keys.pop()

    def _borrow_from_next(self, x: Node, idx: int):
        child = x.children[idx]
        sibling = x.children[idx+1]

        child.keys.append(x.keys[idx])

        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        
        x.keys[idx] = sibling.keys.pop(0)

    def _merge_children(self, x: Node, idx: int):
        child = x.children[idx] # the left child
        sibling = x.children[idx+1] # the right child

        # bring down separator key
        child.keys.append(x.keys[idx])

        child.keys.extend(sibling.keys)

        if not child.leaf:
            child.children.extend(sibling.children)
        
        x.keys.pop(idx) # remove key from parent
        x.children.pop(idx + 1) # pop sibling



# bt = BTree(3)

# for k in [10, 20, 30, 40, 50, 60, 70, 80, 90, 765, 2]:
#     bt.insert(k)

# print("root:", bt.root.keys)
# for i, child in enumerate(bt.root.children):
#     print(f"child {i}:", child.keys)

# print(bt.inorder_keys())
# bt.delete(765)

# for i, child in enumerate(bt.root.children):
#     print(f"child {i}:", child.keys)

# node = bt.root
# print(bt._get_predecessor(node, 0))  # depending on your root layout
# print(bt._get_successor(node, 0))

bt = BTree(3)
for k in [10, 20, 30, 40, 50, 60, 70, 80, 90, 5, 42, 765, 34, 2, 4, 1]:
    bt.insert(k)

for k in [765, 90, 80, 70, 60, 50, 40, 30, 20, 10, 5, 42, 34, 2, 4, 1]:
    bt.delete(k)
    print(bt.inorder_keys())