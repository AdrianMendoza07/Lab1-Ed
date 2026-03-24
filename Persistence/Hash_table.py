from Persistence.Hash_entry import HashEntry
class HashTable:
    def __init__(self, capacity=5000):  
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        self.collisions = 0  
        self.count = 0      

    def hash_function(self, key):
        total = sum(ord(c) for c in key)
        return total % self.capacity

    def insert(self, key, position):
        index = self.hash_function(key)
        bucket = self.buckets[index]
        if bucket:
            self.collisions += 1
        for entry in bucket:
            if entry.key == key:
                entry.position = position
                return
        bucket.append(HashEntry(key, position))
        self.count += 1

    def search(self, key):
        index = self.hash_function(key)
        bucket = self.buckets[index]
        for entry in bucket:
            if entry.key == key:
                return entry.position
        return -1