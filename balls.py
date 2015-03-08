#!/usr/bin/env python
# coding: utf

import pygame
import random
import gameobject
import game
import dnd
import math

RESISTANCE = 0.005
FRICTION = 0.1
GRAVITY = 2

def intn(*arg):
    return map(int,arg)
def speed(dx, dy):
    return math.sqrt(dx*dx + dy*dy)

class Ball(gameobject.GameObject):
    '''Simple ball class'''

    def __init__(self, filename, pos = (0.0, 0.0), speed = (0.0, 0.0)):
        '''Create a ball from image'''
        gameobject.GameObject.__init__(self)
        self.fname = filename
        self.surface = pygame.image.load(filename)
        self.rect = self.surface.get_rect()
        self.speed = speed
        self.pos = pos
        self.newpos = pos
        self.active = True
        self.hit = False

    def draw(self, surface):
        self.rect.center = intn(*self.pos)
        surface.blit(self.surface, self.rect)

    def action(self):
        '''Proceed some action'''
        if self.active:
            self.pos = self.pos[0]+self.speed[0], self.pos[1]+self.speed[1]

    def logic(self, surface):
        x,y = self.pos
        dx, dy = self.speed
        if x < self.rect.width/2:
            x = self.rect.width/2
            dx = -dx
            self.hit = True
        elif x > surface.get_width() - self.rect.width/2:
            x = surface.get_width() - self.rect.width/2
            dx = -dx
            self.hit = True
        if y < self.rect.height/2:
            y = self.rect.height/2
            dy = -dy
            self.hit = True
        elif y > surface.get_height() - self.rect.height/2:
            y = surface.get_height() - self.rect.height/2
            dy = -dy
            self.hit = True
        else:
            self.hit = False
        self.pos = x,y
        dx = dx*(1 - RESISTANCE);
        dy = dy*(1 - RESISTANCE);
        __speed = speed(dx, dy);
        if __speed < 0.7:
            dx = dy = 0
        self.speed = dx,dy

class GravityBall(Ball):
    def __init__(self, filename, pos = (0.0, 0.0), speed = (0.0, 0.0)):
        pass
    def action(self):
        self.speed = (self.speed[0], self.speed[1] + GRAVITY)
    def logic(self, surface):
        x,y = self.pos
        dx, dy = self.speed
        if y > surface.get_height() - self.rect.height/2:
            dx*=(1 - FRICTION)
        self.speed = dx,dy
    def draw(self, surface):
        pass

class GravityBallFinal(GravityBall):
    def __init__(self, filename, pos = (0.0, 0.0), speed = (0.0, 0.0)):
        Ball.__init__(self,filename,pos,speed)
        GravityBall.__init__(self,filename,pos, speed)
    def action(self):
        GravityBall.action(self)
        Ball.action(self)
    def logic(self, surface):
        GravityBall.logic(self, surface)
        Ball.logic(self, surface)
    def draw(self, surface):
        GravityBall.draw(self, surface)
        Ball.draw(self, surface)

class RollBall(Ball):
    def __init__(self, filename, pos = (0.0, 0.0), speed = (0.0, 0.0)):
        self.angle = 0
        self.orig_rect = self.rect
        self.orig_surface = self.surface
    def action(self):
        dx, dy = self.speed
        __speed = speed(dx, dy)
        if dx > 0 and dy > 0:
            self.angle += __speed
        elif dx > 0 and dy <= 0:
            self.angle -= __speed
        elif dx <= 0 and dy <= 0:
            self.angle += __speed
        #elif dx <= 0 and dy > 0:    
        else:
            self.angle -= __speed
    def logic(self, surface):
        self.rect = self.orig_rect
    def draw(self, surface):
        self.surface = pygame.transform.rotate(self.orig_surface, self.angle)
        self.rect = self.surface.get_rect(center=self.pos)

class RollBallFinal(RollBall):
    def __init__(self, filename, pos = (0.0, 0.0), speed = (0.0, 0.0)):
        Ball.__init__(self,filename,pos,speed)
        RollBall.__init__(self,filename,pos, speed)
    def action(self):
        RollBall.action(self)
        Ball.action(self)
    def logic(self, surface):
        RollBall.logic(self, surface)
        Ball.logic(self, surface)
    def draw(self, surface):
        RollBall.draw(self, surface)
        Ball.draw(self, surface)

class GravityRollBall(GravityBall, RollBall):
    def __init__(self, filename, pos = (0.0, 0.0), speed = (0.0, 0.0)):
        Ball.__init__(self, filename, pos, speed)
        GravityBall.__init__(self,filename, pos, speed)
        RollBall.__init__(self, filename, pos, speed)
        self.roll = True
    def action(self):
        if self.roll:
            RollBall.action(self)
        GravityBall.action(self)
        Ball.action(self);
    def logic(self,surface):
        RollBall.logic(self, surface)
        GravityBall.logic(self, surface)
        self.roll = self.hit
        Ball.logic(self, surface)
        self.roll = not self.roll or not self.hit
    def draw(self, surface):
        GravityBall.draw(self, surface)
        RollBall.draw(self, surface)
        Ball.draw(self, surface) 

