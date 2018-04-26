import sys
import numpy as np

class Queue:


    #constructor
    def __init__(self, tL, cL):
        self.currentLeng = cL
        self.totalLeng = tL

    #enqueue with probability
    def en(self):
        self.currentLeng = self.currentLeng + 1
        if self.currentLeng > self.totalLeng:
            self.currentLeng = self.totalLeng


    #dequeue with probability
    def de(self):
            self.currentLeng = self.currentLeng - 1
            if self.currentLeng < 0:
                self.currentLeng = 0
