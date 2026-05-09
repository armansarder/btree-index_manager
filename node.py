
BLOCK_SIZE = 512
MAX_KEYS = 19
MAX_CHILDREN = 20


class Node:
    def __init__(self, block_id=0, parent_id=0, num_keys=0, keys=None, values=None, children=None):
        self.block_id = block_id
        self.parent_id = parent_id
        self.num_keys = num_keys

        if keys is None:
            self.keys = [0] * MAX_KEYS
        else:
            self.keys = keys

        if values is None:
            self.values = [0] * MAX_KEYS
        else:
            self.values = values

        if children is None:
            self.children = [0] * MAX_CHILDREN
        else:
            self.children = children

    def to_bytes(self):
        data = b""

        data += self.block_id.to_bytes(8, "big")
        data += self.parent_id.to_bytes(8, "big")
        data += self.num_keys.to_bytes(8, "big")

        for key in self.keys:
            data += key.to_bytes(8, "big")

        for value in self.values:
            data += value.to_bytes(8, "big")

        for child in self.children:
            data += child.to_bytes(8, "big")

        remaining_bytes = BLOCK_SIZE - len(data)
        data += b"\x00" * remaining_bytes

        return data

    @staticmethod
    def from_bytes(data):
        block_id = int.from_bytes(data[0:8], "big")
        parent_id = int.from_bytes(data[8:16], "big")
        num_keys = int.from_bytes(data[16:24], "big")

        keys = []
        start = 24
        for i in range(MAX_KEYS):
            key = int.from_bytes(data[start:start + 8], "big")
            keys.append(key)
            start += 8

        values = []
        for i in range(MAX_KEYS):
            value = int.from_bytes(data[start:start + 8], "big")
            values.append(value)
            start += 8

        children = []
        for i in range(MAX_CHILDREN):
            child = int.from_bytes(data[start:start + 8], "big")
            children.append(child)
            start += 8

        return Node(block_id, parent_id, num_keys, keys, values, children)

    def is_leaf(self):
        for child in self.children:
            if child != 0:
                return False
        return True

    def is_full(self):
        return self.num_keys == MAX_KEYS

    def find_key_index(self, key):
        index = 0

        while index < self.num_keys and self.keys[index] < key:
            index += 1

        return index

    def contains_key(self, key):
        index = self.find_key_index(key)

        if index < self.num_keys and self.keys[index] == key:
            return True

        return False