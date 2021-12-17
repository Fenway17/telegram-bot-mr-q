#Start of main.py
import event as Event
import user as User

class EventManager: 
    def __init__(self):
        self.eventHashMap = {} # event -> [user]
        self.allUsers = []

    def add_event(self, event):
        if event not in self.eventHashMap:
            self.eventHashMap[event] = []
        else:
            raise self.throw_exception(event, 'exist')
        
    def remove_event(self, event):
        if event in self.eventHashMap.keys(): # exists in dictionary
            userList = self.eventHashMap[event]
            for user in userList:
                user.leave_event(event)
            self.eventHashMap.pop(event)
            
        else:
            raise self.throw_exception(event, 'not exist')
            
    def add_user(self, user):
        if user not in self.allUsers:
            self.allUsers.append(user)
        else:
            raise self.throw_exception(user, 'exist')

    ### There won't ever be a need to remove users from the total array of users - Josh/ZF###
    # def remove_user(self, user):
    #     if user in self.users:
    #         self.users.remove(user)
    #     else:
    #         raise self.throw_exception(user, 'not exist')

    def add_user_to_event(self, event, user):
        
        #user exists
        if user in self.allUsers:
            # check if user already in event
            if user in self.eventHashMap[event]:
                #user already in event, throw error
                raise self.throw_exception(user, 'exist' , 'already in event participant/waiting list')
            else:
                #user not in event, add him/her to event
                self.eventHashMap[event].append(user)
                event.add_user_to_event(user)
                user.add_event(event)
                
        else:
            #user does not exist
            raise self.throw_exception(user, 'not exist', '\'{username}\' does not exist'
                .format(username=user.get_username()))


    def remove_user_from_event(self, event, user):
        #user exists
        if user in self.allUsers:
            # check if user already in event
            if user in self.eventHashMap[event]:
                #user already in event
                self.eventHashMap[event].pop(user)
                user.leave_event(event)
            else:
                #user not in event, throw error
                raise self.throw_exception(user, 'not exist', '\'{username}\' not in event, unable to remove'
                .format(username=user.get_username()))
                
        else:
            #user does not exist
            raise self.throw_exception(user, 'not exist', '\'{username}\' does not exist'
                .format(username=user.get_username()))

    def throw_exception(self, cause, reason, comment=''):
        err = ''
        match reason:
            case 'exist':
                err = '{str} already contained'.format(str=type(cause).__name__)
                
            case 'not exist':
                err = '{str} is not contained'.format(str=type(cause).__name__)
        err += ' - ' + comment
        raise ValueError(err)

#------------------ DEBUG CODE ------------------

if __name__ == '__main__':
    e = EventManager()
    limit = 15
    newEvent = Event.Event('first event', '01/01/2021', '00:00', limit)


    e.add_event(newEvent)
    
    for i in range(limit + 10): # exceed limit
        user = User.User(i, str(i), str(i), [])
        e.add_user(user)
        e.add_user_to_event(newEvent, user)
            
    for event, userList in e.eventHashMap.items():
        print(event.name, " - partipants queue size", event.participants.size())
        print(event.name, " - waitingList queue size", event.waitingList.size())
    

# Hashmap Key: event Values: array of user
# Hashmap Key: user Values: array of event

# Get EventId -> find eventId in hashmap and get array of userIds -> foreach userId, pop eventId from them
