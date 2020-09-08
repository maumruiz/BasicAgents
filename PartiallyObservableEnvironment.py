import numpy as np

from FullyObservableEnvironment import FullyObservableEnvironment
from ModelBasedAgent import ModelBasedAgent
from agents import *
from Objects import *

class PartiallyObservableEnvironment(FullyObservableEnvironment):
    def __init__(self):
        FullyObservableEnvironment.__init__(self)
        self.radius_of_vision = 1

    def percept(self, agent):
        '''Only perceive near things'''
        x, y = agent.location
        near_locations = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
        things_near = []

        for loc in near_locations:
            things_near += self.percepts_from(agent, loc)
      
        return things_near
    
    def percepts_from(self, agent, location, tclass=Thing):
        things = self.list_things_at((location[0], location[1]))
        percepts = [(p, distance_m(agent.location, p.location), p.location) for p in things if not isinstance(p, Agent)]
        return percepts

    def print_agent_percept(self, agent, percepts):
        agent.print_percepts(percepts, self.radius_of_vision)
