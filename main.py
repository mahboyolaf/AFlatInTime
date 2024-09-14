
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
tilesetdir="maps/tilesets/tilesheets/"
mapfiletmx= "maps/testmap.tmx"
map1=LevelMap(mapfile=mapfiletmx, tilesetdir=tilesetdir, screen=screen)
RIGHTKEY=pygame.K_d
LEFTKEY=pygame.K_a
UPKEY=pygame.K_w
SPACEKEY=pygame.K_SPACE


def is_pressing_both_directions(keyspressedlist):
    return keyspressedlist[RIGHTKEY] and keyspressedlist[LEFTKEY]

def check_for_keyboard_events(hatkid):
    keyspressedlist=pygame.key.get_pressed()


    if keyspressedlist[RIGHTKEY] and not hatkid.dive.divestatus and not is_pressing_both_directions(keyspressedlist):
        #not diving and moving to the right
        hatkid.walk_right()
    elif keyspressedlist[LEFTKEY] and not hatkid.dive.divestatus and not is_pressing_both_directions(keyspressedlist):
        hatkid.walk_left()
    else:
        hatkid.walk.stop()

    if keyspressedlist[UPKEY] or keyspressedlist[SPACEKEY]:
        hatkid.dive.cancel()
        if hatkid.jump.count <2 and hatkid.canjump:
            hatkid.jump.start()





# player

hatkid=HatKid(constants.SCREEN_WIDTH-100,100,screen,map1)
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
    check_for_keyboard_events(hatkid)
    for event in (pygame.event.get()):
        if (pygame.KEYDOWN == event.type and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                game=False 