
import graphviz

M,C,P = 3,3,1

class MissionariesAndCannibal:
	def __init__(self):
		__initials = (M,C,P)
		self.graph = [[__initials]]
		self.shifts = [(1,0),(1,1),(0,1),(2,0),(0,2)]
		self.uniqueNodes = []
		self.visitedNodes = []
		self.nodeFormat = "[{},{},{}]"
		self.figure = graphviz.Digraph('state_space',filename='state_space.gv')

	def generateNewNodes(self,node):
		"""
		It takes a node, finds all the nodes that can be reached from it, and adds them to the graph
		
		:param node: The current node
		:return: The return value is a list of tuples.
		"""
		nodes = []
		if(self.visitedNodes.count(node)):
			return []
		else:
			nextNodes = self.findPath(node)
			for newNode in nextNodes:
				if(self.visitedNodes.count(newNode)):
					continue
				m, c, _ = node
				om, oc, __ = newNode
				isGoal = self.checkGoal(newNode)
				self.addNode(node, newNode,(abs(m-om),abs(c-oc)), isGoal)
				nodes.append(newNode)
				if(isGoal):
					break
			self.visitedNodes.append(node)
			return nodes

	def findPath(self,node):
		"""
		It returns a list of all possible states that can be reached from the current state
		
		:param node: The current node
		:return: A list of possible moves
		"""
		possible=[]
		for shift in self.shifts:
			pm, pc = shift
			m,c,p = node
			om,oc = 3-m, 3-c
			if(p):
				m = m-pm
				c = c-pc
				om = om + pm
				oc = oc + pc
			else:
				m = m+pm
				c = c+pc
				om = om-pm
				oc = oc-pc
			
			if(m>3 or c>3 or m<0 or c<0 or om>3 or oc>3 or om<0 or oc<0 or (m and m<c) or (om and om<oc)):
				continue
			possible.append((m,c,int(not bool(p))))
		return possible
		
	def checkGoal(self,node):
		"""
		If the number of missionaries and cannibals on the left side of the river is zero, then the goal
		has been reached
		
		:param node: a tuple of (m,c,p) where m is the number of missionaries on the left bank, c is the
		number of cannibals on the left bank, and p is the boat's location (0 for left, 1 for right)
		:return: a boolean value.
		"""
		m,c,_ = node
		return (not m) and (not c)
		
	def addNode(self, currentNode, childNode, shift, isGoal):
		"""
		It adds a node to the graph, and if the node is a goal node, it makes it an ellipse, otherwise it
		makes it a rectangle.
		
		:param currentNode: the current node
		:param childNode: the node to be added
		:param shift: count for the missionaries and cannibals that are being shifted to the left
		:param isGoal: True if the node is a goal node, False otherwise
		"""
		pc, pm, pp = currentNode
		cc, cm, cp = childNode
		sc, sm = shift
		if(isGoal):
			self.figure.attr('node', shape='ellipse')
		else:
			self.figure.attr("node", shape='rectangle')
		self.figure.edge(self.nodeFormat.format(pc,pm,pp), self.nodeFormat.format(cc,cm,cp), label="({}, {})".format(sc,sm))

	def solve(self):
		"""
		It takes the first node in the graph, generates all the possible nodes that can be reached from
		that node, and then checks if any of those nodes are the goal node. If none of them are the goal
		node, it takes the next node in the graph and repeats the process.
		Finally, It generates and opens an image named 'Mac.png' where the generated graph is available.
		:return: The graph is being returned.
		"""
		currentRow = 0
		goalReached = False
		while(len(self.graph[currentRow]) and not goalReached):
			nodes = []
			for node in self.graph[currentRow]:
				if(goalReached):
					break
				else:
					liveNodes = self.generateNewNodes(node)
					for live in liveNodes:
						nodes.append(live)
						self.uniqueNodes.append(live)
						isGoal = self.checkGoal(live)
						if(isGoal):
							self.graph.append(nodes)
							goalReached = True
							break
			currentRow = currentRow+1
			self.graph.append(nodes)
		self.figure.render(filename='MaC', format="png", view=True)
		return self.graph

if __name__ == '__main__':
	mac = MissionariesAndCannibal()
	ans = mac.solve()