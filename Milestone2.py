
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
