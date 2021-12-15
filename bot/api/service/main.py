#Start of main.py
import queue

class EventManager: 
    def __init__(self):
        self.events = []

    def addEvent(self, event):
        self.events.append(event)

    # need to handle exception
    def removeEvent(self, event):
        self.events.remove(event)

    def addUserToEvent(self, event, user):
        event.addToEvent(user)

    def removeUserFromEvent(self, event, user):
        event.removeFromEvent(user)

    


