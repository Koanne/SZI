import math
import copy

# A simple implementation of Priority Queue
# using Queue.
class PriorityQueue(object):
    def returnElementAhead(self, state, elements):
        if state.rotation==0:
            for i in elements:
                if state.position[0]==i.position[0] and state.position[1]-1==i.position[1]:
                    return i
        elif state.rotation==1:
            for i in elements:
                if state.position[1]==i.position[1] and state.position[0]+1==i.position[0]:
                    return i
        elif state.rotation==2:
            for i in elements:
                if state.position[0]==i.position[0] and state.position[1]+1==i.position[1]:
                    return i
        elif state.rotation==3:
            for i in elements:
                if state.position[1]==i.position[1] and state.position[0]-1==i.position[0]:
                    return i
    def getSuccessors(self, state, elements):
        succ = []
        if self.returnElementAhead(state, elements) is not None:
            if self.returnElementAhead(state, elements).isPassable():
                astate = copy.deepcopy(state)
                if astate.rotation==0:
                    astate.position[1] += -1
                elif astate.rotation==1:
                    astate.position[0] += 1
                elif astate.rotation==2:
                    astate.position[1] += 1
                else:
                    astate.position[0] += -1
                if True:
                    succ.append(["goAhead", astate])
        lstate = copy.deepcopy(state)
        lstate.rotation = (lstate.rotation-1+4)%4
        succ.append(["turnLeft", lstate])
        rstate = copy.deepcopy(state)
        rstate.rotation = (rstate.rotation+1)%4
        succ.append(["turnRight", rstate])
        return succ

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
			#newq = list(filter(lambda s: 0.1 < math.sqrt((s.position[0]-state.position[0])**2 + (s.position[1]-state.position[1])**2) < 1.1,self.queue))
			#min = newq[0]
    		min = self.queue[0]
    		for s in self.queue:
    			q = []
    			for [action, st] in self.getSuccessors(state, elements):
    				q.append(st)
    			if (s.priority < min.priority) and self.stateValueExists(s, q): 
    				min = s
    		item = min
    		self.queue.remove(item)
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

    def stateValueExists(self, state, states):
        found = False
        for i in states:
            if str(str(i.position)+str(i.rotation))==str(str(state.position)+str(state.rotation)) :
                found = True
                break
        return found