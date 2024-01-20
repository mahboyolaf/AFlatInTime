import pygame
import random
from constants import *
from GameSprite import *
# sprites
# direction of speed
# direction facing
# max speeds
# key inputs
# conditions to start and stop
# flags (states)
# acceleration
# sound effects
class Movement():
    def __init__(self):
        self.MAXXSPEED=3
        self.MAXYSPEED=7.5
        self.X_ACCELERATION=0.1
        self.x_speed = 0
        self.y_speed=0
        self.canjump= True
        self.has_jumped_in_air= False

    def start(self):
        print ("started",self.__class__.__name__)
    def end(self):
        print ("ended",self.__class__.__name__)

    def y_acceleration(self):
        #if self.y_speed <= MAXYSPEED:
        print ("y acceleration",self.__class__.__name__)
    def x_acceleration(self):
        #if self.y_speed <= MAXXSPEED:
        print ("x acceleration",self.__class__.__name__)

    def x_speed(self):
        #x_speed=
        print("x speed",self.__class__.__name__)
    def y_speed(self):
        #y_speed=
        print("y speed",self.__class__.__name__)
    

class Walk(Movement):
    def __init__(self):
        super().__init__()
        self.spritedir="sprite/HatKid/walk/walk"
        direction=None
        self.sprites_right=self.load_sprites()
            
        self.sprites_left=tuple([pygame.transform.flip(sprite,True,False) for sprite in self.sprites_right])

    def load_sprites(self):
        """
        imports walking sprites
        gets: file location of sprites, if flip or not
        returns: tuple of walk sprites
        """
        walks=[]
        for counter in range (1,5):
            walk= pygame.image.load(self.spritedir+str(counter)+".png")
            walk=pygame.transform.scale(walk,HATKIDSIZEWALK)
            walks.append(walk)
        return tuple(walks)

