# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    from util import manhattanDistance
    score=0.0
    for i in newGhostStates:
        j=i.getPosition()
        disGhost=manhattanDistance(j,newPos)
        if(i.scaredTimer!=0):
            if(disGhost==0):
                score+=1000
            else:
                score+=500/disGhost
        else:
            if(disGhost<2):
               score-=1000
    
    for i in currentGameState.getCapsules():
        disCap=manhattanDistance(i,newPos)
        if(disCap==0):
            score+=100
        else:
            score+=10.0/disCap
    food=newFood.asList()        
    for i in food:
        disFood=manhattanDistance(i,newPos)
        score+=10.0/disFood
    nowFood=currentGameState.getFood().asList()
    for i in nowFood:
        disNowFood=manhattanDistance(i,newPos)
        if(disNowFood==0):
            score+=100
    if(action==Directions.STOP):
        score-=100
            
    return score
    #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    return self.minimax(gameState)
    util.raiseNotDefined()
    
  def minimax(self,gameState):
      depth=1
      bestaction=self.max(gameState,depth)
      return bestaction
      
  def max(self,gameState,depth):
      if depth==self.depth or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
      value=-999999999999.99
      
      actions=gameState.getLegalActions(0)
      act=actions[0]
      for action in actions:
          successor=gameState.generateSuccessor(0,action)
          mvalue=self.mini(successor,depth,1)
          if(mvalue>value):
              value=mvalue
              act=action
      if(depth==1):
          return act
      else:
          return value
  def mini(self,gameState,depth,agentIndex):
      #print agentIndex
      if depth==self.depth or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
      value=99999999999999.99
      actions=gameState.getLegalActions(agentIndex)
      for action in actions:
          successor=gameState.generateSuccessor(agentIndex,action)
          number=gameState.getNumAgents()
          #print number
          if(agentIndex<number-1):
              #print agentIndex
              nextAgent=agentIndex+1
              mvalue=self.mini(successor,depth,nextAgent)
              
          else:
              #print 'iii'
              nextDepth=depth+1
              mvalue=self.max(successor,nextDepth)
          if(value>mvalue):
              value=mvalue
      return value

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    
    return self.abSearch(gameState)
    util.raiseNotDefined()
    
  def abSearch(self,gameState):
      depth=1
      a=-9999999999.99
      b=9999999999.99
      bestaction=self.max(gameState,depth,a,b)
      return bestaction
      
  def max(self,gameState,depth,a,b):
      if depth==self.depth or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
      value=-999999999999.99
      
      actions=gameState.getLegalActions(0)
      act=actions[0]
      for action in actions:
          successor=gameState.generateSuccessor(0,action)
          mvalue=self.mini(successor,depth,1,a,b)
          if(mvalue>value):
              value=mvalue
              act=action
          if(value>=b):
              if(depth==1):
                  return act
              else:
                  return value
          if(value>a):
              a=value
      if(depth==1):
          return act
      else:
          return value
  def mini(self,gameState,depth,agentIndex,a,b):
      #print agentIndex
      if depth==self.depth or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
      value=99999999999999.99
      actions=gameState.getLegalActions(agentIndex)
      for action in actions:
          successor=gameState.generateSuccessor(agentIndex,action)
          number=gameState.getNumAgents()
          #print number
          if(agentIndex<number-1):
              #print agentIndex
              nextAgent=agentIndex+1
              mvalue=self.mini(successor,depth,nextAgent,a,b)
              
          else:
              #print 'iii'
              nextDepth=depth+1
              mvalue=self.max(successor,nextDepth,a,b)
          if(value>mvalue):
              value=mvalue
          if(value<=a):
              return value
          if(value<b):
              b=value
      return value

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    return self.expectimax(gameState)
    util.raiseNotDefined()
    
  def expectimax(self,gameState):
      depth=1
      bestaction=self.max(gameState,depth)
      return bestaction
      
  def max(self,gameState,depth):
      if depth==self.depth or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
      value=-999999999999.99
      
      actions=gameState.getLegalActions(0)
      act=actions[0]
      for action in actions:
          successor=gameState.generateSuccessor(0,action)
          mvalue=self.mini(successor,depth,1)
          if(mvalue>value):
              value=mvalue
              act=action
      if(depth==1):
          return act
      else:
          return value
  def mini(self,gameState,depth,agentIndex):
      #print agentIndex
      if depth==self.depth or gameState.isWin() or gameState.isLose():
          return self.evaluationFunction(gameState)
      value=99999999999999.99
      from util import Counter
      actions=gameState.getLegalActions(agentIndex)
      counter=Counter()
      act=actions[0]
      for action in actions:
          counter[action]=1.0
          #print counter[action]
      #print 'kkkkk'
      counter.normalize()
      #for action in actions:
          #print counter[action]
      for action in actions:
          successor=gameState.generateSuccessor(agentIndex,action)
          number=gameState.getNumAgents()
          #print number
          if(agentIndex<number-1):
              #print agentIndex
              nextAgent=agentIndex+1
              mvalue=self.mini(successor,depth,nextAgent)
              
          else:
              #print 'iii'
              nextDepth=depth+1
              mvalue=self.max(successor,nextDepth)
          if(value>mvalue):
              value=mvalue
              act=action
      value=value*counter[act]
      return value

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  
  foods=currentGameState.getFood().asList()
  position=currentGameState.getPacmanPosition()
  foodNumber=currentGameState.getNumFood()
  ghostStates=currentGameState.getGhostStates()
  capsules=currentGameState.getCapsules()
  
  score=0.00
  from searchAgents import mazeDistance
  from util import manhattanDistance
    
  for i in ghostStates:
        j=i.getPosition()
        disGhost=mazeDistance(j,position,currentGameState)
        #disGhost=manhattanDistance(j,position)
        if(i.scaredTimer!=0):
            if(disGhost==0):
                score+=1000
            else:
                score+=500.0/disGhost
        else:
            if(disGhost<2):
               score-=1000
    
  for i in capsules:
        disCap=mazeDistance(i,position,currentGameState)
        #disCap=manhattanDistance(i,position)
        if(disCap==0):
            score+=100
        else:
            score+=10.0/disCap
        
  for i in foods:
        disFood=mazeDistance(i,position,currentGameState)
        #disFood=manhattanDistance(i,position)
        score+=10.0/disFood

  score+=6000/(foodNumber+1)
  #print foodNumber
  return score
  
  
  
  
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

