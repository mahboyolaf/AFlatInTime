import pygame

#set up back ground music
def bg_music():
    pygame.mixer.music.load("Theme1.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()
