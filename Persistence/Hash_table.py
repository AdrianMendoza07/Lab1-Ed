from Persistence.Hash_entry import HashEntry
class HashTable:
    def __init__(self, capacity=10):
        self.capacity=capacity
        self.buckets = []
        for i in range(capacity):
            self.buckets.append([])

    def hash_function(self, key):
        total=0
        for c in key:
            total = total + ord(c)
        return total % self.capacity
    
    def insert(self, key, position):
        index = self.hash_function(key)
        bucket = self.buckets[index]
        for entry in bucket:
            if entry.key == key:
                entry.position = position
                return
        bucket.append(HashEntry(key, position))
        
    def search(self, key):
        index = self.hash_function(key)
        bucket = self.buckets[index]
        for entry in bucket:
            if entry.key == key:
                return entry.position
        return -1