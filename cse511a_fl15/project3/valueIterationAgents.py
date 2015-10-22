# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
     
    "*** YOUR CODE HERE ***"
    
    stateList=mdp.getStates()
    iter=0
    while iter<iterations:
        values=self.values.copy()
        for state in stateList:
            if not self.mdp.isTerminal(state):
              maxvalue=-2.00
              actions=mdp.getPossibleActions(state)
              for action in actions:
                Qvalue=self.getQValue(state, action)
                if Qvalue>maxvalue:
                    maxvalue=Qvalue
              values[state]=maxvalue
        self.values=values    
        iter=iter+1


  def getValue(self, state):
   
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    
    value=0.00
    for possibleState, probability in self.mdp.getTransitionStatesAndProbs(state,action):
        value=value+probability*(self.mdp.getReward(state,action,possibleState)+(self.discount*self.getValue(possibleState)))
    return value

    util.raiseNotDefined()

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    
    everyQvalues=util.Counter()
    PossibleActions=self.mdp.getPossibleActions(state)
    
    if self.mdp.isTerminal(state):
        return None
    
    for action in PossibleActions:
        everyQvalues[action]=self.getQValue(state, action)
    return everyQvalues.argMax()
    

    util.raiseNotDefined()

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
