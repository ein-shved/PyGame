import gameobject
import pygame
import game

class DnD(gameobject.GameObject):
    def __init__(self, game):
        self.__game = game
        self.__drag = None

    def process(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = self.__game.locate(event.pos)
            if click:
                self.__drag = click[0]
                self.__drag.processed = True
        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
            if self.__drag:
                self.__drag.pos = event.pos
                self.__drag.speed = event.rel
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.__drag:
                self.__drag.processed = False
                self.__drag = None

    def action(self):
        if self.__drag:
            self.__drag.processed = True
