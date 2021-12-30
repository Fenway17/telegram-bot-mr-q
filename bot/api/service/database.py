import os, json, base64

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# from .customqueue import CustomQueue
from user import User
from event import Event

class Database:
	def __init__(self, G_KEY):
		DECODED_G_KEY = base64.b64decode(G_KEY)
		cred_obj = credentials.Certificate(json.loads(DECODED_G_KEY.decode('utf8').replace("'", '"')))
		# Initialize the app with a service account, granting admin privileges
		firebase_admin.initialize_app(cred_obj)
		self.db = firestore.client()

	# possible bug - what happens if you create an identical event? 
	def add_event(self, event):
		self.db.collection(u'events').add(event.to_dict())

	def remove_event(self, event):
		collection_ref = self.db.collection(u'events')
		
		# goal is to filter out the event based on its event id, and subsequently delete it.
		# unable to filter out the event. 
		# suspect where clause does not perform the eqaulity comparison correctly 
		# tried proposed fix below: https://forums.appgyver.com/t/filtering-a-firestore-collection-with-a-number-field-using-condition-type-equal-returns-an-error/9867/3, does not work
		documents = collection_ref.where(u'event_id', u'>', event.id - 1).where(u'event_id', u'<', event.id + 1).get()
		
		# expected: list containing the test event created in the main function. actual: empty list is printed
		# suspect the issue has to do with the equality comparison (see above)
		print(documents)
		
		# document_ref.delete()

	# user-related functions (jeremy)
	def add_user(self, user):
		self.db.collection(u'users').add(user.to_dict())


if __name__ == '__main__':
	test_event = Event('volleyball IG training', firestore.SERVER_TIMESTAMP, 10, 10)
	d = Database()
	d.add_user(User(1, "jeremy yeo", "jyeo", 1))
	# d.add_event(test_event) 
	d.remove_event(test_event)
	