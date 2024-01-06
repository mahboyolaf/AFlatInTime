from GameSprite import *
from constants import *
class LevelMap():
    class Tile(GameSprite):
        def __init__(self, x, y, filename=None, screen=None):
            super().__init__(x, y, filename, screen)
    
        def set_image(self, filename):
            self.image= pygame.image.load(filename)
            self.image=pygame.transform.scale(self.image,(TILE_SIZE,TILE_SIZE))
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.x, self.y]


    def __init__(self,tilesetdir,mapfile,screen):
        self.tiles=pygame.sprite.Group()
        self.tileindexs=[]
        #tileindex is location of tiles on screen (in tiles)
        #tileindex[0][0] is the first tile in the first row and coloumn
        self.screen=screen
        self.mapfile = mapfile
        self.tileset=[]
        self.tilesetdir=tilesetdir

        self.createtiles()


    def createtiles(self):
        with open(self.mapfile) as maptmx:
            columnindex=-1
            rowindex=-1
            line=None
            #TODO fix empty line in middle
            while line !="":
                line=maptmx.readline()
                line=line.strip()
                if line.find("<") == -1:
                    rowindex+=1
                    columnindex=-1
                    for tileindex in line.split(sep=","):
                        if tileindex.strip().isnumeric():
                            columnindex+=1
                            tileindex=int(tileindex)
                            if tileindex!=0:
                                filename = self.tilesetdir+r"%03d.png"%(tileindex)
                                x=columnindex*TILE_SIZE
                                y=rowindex*TILE_SIZE
                                tile= LevelMap.Tile(x,y,filename,self.screen)
                                self.tiles.add(tile)

                        

                        


    
    def draw(self):
        self.screen.fill(("#888888"))
        self.tiles.draw(self.screen)
