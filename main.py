
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
DIVEKEY=pygame.K_LCTRL


def is_pressing_both_directions(keyspressedlist):
    return keyspressedlist[RIGHTKEY] and keyspressedlist[LEFTKEY]

def input_start_dive(hatkid,keyspressedlist):
    return not hatkid.dive.ctrlpaststatus and keyspressedlist[DIVEKEY] and not hatkid.dive.divestatus
def dive_decelerate_condition(hatkid):
    return hatkid.dive.divestatus and hatkid.is_on_ground
def input_cancel_dive(hatkid,keyspressedlist):
    return (keyspressedlist[UPKEY] or keyspressedlist[SPACEKEY] or keyspressedlist[DIVEKEY]) and hatkid.dive.divestatus
def input_continue_dive(hatkid,keyspressedlist):
    return hatkid.dive.divestatus and not (keyspressedlist[UPKEY] or keyspressedlist[SPACEKEY] or keyspressedlist[DIVEKEY])
def check_for_keyboard_events(hatkid):
    keyspressedlist=pygame.key.get_pressed()




    # if not hatkid.dive.ctrlpaststatus and keyspressedlist[DIVEKEY] and hatkid.dive.divestatus:
    #     hatkid.dive.divestatus= False
    #     hatkid.dive.cancel()
    #     print ("start dive cancel")
    # elif hatkid.dive.divestatus:
    #     hatkid.dive.start()
    #     print ("continue dive")
    #     hatkid.current_frame=hatkid.diveright[0]
    if input_start_dive(hatkid,keyspressedlist):
        hatkid.dive.divestatus= True

        hatkid.dive.start()
        hatkid.dive.load("sprite/HatKid/dive",Movement.Direction.RIGHT)
        hatkid.current_frame=hatkid.diveright[0]
        print ("start dive")
        hatkid.set_x_speed(DIVESPEED*hatkid.get_x_movement_direction())
        hatkid.rect.y-=DIVEHOPHEIGHT



    # elif hatkid.dive.divestatus and keyspressedlist[RIGHTKEY] and not is_pressing_both_directions(keyspressedlist) and not hatkid.is_stopped_x():
    #     hatkid.dive_ground_right()


    # elif hatkid.dive.divestatus and keyspressedlist[LEFTKEY] and not is_pressing_both_directions(keyspressedlist):
    #     hatkid.dive_ground_left()
    # elif not hatkid.dive.divestatus:
    #     hatkid.walk.stop()
    elif input_cancel_dive(hatkid,keyspressedlist):
        hatkid.dive.divestatus=False
        print ("if cancel",input_cancel_dive(hatkid,keyspressedlist))

    elif dive_decelerate_condition(hatkid):
        hatkid.decelerate_x(DIVEDECELERATE)
        
    elif input_continue_dive(hatkid,keyspressedlist):
        hatkid.dive_ground_right()
    # elif not hatkid.dive.ctrlpaststatus and not keyspressedlist[DIVEKEY] and not hatkid.dive.divestatus:
    #     hatkid.dive.load("sprite/HatKid/dive",Movement.Direction.RIGHT)
    #     print ("no input")

    hatkid.dive.ctrlpaststatus=keyspressedlist[DIVEKEY]
            






    if keyspressedlist[RIGHTKEY] and not hatkid.dive.divestatus and not is_pressing_both_directions(keyspressedlist):
        #not diving and moving to the right
        hatkid.walk_right()
    elif keyspressedlist[LEFTKEY] and not hatkid.dive.divestatus and not is_pressing_both_directions(keyspressedlist):
        hatkid.walk_left()
    elif not hatkid.dive.divestatus:
        hatkid.walk.stop()

    if (keyspressedlist[UPKEY] or keyspressedlist[SPACEKEY]) and not hatkid.dive.divestatus:
        hatkid.dive.cancel()
        if hatkid.jump.count <2 and hatkid.canjump:
            hatkid.jump.start()

def set_can_dive(hatkid):
    if not HatKid.is_press_dive_key():
        hatkid.candive=True

def is_press_dive_key():
    keyspressedlist=pygame.key.get_pressed()        
    return keyspressedlist[DIVEKEY]



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