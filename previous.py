import numpy as np

class ModelAgent(Agent):
    pass
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
        self.internal_state = [[{'Visited': -1, 'Gold': -1, 'Traps': -1} for row in range(5)] for col in range(5)]
        self.internal_state[self.location[0]][self.location[1]]['Visited'] = 1

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

    def print_internal_state(self):
        print('Agent internal state')
        for r in range(len(self.internal_state)):
            row = ''
            row2 = ''
            for c in range(len(self.internal_state[r])):
                visited = '?' if self.internal_state[r][c]['Visited'] < 0 else '-' if self.internal_state[r][c]['Visited'] == 0 else 'V'
                golds = '?' if self.internal_state[r][c]['Gold'] < 0 else '-' if self.internal_state[r][c]['Gold'] == 0 else self.internal_state[r][c]['Gold']
                traps = '?' if self.internal_state[r][c]['Traps'] < 0 else '-' if self.internal_state[r][c]['Traps'] == 0 else self.internal_state[r][c]['Traps']

                row += '(%s %s %s) ' % (visited, golds, traps)
                row2 +='(%s %s %s) ' % (self.internal_state[r][c]['Visited'], self.internal_state[r][c]['Gold'], self.internal_state[r][c]['Traps'])
            print(row)
            ##print(row2)
        pass

    def print_percepts(self, percept):
        print("Percept")
        percept_distance=1
        for row in range(self.location[0]+percept_distance*-1, self.location[0]+percept_distance):
            for column in range(self.location[1]+percept_distance*-1, self.location[1]+percept_distance):
                agent = '-'
                gold = '-'
                trap = '-'
                if self.location[0]==row and self.location[1]==column:
                    agent = self.direction
                else:
                    if self.internal_state[row][column]['Gold']>0:
                        gold = self.internal_state[row][column]['Gold']
                    if self.internal_state[row][column]['Traps']>0:
                        trap = self.internal_state[row][column]['Traps']

                print('%s %s %s' % (agent, gold, trap))

    '''States when the agent enters a cell with a gold'''
    def PickGold(self):
        '''Gives 10 point from the agent'''
        self.performance += 10
        self.internal_state[self.location[0]][self.location[1]]['Gold'] -= 1
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
                tupleList[1] = tupleList[1]+1
        elif self.direction == "D":
            if tupleList[0] != 4:
                tupleList[0] = tupleList[0]+1
        elif self.direction == "L":
            if tupleList[1] != 0:
                tupleList[1] = tupleList[1]-1
        self.location = tuple(tupleList)

        '''Reduces the performance if the agent enters a visited cell'''
        if self.internal_state[self.location[0]][self.location[1]]['Visited'] == 1:
            self.performance -= 2
        else:
            self.internal_state[self.location[0]][self.location[1]]['Visited'] = 1
        # print("Advance")

    def FallInTrap(self):
        '''Takes 5 points from the agent'''
        self.performance -= 5
        self.internal_state[self.location[0]][self.location[1]]['Traps'] -= 1
        # print("Fall in Trap")

    def update_internal_state(self, percepts):
        # Delete internal state in percept radious
        for percept in percepts:
            self.internal_state[percept[2][0]][percept[2][1]]['Gold'] = 0
            self.internal_state[percept[2][0]][percept[2][1]]['Traps'] = 0
            if self.internal_state[percept[2][0]][percept[2][1]]['Visited'] == -1:
                self.internal_state[percept[2][0]][percept[2][1]]['Visited'] = 0

        # Update internal state in percept radious
        for percept in percepts:
            if isinstance(percept, Trap):
                self.internal_state[percept.location[0]][percept.location[1]]['Traps'] += 1
            if isinstance(percept, Gold):
                self.internal_state[percept.location[0]][percept.location[1]]['Gold'] += 1



    def program(self, percepts):
        '''Reads the percept and returns the action'''
        self.update_internal_state(percepts)

        golds = [p for p in percepts if isinstance(p[0], Gold)]
        if len(golds) < 1:
            golds = []
            for row in range(self.internal_state.shape[0]):
                for column in range(self.internal_state.shape[1]):
                    if self.internal_state[row][column]['Gold'] > 0:
                        distance = distance_m((row, column), self.location)
                        golds.append(((row,column), distance, (row,column)))

            # sort by distance
            golds = sorted(golds, key=lambda tup: tup[1])

        state = golds[0]
        xGold = state[2][0] 
        yGold = state[2][1]
        xAgent = self.location[0]
        yAgent = self.location[1]

        # If is in line
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

            #Default move
        return ['TURN','ADVANCE'][random.randint(0,1)]
            # return 'TURN'


class ReflexAgent(Agent):
@@ -88,7 +273,7 @@ def Advance(self):

        '''Reduces the performance if the agent enters a visited cell'''
        if self.internal_state[self.location[0]][self.location[1]]:
            self.performance -= 1
            self.performance -= 2
        else:
            self.internal_state[self.location[0]][self.location[1]] = True
        # print("Advance")
@@ -208,13 +393,131 @@ def step(self):
                    self.delete_thing(traps[0])

                print(self)
                agent.print_internal_state()
                print("Agent performance: %s" % agent.performance)



    def percept(self, agent):
        '''By default, agent perceives things within a default radius.'''
        return self.things_near(agent.location)
        things_near = self.things_near(agent.location)        
        return things_near


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


''' ................................................. '''
class PartiallyObservableEnvironment(Environment):
    def __init__(self, width=5, height=5):
        super(GridEnvironment, self).__init__()
        self.width = width
        self.height = height
        self.x_start, self.y_start = (0, 0)
        self.x_end, self.y_end = (self.width, self.height)
        self.perceptible_distance = 1   

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
        things_near = self.things_near(agent.location)        
        return things_near


    def things_near(self, location, radius=None):
@@ -262,8 +565,11 @@ def is_done(self):
if __name__ == "__main__":
    grid = GridEnvironment()

    reflexAgent = ReflexAgent()
    grid.add_thing(reflexAgent, reflexAgent.location)
    # reflexAgent = ReflexAgent()
    # grid.add_thing(reflexAgent, reflexAgent.location)

    modelAgent = ModelAgent()
    grid.add_thing(modelAgent, modelAgent.location)

    gold = Gold()
    grid.add_thing(gold, (2,3))
@@ -289,14 +595,14 @@ def is_done(self):
    print('Original Grid')
    print('---------------------------')
    print("<STARTING>")
    print("Agent state: %s" % reflexAgent)
    print("Agent performance: %s" % reflexAgent.performance)
    print("Agent state: %s" % modelAgent)
    print("Agent performance: %s" % modelAgent.performance)
    print(grid)
    grid.run()

    print('---------------------------')
    print('Final Grid')
    print('---------------------------')
    print(grid)
    print(reflexAgent.performance)
    print(modelAgent.performance)
    # print(reflexAgent.internal_state) 