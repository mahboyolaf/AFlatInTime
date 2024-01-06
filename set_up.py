import pygame
import os

#set up back ground music
def bg_music():
    pygame.mixer.music.load("music/Theme1.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()

def sfx(sfx_dir,volume):
    sfx_list=[]
    for file in os.listdir(sfx_dir):
        sfx=pygame.mixer.Sound(sfx_dir+file)
        sfx.set_volume(volume)
        sfx_list.append(sfx)
    return tuple(sfx_list) 