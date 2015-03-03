import pygame

class GameMode:
    '''Basic game mode class'''
    def __init__(self):
        self.background = pygame.Color("black")

    def Events(self,event):
        '''Event parser'''
        pass

    def Draw(self, screen):
        screen.fill(self.background)

    def Logic(self, screen):
        '''What to calculate'''
        pass

    def Leave(self):
        '''What to do when leaving this mode'''
        pass

    def Init(self):
        '''What to do when entering this mode'''
        pass

class Universe:
    '''Game universe'''

    def __init__(self, msec, tickevent = pygame.USEREVENT):
        '''Run a universe with msec tick'''
        self.msec = msec
        self.tickevent = tickevent

    def Start(self):
        '''Start running'''
        pygame.time.set_timer(self.tickevent, self.msec)

    def Finish(self):
        '''Shut down an universe'''
        pygame.time.set_timer(self.tickevent, 0)

class GameWithObjects(GameMode):

    def __init__(self, universe, objects=[]):
        GameMode.__init__(self)
        self.objects = objects
        self.universe = universe

    def locate(self, pos):
        objs = [];
        for obj in self.objects:
            try:
                if obj.rect.collidepoint(pos):
                    objs.append(obj);
            except AttributeError as e:
                pass
        return objs

    def Events(self, event):
        GameMode.Events(self, event)
        if event.type == self.universe.tickevent:
            for obj in self.objects:
                obj.action()
        for obj in self.objects:
            if not obj.processed:
                obj.process(event)

    def Logic(self, surface):
        GameMode.Logic(self, surface)
        for obj in self.objects:
            obj.logic(surface)

    def Draw(self, surface):
        GameMode.Draw(self, surface)
        for obj in self.objects:
            obj.draw(surface)
