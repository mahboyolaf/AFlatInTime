import pygame
class GameSprite(pygame.sprite.Sprite):
    def __init__(self,x,y,filename=None,screen=None,size=(32,64)):

        pygame.sprite.Sprite.__init__(self)
        self.screen=screen
        self.x=x
        self.y=y
        self.size=size
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

        if filename != None:
            self.set_image(filename)
            
    def set_image(self, filename):
            self.image= pygame.image.load(filename)
            if self.size != None:
                self.image=pygame.transform.scale(self.image,self.size)
            self.rect = self.image.get_rect()
            self.rect.center = [self.x, self.y]

    def update(self):
        pass

    def draw(self):
        if self.image == None or self.rect==None:
            raise Exception("Sprite image is not properly defined")

        self.screen.blit(self.image, self.rect)

