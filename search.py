# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

###############################CLASSES AND FUNCTIONS THAT ALL METHODS USE###############################

class Node:
    def __init__(self, state, parent, move): #We tie the Node with its Parent and the Move we made to get there together                                          
        self.State = state  #in order to be able to follow our initial path back
        self.Parent = parent
        self.Move = move

#The same class but we will need the cost as well for the UCS and A*
class NodeWCost:
    def __init__(self, state, parent, move, cost): 
        self.State = state
        self.Parent = parent
        self.Move = move
        self.Cost = cost

#Return path_to_node function
def path_to_Node(node):
    path = []
    #Until you reach the start node, add the moves to the path and check the parent node
    while(node.Parent != None):
        path.append(node.Move)
        node = node.Parent
    #We must return in the reverse order, the move we appended first is essentially the last
    return path[::-1]
###############################CLASSES AND FUNCTIONS THAT ALL METHODS USE###############################

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from util import Stack 
    
    #We use the stack for DFS
    frontier = Stack() 
    expanded = set() 

    #frontier = [startNode]
    startNode = Node(problem.getStartState(), None, None)
    frontier.push(startNode)

    #while frontier is not Empty
    while not frontier.isEmpty():
        node = frontier.pop()
        #if isGoal(node)
        if(problem.isGoalState(node.State)):
            #return path_to_node
            return path_to_Node(node)
        #if node not in expanded
        if node.State not in expanded:
            #expanded.add(node)
            expanded.add(node.State)
            successors = problem.getSuccessors(node.State)
            #for its child of the node
            for successor in successors:
                #We need to turn the successor into our Node class before pushing it to our stack
                successorNode = Node(successor[0], node, successor[1])
                #frontier push(child)
                frontier.push(successorNode)
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    
    #We use the Queue for BFS
    frontier = Queue()
    expanded = set() 

    #frontier = [startNode]
    startNode = Node(problem.getStartState(), None, None)
    frontier.push(startNode)

    while not frontier.isEmpty():
        node = frontier.pop()
        #if isGoal(node)
        if(problem.isGoalState(node.State)):
            #return path_to_node
            return path_to_Node(node)
        #if node not in expanded
        if node.State not in expanded:
            #expanded.add(node)
            expanded.add(node.State)
            successors = problem.getSuccessors(node.State)
            #for its child of the node
            for successor in successors:
                #We need to turn the successor into our Node class before pushing it to our queue
                successorNode = Node(successor[0], node, successor[1])
                #frontier push(child)
                frontier.push(successorNode)

    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
   
    #We use the PriorityQueue for UCS
    frontier = PriorityQueue()
    expanded = set() 

    #frontier = [startNode]
    startNode = NodeWCost(problem.getStartState(), None, None, 0)
    frontier.push(startNode, startNode.Cost) #push the start node into the Pqueue with cost zero

    while not frontier.isEmpty():
        node = frontier.pop()
        #if isGoal(node)
        if(problem.isGoalState(node.State)):
            #return path_to_node
            return path_to_Node(node)
        #if node not in expanded
        if node.State not in expanded:
            #expanded.add(node)
            expanded.add(node.State)
            successors = problem.getSuccessors(node.State)
            #for its child of the node
            for successor in successors:
                #We need to turn the successor into our Node class before pushing it to our PriorityQueue
                successorNode = NodeWCost(successor[0], node, successor[1], node.Cost + successor[2])
                #frontier push(child)
                frontier.push(successorNode, successorNode.Cost)


    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
   
    #We use the PriorityQueue for A*
    frontier = PriorityQueue()
    expanded = set() 

    #frontier = [startNode]
    startNode = NodeWCost(problem.getStartState(), None, None, 0)
    frontier.push(startNode, 0 + heuristic(problem.getStartState(), problem)) #push the cost of the move (zero) and the value of the heuristic

    while not frontier.isEmpty():
        node = frontier.pop()
        #if isGoal(node)
        if(problem.isGoalState(node.State)):
            #return path_to_node
            return path_to_Node(node)
        #if node not in expanded
        if node.State not in expanded:
            #expanded.add(node)
            expanded.add(node.State)
            successors = problem.getSuccessors(node.State)
            #for its child of the node
            for successor in successors:
                #We need to turn the successor into our Node class before pushing it to our PriorityQueue
                successorNode = NodeWCost(successor[0], node, successor[1], node.Cost + successor[2])
                #frontier push(child)
                frontier.push(successorNode, successorNode.Cost + heuristic(successorNode.State, problem))
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
