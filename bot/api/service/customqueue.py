# global strings to use for exception messages 
queue_is_full = "The queue is full. You cannot enqueue any more users"

class CustomQueue:
    def __init__(self, limit = None):
        self.items = []
        self.limit = limit

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        if not self.is_full():
            self.items.append(item)
        else: 
            raise Exception(queue_is_full)

    def dequeue(self):
        return self.items.pop()
    
    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
    
    def dequeue_index(self, index: int):
        return self.items.pop(index)

    def index_of(self, item):
        return self.items.index(item)

    def contains(self, item):
        return item in self.items 

    def is_full(self):
        return self.limit is not None and self.size() == self.limit
    
    def size(self):
        return len(self.items)

    def update_limit(self, newLimit):
        self.limit = newLimit

# ------------------ DEBUG CODE ------------------
if __name__ == '__main__':
    q1 = CustomQueue()
    q2 = CustomQueue(4)
    q3 = CustomQueue(0)

    q1.enqueue('a')
    q1.enqueue('b')
    q1.enqueue('c')
    q1.enqueue('d')
    print(q1.index_of('c'))
    print(q1.size())
    print(q1.is_full())
    print(q1.contains('b'))
    print(q1.is_empty())
    print(q1.dequeue())
    print(q1.dequeue_index(1))
    q1.update_limit(2)
    # q1.enqueue('haha')

    print("-----------------------------------")

    q2.enqueue('a')
    q2.enqueue('b')
    q2.enqueue('c')
    q2.enqueue('d')
    print(q2.dequeue_index(3))
    print(q2.dequeue_index(1))
    q2.enqueue('e')
    q2.enqueue('f')
    print(q2.dequeue())
    q2.enqueue('g')
    # q2.enqueue('haha')

    print("-----------------------------------")

    # q3.enqueue('a')

    

    