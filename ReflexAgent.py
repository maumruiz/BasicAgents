import numpy as np

from agents import *
from Objects import *

class ReflexAgent(Agent):
    '''
    Initializes the Agent's variables. Every Agent starts being alive with a performance of 100 and facing the right direction.
    '''
    def __init__(self):
        self.location = (0,0)
        self.direction = 'R'
        self.performance = 100
        self.alive = True

        '''Declares the internal state to register the visited cells into the performance, which will only work to
            penalize if it moves to a previously visited cell'''
        self.visited_cells = np.full((5, 5), False)
        self.visited_cells[self.location[0]][self.location[1]] = True

    def __str__(self):
        '''Prints the internal state of the agent'''
        facing = {'U': 'UP', 'R': 'RIGHT', 'D': 'DOWN', 'L': 'LEFT'}
        return "(%s, %s, %s)" % (self.location[0], self.location[1], facing[self.direction])

    def print_percepts(self, percepts, radius):
        '''
        Receives a list of percepts around the player and show them.
        '''
        print("Percept")
        
        x, y = self.location

        '''Gets all the gold perceived around the player'''
        gold_grid = [[0 for row in range(5)] for col in range(5)]
        '''Gets all the traps perceived around the player'''
        traps_grid = [[0 for row in range(5)] for col in range(5)]

        for percept in percepts:
            xPercept, yPercept = percept[2]
            if isinstance(percept[0], Trap):
                traps_grid[xPercept][yPercept] += 1
            if isinstance(percept[0], Gold):
                gold_grid[xPercept][yPercept] += 1

        row = '  '
        for c in range(-radius, radius+1):
            if self.is_inbounds((0, y+c)):
                row += '   %s    ' % (y+c)                    
        print(row)

        for r in range(-radius, radius+1):
            if self.is_inbounds((x+r, 0)):
                row = '%s ' % (x+r)
            
                for c in range(-radius, radius+1):
                    if self.is_inbounds((x+r, y+c)):
                        agentState = '-' if x != x+r or y != y+c else self.direction

                        cellGold = gold_grid[x+r][y+c]
                        gold = '-' if cellGold < 1 else cellGold

                        cellTraps = traps_grid[x+r][y+c]
                        traps = '-' if cellTraps < 1 else cellTraps

                        row += '(%s %s %s) ' % (agentState, gold, traps)
                    
                print(row)
        print('')

    def is_inbounds(self, location):
        '''Checks to make sure that the location is inbounds'''
        x,y = location
        return not (x < 0 or x >= 5 or y < 0 or y >= 5)
    
    def get_gold(self):
        '''States when the agent enters a cell with a gold'''
        self.performance += 10

    def fall_in_trap(self):
        '''Takes 5 points from the agent when the agent enter a cell with traps'''
        self.performance -= 5

    def turn_clockwise(self):
        '''States when the agent turns. 
        Reduces 1 point from the agent'''
        self.performance -= 1
        
        '''Turns its direction clockwise'''
        turns = {'U': 'R', 'R': 'D', 'D': 'L', 'L': 'U'}
        self.direction = turns[self.direction]

    def move_forward(self):
        '''Reduces 1 point from the agent'''
        self.performance -= 1

        '''Advances in the direction of the agent'''
        '''And checks that the agents does not move outside the grid'''
        r = self.location[0]
        c = self.location[1]

        if self.direction == "U" and r != 0:
            r = r-1
        elif self.direction == "R" and c != 4:
            c = c+1
        elif self.direction == "D" and r != 4:
            r = r+1
        elif self.direction == "L" and c != 0:
            c = c-1
        self.location = (r, c)

        '''Reduces the performance if the agent enters a visited cell'''
        if self.visited_cells[r][c]:
            self.performance -= 2
        else:
            self.visited_cells[r][c] = True
    
    def program(self, percepts):
        '''Reads the percept and returns the action'''
        golds = [p for p in percepts if isinstance(p[0], Gold)]

        if len(golds) < 1:
            r = self.location[0]
            c = self.location[1]
            
            if self.direction == 'U' and r > 1:
                return 'ADVANCE'
            elif self.direction == 'R' and c < 3:
                return 'ADVANCE'
            elif self.direction == 'D' and r < 3:
                return 'ADVANCE'
            elif self.direction == 'L' and c > 1:
                return 'ADVANCE'

            return 'TURN'
        

        state = golds[0]
        rGold = state[2][0] 
        cGold = state[2][1]
        rAgent = self.location[0]
        cAgent = self.location[1]

        # If there is gold in the current location, stay
        if cGold == cAgent and rGold == rAgent:
            return 'STAY'
        
        # TODO: Agregar que si esta en linea con la dirección, se mueva adelante

        # Check if the percepted gold is in front of the agent
        if self.direction == 'U' and rGold < rAgent and cGold >= cAgent:
            return 'ADVANCE'
        elif self.direction == 'R' and rGold >= rAgent and cGold > cAgent:
            return 'ADVANCE'
        elif self.direction == 'D' and rGold > rAgent and cGold <= cAgent:
            return 'ADVANCE'
        elif self.direction == 'L' and rGold <= rAgent and cGold < cAgent:
            return 'ADVANCE'

        return 'TURN'