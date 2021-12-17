from event import Event

class User:
    def __init__(self, userId, username, chatId, events = []):
        self.userId = userId
        self.username = username 
        self.chatId = chatId 
        self.events = events

    def get_user_id(self):
        return self.userId

    def get_username(self):
        return self.username

    def get_events(self):
        return self.events

    def add_event(self, event):
        self.events.append(event) # to-do discuss changes here

    def leave_event(self, event):
        self.events.remove(event) # to-do discuss changes here

class Admin(User):
    def __init__(self, chatId, events: dict, eventsBeingManaged: dict):
        super().__init__(chatId, events)
        self.eventsBeingManaged = eventsBeingManaged

    def create_event(self, name, date, time, participantsLimit, waitingListLimit = None):
        newEvent = Event(name, date, time, participantsLimit, waitingListLimit)
        self.eventsBeingManaged[newEvent.get_event_id()] = newEvent

    def delete_event(self, eventId):
        self.eventsBeingManaged.pop(eventId)

    def get_managed_event(self, eventId):
        return self.eventsBeingManaged[eventId]

    def add_user_to_event(self, event, user):
        event.add_user_to_event(user)

    def remove_user_from_event(self, event, user):
        event.remove_from_event(user)
