#to-do create exceptions

from queue import Queue

class Event:
    id = 0

    def __init__(self, eventId, name, date, time):
        self.eventId = Event.id 
        self.name = name 
        self.date = date
        self.time = time
        self.participants = Queue()
        self.waitingList = Queue()

        Event.id += 1

    def joinEvent(self, user):
        if self.participants.contains(user):
            print("throw already in queue exception")
        elif self.waitingList.contains(user):
            print("throw already in waiting list exception")
        else:
            self.addToEvent(user)

    def addToEvent(self, user):
        try: 
            self.participants.enqueue()
        except queueFullException:
            try: 
                self.waitingList.enqueue()
            except waitingListFullException:
                print("rip the event is full")

    # there is some code repetition here
    def removeFromEvent(self, user):
        if self.participants.contains(user):
            removeFromParticipants(user)
        elif self.waitingList.contains(user):
            removeFromWaitingList(user)

    def removeFromParticipants(self, user): 
        queueIndex = self.participants.indexOf(user)
        if not self.waitingList.isEmpty(): 
            self.participants.dequeueIndex(queueIndex)
            newParticipant = self.waitingList.dequeue()
            self.participants.enqueue(newParticipant)
        else: 
            self.participants.dequeueIndex(queueIndex)

    def removeFromWaitingList(self, user):
        queueIndex = self.waitingList.indexOf(user)
        self.waitingList.dequeueIndex(queueIndex)
    
    

