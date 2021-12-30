import sys
from customqueue import CustomQueue

# global strings to use for exception messages 
already_in_participants = "The user you are trying to add is already in the participants list"
already_in_waiting_list = "The user you are trying to add is already in the waiting list"
not_in_event = "The user you are trying to remove is not in this event"
event_is_full = "The event is full. You cannot add the user to this event."

class Event:
	id = 0

	def __init__(self, name, datetime, participants_limit=sys.maxsize, waiting_list_limit=0):
		print("Init event class")
		self.eventId = Event.id
		self.name = name 
		self.datetime = datetime
		self.participants_limit = participants_limit # added this for convenience - yr
		self.waiting_list_limit = waiting_list_limit # added this for from_dict function - jeremy
		self.participants_list = CustomQueue(participants_limit)
		self.waiting_list = CustomQueue(waiting_list_limit)
		
		Event.id += 1

	def get_event_id(self):
		return self.event_id

	def print_participant_list(self):
		for user in self.participants_list.items:
			print("###Participants List for " + self.name + "###")
			print("User: " + user.username)

	def get_waiting_list(self):
		for user in self.waiting_list.items:
			print("###Waiting List for " + self.name + "###")
			print("User: " + user.username)

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
			self.participants_list.remove(user)
			if not self.waiting_list.is_empty():
				new_participant_user = self.waiting_list.dequeue()
				print("pop " + new_participant_user.username + " from waiting list")
				print("add " + new_participant_user.username + " into participant list")
				self.participants_list.enqueue(new_participant_user) 
		elif self.waiting_list.contains(user):
			self.waiting_list.remove(user)
		else: 
			raise Exception(not_in_event)

	def update_participants_limit(self, newLimit):
		self.participants_list.update_limit(newLimit)

	def update_waiting_list_limit(self, newLimit):
		self.waiting_list.update_limit(newLimit)

	@staticmethod
	def from_dict(source):
		# [START_EXCLUDE]
		event = Event(source[u'name'], 
			source[u'datetime'], 
			source[u'participants_limit'],
			source[u'waiting_list_limit'])

		if u'eventId' in source: 
			event.eventId = source[u'eventId']

		if u'name' in source:
			event.name = source[u'name']

		if u'datetime' in source:
			event.datetime = source[u'datetime']
		
		if u'participants_limit' in source:
			event.participants_limit = source[u'participants_limit']

		if u'waiting_list_limit' in source:
			event.waiting_list_limit = source[u'waiting_list_limit']

		if u'participants_list' in source:
			event.participants_list = CustomQueue.from_dict(source[u'participants_list'])
			
		if u'waiting_list' in source:
			event.waiting_list = CustomQueue.from_dict(source[u'waiting_list'])

		return event
		# [END_EXCLUDE]

	def to_dict(self):
		# [START_EXCLUDE]
		dest = {
			u'eventId': self.eventId,
			u'name': self.name,
			u'datetime': self.datetime,
			u'participants_limit': self.participants_limit,
			u'waiting_list_limit': self.waiting_list_limit,
			u'participants_list': self.participants_list.to_dict(),
			u'waiting_list': self.waiting_list.to_dict()
		}

		if self.eventId:
			dest[u'eventId'] = self.eventId

		if self.name:
			dest[u'name'] = self.name

		if self.datetime:
			dest[u'datetime'] = self.datetime

		if self.participants_limit:
			dest[u'participants_limit'] = self.participants_limit

		if self.waiting_list_limit:
			dest[u'waiting_list_limit'] = self.waiting_list_limit

		if self.participants_list:
			dest[u'participants_list'] = self.participants_list.to_dict()

		if self.waiting_list:
			dest[u'waiting_list'] = self.waiting_list.to_dict()

		return dest
		# [END_EXCLUDE]

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
	

