#!/usr/bin/env python
# coding: utf

import pygame
import random
import gameobject
import game
import dnd
import math

from operator import mul, add, sub, div

RESISTANCE = 0.005
FRICTION = 0.1
GRAVITY = 2

def intn(*arg):
    return map(int,arg)
def vadd(a, b):
    return map (add,a,b)
def vsub(a, b):
    return map (sub,a,b)
def vmul(a, v):
    return map (lambda x: x * v, a)
def vdiv(a, v):
    return map (lambda x: x/v, a)
def vdot(a, b):
    s = 0;
    for e in map(mul,a,b):
        s += e;
    return s;
def vlen(a):
    return math.sqrt(vdot(a,a))
def vnormalize(a):
    l = vlen(a)
    if (l == 0):
        return a
    return vdiv(a,l)



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
        elif x > surface.get_width() - self.rect.width/2:
            x = surface.get_width() - self.rect.width/2
            dx = -dx
        if y < self.rect.height/2:
            y = self.rect.height/2
            dy = -dy
        elif y > surface.get_height() - self.rect.height/2:
            y = surface.get_height() - self.rect.height/2
            dy = -dy
        self.hit =  x == self.rect.width/2 or y < self.rect.height/2 or \
                    x == surface.get_width() - self.rect.width/2 or \
                    y == surface.get_height() - self.rect.height/2
        self.pos = x,y
        dx = dx*(1 - RESISTANCE);
        dy = dy*(1 - RESISTANCE);
        speed = vlen((dx, dy));
        if speed < 0.7:
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
        speed = vlen((dx, dy))
        if dx > 0 and dy > 0:
            self.angle += speed
        elif dx > 0 and dy <= 0:
            self.angle -= speed
        elif dx <= 0 and dy <= 0:
            self.angle += speed
        #elif dx <= 0 and dy > 0:
        else:
            self.angle -= speed
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

class HitBall(Ball):
    def __init__(self, filename, game, pos = (0.0, 0.0), speed = (0.0, 0.0), \
                 mass = 10):
        Ball.__init__(self, filename, pos, speed)
        self.__game = game
        self.mass = mass
        self.hits = []
        self.surface = pygame.transform.scale(self.surface, \
                       map(int, vmul(self.surface.get_size(),mass/10.)))
        self.rect = self.surface.get_rect()
        self.radius = self.surface.get_width()/2
    def action(self):
        for obj in self.hits:
            self.processHit(obj)
            obj.hits.remove(self)
        self.hits = []
        pass
    def logic(self, surface):
        speed = vlen(self.speed)
        if speed > self.radius * 1.5:
            vmul(self.speed, self.radius * 1.5 / speed)
        for obj in self.__game.objects:
            if obj in self.hits or obj == self:
                continue
            self.hitball(obj)
    def draw(self, surface):
        pass
    def hitball (self, other):
        try:
            if not self.rect.colliderect(other.rect):
                return
            hits = other.hits;
            delta = vsub(self.pos, other.pos);
            d = vlen(delta)
            if d < self.radius + other.radius:
                self.hits.append(other)
                hits.append(self)
        except AttributeError:
            pass
    def processHit (self, other):
        ''' from stack overflow:
            http://stackoverflow.com/questions/345838/ball-to-ball-collision-detection-and-handling '''
        delta = vsub(self.pos, other.pos);
        d = vlen(delta)
        if d == 0.:
            d = 0.1
        mtd = vmul(delta, (self.radius + other.radius - d)/d)
        im1 = 1.0/self.mass
        im2 = 1.0/other.mass
        self.pos = vadd(self.pos, vmul(mtd, im1/(im1 + im2)))
        other.pos = vsub(other.pos, vmul(mtd, im2/(im1 + im2)))
        v = vsub(self.speed, other.speed);
        vn = vdot(vnormalize(mtd), v)
        if vn > 0.:
            return
        i = (-(1 + 0.5) *vn) / (im1 + im2);
        impulse = vmul(vnormalize(mtd), i);
        self.speed = vadd(self.speed, vmul(impulse, im1))
        other.speed = vsub(other.speed, vmul(impulse, im2))

class HitBallFinal(HitBall):
    def __init__(self, filename, game, pos = (0.0, 0.0), speed = (0.0, 0.0), 
                 mass = 10):
        Ball.__init__(self,filename,pos,speed)
        HitBall.__init__(self,filename, game, pos, speed, mass)
    def action(self):
        HitBall.action(self)
        Ball.action(self)
    def logic(self, surface):
        HitBall.logic(self, surface)
        Ball.logic(self, surface)
    def draw(self, surface):
        HitBall.draw(self, surface)
        Ball.draw(self, surface)

class GravityRollHitBall(GravityBall, RollBall, HitBall):
    def __init__(self, filename, game, pos = (0.0, 0.0), speed = (0.0, 0.0), 
                 mass = 10):
        Ball.__init__(self, filename, pos, speed)
        GravityBall.__init__(self,filename, pos, speed)
        HitBall.__init__(self, filename, game, pos, speed, mass)
        RollBall.__init__(self, filename, pos, speed)
        self.roll = True
    def action(self):
        HitBall.action(self)
        if self.roll:
            RollBall.action(self)
        GravityBall.action(self)
        Ball.action(self);
    def logic(self,surface):
        HitBall.logic(self, surface)
        RollBall.logic(self, surface)
        GravityBall.logic(self, surface)
        self.roll = self.hit
        Ball.logic(self, surface)
        self.roll = not self.roll or not self.hit
    def draw(self, surface):
        HitBall.draw(self, surface)
        GravityBall.draw(self, surface)
        RollBall.draw(self, surface)
        Ball.draw(self, surface)
