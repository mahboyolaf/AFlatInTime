import pygame
import constants
import os
screen=pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))
tiles=[]
for file in os.listdir("maps/tilesets/grass16"):
    tile=pygame.image.load("maps/tilesets/grass16/"+file)
    tile=pygame.transform.scale(tile,(constants.TILE_SIZE,constants.TILE_SIZE))
    tiles.append(tile)


mapfile="testing2.tmx"

tileindexs=[]

#import tmx and make into list of indices
with open("maps/"+mapfile) as map:
    line=map.readline()
    while line !="":
        line=map.readline()
        if line.strip()=='<data encoding="csv">':
            while line.strip()!="</data>":
                line=map.readline().strip()
                if line[-1]== ",":
                    line=line [0:-1]
                tileindexs.append(line.split(","))
                print (line)
            tileindexs.pop()



#convert indices into integers
for rows in range (len(tileindexs)):
    for column in range (len(tileindexs[0])):
        tileindexs[rows][column]=int(tileindexs[rows][column])
for rows in tileindexs:
    print (rows)

#draw tiles

# for counter_row in range(0,64):
#     screen.blit(tiles[counter_row]),(counter_row*constants.TILE_SIZE,counter_row//8*-counter_row*8(constants.TILE_SIZE))

row_counter=0
for counter_row in range (0,26):
    row_counter=row_counter+1/14
    screen.blit((tiles[counter_row]),(counter_row*constants.TILE_SIZE*8*int(row_counter),counter_row*constants.TILE_SIZE,))





while True:
    pygame.display.update()