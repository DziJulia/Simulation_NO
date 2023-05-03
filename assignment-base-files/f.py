import random # need a random number generator
import time
from simanneal import Annealer # import the annealler from the sim anneal library

from NewSimulation import Simulation1
from simulation import Simulation


class CryptoAnneal(Annealer):
    def __init__(self, weights , totalNetValue, closing_values, name):
        self.weights = weights
        self.name = name
        self.totalNetValue = totalNetValue
        self.closing_values = closing_values
        super(CryptoAnneal, self).__init__(weights) # annealer needs the initial list of name

    def move(self):
        # pick two cities that we will swap
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        temp = self.state[a]
        self.state[a] = self.state[b]
        self.state[b] = temp

        #time.sleep(0.01)

    def energy(self):
        total =0
        for i in range(0, len(self.state) - 1):
            simulation = Simulation1(self.closing_values, self.state)
            simulation.simulate()
            total += simulation.totalNetValue()
        return total






