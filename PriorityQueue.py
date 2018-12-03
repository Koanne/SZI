class Skill(object):
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print('New Level:', description)
        return
# A simple implementation of Priority Queue
# using Queue.
class PriorityQueue(object):
	def __init__(self):
		self.queue = []

	def __str__(self):
		return ' '.join([str(i) for i in self.queue])

	# for checking if the queue is empty
	def isEmpty(self):
		return len(self.queue) == []

	# for inserting an element in the queue
	def insert(self, data):
		self.queue.append(data)

	# for popping an element based on Priority
	def delete(self):
		try:
			max = 0
			for i in range(len(self.queue)):
				if self.queue[i].priority < self.queue[max].priority:
					max = i
			item = self.queue[max]
			del self.queue[max]
			return item
		except IndexError:
			print()
			exit()


if __name__ == '__main__':
	myQueue = PriorityQueue()
	myQueue.insert(Skill(12,'AAA'))
	myQueue.insert(Skill(10,'BBB'))
	myQueue.insert(Skill(15,'CCC'))
	while not myQueue.isEmpty():
		print(myQueue.delete().description)
