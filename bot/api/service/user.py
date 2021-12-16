from event import Event

class User:
    def __init__(self, chatId, eventsUserIsIn: dict):
        self.chatId = chatId 
        self.eventsUserIsIn = eventsUserIsIn

    def getEventUserIsIn(self, eventIdx):
        return self.eventsUserIsIn[eventIdx]

    def joinEvent(self, event):
        event.joinEvent(self)

    def leaveEvent(self, event):
        event.removeFromEvent(self)

class Admin(User):
    def __init__(self, chatId, eventsUserIsIn: dict, eventsBeingManaged: dict):
        super().__init__(chatId, eventsUserIsIn)
        self.eventsBeingManaged = eventsBeingManaged

    def createEvent(self, name, date, time):
        newEvent = Event(name, date, time)
        self.eventsBeingManaged[newEvent.getEventId()] = newEvent

    def deleteEvent(self, eventIdx):
        self.eventsBeingManaged.pop(eventIdx)

    def getEventsBeingManaged(self, eventIdx):
        return self.eventsBeingManaged[eventIdx]

    def addToEvent(self, event, user):
        event.joinEvent(user)

    def removeFromEvent(self, event, user):
        event.removeFromEvent(user)
