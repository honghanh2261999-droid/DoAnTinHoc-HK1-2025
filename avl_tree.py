# avl_tree.py
from collections import deque

class AVLNode:
    def __init__(self, key, record=None):
        self.key = key
        self.record = record
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def getHeight(self, node):
        return 0 if node is None else node.height

    def getBalance(self, node):
        return 0 if node is None else self.getHeight(node.left) - self.getHeight(node.right)

    def get_min_value_node(self, node):
        cur = node
        while cur.left is not None:
            cur = cur.left
        return cur

    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def insert(self, root, key, record=None):
        if root is None:
            return AVLNode(key, record)
        if key < root.key:
            root.left = self.insert(root.left, key, record)
        elif key > root.key:
            root.right = self.insert(root.right, key, record)
        else:
            # duplicate key: update record (optional) and return
            root.record = record
            return root

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        balance = self.getBalance(root)

        # LL
        if balance > 1 and key < root.left.key:
            return self.rightRotate(root)
        # RR
        if balance < -1 and key > root.right.key:
            return self.leftRotate(root)
        # LR
        if balance > 1 and key > root.left.key:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        # RL
        if balance < -1 and key < root.right.key:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def delete(self, root, key):
        """Return new root after deletion."""
        if root is None:
            return None

        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # found
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            else:
                temp = self.get_min_value_node(root.right)
                root.key = temp.key
                root.record = temp.record
                root.right = self.delete(root.right, temp.key)

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        balance = self.getBalance(root)

        # LL
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)
        # LR
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        # RR
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)
        # RL
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def search(self, root, key):
        if root is None:
            return None
        if key == root.key:
            return root
        elif key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

    def inorder(self, root, out):
        if root:
            self.inorder(root.left, out)
            out.append(root.record)
            self.inorder(root.right, out)

    def preorder(self, root, out):
        if root:
            out.append(root.record)
            self.preorder(root.left, out)
            self.preorder(root.right, out)

    def postorder(self, root, out):
        if root:
            self.postorder(root.left, out)
            self.postorder(root.right, out)
            out.append(root.record)

    def level_order_pairs(self, root):
        res = []
        if root is None:
            return res
        q = deque([(root,0)])
        while q:
            n,l = q.popleft()
            res.append((n,l))
            if n.left: q.append((n.left,l+1))
            if n.right: q.append((n.right,l+1))
        return res

    def tree_height(self, root):
        pairs = self.level_order_pairs(root)
        if not pairs: return 0
        return max(l for _,l in pairs) + 1

    def count_leaves(self, root):
        if root is None: return 0
        if root.left is None and root.right is None: return 1
        return self.count_leaves(root.left) + self.count_leaves(root.right)

    def get_nodes_at_level(self, root, level):
        res = []
        if root is None: return res
        q = deque([(root, 1)])  # tầng gốc = 1
        while q:
            n, l = q.popleft()
            if l == level: res.append((n.key, n.record))
            if n.left: q.append((n.left, l + 1))
            if n.right: q.append((n.right, l + 1))
        return res

