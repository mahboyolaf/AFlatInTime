import pygame
import time
import os
import random
clock = pygame.time.Clock()
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Theme1.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()
#pygame.mixer.music.fadeout(5000)
BGCOLOUR=(88,159,223)
screen=pygame.display.set_mode((480*2,320*2))
jumpsoundeffects= []
doublejumpsoundeffects= []
for file in os.listdir("sounds/jumps"):

    sfx=pygame.mixer.Sound("sounds/jumps/"+file)
    sfx.set_volume(0.25)
    jumpsoundeffects.append(sfx)
for file in os.listdir("sounds/doublejumps"):
    sfx=pygame.mixer.Sound("sounds/doublejumps/"+file)
    sfx.set_volume(0.25)
    doublejumpsoundeffects.append(sfx)

class GameSprite:
    def __init__(self,x,y,filename):
        self.x=x
        self.y=y
        self.image= pygame.image.load(filename)
        self.rect = self.image.get_rect()

class Map(GameSprite):
    def __init__(self,filename):
        super().__init__(0,0,filename)
        self.image= pygame.transform.scale(self.image,(480*2,320*2))
        self.platform1= pygame.image.load("platform1.png")
        
    def update(self):
        screen.fill(BGCOLOUR)
        screen.blit(self.image,(0,0))
        self.drawplatform1(224,192)

        self.drawplatform1(576,256)
        self.drawplatform1(384,256)
        #224,192
        #576,256
        #384,256
    def drawplatform1(self,x,y):
        platform1_surface= pygame.Surface((96,32))
        platform1_surface.fill(BGCOLOUR)
        platform1_surface.blit(self.platform1,(0,0))
        screen.blit(platform1_surface,(x,y))
        self.platform1=platform1_surface



class HatKid(GameSprite):
    def __init__(self,filename):
        super().__init__(0,0,filename)
        
        self.walk1= pygame.image.load("sprite/HatKid/walk1.png")
        self.walk2= pygame.image.load("sprite/HatKid/walk2.png")
        self.standing= pygame.image.load("sprite/HatKid/standing.png")
        self.prejump= pygame.image.load("sprite/HatKid/prejump.png")
        self.fall= pygame.image.load("sprite/HatKid/fall.png")

        self.walk1= pygame.transform.scale(self.walk1,(52,52))
        self.walk2= pygame.transform.scale(self.walk2,(52,52))
        self.standing= pygame.transform.scale(self.standing,(52,52))
        self.prejump= pygame.transform.scale(self.prejump,(52,52))
        self.fall= pygame.transform.scale(self.fall,(52,52))
        self.yspeed=0
        self.jumps=0
        self.canjump= True
    def update(self,keyspressedlisted):

        
        #if self.rect.colliderect(p1):
        #    print ("collidead",p1.x,p1.y)
        #print (self.x,self.y,"hatkid")
        if self.yspeed <= 5:
            self.yspeed +=0.2
        else:
            self.yspeed=5
        if self.y >= 300:
            self.yspeed=0
            self.y=300
            self.jumps=0

        
        #time.sleep(0.2)
        #screen.blit(self.walk2,(0,0))
        #time.sleep(0.2)
        keyspressedlisted=pygame.key.get_pressed()
        if keyspressedlisted[pygame.K_w] or keyspressedlisted[pygame.K_SPACE]:
            if self.jumps <2 and self.canjump:
                self.yspeed =-5
                self.jumps+=1
                self.canjump= False
                if self.jumps==1:
                    randomnumber=random.randint(0,13)
                    jumpsoundeffects[randomnumber].play()
                    print(randomnumber)
                if self.jumps==2:
                    randomnumber=random.randint(0,1)
                    doublejumpsoundeffects[randomnumber].play()
                    print(randomnumber)
        else:
            self.canjump=True

        if keyspressedlisted[pygame.K_s]:
            self.y +=3

        if keyspressedlisted[pygame.K_d]:
            self.x +=3

        if keyspressedlisted[pygame.K_a]:
            self.x -=3

        #print(self.yspeed,self.y,self.jumps,self.canjump)
        self.y+=self.yspeed

        screen.blit(self.walk1,(self.x,self.y))

class Rectangle():
    def __init__(self,xcoord,ycoord,width,height):
        self.rectangle=pygame.Rect(xcoord,ycoord,width,height)

    def draw(self,screen):
        pygame.draw.rect(screen,BGCOLOUR,self.rectangle)

class Image(Rectangle):
    def __init__(self,xcoord,ycoord,width,height,file_name):
        super().__init__(xcoord,ycoord,width,height)
        self.image= pygame.image.load(file_name)

    def draw(self,screen):
        super().draw(screen)
        screen.blit(self.image,((self.rectangle.x,self.rectangle.y)))

hatkid=HatKid("sprite/HatKid/walk1.png")
map1=Map("map64.png")
game=True
p1= None
while game:

    keyspressedlisted=pygame.key.get_pressed()
    map1.update()

    p1=map1.platform1.get_rect()
    hk=hatkid.rect
    #print(p1.x,p1.y,p1.height,p1.width)
    #print(hk.x,hk.y,hk.height,hk.width)
    hatkid.update(keyspressedlisted)
    clock.tick(60)
    pygame.display.update()

    for event in (pygame.event.get()):
        if (pygame.KEYDOWN == event.type and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            game=False







#480 320