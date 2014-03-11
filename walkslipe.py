SCREEN_SIZE = (75*8, 75*7)
SPEED = 24
X_FLOORALIGN_Y =  lambda x,y:x-x%y
AUTOMODE = True
eater = "walkman75x75.jpg"
eatee = "zzqq75x75p.jpg"
background_image_name="background640x640.jpg"
import pygame
import pygame._view
from pygame.locals import *
from sys import exit
from gameobjects.vector2 import Vector2
from random import randint, choice
from math import *

MOVE_LEFT = Vector2(-1,0)
MOVE_RIGTH = Vector2(1,0)
MOVE_UP = Vector2(0,-1)
MOVE_DOWN = Vector2(0,1)
DEFAULT_VECTOR= MOVE_RIGTH

def getVectorAngle(v1,v2):
    x,y = v1*v2
    cosxy = (x+y)/(v1.get_length()*v2.get_length())
    x1,y1 = v1
    x2,y2 = v2
    radian_xy = acos(cosxy)
    cross = x1*y2 - x2*y1
    if cross < 0:
        radian_xy = 2*pi - radian_xy    
    return radian_xy*180.0 / pi

class GameEntity(object):
 
    def __init__(self, image,location,active_area):
        self.image = image
        self.location = location
        self.destination = Vector2(0, 0)
        self.speed = 0.
        self.id = 0
        self.active_area = active_area

    def render(self, surface):
        x, y = self.location
        w, h = self.image.get_size()
        surface.blit(self.image, (x-w/2, y-h/2))   
 
    def process(self, time_passed):
        self.brain.think()
        if self.speed > 0. and self.location != self.destination:
            vec_to_destination = self.destination - self.location
            distance_to_destination = vec_to_destination.get_length()
            heading = vec_to_destination.get_normalized()
            travel_distance = min(distance_to_destination, time_passed * self.speed)
            self.location += travel_distance * heading

class Spritegroup:
  def __init__(self,name):
    self.name = name
    self.entities = []
    self.length=0
    self.head = {}
  def setHead(self,entity):
    self.head = entity
  def timepassed(self,timepass):
    self.time_passed =timepass
  def add(self,entity):
    self.entities.append(entity)
    self.length += 1
  def remove(self,entity):
    self.entities.remove(entity)
    self.length -= 1
  def pop(self):
    self.entities.pop()
    self.length -= 1
  def get(self,index):
    return self.entities[index]
  def getLast(self):
    return self.entities[self.length-1]  
  def process(self,option):
     firstsnake = self.entities[0]
     firstsnake.process(option,self.time_passed)
     lastsnake=self.entities.pop()
     self.entities.insert(0,lastsnake)
     # print firstsnake.destination
     lastsnake.destination = firstsnake.destination
     lastsnake.direction = firstsnake.direction
     lastsnake.image = firstsnake.image
     if len(self.entities) > 1:
        firstsnake.destination = firstsnake.location
    
     # for entity in self.entities:
     #    entity.process(option)
  def render(self, surface):
    for entity in self.entities:
        entity.render(surface)

class Snake(GameEntity):
  def __init__(self,image,location,active_area):
    GameEntity.__init__(self,image,location,active_area)
    self.direction = MOVE_RIGTH
    self.destination = Vector2(0,0)
    self.speed = SPEED
    self.israndom = True
    self.src_image = image
 
  def render(self,screen):
    x, y = self.destination
    w,h = self.image.get_size()
    screen.blit(self.image, (x, y))
    self.location = self.destination

  def process(self,direction,timepassed):
    if self.direction != direction:
      self.orginal_direction = self.direction
    self.direction = direction
    sw,sh = self.active_area
    w,h = self.image.get_size()    
    destination=self.destination = self.location + self.direction*self.speed*timepassed   
    rotete_angle = getVectorAngle(DEFAULT_VECTOR,self.direction*(1,-1))+90
    self.image = pygame.transform.rotate(self.src_image, rotete_angle)
    # print destination
    if self.direction == MOVE_LEFT:
      if destination[0] < 0:
        destination[0]= SCREEN_SIZE[0]-w
      if self.israndom and randint(1, 20)==1:
        self.direction=MOVE_UP           
    elif self.direction == MOVE_RIGTH:
      if destination[0] > SCREEN_SIZE[0]-w:
        destination[0] = 0
      if self.israndom and randint(1, 20)==1:
        self.direction=MOVE_DOWN
    elif self.direction == MOVE_UP:
      if destination[1] < 0:
        destination[1]= SCREEN_SIZE[1]- h       
      if self.israndom and randint(1, 20)==1:
        self.direction=MOVE_RIGTH         
    elif self.direction == MOVE_DOWN:
      if destination[1] > SCREEN_SIZE[1]-h:
        destination[1]= 0
      if self.israndom and randint(1, 20)==1:
        self.direction=MOVE_LEFT 
    else:
      pass

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
snake_image = pygame.image.load(eater).convert_alpha()
leaf_image = pygame.image.load(eatee).convert_alpha()
background = pygame.image.load(background_image_name).convert_alpha()

font = pygame.font.SysFont("arial", 16);
snake_image = pygame.transform.rotate(snake_image, -90)
snake_w, snake_h = snake_image.get_size()
font_height = font.get_linesize()
SPEED = snake_w
w = snake_w/2
h = snake_h/2

sw, sh = SCREEN_SIZE
clock = pygame.time.Clock()

leaf_width,leaf_height = leaf_image.get_size()
destination=location = Vector2(300, 300)
snake = Snake(snake_image, location,SCREEN_SIZE)
snakegroups = Spritegroup("snake")
snakegroups.add(snake)
# self.background = pygame.surface.Surface(SCREEN_SIZE).convert()
#      self.background.fill((255, 255, 255))


leftcount=0
leaflocation = Vector2(0, 0)
mindistance = 1000
israndom = False
eatcount = 0
eatcount_text = "0"
press_direction = MOVE_RIGTH

while True:
    for event in pygame.event.get():
      if event.type == QUIT:
        	exit()
      if event.type == MOUSEBUTTONDOWN:
          if AUTOMODE == True:
            AUTOMODE = False
          else:
            AUTOMODE = True
    # if pygame.mixer.music.get_busy() == False:
    #     pygame.mixer.music.load('kukouly.mp3')
        # pygame.mixer.music.play() 
    pressed_keys = pygame.key.get_pressed()
    time_passed = clock.tick(30)
    time_passed = time_passed / 100.0
    # print snake_image.get_rect()
    snakegroups.timepassed(1)
    if pressed_keys[K_ESCAPE]:
        exit()
    if pressed_keys[K_LEFT]:
        if press_direction != MOVE_RIGTH:
          press_direction = MOVE_LEFT
        if AUTOMODE == False:
          snakegroups.process(MOVE_LEFT)
        # destination = snake.location + snake.direction*snake.speed
    if pressed_keys[K_RIGHT]:
        if press_direction != MOVE_LEFT:
          press_direction = MOVE_RIGTH
        # destination = snake.location + snake.direction*snake.speed
        if AUTOMODE == False:
          snakegroups.process(MOVE_RIGTH)
    if pressed_keys[K_UP]:
        if press_direction != MOVE_DOWN:
          press_direction = MOVE_UP
        # destination = snake.location + snake.direction*snake.speed
        if AUTOMODE == False:
          snakegroups.process(MOVE_UP)
    if pressed_keys[K_DOWN]:
        if press_direction != MOVE_UP:
          press_direction = MOVE_DOWN
        # destination = snake.location + snake.direction*snake.speed
        if AUTOMODE == False:
          snakegroups.process(MOVE_DOWN)
    
    # destination = snake.location + snake.direction*snake.speed

    # screen.fill((0, 0, 0))    
    screen.blit(background, (0,0))
    if leftcount==1:
      snakehead = snakegroups.get(0)
      reallocation = snakehead.location 
      distancels = reallocation.get_distance_to(leaflocation)
      mindistance = min(mindistance,distancels)
      # print(distancels)
      # print "snake=%s leaf=%s distance=%s" %(snake.location,leaflocation,distancels)
      if distancels > 25.0:
        screen.blit(leaf_image, leaflocation)
      else:
        leftcount-=1
        eatcount+=1
        snaketail = snakegroups.getLast()
        newsnakelocation = snaketail.location - snaketail.direction*snake.image.get_size()
        new_snake = Snake(snake_image, newsnakelocation,SCREEN_SIZE)
        new_snake.direction = snaketail.direction  
        new_snake.destination = new_snake.location + new_snake.direction*new_snake.speed     
        snakegroups.add(new_snake)

    if AUTOMODE == True:
      snakegroups.process(press_direction)

    if leftcount == 0:
      leaf_unit_x = X_FLOORALIGN_Y(max(leaf_width, SPEED),SPEED)   
      factor_x = int(((SCREEN_SIZE[0]-leaf_unit_x) / leaf_unit_x))
      leaf_unit_y = X_FLOORALIGN_Y(max(leaf_height, SPEED),SPEED) 
      factor_y = int(((SCREEN_SIZE[1]-leaf_unit_y) / leaf_unit_y))

      new_leaf_location_x = randint(0,factor_x)*leaf_unit_x
      new_leaf_location_y = randint(0,factor_y)*leaf_unit_y
      leaflocation = Vector2(new_leaf_location_x, new_leaf_location_y)
      x, y = leaflocation     
      print leaflocation
      screen.blit(leaf_image, (x, y))    
      leftcount+=1

    # snake.location = destination
    # x, y = snake.location
    # screen.blit(snake.image, (x-w, y-h))
    snakegroups.render(screen)
    eatcount_text = str(eatcount)
    screen.blit( font.render(eatcount_text, True, (0, 0, 0)), (0, 0) )

    pygame.display.update()
    clock.tick(10)