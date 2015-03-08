#!/usr/bin/env python
# coding: utf

class GameObject(object):
    '''Base class for objects in screen'''
    def __init__(self):
        self.processed = False
    def draw(self, surface):
        pass
    def action(self):
        pass
    def logic(self, surface):
        pass
    def process(self, event):
        pass
    def setProcessed(self, processed = False):
        self.processed = processed;
