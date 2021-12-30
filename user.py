from event import Event

class User:
	def __init__(self, user_id, fullname, username, chat_id=0, events = []):
		print("Init user class")
		self.user_id = user_id
		self.fullname = fullname
		self.username = username 
		self.chat_id = chat_id 
		self.events = events # might wanna check this

	def get_user_id(self):
		return self.user_id

	def get_username(self):
		return self.username

	def get_events(self):
		return self.events
	
	def get_fullname(self):
		return self.fullname

	def add_event(self, event):
		self.events.append(event) # to-do discuss changes here

	def leave_event(self, event):
		self.events.remove(event) # to-do discuss changes here

	@staticmethod
	def from_dict(source):
		# [START_EXCLUDE]
		user = User(source[u'user_id'], 
			source[u'fullname'], 
			source[u'username'], 
			source[u'chat_id'], 
			source[u'events'])

		if u'user_id' in source:
			user.user_id = source[u'user_id']

		if u'fullname' in source:
			user.fullname = source[u'fullname']

		if u'username' in source:
			user.username = source[u'username']
		
		if u'chat_id' in source:
			user.chat_id = source[u'chat_id']

		if u'events' in source:
			user.events = source[u'events']

		return user
		# [END_EXCLUDE]

	def to_dict(self):
		# [START_EXCLUDE]
		dest = {
			u'user_id': self.user_id,
			u'fullname': self.fullname,
			u'username': self.username,
			u'chat_id': self.chat_id,
			u'events': self.events
		}

		if self.user_id:
			dest[u'user_id'] = self.user_id

		if self.fullname:
			dest[u'fullname'] = self.fullname

		if self.username:
			dest[u'username'] = self.username

		if self.chat_id:
			dest[u'chat_id'] = self.chat_id

		if self.events:
			dest[u'events'] = self.events

		return dest
		# [END_EXCLUDE]

class Admin(User):
	def __init__(self, user_id, fullname, username, chat_id, events_being_managed: dict, events = []):
		super().__init__(user_id, fullname, username, chat_id, events)
		self.events_being_managed = events_being_managed

	def create_event(self, name, date, time, participants_limit, waiting_list_limit = None):
		newEvent = Event(name, date, time, participants_limit, waiting_list_limit)
		self.events_being_managed[newEvent.get_event_id()] = newEvent

	def delete_event(self, eventId):
		self.events_being_managed.pop(eventId)

	def get_managed_event(self, eventId):
		return self.events_being_managed[eventId]

	def add_user_to_event(self, event, user):
		event.add_user_to_event(user)

	def remove_user_from_event(self, event, user):
		event.remove_from_event(user)
