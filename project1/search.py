# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:


    """
    "*** YOUR CODE HERE ***"
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    

    from util import Stack
    explored = []
    stack=Stack()
    result = []
    record = []

    if problem.isGoalState(problem.getStartState()):
        return []
    
    stack.push((problem.getStartState(),record))
    explored.append(problem.getStartState())

    while not stack.isEmpty():
        node = stack.pop()
        result = node[1]
        for i in problem.getSuccessors(node[0]):
            succesor = i[0]
            step = i[1]
            record = list(result)
            if problem.isGoalState(succesor):
                explored.append(succesor)
                result.append(step)
                return result
            elif not succesor in explored:
                explored.append(succesor)
                record.append(step)
                stack.push((succesor,record))

    #return result
    util.raiseNotDefined()
    


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    from util import Queue
    explored = []
    queue=Queue()
    result = []
    record = []

    if problem.isGoalState(problem.getStartState()):
        return []
    
    queue.push((problem.getStartState(),record))
    explored.append(problem.getStartState())

    while not queue.isEmpty():
        node = queue.pop()
        result = node[1]
        for i in problem.getSuccessors(node[0]):
            succesor = i[0]
            step = i[1]
            record = list(result)
            if problem.isGoalState(succesor):
                explored.append(succesor)
                result.append(step)
                return result
            
            elif not succesor in explored:
                explored.append(succesor)
                record.append(step)
                queue.push((succesor,record))
    #return result

    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    """
    from util import PriorityQueue
    explored = []
    queue=PriorityQueue()
    result = []

    if problem.isGoalState(problem.getStartState()):
       


        return []
    
    queue.push((problem.getStartState(),[],0),0)
    explored.append(problem.getStartState())

    while not queue.isEmpty():
        node = queue.pop()
        result = node[1]
        cost=node[2]
        for i in problem.getSuccessors(node[0]):
            succesor = i[0]
            step = i[1]
            newcost=i[2]
            if problem.isGoalState(succesor):
                explored.append(succesor)
                result=result+[step]
                #print explored
                #print problem.getCostOfActions(result)
                return result
            elif not succesor in explored:
                explored.append(succesor)
                result=result+[step]
                queue.push((succesor,result,cost+newcost),problem.getCostOfActions(result))
                #print problem.getCostOfActions(record)
                #print'!!!!!!!!'
    """
    from util import PriorityQueue
    PQueue =PriorityQueue()
    PQueue.push( (problem.getStartState(), []), 0)
    explored = []
    result=[]
    record=[]

    while not PQueue.isEmpty():
        node= PQueue.pop()
        result=node[1]
        if problem.isGoalState(node[0]):
            
            return result

        explored.append(node[0])

        for i in problem.getSuccessors(node[0]):
            succesor=i[0]
            step=i[1]
            record=list(result)
            if not i[0] in explored:
                record.append(step)
                PQueue.push((succesor,record), problem.getCostOfActions(record))

    
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):

    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    
    from util import PriorityQueue
    explored = []
    queue=PriorityQueue()
    result = []
    record = []

    if problem.isGoalState(problem.getStartState()):
        return []
    
    queue.push((problem.getStartState(),record),heuristic(problem.getStartState(),problem))
    explored.append(problem.getStartState())

    while not queue.isEmpty():
        node = queue.pop()
        result = node[1]
        if problem.isGoalState(node[0]):
            
            return result
        
        explored.append(node[0])
        for i in problem.getSuccessors(node[0]):
            succesor = i[0]
            step = i[1]
            record = list(result)
            
            if not succesor in explored:

                record.append(step)
                queue.push((succesor,record),problem.getCostOfActions(record)+heuristic(succesor,problem))
    #print problem.getCostOfActions(result)
    #return result
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
