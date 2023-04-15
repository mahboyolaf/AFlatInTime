import constants
import pygame




class GameSprite:
    def __init__(self,x,y,filename,screen):
        self.screen=screen
        self.x=x
        self.y=y
        self.image= pygame.image.load(filename)
        self.rect = self.image.get_rect()

class Map(GameSprite):
    def __init__(self,filename,screen):
        super().__init__(0,0,filename,screen)
        self.image= pygame.transform.scale(self.image,(480*2,320*2))
        self.platform1= pygame.image.load("platform1.png")
        
    def update(self):
        self.screen.fill(constants.BGCOLOUR)
        self.screen.blit(self.image,(0,0))
        self.drawplatform1(224,192)

        self.drawplatform1(576,256)
        self.drawplatform1(384,256)
        #224,192
        #576,256
        #384,256
    def drawplatform1(self,x,y):
        platform1_surface= pygame.Surface((96,32))
        platform1_surface.fill(constants.BGCOLOUR)
        platform1_surface.blit(self.platform1,(0,0))
        self.screen.blit(platform1_surface,(x,y))
        self.platform1=platform1_surface



class HatKid(GameSprite):
    def __init__(self,filename,screen):

        super().__init__(0,0,filename,screen)
        self.walks=[]

        self.walkright=self.load_walk("sprite/HatKid/new_sprite","right")
        self.walkleft=self.load_walk("sprite/HatKid/new_sprite","left")
        self.idleright=self.load_idle("sprite/HatKid/new_sprite","right")
        self.idleleft=self.load_idle("sprite/HatKid/new_sprite","left")
        self.diveright=self.load_dive("sprite/HatKid/new_sprite","right")
        self.diveleft=self.load_dive("sprite/HatKid/new_sprite","left")
        self.climbright=self.load_climb("sprite/HatKid/new_sprite","right")
        self.climbleft=self.load_climb("sprite/HatKid/new_sprite","left")


        self.direction="right"
        self.x_speed = 0




        #self.standing= pygame.image.load("sprite/HatKid/standing.png")
        #self.prejump= pygame.image.load("sprite/HatKid/prejump.png")
        #self.fall= pygame.image.load("sprite/HatKid/fall.png")

        #self.standing= pygame.transform.scale(self.standing,(52,52))
        #self.prejump= pygame.transform.scale(self.prejump,(52,52))
        #self.fall= pygame.transform.scale(self.fall,(52,52))
        self.yspeed=0
        self.jumps=0
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
        if self.yspeed <= 5:
            self.yspeed +=0.2
        else:
            self.yspeed=5
        #TODO: make proper collisions
        if self.y >= 300:
            self.yspeed=0
            self.y=300
            self.jumps=0

    def animate(self):

        keyspressedlist=pygame.key.get_pressed()

        if keyspressedlist[pygame.K_d] and keyspressedlist[pygame.K_a]:
            pass
        elif keyspressedlist[pygame.K_d]:
            self.walk("right")
        elif keyspressedlist[pygame.K_a]:
            self.walk("left")
    def walk(self,direction):
        print (direction)

        
    def update(self):
        #gravity
        self.make_gravity()

        #walking sprite
        
        #set up display frame
        self.animate()
        #sound effects

        #move and display
