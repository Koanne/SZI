import math
# A simple implementation of Priority Queue
# using Queue.
class PriorityQueue(object):
	def __init__(self):
		self.queue = []
		self.first = True

	def __str__(self):
		return ' '.join([str(i) for i in self.queue])

	# for checking if the queue is empty
	def isEmpty(self):
		return len(self.queue) == []

	# for inserting an element in the queue
	def insert(self, data):
		self.queue.append(data)

	# for popping an element based on Priority
	def delete(self, state):
		if self.first:
			self.first = False
			return self.queue[0]

		try:
			newq = list(filter(lambda s: 0.1 < math.sqrt((s.position[0]-state.position[0])**2 + (s.position[1]-state.position[1])**2) < 1.1,self.queue))
			min = newq[0]
			for s in newq:
				if (s.priority < min.priority):
					min = s
			item = min
			self.queue.remove(state)
		#max = 0
		# for i in range(len(self.queue)):
		# 	if self.queue[i].priority < self.queue[max].priority:
		# 		max = i
		# item = self.queue[max]
		# del self.queue[max]
			return item
		except IndexError:
			print()
			exit()
