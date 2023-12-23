
import pygame
import random
from constants import *
from GameSprite import *

class HatKid(GameSprite):
    def __init__(self,x,y,screen):
        hatkid_filename = "sprite/HatKid/walk1.png"
        size = (TILE_SIZE,TILE_SIZE)
        super().__init__(x,y,hatkid_filename,screen,size)

        self.walks=[]
        
        self.walkright=self.load_walk("sprite/HatKid/new_sprite","right")
        self.walkleft=self.load_walk("sprite/HatKid/new_sprite","left")
        self.idleright=self.load_idle("sprite/HatKid/new_sprite","right")
        self.idleleft=self.load_idle("sprite/HatKid/new_sprite","left")
        self.diveright=self.load_dive("sprite/HatKid/new_sprite","right")
        self.diveleft=self.load_dive("sprite/HatKid/new_sprite","left")
        self.climbright=self.load_climb("sprite/HatKid/new_sprite","right")
        self.climbleft=self.load_climb("sprite/HatKid/new_sprite","left")

        self.can_jump=True
        self.jumps=0
        self.can_jump = True
        self.direction="right"
        self.x_speed = 0
        self.current_frame = self.idleright[0]
        self.walk_index= 0
        self.is_on_ground= True
        self.has_jumped_in_air= False
        self.y_speed=0
        self.canjump= True
        self.walk_index=0
    def load_walk(self,spritedir,direction):
        walks=[]
        for counter in range (1,5):
            walk= pygame.image.load(spritedir+"/walk"+str(counter)+".png")
            walk=pygame.transform.scale(walk,HATKIDSIZEWALK)
            if direction=="left":
                walk=pygame.transform.flip(walk,True,False)
            walks.append(walk)
        return tuple(walks)

    def load_idle(self,spritedir,direction):
        idles=[]
        for counter in range (1,4):
            idle= pygame.image.load(spritedir+"/idle"+str(counter)+".png")
            idle=pygame.transform.scale(idle,HATKIDSIZEIDLE)
            if direction=="left":
                idle=pygame.transform.flip(idle,True,False)
            idles.append(idle)
        return tuple(idles)
    
    def load_dive(self,spritedir,direction):
        dives=[]
        for counter in range (1,3):
            dive= pygame.image.load(spritedir+"/dive"+str(counter)+".png")
            dive=pygame.transform.scale(dive,HATKIDSIZEDIVE)
            if direction=="left":
                dive=pygame.transform.flip(dive,True,False)
            dives.append(dive)
        return tuple(dives)
    
    def load_climb(self,spritedir,direction):
        climbs=[]
        for counter in range (1,2):
            climb= pygame.image.load(spritedir+"/climb"+str(counter)+".png")
            climb=pygame.transform.scale(climb,HATKIDSIZECLIMB)
            if direction=="left":
                climb=pygame.transform.flip(climb,True,False)
            climbs.append(climb)
        return tuple(climbs)    

    #def animate(self):

        # keyspressedlist=pygame.key.get_pressed()

        # if keyspressedlist[pygame.K_d] and keyspressedlist[pygame.K_a]:
        #     self.stop_walk()
        # elif keyspressedlist[pygame.K_d]:
        #     if self.direction == "left":
        #         self.stop_walk()
        #     self.walk("right")
        # elif keyspressedlist[pygame.K_a]:
        #     if self.direction == "right":
        #         self.stop_walk()
        #     self.walk("left")
        # else:
        #     self.stop_walk()

        # if keyspressedlist[pygame.K_w] or keyspressedlist[pygame.K_SPACE]:
        #     if self.jumps <2 and self.canjump:
        #         self.jump()
        # else:
        #     self.canjump=True

    def get_walk_index(self):
        if self.walk_index > 4-1/15:
            self.walk_index = 0
        else:
            self.walk_index += 1/15
        return int(self.walk_index)

    def walk(self,direction):
        """set current frame"""
        #walking right
        direction_multiplyer=None
        if self.direction=="right":
            self.current_frame=self.walkright[self.get_walk_index()]
            direction_multiplyer=1
        elif self.direction=="left":
            self.current_frame=self.walkleft[self.get_walk_index()]
            direction_multiplyer=-1
        self.direction = direction

        if abs(self.x_speed)<MAXXSPEED:
            #accelerate
            self.x_speed+=(X_ACCELERATION*direction_multiplyer)
        else:
            #keep at max speed
            self.x_speed= (MAXXSPEED*direction_multiplyer)



        #print (direction)
    def dive(self):
        #s p e e d  in x speed, ctrl key to dive
        pass

    def stop_walk(self):
        #FIX: when it changes direction it doesnt slow down if you press both keys first
        if self.is_on_ground or (self.x_speed <-0.1 and pygame.key.get_pressed()[pygame.K_d]) or (self.x_speed >0.1 and pygame.key.get_pressed()[pygame.K_a]):
            if abs(self.x_speed)> 0.1:
                #decelerate
                self.x_speed *= 0.9
            else:
                self.x_speed=0
                if self.direction== "right":
                    self.current_frame=self.idleright[0]
                elif self.direction== "left":
                    self.current_frame=self.idleleft[0]

    def jump(self,map1):
        self.y_speed= -MAXYSPEED
        self.jumps+=1
        self.canjump= False

        if self.jumps==1:
        #jump sfx
            randomnumber=random.randint(0,13)
            JUMP_SFX[randomnumber].play()
        elif self.jumps==2:
        #doublejuump sfx
            randomnumber=random.randint(0,1)
            DOUBLE_JUMP_SFX[randomnumber].play()
            if pygame.key.get_pressed()[pygame.K_d] and not self.tilesright(map1):
                self.x_speed=MAXXSPEED 
            elif pygame.key.get_pressed()[pygame.K_a] and not self.tilesleft(map1):
                self.x_speed=-MAXXSPEED

    def check5pixel(self,map):
        """checks for doublejump"""
        self.rect.move_ip([0,-MAXYSPEED])
        hitlist=pygame.sprite.spritecollide(self,map.tiles,False)
        self.rect.move_ip([0,MAXYSPEED])
        return hitlist

    def update(self,map1):
        #print(self.x_speed)
        #gravity
        if self.y_speed <= MAXYSPEED:
            self.y_speed +=0.2

        #checks if theres a tile
        if self.check5pixel(map1):
            #print ("cant double jump")
            self.canjump=False

        #if on ground does this
        if tilesunder:= self.tilesunder(map1):
            #print("tile under")
            self.jumpdirection=False
            self.jumps=0
            self.is_on_ground= True
            self.has_jumped_in_air= False
            if self.y_speed >= 0:
                #print("not space")
                self.y_speed=0
                self.rect.bottom=tilesunder[0].rect.top
        else:
            self.is_on_ground= False

        if (tilesabove:= self.tilesabove(map1)) and self.y_speed <= 0:
            self.y_speed=0
            self.rect.top=tilesabove[0].rect.bottom

        # and pygame.key.get_pressed()[pygame.K_a]
        if (tilesleft:= self.tilesleft(map1)) and self.x_speed <= 0:
            self.x_speed=0
            self.rect.left=tilesleft[0].rect.right

            
        if (tilesright:= self.tilesright(map1)) and self.x_speed >= 0:
            self.x_speed=0
            self.rect.right=tilesright[0].rect.left
        #walking sprite
        
        #set up display frame
        

        keyspressedlist=pygame.key.get_pressed()
        if keyspressedlist[pygame.K_LCTRL]:
            print("wow dive")
        if keyspressedlist[pygame.K_d] and keyspressedlist[pygame.K_a]:
            self.stop_walk()
        elif keyspressedlist[pygame.K_d]:
            if self.direction == "left":
                self.stop_walk()
            elif self.jumps == 2 and self.jumpdirection == False:
                #self.x_speed=MAXXSPEED
                self.jumpdirection=True
            self.walk("right")

        elif keyspressedlist[pygame.K_a]:
            if self.direction == "right":
                self.stop_walk()
            elif self.jumps == 2 and self.jumpdirection == False:
                #self.x_speed=MAXXSPEED
                self.jumpdirection=True
            
            self.walk("left")
        else:
            self.stop_walk()

        if keyspressedlist[pygame.K_w] or keyspressedlist[pygame.K_SPACE]:
            if self.jumps <2 and self.canjump:
                self.jump(map1)
        else:
            self.canjump=True

        if(self.ispastleft()):
            if 0>=self.x_speed:
                self.x_speed=0
                self.rect.left=0

        if(self.ispastright()):
            if 0<=self.x_speed:
                self.x_speed=0
                self.rect.right=SCREEN_WIDTH
        if(self.ispastbottom()):
            self.rect.x,self.rect.y=100,100

#check 1,2,3,4,5 but with y_speed and makes it not over shoot
            

        self.rect.x+=self.x_speed
        self.rect.y+=self.y_speed



    def tilesunder(self,map):
        """return a list of tiles below the kid"""
        checkahead=MAXYSPEED
        self.rect.move_ip([0,checkahead])
        hitlist=pygame.sprite.spritecollide(self,map.tiles,False)
        self.rect.move_ip([0,-checkahead])
        return hitlist
    def tilesabove(self,map):
        """return a list of tiles above the kid"""
        self.rect.move_ip([0,-1])
        hitlist=pygame.sprite.spritecollide(self,map.tiles,False)
        self.rect.move_ip([0,1])
        return hitlist    
    def tilesleft(self,map):
        """return a list of tiles above the kid"""
        self.rect.move_ip([-3,0])
        hitlist=pygame.sprite.spritecollide(self,map.tiles,False)
        self.rect.move_ip([3,0])
        return hitlist 
    def tilesright(self,map):
        self.rect.move_ip([3,0])
        hitlist=pygame.sprite.spritecollide(self,map.tiles,False)
        self.rect.move_ip([-3,0])
        return hitlist   
    
    def ispastleft(self):
        checkahead=MAXXSPEED
        self.rect.move_ip([0,-checkahead])
        check=self.rect.x <= 0
        self.rect.move_ip([0,checkahead])
        return check

    def ispastright(self):
        self.rect.move_ip([0,self.x_speed])
        check=self.rect.x+TILE_SIZE >= WIDTHINTILES*TILE_SIZE
        self.rect.move_ip([0,-self.x_speed])
        return check


    def ispastbottom(self):
        """true or false if touching barrier on bottom"""
        return self.rect.y+TILE_SIZE >= HEIGHTINTILES*TILE_SIZE

    def draw(self):
        pygame.draw.rect(self.screen,"0xffffff",(self.rect.topleft[0],self.rect.topleft[1],HATKIDSIZEIDLE[0],HATKIDSIZEIDLE[1]))
        self.screen.blit(self.current_frame,self.rect)

