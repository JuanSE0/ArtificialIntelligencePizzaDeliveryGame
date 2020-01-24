'''
    Uninformed Search 
    
    Problem:
      Initial State: A
      Actions: move to a connected node
      Goal: H
      Heuristic: no
      Algorithm: breadth-first

'''
import os
import sys

# To access to the simpleai library
sys.path.append(os.path.abspath("simpleai-0.8.1"))

from simpleai.search import SearchProblem
from simpleai.search.viewers import BaseViewer
from simpleai.search import breadth_first,depth_first,astar,greedy

# Class MapProblem definition
class MapProblem(SearchProblem):
    
    # Class attributes, to access them you need to use the self statement self.mapProblem or self.final_state
    # self.mapProblem contains all the state in the problem along with the possible transitions from it
    mapProblem=None
    # self.final_state contains the goal state
    final_state=None

    # --------------- Common methods to the SearchProblem -----------------
   
    # METHOD THAT GIVEN A STATE RETURNS A LIST OF THE APPLICABLE ACTIONS FOR SUCH STATE
    def actions(self, state):
        
        return None

    # METHOD THAT GIVEN A STATE AND AN ACTION RETURNS THE STATE REACHED AFTER APPLYING THE ACTIONS TO THE GIVEN STATE
    def result(self, state, action):
        
        return None

    # METHOD THAT RETURNS TRUE IF THE GIVEN STATE IS THE GOAL STATE, OTHERWISE IT RETURNS FALSE
    def is_goal(self, state):
        
        return False
   
    # METHOD THAT RETURNS THE COST OF APPLYING THE GIVEN ACTION IN THE GIVEN STATE WHEN REACHING STATE2
    def cost(self, state, action, state2):
        
        return 1

    # METHOD THAT RETURN THE HEURISTIC VALUE FOR THE GIVEN STATE
    def heuristic(self, state):
        
        return 0


# --------------- Other methods outside the MapProblem class -----------------

def MapExercise(problem,algorithm,use_viewer=None):
    
    result = algorithm(problem,graph_search=True,viewer=use_viewer)
    
    print("Final state:" + result.state)
    print("Path: {0}".format(result.path()))
    print("Cost: {0}".format(getTotalCost(problem,result)))
    
    if use_viewer:
        stats = [{'name': stat.replace('_', ' '), 'value': value}
                         for stat, value in list(use_viewer.stats.items())]
        for s in stats:
            print ('{0}: {1}'.format(s['name'],s['value']))
    return result

def getTotalCost (problem,result):
    originState = problem.initial_state
    totalCost = 0
    for action,endingState in result.path():
        if action is not None:
            totalCost += problem.cost(originState,action,endingState)
            originState = endingState
    return totalCost

# END MapExercise

# -------------------------  PROBLEM SOLVING ----------------------

initial_state = None
final_state = None
map_problem = None

problem = MapProblem(initial_state)
problem.mapProblem = map_problem
problem.final_state = final_state

MapExercise(problem,algorithm=breadth_first,use_viewer=BaseViewer())
