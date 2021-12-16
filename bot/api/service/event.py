#to-do create exceptions

from customqueue import CustomQueue

class Event:
    id = 0

    def __init__(self, name, date, time):
        self.eventId = Event.id #should this be changed to name + date/time?
        self.name = name 
        self.date = date
        self.time = time
        self.participants = CustomQueue()
        self.waitingList = CustomQueue()

        Event.id += 1

    def get_event_id(self):
        return self.eventId

# Add user to a new event
    def add_user_to_event(self, user):
        if self.participants.contains(user):
            print("throw already in queue exception")
        elif self.waitingList.contains(user):
            print("throw already in waiting list exception")
        else:
            try: 
                self.participants.enqueue(user)
            except queueFullException:
                try: 
                    self.waitingList.enqueue(user)
                except waitingListFullException:
                    print("rip the event is full")

# Remove user from an event

    # there is some code repetition here
    def remove_from_event(self, user):
        if self.participants.contains(user):
            self.remove_from_participant_queue(user)
        elif self.waitingList.contains(user):
            self.removeFromWaitingList(user)

    def remove_from_participant_queue(self, user): 
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

    def updateParticipantsLimit(self, newLimit):
        self.participants.updateLimit(newLimit)

    def updateWaitingListLimit(self, newLimit):
        self.waitingList.updateLimit(newLimit)

    

