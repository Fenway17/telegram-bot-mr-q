#Start of main.py
from . import event as Event
from . import user as User

class EventManager: 
    def __init__(self):
        print("Initialising Event Manager")
        self.event_hash_map = {} # event -> [user]
        self.all_users = []
    
    def add_event(self, event):
        print("Adding event: " + event.name + " to EventManager")
        if event not in self.event_hash_map:
            self.event_hash_map[event] = []
        else:
            raise self.throw_exception(event, 'exist')
        
    def remove_event(self, event):
        print("Removing event: " + event.name + " from EventManager")
        if event in self.event_hash_map.keys(): # exists in dictionary
            user_list = self.event_hash_map[event]
            for user in user_list:
                user.leave_event(event)
            self.event_hash_map.pop(event)
            
        else:
            raise self.throw_exception(event, 'not exist')
            
    def add_user(self, user):
        print("Adding user: " + user.username + " to EventManager user database")
        found_user = next((x for x in self.all_users if x == user), None)
        if found_user == None:
            self.all_users.append(user)
        else:
            return found_user
        # if user not in self.all_users:
        #     self.all_users.append(user)
        # else:
        #     raise self.throw_exception(user, 'exist')

    ### There won't ever be a need to remove users from the total array of users - Josh/ZF###
    # def remove_user(self, user):
    #     if user in self.users:
    #         self.users.remove(user)
    #     else:
    #         raise self.throw_exception(user, 'not exist')

    def add_user_to_event(self, event, user):
        print("Adding " + user.username + " to " + event.name)
        #user exists
        if user in self.all_users:
            # check if user already in event
            if user in self.event_hash_map[event]:
                #user already in event, throw error
                raise self.throw_exception(user, 'exist' , 'already in event participant/waiting list')
            else:
                #user not in event, add him/her to event
                self.event_hash_map[event].append(user)
                event.add_user_to_event(user)
                user.add_event(event)
                
        else:
            #user does not exist
            raise self.throw_exception(user, 'not exist', '\'{username}\' does not exist'
                .format(username=user.get_username()))
    
    def remove_user_from_event(self, event, user):
        print("Removing " + user.username + " from " + event.name)
        #user exists
        if user in self.all_users:
            # check if user already in event
            if user in self.event_hash_map[event]:
                #user already in event
                # self.eventHashMap[event].remove(user)
                user.leave_event(event)
                event.remove_from_event(user)
            else:
                #user not in event, throw error
                raise self.throw_exception(user, 'not exist', '\'{username}\' not in event, unable to remove'
                .format(username=user.username))
                
        else:
            #user does not exist
            raise self.throw_exception(user, 'not exist', '\'{username}\' does not exist'
                .format(username=user.username))

    def get_user_events(self, user):
        return user.get_events()
        
    def throw_exception(self, cause, reason, comment=''):
        err = ''
        match reason:
            case 'exist':
                err = '{str} already contained'.format(str=type(cause).__name__)
                
            case 'not exist':
                err = '{str} is not contained'.format(str=type(cause).__name__)
        err += ' - ' + comment
        raise ValueError(err)

    def get_event_status(self, event):
        if event not in self.event_hash_map.keys():
            raise self.throw_exception(event, 'not exist', '-debug not in event, unable to get')
        return (event.participants_list, event.waiting_list)

# DEBUGGING TOOLS
    def print_event_users(self, event):
        if event not in self.event_hash_map.keys(): # does not exists in dictionary
            raise self.throw_exception(event, 'not exist', '-debug not in event, unable to get')
        print('==============PARTICIPANT LIST==============') 
        pl = event.participants_list.items
        for user in pl:
            print(user.username)
        print('==============WAITING LIST==============') 
        wl = event.waiting_list.items
        for user in wl:
            print(user.username)

#------------------ DEBUG CODE ------------------

# if __name__ == '__main__':
#     e = EventManager()
#     limit = 15
#     newEvent = Event.Event('first event', '01/01/2021', '00:00', limit)


#     e.add_event(newEvent)
    
#     for i in range(limit + 10): # exceed limit
#         user = User.User(i, str(i), str(i), [])
#         if i == 3:
#             usertodlt = user
#         if i == 22:
#             usertodlt2 = user
#         e.add_user(user)
#         e.add_user_to_event(newEvent, user)
            
#     for event, userList in e.event_hash_map.items():
#         print(event.name, " - partipants queue size", event.participants_list.size())
#         print(event.name, " - waitingList queue size", event.waiting_list.size())
#     print('BEFORE')
#     e.print_event_users(newEvent)
            
#     for event, userList in e.event_hash_map.items():
#         e.remove_user_from_event(event, usertodlt)
#         e.remove_user_from_event(event, usertodlt2)
#         # testuser = User.User(26, str(26), str(26), [])
#         # e.remove_user_from_event(event, testuser)
#     print('\nAFTER')
#     e.print_event_users(newEvent)

#     a = e.get_event_status(newEvent)
    

# Hashmap Key: event Values: array of user
# Hashmap Key: user Values: array of event

# Get EventId -> find eventId in hashmap and get array of userIds -> foreach userId, pop eventId from them
