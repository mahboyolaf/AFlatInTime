import sprites
import constants
import set_up
import pygame

pygame.init()

pygame.mixer.init()
#setup for background music
#TODO: unmute
#set_up.bg_music()

#set up game clock
clock = pygame.time.Clock()

#set up screen
screen=pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))

hatkid=sprites.HatKid("sprite/HatKid/walk1.png",screen)
#map1= sprites.Map("map64.png",screen)
tilesetdir="maps/tilesets/tilesheet/"
map1=sprites.Map(tilesetdir,screen)
map1.createfromtmx("maps/map2.tmx")
#set up game loop
game=True
while game:
    screen.fill(constants.BGCOLOUR)
    
    map1.draw()
    hatkid.update()      
    clock.tick(constants.FPS)
    pygame.display.update()
     
    for event in (pygame.event.get()):
        if (pygame.KEYDOWN == event.type and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                game=False