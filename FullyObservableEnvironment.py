import numpy as np
import random

from ReflexAgent import ReflexAgent
from ModelBasedAgent import ModelBasedAgent
from agents import *
from Objects import *

class FullyObservableEnvironment(Environment):
    '''Creates a FullyObservableEnvironment as a subclass of Environment'''
    def __init__(self, width=5, height=5, radius=4):
        super(FullyObservableEnvironment, self).__init__()
        self.width = width
        self.height = height
        self.radius_of_vision = radius

    def __str__(self):
        grid = self.get_grid()
        gridStr = []
        gridStr.append('     0       1       2       3       4')
        gridStr.append('  (A G T) (A G T) (A G T) (A G T) (A G T)')
        for r in range(self.width):
            row = ''
            row += str(r)+' '
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
        print('---------------------------')
        print('Initial State')
        print('---------------------------')
        
        print(self)

        for agent in self.agents:
            percepts = self.percept(agent)

            if isinstance(agent, ModelBasedAgent):
                agent.update_internal_state(percepts, self.radius_of_vision)

            self.print_agent_percept(agent, percepts)

            if isinstance(agent, ModelBasedAgent):
                agent.print_internal_state()
                print('')

            print("Agent state: %s" % agent)
            print("Agent performance: %s" % agent.performance)
            print('')
        
        

        print('---------------------------')
        print('Run details')
        print('---------------------------')
        i = 1
        for step in range(steps):
            if self.is_done():
                return
            print('<STEP %s>' % i)
            self.step()
            i += 1
    
    def get_grid(self):
        grid =[]
        for x in range(self.width):
            row = []
            for y in range(self.height):
                row.append(self.list_things_at((x, y)))
            grid.append(row)
        return grid

    def default_location(self, thing):
        return (random.randint(0, self.width-1), random.randint(0, self.width-1))

    def is_done(self):
        golds = [g for g in self.things if isinstance(g, Gold)]

        if not golds:
            return True

        return False         

    def percept(self, agent):
        things_list = [(thing, distance_m(agent.location, thing.location), thing.location) for thing in self.things if not isinstance(thing, Agent)]
        sorted_things = sorted(things_list, key=lambda tup: tup[1])
        return sorted_things

    def execute_action(self, agent, action):
        '''changes the state of the environment based on what the agent does.'''

        if action == "TURN":
            agent.turn_clockwise()
        elif action == "ADVANCE":
            agent.move_forward()
        elif action == "STAY":
            pass
                
        things = self.list_things_at(agent.location)
        golds = [g for g in things if isinstance(g, Gold)]
        traps = [t for t in things if isinstance(t, Trap)]

        if golds:
            agent.get_gold()
            self.delete_thing(golds[0])
                
        if traps:
            agent.fall_in_trap()
            self.delete_thing(traps[0])

        print("SELECTED ACTION: ", action)
        print("Agent state: ", agent)
        print("Agent performance: %s" % agent.performance)

        print('\nEnvironment: ')
        print(self)

        percepts = self.percept(agent)

        if isinstance(agent, ModelBasedAgent):
            agent.update_internal_state(percepts, self.radius_of_vision)

        self.print_agent_percept(agent, percepts)

        if isinstance(agent, ModelBasedAgent):
            agent.print_internal_state()
            print('')

    def print_agent_percept(self, agent, percepts):
        pass