import pygame
import constants
import sprites
import os
screen=pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))
#https://pinetools.com/split-image



mapfile="maps/map2.tmx"



#import tmx and make into list of indices


tilesetdir="maps/tilesets/tilesheet/"

class Map(sprites.GameSprite):
    def __init__(self,tilesetdir,screen):
        self.tiles=[]
        self.importtileset(tilesetdir)
        self.tileindexs=[]
        self.screen=screen
    def importtileset(self,tilesetdir):
        self.tiles=[]
        for file in os.listdir(tilesetdir):
            tile=pygame.image.load(tilesetdir+file)
            tile=pygame.transform.scale(tile,(constants.TILE_SIZE,constants.TILE_SIZE))
            self.tiles.append(tile)  

    def createfromtmx(self,mapfile):
        with open(mapfile) as map:
            line=map.readline()
            while line !="":
                line=map.readline()
                if line.strip()=='<data encoding="csv">':
                    while line.strip().find("</data>") <0:
                        line=map.readline().strip()
                        if line[-1]== ",":
                            line=line [0:-1]
                        self.tileindexs.append(line.split(","))    
        self.tileindexs.pop()
        #convert to int
        for row_counter in range (len(self.tileindexs)):
            for column_counter in range (len(self.tileindexs[0])):
                self.tileindexs[row_counter][column_counter]=int(self.tileindexs[row_counter][column_counter])
 

    def draw(self):
        self.screen.fill(("#888888"))
        row_counter=0
        column_counter=0
        for counter in range (constants.WIDTHINTILES*constants.HEIGHTINTILES+1):
            if self.tileindexs[row_counter][column_counter] != 0:
                self.screen.blit((map1.tiles[self.tileindexs[row_counter][column_counter]-1]),(column_counter*constants.TILE_SIZE,row_counter*constants.TILE_SIZE))
            if column_counter < 24:
                column_counter+=1
            if counter%constants.WIDTHINTILES == 0 and counter < constants.WIDTHINTILES*constants.HEIGHTINTILES+1 and row_counter < 13:
                    row_counter+=1
                    column_counter=0

map1 = Map(tilesetdir,screen)
map1.createfromtmx(mapfile)
clock = pygame.time.Clock()
game= True
while game:

    map1.draw()
    clock.tick(60)
    pygame.display.update()
    for event in (pygame.event.get()):
        if (pygame.KEYDOWN == event.type and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            game=False