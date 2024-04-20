import pygame
import random
import time
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
    class Direction():
        LEFT="left"
        RIGHT="right"
    def __init__(self,map,hatkid):
        self.MAXXSPEED=3
        self.MAXYSPEED=7.5
        self.X_ACCELERATION=0.1
        self.x_speed = 0
        self.y_speed=0
        self.has_jumped_in_air= False
        self.map=map
        self.hatkid=hatkid

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
    def is_on_ground(self):
        """returns true if tiles under"""
        return len(self.tilesunder())>0
    def tilesunder(self):
        """return a list of tiles below the kid"""
        checkahead=self.MAXYSPEED
        self.hatkid.rect.move_ip([0,checkahead])
        hitlist=pygame.sprite.spritecollide(self.hatkid,self.map.tiles,False)
        self.hatkid.rect.move_ip([0,-checkahead])
        return hitlist

class Jump(Movement):
    def __init__(self,map,hatkid):
        super().__init__(map,hatkid)
        self.direction=None
        self.map=map
        self.count=0

    def start(self):
        self.count+=1
        self.hatkid.canjump= False
        if self.hatkid.is_on_ground:
        #jump sfx
            randomnumber=random.randint(0,13)
            JUMP_SFX[randomnumber].play()
            self.hatkid.y_speed= -MAXYSPEED
        elif not self.hatkid.has_jumped_in_air:
        #doublejuump sfx
            randomnumber=random.randint(0,1)
            DOUBLE_JUMP_SFX[randomnumber].play()
            self.hatkid.has_jumped_in_air=True
            self.hatkid.y_speed= -MAXYSPEED
            if pygame.key.get_pressed()[pygame.K_d] and not self.hatkid.tilesright(self.map) and not pygame.key.get_pressed()[pygame.K_a]:
                self.hatkid.x_speed=MAXXSPEED 
            elif pygame.key.get_pressed()[pygame.K_a] and not self.hatkid.tilesleft(self.map) and not pygame.key.get_pressed()[pygame.K_d]:
                self.hatkid.x_speed=-MAXXSPEED

    def can(self,reset=None):
        """returns true if can jump"""
        if reset!=None:
            return reset
        else:
            print (self.is_on_ground(), self.count < 2, self.hatkid.tilesabove(self.map))
            return  self.count < 2 and not self.hatkid.tilesabove(self.map)
        
    
        

class Walk(Movement):
    def __init__(self,map,hatkid):
        super().__init__(map,hatkid)
        self.spritedir="sprite/HatKid/walk/walk"
        self.direction=None
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
    def can(self):
        """returns true if can walk"""
        return self.is_on_ground()
    def start(self):
        """starts walking movement"""
        direction_multiplier=None
        if self.direction==Movement.Direction.RIGHT:
            self.hatkid.current_frame=self.hatkid.walkright[self.get_sprite_index()]
            direction_multiplier=1
        elif self.direction==Movement.Direction.LEFT:
            self.hatkid.current_frame=self.hatkid.walkleft[self.get_sprite_index()]
            direction_multiplier=-1
        if abs(self.hatkid.x_speed)<self.MAXXSPEED:
            #accelerate
            self.hatkid.x_speed=self.hatkid.x_speed+(self.X_ACCELERATION*direction_multiplier)
        
        else:
            #keep at max speed
            self.hatkid.x_speed= (self.MAXXSPEED*direction_multiplier)

    def get_sprite_index(self):
        if self.hatkid.walk_index > 4-1/15:
            self.hatkid.walk_index = 0
        else:
            self.hatkid.walk_index += 1/15
        return int(self.hatkid.walk_index)

    def set_direction(self,direction):
        """set walking direction"""
        self.direction=direction
        self.hatkid.direction=self.direction
    
    def stop(self):
        """stops walking movement with decelerate"""
        if abs(self.hatkid.x_speed)> 0.1:
            self.hatkid.x_speed *= 0.9
        else:
            self.hatkid.x_speed=0
            if self.hatkid.direction==Movement.Direction.RIGHT:
                self.hatkid.current_frame=self.hatkid.idleright[0]
            elif self.hatkid.direction==Movement.Direction.LEFT:
                self.hatkid.current_frame=self.hatkid.idleleft[0]

class Dive(Movement):
    def __init__(self,map,hatkid):
        super().__init__(map,hatkid)
        self.diveright=self.load("sprite/HatKid/dive",Movement.Direction.RIGHT)
        self.diveleft=self.load("sprite/HatKid/dive",Movement.Direction.LEFT)
        self.in_progress=False
        self.has_dived=False
        self.timestart=time.time()  
    def load(self,spritedir,direction):
        dives=[]
        for counter in range (1,3):
            dive= pygame.image.load(spritedir+"/dive"+str(counter)+".png")
            dive=pygame.transform.scale(dive,HATKIDSIZEDIVE)
            if direction==Movement.Direction.LEFT:
                dive=pygame.transform.flip(dive,True,False)
            dives.append(dive)
        return tuple(dives)
    
    def start(self):
        self.in_progress=True
        if self.has_dived==False:
            self.timestart=time.time()            
            if self.hatkid.is_on_ground:
                if pygame.key.get_pressed()[pygame.K_d]:
                    print("right ground dive")
                    self.x_speed=MAXXSPEED+3
                    self.hatkid.rect.y-=10
                    self.has_dived=True
                if pygame.key.get_pressed()[pygame.K_a]:
                    print("left ground dive")
                    self.hatkid.x_speed=-(MAXXSPEED+3)
                    self.hatkid.rect.y-=10
                    self.has_dived=True
            else:
                if self.hatkid.direction== Movement.Direction.RIGHT:
                    print("right air dive")
                    self.x_speed=MAXXSPEED+3
                    self.has_dived=True
                if self.hatkid.direction== Movement.Direction.LEFT:
                    print("left air dive")
                    self.x_speed=-(MAXXSPEED+3)
                    self.has_dived=True
    def cancel(self):
        timeelapsed=(time.time())-(self.timestart)
        if self.has_dived and (timeelapsed>100000):
            self.in_progress=False
            print("dive cancel",timeelapsed)
        self.has_dived= False

    def load(self,spritedir,direction):
        dives=[]
        for counter in range (1,3):
            dive= pygame.image.load(spritedir+"/dive"+str(counter)+".png")
            dive=pygame.transform.scale(dive,HATKIDSIZEDIVE)
            if direction==Movement.Direction.LEFT:
                dive=pygame.transform.flip(dive,True,False)
            dives.append(dive)
        return tuple(dives)
    