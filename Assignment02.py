from agents import *
from random import randrange
import numpy as np

class ModelAgent(Agent):
    pass


class ReflexAgent(Agent):
    def __init__(self):
        # super(ReflexAgent, self).__init__()
        '''States the initial location of the agent'''
        self.location = (3,3)
        # self.location = (randrange(5), randrange(5)) 
        '''States the initial direction of the agent'''
        self.direction = 'U'
        # ii = randrange(4)
        # if ii == 0:
        #   self.direction = 'U'
        # elif ii == 1:
        #   self.direction = 'R'
        # elif ii == 2:
        #   self.direction = 'D'
        # elif ii == 3:
        #   self.direction = 'L'
        '''States the initial performance'''
        self.performance = 100
        '''Declares the internal state to count the visited cells into the performance'''
        self.internal_state = np.full((5, 5), False)
        self.internal_state[self.location[0]][self.location[1]] = True

    def __str__(self):
        '''Prints the internal state of the agent'''
        facing = ""
        if self.direction == "U":
            facing  = "UP"
        elif self.direction == "R":
            facing = "RIGHT"
        elif self.direction == "D":
            facing = "DOWN"
        elif self.direction == "L":
            facing = "LEFT"
        return "(%s, %s, %s)" % (self.location[0], self.location[1], facing)
        # pass
    
    '''States when the agent enters a cell with a gold'''
    def PickGold(self):
        '''Gives 10 point from the agent'''
        self.performance += 10
        # print("Pick gold")

    '''States when the agent turns'''
    def Turn(self):
        '''Reduces 1 point from the agent'''
        self.performance -= 1
        # print("Turn")
        
        '''Turns its direction clockwise'''
        if self.direction == "U":
            self.direction = "R"
        elif self.direction == "R":
            self.direction = "D"
        elif self.direction == "D":
            self.direction = "L"
        elif self.direction == "L":
            self.direction = "U"

    def Advance(self):
        '''Reduces 1 point from the agent'''
        self.performance -= 1

        '''Advances in the direction of the agent'''
        '''And checks that the agents does not move outside the grid'''
        tupleList = list(self.location)
        if self.direction == "U":
            if tupleList[0] != 0:
                tupleList[0] = tupleList[0]-1
        elif self.direction == "R":
            if tupleList[1] != 4:
                tupleList[1] = tupleList[0]+1
        elif self.direction == "D":
            if tupleList[0] != 4:
                tupleList[0] = tupleList[0]+1
        elif self.direction == "L":
            if tupleList[1] != 0:
                tupleList[1] = tupleList[1]-1
        self.location = tuple(tupleList)

        '''Reduces the performance if the agent enters a visited cell'''
        if self.internal_state[self.location[0]][self.location[1]]:
            self.performance -= 1
        else:
            self.internal_state[self.location[0]][self.location[1]] = True
        # print("Advance")
    
    def FallInTrap(self):
        '''Takes 5 points from the agent'''
        self.performance -= 5
        # print("Fall in Trap")
    
    def program(self, percepts):
        '''Reads the percept and returns the action'''
        percepts = [p for p in percepts if isinstance(p[0], Gold)]
        if len(percepts) < 1:
            return 'ADVANCE'
        else:
            state = percepts[0]
            xGold = state[2][0] 
            yGold = state[2][1]
            xAgent = self.location[0]
            yAgent = self.location[1]

            if yGold == yAgent and xGold == xAgent:
                return 'STAY'
            
            if self.direction == 'U':
                if xGold < xAgent and yGold == yAgent:
                    return 'ADVANCE'
            elif self.direction == 'R':
                if yGold > yAgent and xGold == xAgent:
                    return 'ADVANCE'
            elif self.direction == 'D':
                if xGold > xAgent and yGold == yAgent:
                    return 'ADVANCE'
            elif self.direction == 'L':
                if yGold < yAgent and xGold == xAgent:
                    return 'ADVANCE'

            return ['TURN','ADVANCE'][random.randint(0,1)]
            # return 'TURN'

'''_____________________________________________________________________________________________'''

'''Creates a Gold as a subclass of Thing'''
class Gold(Thing):
    pass

'''_____________________________________________________________________________________________'''

'''Creates a Trap as a subclass of Thing'''
class Trap(Thing):
    pass

'''_____________________________________________________________________________________________'''

'''Creates a GridEnvironment as a subclass of Environment'''
class GridEnvironment(Environment):
    def __init__(self, width=5, height=5):
        super(GridEnvironment, self).__init__()
        self.width = width
        self.height = height
        self.x_start, self.y_start = (0, 0)
        self.x_end, self.y_end = (self.width, self.height)
        self.perceptible_distance = 5

    def __str__(self):
        grid = self.get_grid()
        gridStr = []
        for r in range(self.width):
            row = ''
            for c in range(self.height):
                gold = 0
                traps = 0
                agent = None
                for obj in grid[r][c]:
                    if isinstance(obj, Agent):
                        agent = obj
                    elif isinstance(obj, Gold):
                        gold += 1
                    elif isinstance(obj, Trap):
                        traps += 1
                cell = '(%s %s %s) ' % ('-' if agent is None else agent.direction, '-' if gold < 1 else gold, '-' if traps < 1 else traps)
                row += cell
            row += '\n'
            gridStr.append(row)
        return '\n'.join(gridStr)

    def run(self, steps=1000):
        "Run the Environment for given number of time steps."
        for step in range(steps):
            print("<Step %s>" % step)
            if self.is_done():
                return
            self.step()

    def step(self):
        """Run the environment for one time step. If the
        actions and exogenous changes are independent, this method will
        do.  If there are interactions between them, you'll need to
        override this method."""
        if not self.is_done():
            for agent in self.agents:
                action = agent.program(self.percept(agent))
                print("SELECTED ACTION: ",action)
                print("Agent state: ",agent)
                self.execute_action(agent, action)
                
                things = self.list_things_at(agent.location)
                golds = [g for g in things if isinstance(g, Gold)]
                traps = [t for t in things if isinstance(t, Trap)]

                if golds:
                    agent.PickGold()
                    self.delete_thing(golds[0])
                
                if traps:
                    agent.FallInTrap()
                    self.delete_thing(traps[0])

                print(self)
                print("Agent performance: %s" % agent.performance)
                


    def percept(self, agent):
        '''By default, agent perceives things within a default radius.'''
        return self.things_near(agent.location)

    
    def things_near(self, location, radius=None):
        "Return all things within radius of location."
        # if radius is None:
        #     radius = self.perceptible_distance
        things_list = [(thing, distance_m(location, thing.location), thing.location) for thing in self.things if not isinstance(thing, Agent)]
        # if distance_m(location, thing.location) <= radius2]
        return sorted(things_list, key=lambda tup: tup[1])

    def get_grid(self):
        grid =[]
        for x in range(self.width):
            row = []
            for y in range(self.height):
                row.append(self.list_things_at((x, y)))
            grid.append(row)
        return grid

    def is_inbounds(self, location):
        '''Checks to make sure that the location is inbounds (within walls if we have walls)'''
        x,y = location
        return not (x < self.x_start or x >= self.x_end or y < self.y_start or y >= self.y_end)

    def execute_action(self, agent, action):
        '''changes the state of the environment based on what the agent does.'''

        if action == "TURN":
            agent.Turn()
        elif action == "ADVANCE":
            agent.Advance()
    
    def is_done(self):
        '''The game is over when the Explorer is killed
            or if he climbs out of the cave only at (1,1)'''
        golds = [g for g in self.things if isinstance(g, Gold)]

        if not golds:
            return True

        return False

'''_____________________________________________________________________________________________'''

if __name__ == "__main__":
    grid = GridEnvironment()

    reflexAgent = ReflexAgent()
    grid.add_thing(reflexAgent, reflexAgent.location)

    gold = Gold()
    grid.add_thing(gold, (2,3))
    gold = Gold()
    grid.add_thing(gold, (3,4))
    # gold = Gold()
    # grid.add_thing(gold, (4,4))
    # gold = Gold()
    # grid.add_thing(gold, (2,3))

    trap = Trap()
    grid.add_thing(trap, (2,1))
    trap = Trap()
    grid.add_thing(trap, (1,3))
    trap = Trap()
    grid.add_thing(trap, (1,1))
    trap = Trap()
    grid.add_thing(trap, (3,4))
    trap = Trap()
    grid.add_thing(trap, (2,1))

    print('---------------------------')
    print('Original Grid')
    print('---------------------------')
    print("<STARTING>")
    print("Agent state: %s" % reflexAgent)
    print("Agent performance: %s" % reflexAgent.performance)
    print(grid)
    grid.run()

    print('---------------------------')
    print('Final Grid')
    print('---------------------------')
    print(grid)
    print(reflexAgent.performance)
    # print(reflexAgent.internal_state)