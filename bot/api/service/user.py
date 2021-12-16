from event import Event

class User:
    def __init__(self, username, chatId, events: list):
        self.username = username 
        self.chatId = chatId 
        self.events = []

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

    def create_event(self, name, date, time):
        newEvent = Event(name, date, time)
        self.eventsBeingManaged[newEvent.get_event_id()] = newEvent

    def delete_event(self, eventId):
        self.eventsBeingManaged.pop(eventId)

    def get_managed_events(self, eventId):
        return self.eventsBeingManaged[eventId]

    def add_user_to_event(self, event, user):
        event.joinEvent(user)

    def remove_user_from_event(self, event, user):
        event.remove_from_event(user)
