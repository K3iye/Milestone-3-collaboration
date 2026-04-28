
"""
Enrollment record created by Ryan
"""
class EnrollmentRecord:
    def __init__(self, student, enroll_date):
        self.student = student
        self.enroll_date = enroll_date
        
    def __repr__(self):
        return f"Enrollment Record: {self.student.student_id}, {self.enroll_date}"
    

def binary_search_helper(records: list[EnrollmentRecord], target_id: str):
    return recursive_binary_search(records, target_id, 0, len(records) - 1)

def recursive_binary_search(records: list[EnrollmentRecord], target_id: str, low, high):
    if low > high:
        return -1

    mid = (low + high) // 2
    mid_item = records[mid].student.student_id
    
    if mid_item == target_id:
        return mid
    elif target_id < mid_item:
        return recursive_binary_search(records, target_id, low, mid - 1)
    else:
        return recursive_binary_search(records, target_id, mid + 1, high)

    
"""
    Linked list created by Johnny
"""

class Node:
    def __init__(self, data, next = None):
        self.data = data
        self.next = next
    
    def __repr__(self):
        return f"Node({self.data})"
    
class LinkedQueue:
    def __init__(self): 
        self.head = None
        self.tail = None
        self._size = 0
        
    def enqueue(self,item):
        if self.head is None:
            self.head = Node(item)
            self.tail = self.head
        else:
            self.tail.next = Node(item)
            self.tail = self.tail.next
        self._size += 1
    
    def dequeue(self):
        if self.head is None:
            raise ValueError("Queue is empty")
        item = self.head.data
        
        if self.head.next is None:
            self.head = None
            self.tail = None
            self._size -= 1
            return item
        self.head = self.head.next
        self._size -= 1
        return item
    
    def is_empty(self):
        return self.head is None
    
    def __len__(self):
        return self._size

# Class for key value pairs
class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return str(self.key) + ":" + str(self.value)

# Stores key-value pairs in a list
class ListMapping:
    def __init__(self):
        self._entries = []
    
    def _entry(self, key):
        for e in self._entries:
            if e.key == key:
                return e
        return None
    
    def put(self, key, value):
        e = self._entry(key)
        if e is not None:
            e.value = value
        else:
            self._entries.append(Entry(key, value))

    def get(self, key):
        e = self._entry(key)
        if e is not None:
            return e.value
        else:
            return ValueError
    
    def __len__(self):
        return len(self._entries)
    
    def __str__(self):
        return str([str(e) for e in self._entries])

    def __setitem__(self, key, value):
        self.put(key, value)
    
    def __getitem__(self, key):
        return self.get(key)
    
    def __contains__(self, key):
        e = self._entry(key)
        if e is not None:
            return True
        else:
            return False
    
    def items(self):
        return ((e.key, e.value) for e in self._entries)
    
# Hash Map
class HashMapping:
    def __init__(self, size = 2):
        self._size = size
        self._buckets = [ListMapping() for i in range(self._size)]
        self._length = 0
    
    def _bucket(self, key):
        return self._buckets[hash(key) % self._size]
    
    def rehashing(self):
        print("I need more space")
        old_buckets = self._buckets
        self._size *= 2
        self._buckets = [ListMapping() for i in range(self._size)]

        for bucket in old_buckets:
            for key, value in bucket.items():
                m = self._bucket(key)
                m[key] = value
        
    def __len__(self):
        return self._length
    
    def __setitem__(self, key, value):
        m = self._bucket(key)
        if key not in m:
            self._length += 1
        m[key] = value

        if self._length / self._size >= 0.8:
            self.rehashing()
    
    def __getitem__(self, key):
        m = self._bucket(key)
        return m[key]

    def __repr__(self):
        output = "Hash Table Structure:\n"
        for i in range(len(self._buckets)):
            output += f"Bucket {i}: {self._buckets[i]}\n"
        return output