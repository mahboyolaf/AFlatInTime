
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

def check_for_keyboard_events(hatkid):
    keyspressedlist=pygame.key.get_pressed()
    if keyspressedlist[pygame.K_d] and keyspressedlist[pygame.K_a]:
        #stop walking if moving in both directions
        hatkid.walk.stop()
    elif keyspressedlist[pygame.K_d] and not hatkid.dive.divestatus:
        #not diving and moving to the right
        if hatkid.direction == Movement.Direction.LEFT:
            hatkid.walk.stop()
        elif hatkid.is_moving_left_fast():
            hatkid.walk.stop()
        hatkid.walk.set_direction(Movement.Direction.RIGHT)
        hatkid.walk.start()
    elif keyspressedlist[pygame.K_a] and not hatkid.dive.divestatus:
        if hatkid.direction == Movement.Direction.RIGHT:
            hatkid.walk.stop()
        elif hatkid.is_moving_right_fast():
            hatkid.walk.stop()  
        hatkid.walk.set_direction(Movement.Direction.LEFT)
        hatkid.walk.start()
    else:
        hatkid.walk.stop()

    if keyspressedlist[pygame.K_w] or keyspressedlist[pygame.K_SPACE]:
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