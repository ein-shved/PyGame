#!/usr/bin/env python
# coding: utf

import pygame
import random
import gameobject
import game
import dnd

def intn(*arg):
    return map(int,arg)

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

    def draw(self, surface):
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
        elif x > surface.get_width() - self.rect.width/2:
            x = surface.get_width() - self.rect.width/2
            dx = -dx
        if y < self.rect.height/2:
            y = self.rect.height/2
            dy = -dy
        elif y > surface.get_height() - self.rect.height/2:
            y = surface.get_height() - self.rect.height/2
            dy = -dy
        self.pos = x,y
        self.speed = dx,dy
        self.rect.center = intn(*self.pos)

class GravityBall(Ball):
    def __init__(self, filename, pos = (0.0, 0.0), speed = (0.0, 0.0)):
        Ball.__init__(self, filename, pos, speed)
    def action(self):
        self.speed = (self.speed[0], self.speed[1] + 2)
        Ball.action(self)

class RollBall(Ball):
    def __init__(self, filename, pos = (0.0, 0.0), speed = (0.0, 0.0)):
        self.__angle = 0;
        Ball.__init__(self, filename, pos, speed)

