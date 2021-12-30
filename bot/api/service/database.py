import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# from .customqueue import CustomQueue
from bot.api.service.user import User
from bot.api.service.event import Event
# Fetch the service account key JSON file contents
cred_obj = credentials.Certificate("bot/api/service/queuenow-feb63-firebase-adminsdk-q2oln-356a78dc52.json")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred_obj)

# Is there a better way to do the error handling?
# Change user to user_ref: Participants and Waiting List only stores references now 
# Improve error messages?
class Database:
	def __init__(self) -> None:
		self.db = firestore.client()

	def get_event(self, event_id):
		doc_ref = self.db.collection(u'events').document(event_id)
		doc = doc_ref.get()

		if doc.exists: 
			return Event.from_dict(doc.to_dict())

		raise self.throw_exception(event_id, 'not exist', '-event_id not in events collection, unable to get')

	def get_user(self, user_id):
		doc_ref = self.db.collection(u'users').document(str(user_id).encode("utf-8").decode("utf-8"))
		doc = doc_ref.get()
		
		if doc.exists: 
			return User.from_dict(doc.to_dict())

		raise self.throw_exception(user_id, 'not exist', '-user_id not in users collection, unable to get')

	def add_event(self, event):
		try: 
			self.get_event(event.event_id)
		except:
			# event does not exist in database, so add it to the database
			
			doc_ref = self.db.collection(u'events').document()
			# retrieving the custom id generated by firestore
			id = doc_ref.id
			
			event_dict = event.to_dict()
			
			# assigning the id to event_id field of event
			event_dict['event_id'] = id
			print(event.name + " being assigned the event id: " + id)

			doc_ref.set(event_dict)
			print("added the following event successfully:")
			print(event_dict)

	def remove_event(self, event_id):
		try: 
			event = self.get_event(event_id)
		except Exception as e:
			print(e)
		else:
			user_list = event.participants_list.items + event.waiting_list.items 
			
			# participants and waiting list now stores references to users instead of the users themselves
			for user_ref in user_list:
				# gets the user object given its firestore reference 
				user = User.from_dict(user_ref.get().to_dict())
				user.leave_event(self.get_event_ref(event))
				self.update_user_information(user.user_id, events = user.events)

			self.get_event_ref(event).delete()

			print("removed the following event: " + event.name + " from EventManager")
	
	def add_user(self, user):
		try: 
			self.get_user(user.user_id)
		except: 
			# user does not exist in database yet, so add the user
			self.db.collection(u'users').document(str(user.user_id).encode("utf-8").decode("utf-8")).set(user.to_dict())
			print("Added user: " + user.username + " to user database")

	# haven't implemented logic for removing user from the events he/she is in but i'm too tired for now
	def remove_user(self, user_id):
		try: 
			existingUser = self.get_user(user_id)
		except Exception as e:
			# user to be removed does not exist in database 
			print(e)
		else:
			user_ref = self.get_user_ref(existingUser)
			user_ref.delete()
			print("Removed user " + existingUser.username + "from user database")
			# collection_ref = self.db.collection(u'users')
			# documents = collection_ref.where(u'user_id', u'==', user_id).get()

	def add_user_to_event(self, event_id, user_id):
		try: 
			user = self.get_user(user_id)
			event = self.get_event(event_id)
		except ValueError as e: 
			# either user or event does not exist (or both)
			print(e)
		else: 
			try: 
				# add user to the event participant/waiting list and update the event document in the database
				event.add_user_to_event(self.get_user_ref(user))
			except Exception as e:
				print(e) 
			else:
				self.update_event_information(event_id, 
					participants_list = {"items": event.participants_list.items, "limit": event.participants_limit}, 
					waiting_list = {"items": event.waiting_list.items, "limit": event.waiting_list_limit}
				)

				# add the event to the user's list of events, updates the user document in the database 
				user.add_event(self.get_event_ref(event))

				self.update_user_information(user_id, events = user.events)

				print("Added " + user.username + " to " + event.name)
					

	def remove_user_from_event(self, event_id, user_id):
		try: 
			user = self.get_user(user_id)
			event = self.get_event(event_id)
		except ValueError as e: 
			# either user or event does not exist (or both)
			print(e)
		else:
			try:	
				# remove user from the event participant/waiting list, updates the event document in the database
				event.remove_from_event(self.get_user_ref(user))
			except Exception as e:
				print(e)
			else:
				self.update_event_information(event_id, 
					participants_list = {"items": event.participants_list.items, "limit": event.participants_limit}, 
					waiting_list = {"items": event.waiting_list.items, "limit": event.waiting_list_limit}
				)
				
				# removes the event from the user's list of events, updates the user document in the database 
				user.leave_event(self.get_event_ref(event))
				
				self.update_user_information(user_id, events = user.events)
				
				print("Removed " + user.username + " from " + event.name)

	##################################################
			# Helper Functions #
	##################################################			
	# can be used to any kind of event information (participant list, name, description etc)
	def update_event_information(self, event_id, **event_information):
		collection_ref = self.db.collection(u'events')
		documents = collection_ref.where(u'event_id', u'==', event_id).get()
		
		for doc in documents: 
			doc.reference.update(event_information)

	# can be used to update any kind of user information (user_id, fullname, events etc)	 
	def update_user_information(self, user_id, **user_information):
		collection_ref = self.db.collection(u'users')
		documents = collection_ref.where(u'user_id', u'==', user_id).get()
		
		for doc in documents: 
			doc.reference.update(user_information)

	def get_user_ref(self, user):
		user_ref = self.db.collection(u'users').document(str(user.user_id).encode("utf-8").decode("utf-8"))
		
		return user_ref

	def get_event_ref(self, event):
		event_ref = self.db.collection(u'events').document(event.event_id)
			
		return event_ref
		
	def get_user_events(self, user_id):
		return self.get_user(user_id).events
				
	def throw_exception(self, cause, reason, comment=''):
		err = ''
		match reason:
			case 'exist':
				err = '{str} already contained'.format(str=type(cause).__name__)
				
			case 'not exist':
				err = '{str} is not contained'.format(str=type(cause).__name__)
		err += ' - ' + comment
		raise ValueError(err)

if __name__ == '__main__':
	# TO-DO:
	# test if user will be added to waiting list when participant list is full 
	
	d = Database()

	# creating users and events. 
	# for i in range(100,110):
	# 	test_user = User(i, "jeremy11 yeo", "jyeo", i * 2)
	# 	test_event = Event(str(i) + ' IG training', firestore.SERVER_TIMESTAMP, i * 10, i * 10)
		
	# 	d.add_user(test_user)
	# 	d.add_event(test_event)
	
	# removing users and events
	# d.remove_user(100)
	# d.remove_user(101)
	# d.remove_event("BulinkOcY705mykKyVVY")
	# d.remove_event("DeeKCGGZRch7OExZPwMS")

	# adding users to events 
	# d.add_user_to_event("I7kiJojGjDryrXhUxQ1x", 102)
	# d.add_user_to_event("I7kiJojGjDryrXhUxQ1x", 103)
	# d.add_user_to_event("I7kiJojGjDryrXhUxQ1x", 104)
	# d.add_user_to_event("I7kiJojGjDryrXhUxQ1x", 100000) # no such user exists
	# d.add_user_to_event("I7kiJojGjDryrawefawefXhUxQ1x", 107) # no such event exists

	# removing users from events 
	# d.remove_user_from_event("I7kiJojGjDryrXhUxQ1x", 102)
	# d.remove_user_from_event("I7kiJojGjDryrXhUxQ1x", 103)

	# removing event which has users in it 
	# d.remove_event("I7kiJojGjDryrXhUxQ1x")


	