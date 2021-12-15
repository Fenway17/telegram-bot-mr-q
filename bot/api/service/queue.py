#Dummy code for services
class Queue:
    def __init__(self, limit = None):
        self.items = []
        self.limit = limit

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        if not self.isFull():
            self.items.insert(0, item)
        else: 
            print("throw queue is full exception")

    def dequeue(self):
        return self.items.pop()
    
    def dequeueIndex(self, index: int):
        return self.items.pop(index)

    def indexOf(self, item):
        return self.items.index(item)

    def contains(self, item):
        return item in self.items 

    def isFull(self):
        return self.limit and self.size() == self.limit
    
    def size(self):
        return len(self.items)

    
    