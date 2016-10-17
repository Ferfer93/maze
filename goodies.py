'''
    goodies.py

    Definitions for some example goodies
'''



import random


import numpy as np

from maze import Goody, Baddy, UP, DOWN, LEFT, RIGHT, STAY, PING

class StaticGoody(Goody):
    ''' A static goody - does not move from its initial position '''

    def take_turn(self, _obstruction, _ping_response):
        ''' Stay where we are '''
        return STAY

class RandomGoody(Goody):
    ''' A random-walking goody '''

    def take_turn(self, obstruction, _ping_response):
        ''' Ignore any ping information, just choose a random direction to walk in, or ping '''
        possibilities = filter(lambda direction: not obstruction[direction], [UP, DOWN, LEFT, RIGHT]) + [PING]
        return random.choice(possibilities)

class SimplePingEvadeGoody(Goody):
    ''' A goody that pings every other turn and runs away from the badguy '''

    def __init__(self):
        self.last_ping_response = None

    def take_turn(self, obstruction, _ping_response):
        if _ping_response is not None:
            self.last_ping_response = _ping_response
            self.turns_since_ping = 0
            for player in self.last_ping_response:
                posB = None
                posG = None
                if isinstance(player,Baddy):
                    posB = self.last_ping_response[player]
                else:
                    posG = self.last_ping_response[player]
                self.next_ping = min([int(0.5*sqrt(posB[0]**2+posB[1]**2)),int(0.5*sqrt(posG[0]**2+posG[1]**2))])
                self.last_BG_pos = posB - posG
        else:
            self.next_ping -= 1
            for player in self.last_ping_response:
                if isinstance(player,Goody):
                    self.last_G_pos = self.last_ping_response[player]
                else:
                    self.last_B_pos = self.last_ping_response[player]
                    
                    
        direction = self.strategy(obstruction)
        self.update_ping(direction)
        return direction

    def get_pos(self, target):
            if self.last_ping_response is None:
                return False
            else:
                for key in self.last_ping_response:
                    if isinstance(key, target):
                        return np.array(self.last_ping_response[key])

    def update_ping(self, direction):
        if self.last_ping_response is not None:
            self.last_ping_response -= direction_to_vector(direction)

        

    def strategy(self, obstruction):
        direction = self.get_pos(Baddy);
        if not direction:
            return PING
        else:
            reduced_directon = np.floor(direction/max(abs(direction)))
            if obstruction[reduced_direction]:
                reduced_directon = np.floor(direction/min(abs(direction)))
                if obstruction[reduced_direction]:
                    reduced_directon = -np.floor(direction/min(abs(direction)))
                    if obstruction[reduced_direction]:
                        reduced_directon = -np.floor(direction/max(abs(direction)))
                        if obstruction[reduced_direction]:
                            return STAY
                        else:
                            return reduced_direction
                    else:
                        return reduced_direction
                else:
                    return reduced_direction
            else:
                return reduced_direction
                

def direction_to_vector(direction):
    return {UP: np.array((0,1)),
            DOWN: np.array((0,-1)),
            LEFT: np.array((-1,0)),
            RIGHT: np.array((1,0)),
            PING: np.array((0,0)),
            STAY: np.array((0,0))}[direction]

def vector_to_direction(vector):
    if vector[0] == 1:
        assert vector[1] == 0
        return RIGHT
    elif vector[0] == -1:
        assert vector[1] == 0
        return LEFT
    elif vector[1] == 1:
        assert vector[0] == 0
        return UP
    elif vector[1] == -1:
        assert vector[0] == 0
        return DOWN
    else:
        raise ValueError('The vector must be a unit vector')
