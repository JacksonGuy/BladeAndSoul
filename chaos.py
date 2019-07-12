#Chaos Engine Version 3 (12/6/18)

import math, json
import random
import time
import pygame
import os, sys
import socket

object_list = []

class Object():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = 0 

        self.speed = 1

        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

        self.sprite = None 
        self.color = None 

        object_list.append(self)

        self.is_clicked = False

        self.alive = True

        self.object_type = None

    def draw_self(self):
        if self.alive:
            if self.sprite != None: #object has a sprite
                draw_image(self.sprite,self.x,self.y)
            elif self.radius != 0 and self.color != None: #object doesn't have sprite, but has radius and color (object is a circle)
                draw_circle(self.x,self.y,self.radius,self.color)
            elif self.radius == 0 and self.color != None: #object has no radius, so its a rect
                draw_rect(self.x,self.y,self.width,self.height,self.color)
            elif self.radius != 0 and self.color == None: #has radius, but no color
                draw_circle(self.x,self.y,self.radius,blue)
            else: #fallback statement, no color, no sprite, no radius
                draw_rect(self.x,self.y,self.width,self.height,blue)

    def player_input(self):
        if self.alive:
            pressed = get_input()
            if pressed[pygame.K_w] or pressed[UP]:
                self.y -= self.speed
            if pressed[pygame.K_s] or pressed[DOWN]:
                self.y += self.speed
            if pressed[pygame.K_a] or pressed[LEFT]:
                self.x -= self.speed
            if pressed[pygame.K_d] or pressed[RIGHT]:
                self.x += self.speed

        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.draw_self()

    def player_loop(self): #checks for input and status of being alive
        self.player_input()
        if self.health <= 0: 
            self.alive = False

    def Object_loop(self):
        if self.health <= 0:
            self.alive = False
            
    def projectile_update(self,playerx,playery):
        move_projectile(self,playerx,playery,self.mx,self.my)
        self.x, self.y = int(self.x), int(self.y)
        self.draw_self()

#color presets
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
purple = (128, 0, 128)
magenta = (255, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
orange = (255, 128, 0)

colors = [blue,red,green,yellow,purple,magenta,white,black,orange]

def window_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()

global W_width
global W_height
global screen

pygame.init()

W_width = 800
W_height = 600

screen = pygame.display.set_mode((W_width,W_height))
screen.set_alpha(None)

def draw_rect(x,y,width,height,color):
    pygame.draw.rect(screen,color,pygame.Rect(x,y,width,height))

def draw_circle(x,y,radius,color):
    pygame.draw.circle(screen,color,(x,y),radius)

def draw_line(x1,y1,x2,y2,width,color):
    pygame.draw.line(screen,color,(x1,y1),(x2,y2),width)

def get_input():
    return (pygame.key.get_pressed())

def load_image(image):
    return (pygame.image.load(image))

def draw_image(image,x,y):
    screen.blit(image,(x,y))

def draw_text(text,x,y,color,font):
    Text = font.render(text,True,color)
    screen.blit(Text, (x,y))

def get_mouse_position():
    return (pygame.mouse.get_pos())

def get_mouse_input():
    return (pygame.mouse.get_pressed())

def find_distance(x1,y1,x2,y2):
    return (math.hypot(x1-x2, y1-y2))

def get_random_point(Object, Range): #gets random point near an object
    x1 = Object.x - Range
    x2 = Object.x + Range
    y1 = Object.y - Range
    y2 = Object.y + Range
    new_x = random.choice(range(int(x1),int(x2)))
    new_y = random.choice(range(int(y1),int(y2)))
    return (new_x,new_y)

def check_collision(Object1,Object2):
    return Object1.rect.colliderect(Object2.rect)

def fill_screen(color):
    screen.fill((color))

def check_clicked(object):
    click = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()
    if obj.x + obj.width > mouse[0] > obj.x and obj.y + obj.height > mouse[1] > obj.y:
        if click[0] == 1: #left mouse button 
            if obj.is_clicked == True: #If already true, make it false
                obj.is_clicked = False
                return obj.is_clicked
            else: #if false, make it True
                obj.is_clicked = True
                return obj.is_clicked 

def button(msg,x,y,w,h,font,color): #Create clickable object on screen
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    draw_text(msg, x, y, font, color)
    if x+w > mouse[0] > x and y+h > mouse[1] > y: #if mouse clicked and mouse is in rect
        if click[0] == 1:
            return True 
    draw_text(msg, x, y, font, color)

def get_closest_object(Object, exclude_list): #find closest object to another object
    temp_object_list = []
    closest_target = None
    for thing in object_list: #get object list
        if thing != Object and thing not in exclude_list:
            temp_object_list.append(thing)
        elif exclude_list == None: #no exclude_list is given
            if thing != Object:
                temp_object_list.append(thing)

    for thing in temp_object_list:
        dist = find_distance(Object.x,Object.y,thing.x,thing.y)
        if dist < closest_target or closest_target == None:
            closest_target = thing
        else:
            pass

    return(closest_target)

def move_projectile(Object,startx,starty,mx,my): 
    x1, y1 = mx - startx, my - starty
    angle = math.atan2(y1,x1)
    dx = Object.speed * math.cos(angle)
    dy = Object.speed * math.sin(angle)
    Object.x += dx
    Object.y += dy

def move(Object, x, y): #move object to a position
    x1, y1 = x - Object.x, y - Object.y
    angle = math.atan2(y1,x1)
    dx = Object.speed * math.cos(angle)
    dy = Object.speed * math.sin(angle)
    Object.x += dx
    Object.y += dy

#Defined arrow key input
UP = pygame.K_UP
DOWN = pygame.K_DOWN
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT

