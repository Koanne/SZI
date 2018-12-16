import math
import copy

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
    def delete(self, state, elements):
    	if self.first:
    		self.first = False
    		return self.queue[0]

    	try:
    		min = self.queue[0]
    		for s in self.queue:
    			if (s.priority < min.priority): 
    				min = s
    		item = min
    		self.queue.remove(item)
    		return item
    	except IndexError:
    		print()
    		exit()