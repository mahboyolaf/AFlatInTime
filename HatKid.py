from Movement import *
import pygame
import random
from constants import *
from GameSprite import *

class Hitbox(GameSprite):
    colour =(255,255,255,100)
    def __init__(self,x,y,screen=None):
        super().__init__(x,y,None,screen)
        #pygame.draw.rect(screen,(100,100,100),(x,y))
    def draw(self):
        pygame.draw.rect(self.screen, Hitbox.colour,self.rect)



# BUG if the atoms align you can clip through corners and sides
class HatKid(GameSprite):
    def __init__(self,x,y,screen,map):
        hatkid_filename = "sprite/HatKid/walk/walk1.png"
        size = (TILE_SIZE,TILE_SIZE)
        super().__init__(x,y,hatkid_filename,screen,size)
        self.hitbox=Hitbox(x,y,screen)
        self.walks=[]
        self.walk=Walk(map,self)
        self.jump=Jump(map,self)
        self.dive=Dive(map,self)
        self.walkright=self.walk.sprites_right
        self.walkleft=self.walk.sprites_left
        self.idleright=self.load_idle("sprite/HatKid/idle",Movement.Direction.RIGHT)
        self.idleleft=self.load_idle("sprite/HatKid/idle",Movement.Direction.LEFT)
        self.diveright=self.dive.diveright
        self.diveleft=self.dive.diveleft
        self.climbright=self.load_climb("sprite/HatKid/climb",Movement.Direction.RIGHT)
        self.climbleft=self.load_climb("sprite/HatKid/climb",Movement.Direction.LEFT)

        self.direction=Movement.Direction.RIGHT
        self.x_speed = 0
        self.current_frame = self.idleright[0]
        self.walk_index= 0
        self.is_on_ground= True
        self.has_jumped_in_air= False
        self.y_speed=0
        self.canjump= True
        self.divejumplock= False


    def load_idle(self,spritedir,direction):
        idles=[]
        for counter in range (1,4):
            idle= pygame.image.load(spritedir+"/idle"+str(counter)+".png")
            idle=pygame.transform.scale(idle,HATKIDSIZEIDLE)
            if direction==Movement.Direction.LEFT:
                idle=pygame.transform.flip(idle,True,False)
            idles.append(idle)
        return tuple(idles)
    
    # def load_dive(self,spritedir,direction):
    #     dives=[]
    #     for counter in range (1,3):
    #         dive= pygame.image.load(spritedir+"/dive"+str(counter)+".png")
    #         dive=pygame.transform.scale(dive,HATKIDSIZEDIVE)
    #         if direction==Movement.Direction.LEFT:
    #             dive=pygame.transform.flip(dive,True,False)
    #         dives.append(dive)
    #     return tuple(dives)
    
    def load_climb(self,spritedir,direction):
        climbs=[]
        for counter in range (1,2):
            climb= pygame.image.load(spritedir+"/climb"+str(counter)+".png")
            climb=pygame.transform.scale(climb,HATKIDSIZECLIMB)
            if direction==Movement.Direction.LEFT:
                climb=pygame.transform.flip(climb,True,False)
            climbs.append(climb)
        return tuple(climbs)    

    def dive_ground_right(self):
        print("right ground dive")
        self.has_dived=True
        if self.is_on_ground:
            self.decelerate_x(DIVEDECELERATE)
        else:
            self.decelerate_x(0.98)
        if self.y_speed <= MAXYSPEED:
            self.y_speed -=0.1
        # if self.has_tiles_under and self.is_moving_downward():
        #     self.y_speed=0
        # if self.has_tiles_above and self.is_moving_upwards():
        #     self.y_speed=0

    def dive_ground_left(self):
        print("left ground dive")
        self.x_speed=-DIVESPEED
        self.rect.y-=DIVEHOPHEIGHT
        self.has_dived=True

    #def dive(self):
        # if self.has_dived==False:
        #     if self.is_on_ground:
        #         if pygame.key.get_pressed()[pygame.K_d]:
        #             print("right ground dive")
        #             self.x_speed=MAXXSPEED+3
        #             #self.rect.y-=10
        #             self.has_dived=True
        #         if pygame.key.get_pressed()[pygame.K_a]:
        #             print("left ground dive")
        #             self.x_speed=-(MAXXSPEED+3)
        #             #self.rect.y-=10
        #             self.has_dived=True
        #     else:
        #         if self.direction== Movement.Direction.RIGHT:
        #             print("right air dive")
        #             self.x_speed=MAXXSPEED+3
        #             self.has_dived=True
        #         if self.direction== Movement.Direction.LEFT:
        #             print("left air dive")
        #             self.x_speed=-(MAXXSPEED+3)
        #             self.has_dived=True
    #def dive_cancel(self):
        #TODO:only reset has dived once dive canceled, cool down, change effects

        # if self.has_dived:
        #     self.rect.y-=5
        #     self.has_jumped_in_air=True
        #     self.y_speed=MAXXSPEED
        #     print("dive cancel")

    def check5pixel(self,map):
        """checks for doublejump"""
        self.rect.move_ip([0,-MAXYSPEED])
        hitlist=pygame.sprite.spritecollide(self,map.tiles,False)
        self.rect.move_ip([0,MAXYSPEED])
        return hitlist

    def set_y_speed(self,has_tiles_under,has_tiles_above):
        #gravity
        if self.y_speed <= MAXYSPEED:
            self.y_speed +=0.2
        if has_tiles_under and self.is_moving_downward():
            self.y_speed=0
        if has_tiles_above and self.is_moving_upwards():
            self.y_speed=0

    def set_x_speed(self,xspeed):
        self.x_speed=xspeed
        




    def is_moving_downward(self):
        return self.y_speed > 0
    
    def is_moving_upwards(self):
        return self.y_speed < 0
    
    def is_moving_right_fast(self):
        return self.x_speed >0.1
    def is_moving_left_fast(self):
        return self.x_speed <-0.1
    
    def is_moving_right(self):
        return self.x_speed >0
    def is_moving_left(self):
        return self.x_speed <0

    def set_can_jump(self,has_tiles_above):
        if has_tiles_above and self.is_moving_upwards() or self.divejumplock:
            self.canjump=False
        elif not HatKid.is_press_jump_key():
            self.canjump=True
        

    def is_press_jump_key():
        keyspressedlist=pygame.key.get_pressed()        
        return keyspressedlist[pygame.K_w] or keyspressedlist[pygame.K_SPACE]
    def has_jumpedtwice(self):
        return self.jump.count == 2

    def set_jumpdirection(self,has_tiles_under):
        keyspressedlist=pygame.key.get_pressed()
        if has_tiles_under:
            self.jumpdirection=False
        if keyspressedlist[pygame.K_d] and not self.dive.divestatus and not self.direction == Movement.Direction.LEFT\
              and not self.is_moving_left_fast() and self.has_jumpedtwice() and not self.jumpdirection:
            self.jumpdirection=True
        elif keyspressedlist[pygame.K_a] and not self.dive.divestatus and not self.direction == Movement.Direction.RIGHT\
              and not self.is_moving_right_fast() and self.has_jumpedtwice() and not self.jumpdirection:
            self.jumpdirection=True
    
    def set_jumpcount(self,has_tiles_under):
        if has_tiles_under:
            self.jump.count=0

    def set_isonground(self,has_tiles_under):
        self.is_on_ground= has_tiles_under

    def set_has_jumped_in_air(self,has_tiles_under):
        if has_tiles_under:
            self.has_jumped_in_air= False

    def set_hasdived(self,has_tiles_under):
        if has_tiles_under:
            self.has_dived=False
    def control_ground_collision(self,tilesunder):
        has_tiles_under=len(tilesunder)>0
        if has_tiles_under and (self.is_moving_downward() or self.is_stopped_y()):
                self.snap_to_ground_tile(tilesunder)

    def control_ceiling_collision(self,tilesabove):
        has_tiles_above=len(tilesabove)>0
        if has_tiles_above and self.is_moving_upwards():
            self.snap_to_celing_tile(tilesabove)
            print("something",has_tiles_above and self.is_moving_upwards())


    def control_left_collision(self,tilesleft):
        has_tiles_left=len(tilesleft)>0
        # if has_tiles_left and (self.is_moving_left() or self.is_stopped_x()):
        #     self.stop_x()
        #     self.snap_to_left_tile(tilesleft)
        if self.ispastleft() and self.is_moving_left():
            self.stop_x()
            self.snap_to_left_edge()

    def control_right_collision(self,tilesright):
        has_tiles_right=len(tilesright)>0
        # if has_tiles_right and (self.is_moving_right() or self.is_stopped_x()):
        #     self.stop_x()
        #     self.snap_to_right_tile(tilesright)
        if self.ispastright() and self.is_moving_right():
            self.stop_x()
            self.snap_to_right_edge()

    def snap_to_left_edge(self):
        self.hitbox.left=0


    def snap_to_right_edge(self):
        self.hitbox.right=SCREEN_WIDTH

    def snap_to_right_tile(self,tilesright):
        self.hitbox.rect.right=tilesright[0].rect.left

    def snap_to_left_tile(self,tilesleft):
        self.hitbox.rect.left=tilesleft[0].rect.right
        
    def snap_to_ground_tile(self,tilesunder):
            # NOTE why both hitbox and sprite?
                self.hitbox.rect.bottom=tilesunder[0].rect.top
                self.rect.bottom=tilesunder[0].rect.top
    
    def snap_to_celing_tile(self,tilesabove):
            # NOTE why both hitbox and sprite?
            self.hitbox.rect.top=tilesabove[0].rect.bottom
            self.rect.top=tilesabove[0].rect.bottom
            


    def stop_x(self):
        self.x_speed=0

    def is_stopped_x(self):
        return self.x_speed==0
    def is_stopped_y(self):
        return self.y_speed==0

    def is_direction_left(self):
        return self.direction == Movement.Direction.LEFT

    def is_direction_right(self):
        return self.direction == Movement.Direction.RIGHT
    
    def get_x_movement_direction(self):
        if self.is_direction_left():
            return(-1)
        if self.is_direction_right():
            return(1)
    def walk_right(self):
        if self.is_direction_left() or self.is_moving_left_fast():
            self.walk.stop()
        self.walk.set_direction(Movement.Direction.RIGHT)
        self.walk.start()

    def walk_left(self):
        if self.is_direction_right() or self.is_moving_right_fast():
            self.walk.stop()
        self.walk.set_direction(Movement.Direction.LEFT)
        self.walk.start()
    
    def decelerate_x(self,decelerationrate):
        if abs(self.x_speed)> 0.1:
            self.x_speed *= decelerationrate
        else:
            self.x_speed=0



    def update(self,map1):
        #update hitbox pos
        self.hitbox.rect.center=self.rect.center
        tilesunder= self.tilesunder(map1)
        tilesabove= self.tilesabove(map1)



        has_tiles_under= len(tilesunder)> 0
        has_tiles_above= len(tilesabove)> 0
        
        self.set_y_speed(has_tiles_under,tilesabove)
        self.set_can_jump(has_tiles_above)
        self.set_jumpcount(has_tiles_under)
        self.set_jumpdirection(has_tiles_under)
        self.set_isonground(has_tiles_under)
        self.set_has_jumped_in_air(has_tiles_under)
        self.set_hasdived(has_tiles_under)
        self.divejumplock= self.divejumplock and not self.is_on_ground

        self.control_ground_collision(tilesunder)
        self.control_ceiling_collision(tilesabove) 

        tilesright= self.tilesright(map1)
        tilesleft=  self.tilesleft(map1)
        self.control_left_collision(tilesleft)
        self.control_right_collision(tilesright)

        self.set_xpos()
        self.set_ypos()




        if(self.ispastbottom()):
            self.rect.x,self.rect.y=TILE_SIZE*4-16,TILE_SIZE*5
            self.x_speed,self.y_speed=-1,2

#check 1,2,3,4,5 but with y_speed and makes it not over shoot


    def set_xpos(self):
        self.rect.x+=self.x_speed  
        self.hitbox.rect.x+=self.x_speed

    def set_ypos(self):
        self.rect.y+=self.y_speed
        self.hitbox.rect.y+=self.y_speed

    def tilesunder(self,map):
        """return a list of tiles below hat kid"""
        checkahead=MAXYSPEED
        self.hitbox.rect.move_ip([0,checkahead])
        hitlist=pygame.sprite.spritecollide(self.hitbox,map.tiles,False)
        self.hitbox.rect.move_ip([0,-checkahead])
        return hitlist
    def tilesabove(self,map):
        """return a list of tiles above hat kid"""
        # self.rect.move_ip([0,-(self.y_speed+1)])
        self.hitbox.rect.move_ip([0,-MAXYSPEED*0.65])
        hitlist=pygame.sprite.spritecollide(self.hitbox,map.tiles,False)
        # self.rect.move_ip([0,self.y_speed+1])
        self.hitbox.rect.move_ip([0,MAXYSPEED*0.65])
        return hitlist    
    def tilesleft(self,map):
        """return a list of tiles above hat kid"""
        self.hitbox.rect.move_ip([-MAXXSPEED,0])
        hitlist=pygame.sprite.spritecollide(self.hitbox,map.tiles,False)
        self.hitbox.rect.move_ip([MAXXSPEED,0])
        return hitlist 
    def tilesright(self,map):
        self.hitbox.rect.move_ip([3,0])
        hitlist=pygame.sprite.spritecollide(self.hitbox,map.tiles,False)
        self.hitbox.rect.move_ip([-3,0])
        return hitlist   
    
    def ispastleft(self):
        return self.hitbox.rect.left <= 0

    def ispastright(self):
        return self.hitbox.rect.right >= WIDTHINTILES*TILE_SIZE


    def ispastbottom(self):
        """true or false if touching barrier on bottom"""
        return self.rect.y+TILE_SIZE >= HEIGHTINTILES*TILE_SIZE

    def draw(self):
        self.hitbox.draw()
        #pygame.draw.rect(self.screen, Hitbox.colour,self.rect).
        #self.hitbox=pygame.draw.rect(self.screen,(255,255,255,100),(self.rect.center[0]-self.hitbox.width/2,self.rect.bottomright[1]-self.hitbox.height,self.hitbox.width,self.hitbox.height))
        self.screen.blit(self.current_frame,self.rect)

