import numpy as np
import random

from FullyObservableEnvironment import FullyObservableEnvironment
from PartiallyObservableEnvironment import PartiallyObservableEnvironment
from ReflexAgent import ReflexAgent
from ModelBasedAgent import ModelBasedAgent
from Objects import *



if __name__ == "__main__":
    environment = PartiallyObservableEnvironment()

    agent = ReflexAgent()
    environment.add_thing(agent)

    for _ in range(10):
        gold = Gold()
        environment.add_thing(gold)

    for _ in range(10):
        trap = Trap()
        environment.add_thing(trap)    

    # print('---------------------------')
    # print('Initial State of Environment')
    # print('---------------------------')
    # print("Agent state: %s" % agent)
    # print("Agent performance: %s" % agent.performance)
    # print('')
    # print('Environment:')
    # print(environment)

    environment.run()