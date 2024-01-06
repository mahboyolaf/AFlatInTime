
import constants
import set_up
import pygame
from LevelMap import *
from HatKid import *
pygame.init()

pygame.mixer.init()
#setup for background music
#TODO: unmute
#set_up.bg_music()

#set up game clock
clock = pygame.time.Clock()

#set up screen
screen=pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))

# map
tilesetdir="maps/tilesets/tilesheet/"
mapfiletmx= "maps/testmap.tmx"
map1=LevelMap(mapfile=mapfiletmx, tilesetdir=tilesetdir, screen=screen)


# player

hatkid=HatKid(constants.SCREEN_WIDTH-100,100,screen)
#set up game loop
game=True
while game:
    screen.fill(constants.BGCOLOUR)
    
    map1.draw()
    hatkid.update(map1)
    hatkid.draw()      
    clock.tick(constants.FPS)
    pygame.display.update()
    #hitlist=pygame.sprite.spritecollide(hatkid,map1.tiles,False)
    for event in (pygame.event.get()):
        if (pygame.KEYDOWN == event.type and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                game=False 