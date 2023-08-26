import constants
import pygame
import random
import os
import copy

class GameSprite(pygame.sprite.Sprite):
    def __init__(self,x,y,filename=None,screen=None):
        pygame.sprite.Sprite.__init__(self)
        self.screen=screen
        self.x=x
        self.y=y
        pygame.sprite.Sprite.__init__(self)
        if filename != None:
            self.set_image(filename)
            
    def set_image(self, filename):
            self.image= pygame.image.load(filename)
            self.rect = self.image.get_rect()
            self.rect.center = [self.x, self.y]

    def update(self):
        pass

    def draw(self):
        if self.image == None or self.rect==None:
            raise Exception("Sprite image is not properly defined")

        self.screen.blit(self.image, self.rect)


class HatKid(GameSprite):
    def __init__(self,x,y,screen):
        hatkid_filename = "sprite/HatKid/walk1.png"
        super().__init__(x,y,hatkid_filename,screen)

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
        #self.standing= pygame.image.load("sprite/HatKid/standing.png")
        #self.prejump= pygame.image.load("sprite/HatKid/prejump.png")
        #self.fall= pygame.image.load("sprite/HatKid/fall.png")

        #self.standing= pygame.transform.scale(self.standing,(52,52))
        #self.prejump= pygame.transform.scale(self.prejump,(52,52))
        #self.fall= pygame.transform.scale(self.fall,(52,52))
        self.y_speed=0
        self.canjump= True
        self.walk_index=0
    def load_walk(self,spritedir,direction):
        walks=[]
        for counter in range (1,5):
            walk= pygame.image.load(spritedir+"/walk"+str(counter)+".png")
            walk=pygame.transform.scale(walk,constants.HATKIDSIZEWALK)
            if direction=="left":
                walk=pygame.transform.flip(walk,True,False)
            walks.append(walk)
        return tuple(walks)

    def load_idle(self,spritedir,direction):
        idles=[]
        for counter in range (1,4):
            idle= pygame.image.load(spritedir+"/idle"+str(counter)+".png")
            idle=pygame.transform.scale(idle,constants.HATKIDSIZEIDLE)
            if direction=="left":
                idle=pygame.transform.flip(idle,True,False)
            idles.append(idle)
        return tuple(idles)
    
    def load_dive(self,spritedir,direction):
        dives=[]
        for counter in range (1,3):
            dive= pygame.image.load(spritedir+"/dive"+str(counter)+".png")
            dive=pygame.transform.scale(dive,constants.HATKIDSIZEDIVE)
            if direction=="left":
                dive=pygame.transform.flip(dive,True,False)
            dives.append(dive)
        return tuple(dives)
    
    def load_climb(self,spritedir,direction):
        climbs=[]
        for counter in range (1,2):
            climb= pygame.image.load(spritedir+"/climb"+str(counter)+".png")
            climb=pygame.transform.scale(climb,constants.HATKIDSIZECLIMB)
            if direction=="left":
                climb=pygame.transform.flip(climb,True,False)
            climbs.append(climb)
        return tuple(climbs)    
    
    def make_gravity(self):
        if self.y_speed <= 5:
            self.y_speed +=0.2
        else:
            self.y_speed=5
        #TODO: make proper collisions
        if self.rect.y >= 300:
            self.y_speed=0
            self.rect.y=300
            self.jumps=0
            self.is_on_ground= True
            self.has_jumped_in_air= False

    def animate(self):

        keyspressedlist=pygame.key.get_pressed()

        if keyspressedlist[pygame.K_d] and keyspressedlist[pygame.K_a]:
            self.stop_walk()
        elif keyspressedlist[pygame.K_d]:
            if self.direction == "left":
                self.stop_walk()
            self.walk("right")
        elif keyspressedlist[pygame.K_a]:
            if self.direction == "right":
                self.stop_walk()
            self.walk("left")
        else:
            self.stop_walk()
        
        # if keyspressedlist[pygame.K_SPACE]:
        #     print ("space pressed")
        #     if self.can_jump:
        #         if self.is_on_ground:
        #             self.jump()
        #         elif self.has_jumped_in_air:
        #             print("double jump")
        #             self.can_jump=False
        #             self.double_jump()
        #         else:
        #             self.can_jump=False
        #             pass
        # else:
        #     print ("space let go")
        #     self.can_jump= True


        # if keyspressedlist[pygame.K_w] or keyspressedlist[pygame.K_SPACE]:
        #     print ("space pressed")
        #     if self.is_on_ground== False:
        #         self.jumps+=1


        #     if self.jumps >=2 and self.canjump:
        #         self.y_speed =-5
        #         self.jumps+=1
        #         self.canjump= False


        # else:
        #     self.canjump=True



        #self.canjump= True

        if keyspressedlist[pygame.K_w] or keyspressedlist[pygame.K_SPACE]:
            if self.jumps <2 and self.canjump:
                self.y_speed =-5
                self.jumps+=1
                self.canjump= False
                if self.jumps==1:
                    randomnumber=random.randint(0,13)
                    constants.JUMP_SFX[randomnumber].play()
                    print(randomnumber)
                if self.jumps==2:
                    randomnumber=random.randint(0,1)
                    constants.DOUBLE_JUMP_SFX[randomnumber].play()
                    print(randomnumber)
        else:
            self.canjump=True

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

        if abs(self.x_speed)<constants.MAXSPEED:
            #accelerate
            self.x_speed+=(constants.X_ACCELERATION*direction_multiplyer)
        else:
            #keep at max speed
            self.x_speed= (constants.MAXSPEED*direction_multiplyer)



        print (direction)

    def stop_walk(self):
        #FIX: when it changes direction it doesnt slow down if you press both keys first
        if self.is_on_ground:
            if abs(self.x_speed)> 0.1:
                #decelerate
                self.x_speed *= 0.9
            else:
                self.x_speed=0
                if self.direction== "right":
                    self.current_frame=self.idleright[0]
                elif self.direction== "left":
                    self.current_frame=self.idleleft[0]

    def jump(self):
        self.y_speed-= constants.MAXYSPEED
        randomnumber=random.randint(0,13)
        constants.JUMP_SFX[randomnumber].play()
        self.is_on_ground= False
        self.has_jumped_in_air= True
    
    def double_jump(self):
        self.y_speed-= constants.MAXYSPEED
        randomnumber=random.randint(0,1)
        constants.DOUBLE_JUMP_SFX[randomnumber].play()
        self.is_on_ground= False
        self.has_jumped_in_air= False


    def update(self):
        #gravity
        self.make_gravity()

        #walking sprite
        
        #set up display frame
        self.animate()
        #sound effects

        #move and display
        #if self.rect.y > 300:
        #    self.rect.y=300
        self.rect.x+=self.x_speed
        self.rect.y+=self.y_speed
        pygame.draw.rect(self.screen,"0xffffff",(self.rect.topleft[0],self.rect.topleft[1],constants.HATKIDSIZEIDLE[0],constants.HATKIDSIZEIDLE[1]))
        self.screen.blit(self.current_frame,self.rect)            
        

class LevelMap():
    class Tile(GameSprite):
        def __init__(self, x, y, filename=None, screen=None):
            super().__init__(x, y, filename, screen)
    
        def set_image(self, filename):
            self.image= pygame.image.load(filename)
            self.image=pygame.transform.scale(self.image,(constants.TILE_SIZE,constants.TILE_SIZE))
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]


    def __init__(self,tilesetdir,mapfile,screen):
        self.tiles=pygame.sprite.Group()
        self.tileindexs=[]
        #tileindex is location of tiles on screen (in tiles)
        #tileindex[0][0] is the first tile in the first row and coloumn
        self.screen=screen
        self.mapfile = mapfile
        self.tileset=[]
        self.tilesetdir=tilesetdir

        self.createtiles()


    def createtiles(self):
        with open(self.mapfile) as maptmx:
            columnindex=-1
            rowindex=-1
            line=None
            #TODO fix empty line in middle
            while line !="":
                line=maptmx.readline()
                line=line.strip()
                if line.find("<") == -1:
                    rowindex+=1
                    columnindex=-1
                    for tileindex in line.split(sep=","):
                        if tileindex.strip().isnumeric():
                            columnindex+=1
                            tileindex=int(tileindex)
                            if tileindex!=0:
                                filename = self.tilesetdir+r"%03d.png"%(tileindex)
                                x=columnindex*constants.TILE_SIZE
                                y=rowindex*constants.TILE_SIZE
                                tile= LevelMap.Tile(x,y,filename,self.screen)
                                self.tiles.add(tile)

                        

                        


    
    def draw(self):
        self.screen.fill(("#888888"))
        self.tiles.draw(self.screen)
