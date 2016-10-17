'''
    goodies.py

    Definitions for some example goodies
'''



import random


import numpy as np

from math import sqrt

from maze import Goody, Baddy, UP, DOWN, LEFT, RIGHT, STAY, PING, ZERO, Position

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
    ''' A goody that tries to chase the 2nd goody, intercalating random movements
        as a way to avoid dead ends, and avoids the baddy when it's too close'''

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
        self.move_randomly = False
        self.steps_random = 0
        self.rec_pos = (0,0)

    def take_turn(self, obstruction, _ping_response):
        
        if self.initialized == True:
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
            #print posB
            self.next_ping = max([2,min([int(0.5*sqrt(posB.x**2+posB.y**2)),int(0.5*sqrt(posG.x**2+posG.y**2))])])
            self.last_BG_pos = posB - posG
            
        '''if self.last_G_pos.x == 1:
            return RIGHT
        elif self.last_G_pos.x == -1:
            return LEFT
        elif self.last_G_pos.y == 1:
            return UP
        elif self.last_G_pos.y == -1:
            return DOWN'''
                    
        if self.next_ping == 0:
            self.next_ping = 10
            return PING
        else:
            self.next_ping -= 1
                    
        if self.move_randomly:
            if self.steps_random > 0:
                self.steps_random -= 1
                possibilities = filter(lambda direction: not obstruction[direction], [UP, DOWN, LEFT, RIGHT])
                return random.choice(possibilities)
            else:
                self.move_randomly = False
        #print self.steps_random
        if self.last_B_pos.x**2 + self.last_B_pos.y**2 > 3:
            
            direction = self.s_chase(obstruction)
            self.curr_pos += direction
            
            if self.steps_staying == 0 and self.move_randomly == False:
                self.rec_pos = self.curr_pos
                self.steps_staying += 1
            if self.steps_staying > 0:
                self.steps_staying += 1
            if self.steps_staying == 10:
                #print 'asdf'
                if abs(self.curr_pos[0]-self.rec_pos[0])+abs(self.curr_pos[1]-self.rec_pos[1]) < 5:
                    self.move_randomly = True
                    self.steps_random = 5
                    self.steps_staying = 0
            #print 'asdf'
            return vector_to_direction(direction)
        else:
            possibilities = filter(lambda direction: not obstruction[direction], [UP, DOWN, LEFT, RIGHT])
            possibilities.append(STAY)
            distances = [distance(move_to_location(possibility), self.last_B_pos)
                          for possibility in possibilities]
            return possibilities[distances.index(max(distances))]
        
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
            
            
    def s_chase(self, obstruction):
        #chase G only if B is further
        diag_G_x = self.last_G_pos.x + self.last_G_pos.y
        diag_G_y = self.last_G_pos.x - self.last_G_pos.y
        if diag_G_x >= 0 and diag_G_y <= 0:
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
        elif diag_G_x >= 0 and diag_G_y >= 0:
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
        elif diag_G_x <= 0 and diag_G_y >= 0:
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
        elif diag_G_x <= 0 and diag_G_y <= 0:
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
            prod_list(self.knownmat,self.rec_list,self.curr_pos,self.knownmat,self.last_G_pos)
        
def prod_list(mat,moves,position,pathmat,goal):
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
    
def distance(position1, position2):
    ''' Find distance between two points '''
    return (abs(position1.x - position2.x) +  abs(position1.y - position2.y))

def move_to_location(move):
    ''' This maps a 'move' label to an x and y increment. '''
    mapper = {
        STAY  : ZERO,
        LEFT  : Position(-1, 0),
        RIGHT : Position(1, 0),
        UP    : Position(0, 1),
        DOWN  : Position(0, -1)}
    return mapper[move]
