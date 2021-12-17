from customqueue import CustomQueue
# FOR DEBUGGING
from user import * 

# global strings to use for exception messages 
already_in_participants = "The user you are trying to add is already in the participants list"
already_in_waiting_list = "The user you are trying to add is already in the waiting list"
not_in_event = "The user you are trying to remove is not in this event"
event_is_full = "The event is full. You cannot add the user to this event."

class Event:
    id = 0

    def __init__(self, name, date, time, participantsLimit, waitingListLimit = None):
        self.eventId = Event.id #should this be changed to name + date/time?
        self.name = name 
        self.date = date
        self.time = time
        self.participants_list = CustomQueue(participantsLimit)
        self.waiting_list = CustomQueue(waitingListLimit)

        Event.id += 1

    def get_event_id(self):
        return self.eventId

    # Add user to a new event
    def add_user_to_event(self, user):
        if self.participants_list.contains(user):
            raise Exception(already_in_participants)
        elif self.waiting_list.contains(user):
            raise Exception(already_in_waiting_list)
        else:
            try: 
                self.participants_list.enqueue(user)
            except:
                try: 
                    self.waiting_list.enqueue(user)
                except:
                    raise Exception(event_is_full)

    # Remove user from an event
    def remove_from_event(self, user):
        if self.participants_list.contains(user):
            self.remove_from_participants_list(user)
        elif self.waiting_list.contains(user):
            self.remove_from_waiting_list(user)
        else: 
            raise Exception(not_in_event)

    def remove_from_participants_list(self, user): 
        queueIndex = self.participants_list.indexOf(user)
        if not self.waiting_list.isEmpty(): 
            self.participants_list.dequeueIndex(queueIndex)
            newParticipant = self.waiting_list.dequeue()
            self.participants_list.enqueue(newParticipant)
        else: 
            self.participants_list.dequeueIndex(queueIndex)

    def remove_from_waiting_list(self, user):
        queueIndex = self.waiting_list.indexOf(user)
        self.waiting_list.dequeueIndex(queueIndex)

    def updateParticipantsLimit(self, newLimit):
        self.participants_list.updateLimit(newLimit)

    def updateWaitingListLimit(self, newLimit):
        self.waiting_list.updateLimit(newLimit)

# ------------------ DEBUG CODE ------------------
# if __name__ == '__main__':
#     # e1 = Event("bball", "20 dec", "11am", 2, 0)
#     # e2 = Event("soccer", "21 dec", "12am", 3, 3)
#     # u1 = User("jojo", "j0j0")
#     # u2 = User("zaza", "z@z@")
#     # u3 = User("kuku", "kUkU")

#     # print(e1.get_event_id())
#     # print(e2.get_event_id())
#     # e1.add_user_to_event(u1)
#     # e1.add_user_to_event(u2)
#     # e1.add_user_to_event(u3)
    

