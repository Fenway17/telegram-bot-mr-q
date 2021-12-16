#Start of main.py
import event as Event
import user as User

class EventManager: 
    def __init__(self):
        self.events = []
        self.users = []

    def add_event(self, event):
        if not self.events or event.get_event_id() not in self.events:
            self.events.append(event)
        else:
            raise self.throw_exception(event, 'exist')
        
    def remove_event(self, event):
        if event in self.events:
            self.events.remove(event)
        else:
            raise self.throw_exception(event, 'not exist')

    def add_user(self, user):
        if not self.users or user.get_username() not in self.users:
            self.users.append(user)
        else:
            raise self.throw_exception(user, 'exist')
            
    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)
        else:
            raise self.throw_exception(user, 'not exist')

    def add_user_to_event(self, event, user):
        if user in self.users:
            self.events[event.get_event_id()].add_user_to_event(user)
            for idx, u in enumerate(self.users):
                if u.get_username() == user.get_username():
                    newUser = u
                    newUser.add_event(event)
                    self.users[idx] = newUser
                    break
        else:
            raise self.throw_exception(user, 'not exist', 'Add \'{username}\' to list of users by invoking \'add_user()\''
                .format(username=user.get_username()))


    def remove_user_from_event(self, event, user):
        event.removeFromEvent(user)

    def throw_exception(self, cause, reason, comment=''):
        err = ''
        match reason:
            case 'exist':
                err = '{str} already contained in the list of {str}s'.format(str=type(cause).__name__)
                
            case 'not exist':
                err = '{str} is not contained in the list of {str}s'.format(str=type(cause).__name__)
        err += ' - ' + comment
        raise ValueError(err)

#------------------ DEBUG CODE ------------------

# if __name__ == '__main__':
#     e = EventManager()
#     newEvent = Event.Event('first event', '01/01/2021', '00:00')
#     newUser1 = User.User('joshua', 1, [])
#     newUser2 = User.User('Keith', 2, [])
#     e.add_event(newEvent)
#     e.add_user(newUser1)
#     e.add_user(newUser2)
#     e.add_user_to_event(newEvent, newUser1)
#     e.add_user_to_event(newEvent, newUser2)
#     newsEvent = Event.Event('second event', '01/01/2021', '00:00')
#     newUser3 = User.User('george', 2, [])
#     e.add_event(newsEvent)
#     e.add_user(newUser3)
#     e.add_user_to_event(newsEvent, newUser3)
#     e.remove_user(newUser3)
    
#     for event in e.events:
#         print(event.name, " - queue size", event.participants.size())

#     e.remove_event(newEvent)

#     print('-----After event is removed-----')

#     for event in e.events:
#         print(event.name, " - queue size", event.participants.size())
    

