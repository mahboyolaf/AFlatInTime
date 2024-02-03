from Movement import *
import pygame
import random
from constants import *
from GameSprite import *

class HatKid(GameSprite):
    def __init__(self,x,y,screen,map):
        hatkid_filename = "sprite/HatKid/walk/walk1.png"
        size = (TILE_SIZE,TILE_SIZE)
        super().__init__(x,y,hatkid_filename,screen,size)
        self.walks=[]
        self.walk=Walk(map,self)
        self.walkright=self.walk.sprites_right
        self.walkleft=self.walk.sprites_left
        self.idleright=self.load_idle("sprite/HatKid/idle",Movement.Direction.RIGHT)
        self.idleleft=self.load_idle("sprite/HatKid/idle",Movement.Direction.LEFT)
        self.diveright=self.load_dive("sprite/HatKid/dive",Movement.Direction.RIGHT)
        self.diveleft=self.load_dive("sprite/HatKid/dive",Movement.Direction.LEFT)
        self.climbright=self.load_climb("sprite/HatKid/climb",Movement.Direction.RIGHT)
        self.climbleft=self.load_climb("sprite/HatKid/climb",Movement.Direction.LEFT)

        self.can_jump=True
        self.jumps=0
        self.can_jump = True
        self.direction=Movement.Direction.RIGHT
        self.x_speed = 0
        self.current_frame = self.idleright[0]
        self.walk_index= 0
        self.is_on_ground= True
        self.has_jumped_in_air= False
        self.y_speed=0
        self.canjump= True

    def load_idle(self,spritedir,direction):
        idles=[]
        for counter in range (1,4):
            idle= pygame.image.load(spritedir+"/idle"+str(counter)+".png")
            idle=pygame.transform.scale(idle,HATKIDSIZEIDLE)
            if direction==Movement.Direction.LEFT:
                idle=pygame.transform.flip(idle,True,False)
            idles.append(idle)
        return tuple(idles)
    
    def load_dive(self,spritedir,direction):
        dives=[]
        for counter in range (1,3):
            dive= pygame.image.load(spritedir+"/dive"+str(counter)+".png")
            dive=pygame.transform.scale(dive,HATKIDSIZEDIVE)
            if direction==Movement.Direction.LEFT:
                dive=pygame.transform.flip(dive,True,False)
            dives.append(dive)
        return tuple(dives)
    
    def load_climb(self,spritedir,direction):
        climbs=[]
        for counter in range (1,2):
            climb= pygame.image.load(spritedir+"/climb"+str(counter)+".png")
            climb=pygame.transform.scale(climb,HATKIDSIZECLIMB)
            if direction==Movement.Direction.LEFT:
                climb=pygame.transform.flip(climb,True,False)
            climbs.append(climb)
        return tuple(climbs)    

    #def animate(self):

        # keyspressedlist=pygame.key.get_pressed()

        # if keyspressedlist[pygame.K_d] and keyspressedlist[pygame.K_a]:
        #     self.walk.stop()
        # elif keyspressedlist[pygame.K_d]:
        #     if self.direction == Movement.Direction.LEFT:
        #         self.walk.stop()
        #     self.walk(Movement.Direction.RIGHT)
        # elif keyspressedlist[pygame.K_a]:
        #     if self.direction == Movement.Direction.RIGHT:
        #         self.walk.stop()
        #     self.walk(Movement.Direction.LEFT)
        # else:
        #     self.walk.stop()

        # if keyspressedlist[pygame.K_w] or keyspressedlist[pygame.K_SPACE]:
        #     if self.jumps <2 and self.canjump:
        #         self.jump()
        # else:
        #     self.canjump=True

    def dive(self):
        if self.has_dived==False:
            if self.is_on_ground:
                if pygame.key.get_pressed()[pygame.K_d]:
                    print("right ground dive")
                    self.x_speed=MAXXSPEED+3
                    self.rect.y-=10
                    self.has_dived=True
                if pygame.key.get_pressed()[pygame.K_a]:
                    print("left ground dive")
                    self.x_speed=-(MAXXSPEED+3)
                    self.rect.y-=10
                    self.has_dived=True
            else:
                if self.direction== Movement.Direction.RIGHT:
                    print("right air dive")
                    self.x_speed=MAXXSPEED+3
                    self.has_dived=True
                if self.direction== Movement.Direction.LEFT:
                    print("left air dive")
                    self.x_speed=-(MAXXSPEED+3)
                    self.has_dived=True
    def dive_cancel(self):
        if self.has_dived:
            self.rect.y-=5
            self.has_jumped_in_air=True
            self.y_speed=MAXXSPEED


    def jump(self,map1):
        self.jumps+=1
        self.canjump= False
        if self.is_on_ground:
        #jump sfx
            randomnumber=random.randint(0,13)
            JUMP_SFX[randomnumber].play()
            self.y_speed= -MAXYSPEED
        elif not self.has_jumped_in_air:
        #doublejuump sfx
            randomnumber=random.randint(0,1)
            DOUBLE_JUMP_SFX[randomnumber].play()
            self.has_jumped_in_air=True
            self.y_speed= -MAXYSPEED
            if pygame.key.get_pressed()[pygame.K_d] and not self.tilesright(map1) and not pygame.key.get_pressed()[pygame.K_a]:
                self.x_speed=MAXXSPEED 
            elif pygame.key.get_pressed()[pygame.K_a] and not self.tilesleft(map1) and not pygame.key.get_pressed()[pygame.K_d]:
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
            self.has_dived=False
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
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.dive_cancel
        if keyspressedlist[pygame.K_LCTRL]:
            self.dive()


        elif keyspressedlist[pygame.K_d] and keyspressedlist[pygame.K_a]:
            self.walk.stop()
        elif keyspressedlist[pygame.K_d]:
            if self.direction == Movement.Direction.LEFT:
                self.walk.stop()
            elif self.x_speed <-0.1:
                self.walk.stop()
            elif self.jumps == 2 and self.jumpdirection == False:
                self.jumpdirection=True
            self.walk.set_direction(Movement.Direction.RIGHT)
            self.walk.start()
        elif keyspressedlist[pygame.K_a]:
            if self.direction == Movement.Direction.RIGHT:
                self.walk.stop()
            elif self.x_speed >0.1:
                self.walk.stop()  
            elif self.jumps == 2 and self.jumpdirection == False:
                self.jumpdirection=True
            self.walk.set_direction(Movement.Direction.LEFT)
            self.walk.start()
        else:
            self.walk.stop()

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

