'''
    goodies.py

    Definitions for some example goodies
'''



import random


import numpy as np

from math import sqrt

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

class OurGoody(Goody):
    ''' A goody that pings every other turn and runs away from the badguy '''

    def __init__(self):
        self.last_ping_response = None
        self.next_ping = 0
        self.last_B_pos = None
        self.last_G_pos = None
        self.last_BG_pos = None
        self.initialized = True
        self.knownmat = np.zeros((100,100))
        self.curr_pos = (0,0)
        self.steps_staying = 0
        self.rec_list = []

    def take_turn(self, obstruction, _ping_response):
        
        #Include obstructions
        if obstruction[UP]:
            self.knownmat[self.curr_pos[0]][self.curr_pos[1]+1] = 1
        else:
            self.knownmat[self.curr_pos[0]][self.curr_pos[1]+1] = -1
        if obstruction[DOWN]:
            self.knownmat[self.curr_pos[0]][self.curr_pos[1]-1] = 1
        else:
            self.knownmat[self.curr_pos[0]][self.curr_pos[1]-1] = -1
        if obstruction[RIGHT]:
            self.knownmat[self.curr_pos[0]+1][self.curr_pos[1]] = 1
        else:
            self.knownmat[self.curr_pos[0]+1][self.curr_pos[1]] = -1
        if obstruction[LEFT]:
            self.knownmat[self.curr_pos[0]-1][self.curr_pos[1]] = 1
        else:
            self.knownmat[self.curr_pos[0]-1][self.curr_pos[1]] = -1
        
        if self.initialized:
            self.initialized = False
            return PING
        
        if _ping_response is not None:
            self.last_ping_response = _ping_response
            self.turns_since_ping = 0
            posB = None
            posG = None
            for player in self.last_ping_response:
                if isinstance(player,Baddy):
                    posB = self.last_ping_response[player]
                    self.last_B_pos = self.last_ping_response[player]
                else:
                    posG = self.last_ping_response[player]
                    self.last_G_pos = self.last_ping_response[player]
            print posB
            self.next_ping = min([int(0.5*sqrt(posB.x**2+posB.y**2)),int(0.5*sqrt(posG.x**2+posG.y**2))])
            self.last_BG_pos = posB - posG
        else:
            self.next_ping -= 1
                    
        if self.next_ping == 0:
            return PING
                    
        if self.last_B_pos.x**2 + self.last_B_pos.y**2 > self.last_G_pos.x**2 + self.last_G_pos.y**2 or 1 == 1:
            direction = self.s_chase(obstruction)
            self.curr_pos += direction
            if vector_to_direction(direction) == STAY:
                self.steps_staying += 1
            return vector_to_direction(direction)
        else:
            direction = self.strategy(obstruction)
            #self.update_ping(direction)
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
            
            
    def s_chase(self, obstruction):
        #chase G only if B is further
        diag_G_x = self.last_G_pos.x + self.last_G_pos.y
        diag_G_y = self.last_G_pos.x - self.last_G_pos.y
        if diag_G_x > 0 and diag_G_y < 0:
            if not obstruction[UP]:
                return np.array((0,1))
            else:
                if np.random.randint(0,2) == 0:
                    if not obstruction[LEFT]:
                        return np.array((-1,0))
                    elif not obstruction[RIGHT]:
                        return np.array((1,0))
                else:
                    if not obstruction[RIGHT]:
                        return np.array((1,0))
                    elif not obstruction[LEFT]:
                        return np.array((-1,0))
                return np.array((0,0))
        elif diag_G_x > 0 and diag_G_y > 0:
            #G is right
            if not obstruction[RIGHT]:
                return np.array((1,0))
            else:
                if np.random.randint(0,2) == 0:
                    if not obstruction[UP]:
                        return np.array((0,1))
                    elif not obstruction[DOWN]:
                        return np.array((0,-1))
                else:
                    if not obstruction[DOWN]:
                        return np.array((0,-1))
                    elif not obstruction[UP]:
                        return np.array((0,1))
                return np.array((0,0))
        elif diag_G_x < 0 and diag_G_y > 0:
            #G is down
            if not obstruction[DOWN]:
                return np.array((0,-1))
            else:
                if np.random.randint(0,2) == 0:
                    if not obstruction[LEFT]:
                        return np.array((-1,0))
                    elif not obstruction[RIGHT]:
                        return np.array((1,0))
                else:
                    if not obstruction[RIGHT]:
                        return np.array((1,0))
                    elif not obstruction[LEFT]:
                        return np.array((-1,0))
                return np.array((0,0))
        elif diag_G_x < 0 and diag_G_y < 0:
            #G is left
            if not obstruction[LEFT]:
                return np.array((-1,0))
            else:
                if np.random.randint(0,2) == 0:
                    if not obstruction[UP]:
                        return np.array((0,1))
                    elif not obstruction[DOWN]:
                        return np.array((0,-1))
                else:
                    if not obstruction[DOWN]:
                        return np.array((0,-1))
                    elif not obstruction[UP]:
                        return np.array((1,0))
                return np.array((0,0))
        else:
            return np.array((0,0))
        
        
    def rec_list(self):
        if len(self.rec_list) != 0:
            return self.rec_list.pop(0)
        else:
            self.rec_list = []
            prod_list(self.knownmat,self.rec_list,self.curr_pos,self.knownmat)
        
def prod_list(mat,moves,position,pathmat):
    ##do nothing
    return None
    
               
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
        return STAY
        raise ValueError('The vector must be a unit vector')
