# global strings to use for exception messages 
queue_is_full = "The queue is full. You cannot enqueue any more users"

class CustomQueue:
	def __init__(self, limit=0):
		print("Init custom queue")
		self.items = []
		self.limit = limit

	def is_empty(self):
		return self.items == []

	def enqueue(self, item):
		if not self.is_full():
			self.items.append(item)
		else: 
			raise Exception(queue_is_full)

	def dequeue(self):
		return self.items.pop(0)
	
	def remove(self, item):
		if item in self.items:
			self.items.remove(item)
	
	def dequeue_index(self, index: int):
		return self.items.pop(index)

	def index_of(self, item):
		return self.items.index(item)

	def contains(self, item):
		return item in self.items 

	def is_full(self):
		return self.limit is not None and self.size() == self.limit
	
	def size(self):
		return len(self.items)

	def update_limit(self, newLimit):
		self.limit = newLimit
	
	@staticmethod
	def from_dict(source):
		# [START_EXCLUDE]
		custom_queue = CustomQueue(source[u'items'], source[u'limit'])

		if u'items' in source:
			custom_queue.items = source[u'items']

		if u'limit' in source:
			custom_queue.limit = source[u'limit']

		return custom_queue
		# [END_EXCLUDE]

	def to_dict(self):
		# [START_EXCLUDE]
		dest = {
			u'items': self.items,
			u'limit': self.limit
		}

		if self.items:
			dest[u'items'] = self.items

		if self.limit:
			dest[u'limit'] = self.limit

		return dest
		# [END_EXCLUDE]
