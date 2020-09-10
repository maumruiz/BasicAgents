import numpy as np

from ReflexAgent import ReflexAgent
from agents import *
from Objects import *

class ModelBasedAgent(Agent):
    '''
    Initializes the Agent's variables. Every Agent starts being alive with a performance of 100 and facing the right direction.
    '''
    def __init__(self):
        self.location = (0,0)
        self.direction = 'R'
        self.performance = 100
        self.alive = True

        '''Initialized the Agent's internal state which will be more helpful in case of a Partially Observable Enrivonment'''
        self.internal_state = [[{'Visited': -1, 'Gold': -1, 'Traps': -1} for row in range(5)] for col in range(5)]
    
    def __str__(self):
        '''Prints the internal state of the agent'''
        facing = {'U': 'UP', 'R': 'RIGHT', 'D': 'DOWN', 'L': 'LEFT'}
        return "(%s, %s, %s)" % (self.location[0], self.location[1], facing[self.direction])
    
    def print_internal_state(self):
        '''
        Show the actual internal state of the Agent, with information about the visited cells, gold and traps discovered by previous steps.
        '''
        print('Agent internal state:')
        print('     0       1       2       3       4')
        print('  (A G T) (A G T) (A G T) (A G T) (A G T)')
        for r in range(len(self.internal_state)):
            row = '%s ' % r
            row2 = ''
            for c in range(len(self.internal_state[r])):
                visited = '?' if self.internal_state[r][c]['Visited'] < 0 else '-' if self.internal_state[r][c]['Visited'] == 0 else 'V'
                golds = '?' if self.internal_state[r][c]['Gold'] < 0 else '-' if self.internal_state[r][c]['Gold'] == 0 else self.internal_state[r][c]['Gold']
                traps = '?' if self.internal_state[r][c]['Traps'] < 0 else '-' if self.internal_state[r][c]['Traps'] == 0 else self.internal_state[r][c]['Traps']
                
                row += '(%s %s %s) ' % (visited, golds, traps)
                row2 +='(%s %s %s) ' % (self.internal_state[r][c]['Visited'], self.internal_state[r][c]['Gold'], self.internal_state[r][c]['Traps'])
            print(row)

    def print_percepts(self, percept, radius):
        '''
        Receives a list of percepts around the player and show them in a grid form.
        '''
        print("Percept:")
        
        x, y = self.location

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

                        cellGold = self.internal_state[x+r][y+c]['Gold']
                        gold = '-' if cellGold < 1 else cellGold

                        cellTraps = self.internal_state[x+r][y+c]['Traps']
                        traps = '-' if cellTraps < 1 else cellTraps

                        row += '(%s %s %s) ' % (agentState, gold, traps)
                    
                print(row)
        print('')
    
    '''Action when the agent enters a cell with a gold'''
    def get_gold(self):
        '''Gives 10 point from the agent'''
        self.performance += 10

    '''Action when the agent falls into a trap'''
    def fall_in_trap(self):
        '''Takes 5 points from the agent'''
        self.performance -= 5

    '''State when the agent recieve the action to turn'''
    def turn_clockwise(self):
        '''Reduces 1 point from the agent'''
        self.performance -= 1
        
        '''Turns its direction clockwise'''
        turns = {'U': 'R', 'R': 'D', 'D': 'L', 'L': 'U'}
        self.direction = turns[self.direction]

    '''State when the agent recieve the action to advance'''
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
        if self.internal_state[r][c]['Visited'] == 1:
            self.performance -= 2

    def is_inbounds(self, location):
        '''Checks to make sure that the location is inbounds (within walls if we have walls)'''
        x,y = location
        return not (x < 0 or x >= 5 or y < 0 or y >= 5)
    
    # Update the internal state of the agent, with the new information after executing an action
    def update_internal_state(self, percepts, radius=4):
        
        x, y = self.location
        near_locations = []

        # Find the locations where the agent need to update its internal state
        for r in range(-radius, radius+1):
            for c in range(-radius, radius+1):
                near_locations.append((x+r, y+c))

        # Delete internal state in percept radious
        for loc in near_locations:
            if self.is_inbounds(loc):
                cell = self.internal_state[loc[0]][loc[1]]
                cell['Gold'] = 0
                cell['Traps'] = 0

                if cell['Visited'] == -1:
                    cell['Visited'] = 0
        
        # Update internal state in percept radious
        for percept in percepts:
            xPercept, yPercept = percept[2]
            if isinstance(percept[0], Trap):
                self.internal_state[xPercept][yPercept]['Traps'] += 1
            if isinstance(percept[0], Gold):
                self.internal_state[xPercept][yPercept]['Gold'] += 1
        
        # Mark the current agent location as visited
        self.internal_state[x][y]['Visited'] = 1
    
    def program(self, percepts):
        '''Reads the percept and returns the action'''

        golds = [p for p in percepts if isinstance(p[0], Gold)]

        # If there is no gold, look in the internal state for gold
        if len(golds) < 1:
            golds = []
            for row in range(len(self.internal_state)):
                for column in range(len(self.internal_state[0])):
                    if self.internal_state[row][column]['Gold'] > 0:
                        distance = distance_m((row, column), self.location)
                        golds.append(((row,column), distance, (row,column)))
            
            # Sort gold by distance
            golds = sorted(golds, key=lambda tup: tup[1])

        # If there is still no gold found, take default behaviour
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