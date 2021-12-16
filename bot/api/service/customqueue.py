class CustomQueue:
    def __init__(self, limit = None):
        self.items = []
        self.limit = limit

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        if not self.is_full():
            self.items.insert(0, item)
        else: 
            print("throw queue is full exception")

    def dequeue(self):
        return self.items.pop()
    
    def dequeue_index(self, index: int):
        return self.items.pop(index)

    def index_of(self, item):
        return self.items.index(item)

    def contains(self, item):
        return item in self.items 

    def is_full(self):
        return self.limit and self.size() == self.limit
    
    def size(self):
        return len(self.items)

    def update_limit(self, newLimit):
        self.limit = newLimit

    
    