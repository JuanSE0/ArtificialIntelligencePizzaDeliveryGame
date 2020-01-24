
'''
    ARTIFICIAL INTELLIGENCE - UC3M 2019
    Final Project - Logistics Problem
    Rafael Pablos Sarabia 100372175
    Juan Sanchez Esquivel 100383422
    Class gameProblem, implements simpleai.search.SearchProblem
'''


from simpleai.search import SearchProblem
# from simpleai.search import breadth_first,depth_first,astar,greedy
import simpleai.search


class GameProblem(SearchProblem):

    ALGORITHM = 'astar'  # Possible algorithms: astar, breadth_first, depth_first.

    # Object attributes, can be accessed in the methods below.
    # These variables are initialized in method setup.
    MAP = None  # Contains the attributes of every cell from the input file
    POSITIONS = None  # Stores the different positions for each type of cell
    INITIAL_STATE = None  # Initial state for the complete logistics problem
    GOAL = None  # Goal for the whole logistics problem
    CONFIG = None  # Configuration file for current execution
    AGENT_START = None  # Start position of the agent
    SHOPS = None  # Pizza restaurants where delivery worker can obtain more pizzas
    CUSTOMERS = None  # Current customers and orders prior delivery starts
    MAXBAGS = 0  # Maximum numbers of pizzas in the bike
    MOVES = ('West', 'North', 'East', 'South', 'Load', 'Unload')  # Valid actions for the delivery worker

    # --------------- Common functions to a SearchProblem -----------------

    '''
        This method must create the initial state, final state and specify the algorithm to be used.
        This values are later stored as globals that are used when calling the search algorithm.
        It also must set the values of the object attributes that the methods need, as for example, self.SHOPS or self.MAXBAGS
    '''
    def setup(self):
        print '\nMAP: ', self.MAP, '\n'
        print 'POSITIONS: ', self.POSITIONS, '\n'
        print 'CONFIG: ', self.CONFIG, '\n'

        # Obtain maximum number of pizzas in bike from configuration file
        self.MAXBAGS = self.CONFIG["maxBags"]

        # Create list with customers as [[(x,y),...(x,y)][Customer2][Customer3]]
        # where customers in Customer2 have 2 pizzas left and similarly for the others.
        self.CUSTOMERS = []
        for c in ['customer1', 'customer2', 'customer3']:
            input = self.POSITIONS.get(c)
            if input is None:
                input = []
            self.CUSTOMERS = self.CUSTOMERS + [input]

        # Declare initial and final state.
        # States: (<Position (x,y)>, <Customer1 (x,y)>, <Customer2 (x,y)>, <Customer3 (x,y)>, <Pizzas in bike>).
        # Initial state: initial position, all pending orders and initial pizzas on bike (0).
        # Final state: must return to starting position, with no pending orders and no pizzas loaded.
        initial_state = (self.AGENT_START, tuple(self.CUSTOMERS[0]), tuple(self.CUSTOMERS[1]), tuple(self.CUSTOMERS[2]), 0)
        final_state = (self.AGENT_START, tuple(), tuple(), tuple(), 0)

        # Store restaurants in variable SHOPS
        self.SHOPS = []
        if 'pizza' in self.POSITIONS:
            for restaurant in self.POSITIONS['pizza']:
                self.SHOPS = self.SHOPS + [restaurant]

        # Choose algorithm based on variable declaration at the top of the file
        if self.ALGORITHM == 'astar':
            algorithm = simpleai.search.astar
        elif self.ALGORITHM == 'breadth_first':
            algorithm = simpleai.search.breadth_first
        elif self.ALGORITHM == 'depth_first':
            algorithm = simpleai.search.depth_first

        return initial_state, final_state, algorithm

    '''
        Returns a list with possible actions that the delivery worker can take given a state.
        State = (<Position (x,y)>, <Customers with 1 pizza left ((x,y),...)>, <Customers 2>, <Customers 3>, <Pizzas>)
    '''
    def actions(self, state):
        possible_actions = []  # Possible actions for current state
        x = state[0][0]  # Current x position
        y = state[0][1]  # Current y position

        # Attempt to move West
        if (x - 1) >= 0 and self.MAP[(x - 1)][y][0] != 'building' and self.MAP[(x - 1)][y][0] != 'sea':
            possible_actions.append('West')
        # Attempt to move North
        if (y - 1) >= 0 and self.MAP[x][(y - 1)][0] != 'building' and self.MAP[x][(y - 1)][0] != 'sea':
            possible_actions.append('North')
        # Attempt to move East
        if (x + 1) < len(self.MAP) and self.MAP[(x + 1)][y][0] != 'building' and self.MAP[(x + 1)][y][0] != 'sea':
            possible_actions.append('East')
        # Attempt to move South
        if (y + 1) < len(self.MAP[0]) and self.MAP[x][(y + 1)][0] != 'building' and self.MAP[x][(y + 1)][0] != 'sea':
            possible_actions.append('South')

        # If position is restaurant and we are not fully loaded, possible action is to load.
        if state[0] in self.SHOPS and state[4] != self.MAXBAGS:
            possible_actions.append('Load')

        # If we have loaded pizzas and there is a customer, possible action is to unload.
        if state[4] > 0:
            # If there is any customer
            if state[0] in state[1] or state[0] in state[2] or state[0] in state[3]:
                possible_actions.append('Unload')

        return possible_actions

    '''
        Function that receives a state and an action and returns the next state.
        It returns the next state, considering position, remaining customers and pizzas left in bike.
    '''
    def result(self, state, action):
        # First we will check for all actions implying movement
        if action == 'North' or action == 'South' or action == 'West' or action == 'East':
            next_coordinates = (state[0][0], state[0][1])  # By default next position coordinates will be the same
            if action == 'North':
                next_coordinates = (state[0][0], state[0][1]-1)
            elif action == 'South':
                next_coordinates = (state[0][0], state[0][1]+1)
            elif action == 'West':
                next_coordinates = (state[0][0]-1, state[0][1])
            elif action == 'East':
                next_coordinates = (state[0][0]+1, state[0][1])
            return next_coordinates, state[1], state[2], state[3], state[4]

        # Load action
        elif action == 'Load':
            needed = len(state[1]) + len(state[2])*2 + len(state[3])*3
            carrying = min(self.MAXBAGS, needed)
            return state[0], state[1], state[2], state[3], carrying

        # Unload action
        elif action == 'Unload':
            carrying = state[4]  # Just for convenience the number of pizzas that we are carrying will be stored here
            # If position is customer with 1 pizza left
            if state[0] in state[1]:
                carrying = carrying - 1
                tmp = list(state[1])
                tmp.remove(state[0])
                return state[0], tuple(tmp), state[2], state[3], carrying

            # If position is customer with 2 pizzas left
            elif state[0] in state[2]:
                remaining = max(2 - carrying, 0)
                carrying = carrying - 2 + remaining
                tmp1 = list(state[1])
                tmp2 = list(state[2])
                if remaining == 0:  # Remove tuple if all delivered
                    tmp2.remove(state[0])
                else:  # Change client to customers with 1 pizza left
                    tmp2.remove(state[0])
                    tmp1.append(state[0])
                return state[0], tuple(tmp1), tuple(tmp2), state[3], carrying

            # If position is customer with 3 pizzas left
            elif state[0] in state[3]:
                remaining = max(3 - carrying, 0)
                carrying = carrying - 3 + remaining
                tmp1 = list(state[1])
                tmp2 = list(state[2])
                tmp3 = list(state[3])
                if remaining == 0:  # Remove tuple if all delivered
                    tmp3.remove(state[0])
                elif remaining == 1:  # Change client to customers with 1 pizza left
                    tmp3.remove(state[0])
                    tmp1.append(state[0])
                else:  # Change client to customers with 2 pizzas left
                    tmp3.remove(state[0])
                    tmp2.append(state[0])
                return state[0], tuple(tmp1), tuple(tmp2), tuple(tmp3), carrying

        # Returns current state if no other action could be performed
        return state

    '''
        Returns true if state is the final state
    '''
    def is_goal(self, state):
        return state == self.GOAL

    '''
        Returns the cost of applying `action` from `state` to `state2`.The returned value is a number (integer or 
        floating point). By default this function returns `1` for part 1. Loading pizza and unloading pizza also
        have a cost of one. Hill has a cost of 5 and off-road a cost of 2.
    '''
    def cost(self, state, action, state2):
        # Check whether there are hills and we are in one of them
        if 'hill' in self.POSITIONS:
            for hill in self.POSITIONS['hill']:
                if state[0] == hill:
                    return 5

        # Check whether there are offroads and if we are offroad
        if 'offroad' in self.POSITIONS:
            for offroad in self.POSITIONS['offroad']:
                if state[0] == offroad:
                    return 2

        # Return 1 for remaining cases (movement in other terrains or load/unload)
        return 1

    '''
        Returns the heuristic for 'state'. The heuristic will depend on the state of the problem as explained below.
        For part 1, the Manhattan Distance will be used. This is explained in detail in the report. This heuristic
        function is valid for more advanced problems than the basic one since we allow customer to order up to 
        3 pizzas. Only valid for 1 client and 1 pizza restaurant. It may work on other cases but it is not guaranteed.
        The uncommented heuristic is for the advanced part which may have multiple clients and restaurants.
    '''
    def heuristic(self, state):

        # Heuristic for cases with more than one pizza and restaurant
        distanceHome = abs(state[0][0]-self.AGENT_START[0]) + abs(state[0][1]-self.AGENT_START[1])
        return distanceHome + len(state[1])+len(state[2])+len(state[3])

        '''
        # Heuristic to be used for only one pizza and one restaurant, more efficient for those cases

        # If no pizzas are to be delivered, find Manhattan distance from current position to initial position.
        if not (state[1] or state[2] or state[3]):
            sol = abs(state[0][0] - self.AGENT_START[0]) + abs(state[0][1] - self.AGENT_START[1])
            return sol

        # If we arrive here we still have at least a customer remaining.
        # Now we will store client coordinates
        if state[1]:
            cl_x = state[1][0][0]
            cl_y = state[1][0][1]
        elif state[2]:
            cl_x = state[2][0][0]
            cl_y = state[2][0][1]
        else:
            cl_x = state[3][0][0]
            cl_y = state[3][0][1]

        # If we have no pizzas, heuristic will be distance to pizzeria, then to client, then back to start point.
        if state[4] == 0 and len(self.SHOPS)>0:
            # We store the restaurant coordinates
            re_x = self.SHOPS[0][0]
            re_y = self.SHOPS[0][1]
            # Distance to restaurant
            sol = abs(state[0][0] - re_x) + abs(state[0][1] - re_y)
            # Distance restaurant to client + previous
            sol = sol + abs(re_x - cl_x) + abs(re_y - cl_y)
        else:
            # Distance delivery worker to client
            sol = abs(state[0][0] - cl_x) + abs(state[0][1] - cl_y)

        # Distance client to base + previous
        sol = sol + abs(cl_x - self.AGENT_START[0]) + abs(cl_y - self.AGENT_START[1])
        return sol
    '''


    '''
        Returns a string well-formatted with the state information
    '''
    def printState(self, state):
        str = 'Information:\n'
        pos = "Delivery worker position: %s" % (state[0],)
        c1 = "Customers waiting for 1 pizza: %s" % (state[1],)
        c2 = "Customers waiting for 2 pizzas: %s" % (state[2],)
        c3 = "Customers waiting for 3 pizzas: %s" % (state[3],)
        pizzas = "Pizzas loaded in bike: %s" % (state[4],)
        return str+pos+"\n"+c1+"\n"+c2+"\n"+c3+"\n"+pizzas

    '''
        Return the number of pending requests in the given position (0-N). 
        MUST return None if the position is not a customer.
        This information is used to show the proper customer image.
    '''
    def getPendingRequests(self,state):
        # Find if current positions belong to customers with 1, 2 or 3 remaining pizzas.
        for customerAmount in range(1, 4):
            if state[0] in state[customerAmount]:
                return customerAmount

        # If this point is reached, all pizzas where delivered or position is not for customer.
        for customers in self.CUSTOMERS:
            if state[0] in customers:
                return 0

        # Position does not belong to a client
        return None

    # -------------------------------------------------------------- #
    # --------------- DO NOT EDIT BELOW THIS LINE  ----------------- #
    # -------------------------------------------------------------- #

    def getAttribute (self, position, attributeName):
        '''Returns an attribute value for a given position of the map
           position is a tuple (x,y)
           attributeName is a string

           Returns:
               None if the attribute does not exist
               Value of the attribute otherwise
        '''
        tileAttributes=self.MAP[position[0]][position[1]][2]
        if attributeName in tileAttributes.keys():
            return tileAttributes[attributeName]
        else:
            return None

    def getStateData (self,state):
        stateData={}
        pendingItems=self.getPendingRequests(state)
        if pendingItems >= 0:
            stateData['newType']='customer{}'.format(pendingItems)
        return stateData

    # THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
    def initializeProblem(self,map,positions,conf,aiBaseName):
        self.MAP=map
        self.POSITIONS=positions
        self.CONFIG=conf
        self.AGENT_START = tuple(conf['agent']['start'])

        initial_state,final_state,algorithm = self.setup()
        if initial_state == False:
            print ('-- INITIALIZATION FAILED')
            return True

        self.INITIAL_STATE=initial_state
        self.GOAL=final_state
        self.ALGORITHM=algorithm
        super(GameProblem,self).__init__(self.INITIAL_STATE)

        print ('-- INITIALIZATION OK')
        return True

    # END initializeProblem 

