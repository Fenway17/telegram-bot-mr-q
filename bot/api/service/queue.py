#Dummy code for services
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop()
    
    def dequeueIndex(self, index: int):
        return self.items.pop(index)

    def size(self):
        return len(self.items)
    