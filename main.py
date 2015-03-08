import pygame
import random
import gameobject
import game
import balls
import dnd

SIZE = 640, 480

def Init(sz):
    '''Turn PyGame on'''
    global screen, screenrect
    pygame.init()
    screen = pygame.display.set_mode(sz)
    screenrect = screen.get_rect()

class GameWithDnD(game.GameWithObjects):
    def __init__(self, universe, *argp, **argn):
        game.GameWithObjects.__init__(self, universe, [ dnd.DnD(self) ] )

Init(SIZE)
Game = game.Universe(50)

Run = GameWithDnD(Game)

x, y = random.randrange(screenrect.w), random.randrange(screenrect.h)
dx, dy = 1+random.random()*5, 1+random.random()*5
Run.objects.append(balls.Ball("ball.gif",(x,y),(dx,dy)))

x, y = random.randrange(screenrect.w), random.randrange(screenrect.h)
dx, dy = 1+random.random()*5, 1+random.random()*5
Run.objects.append(balls.GravityBallFinal("ball.gif",(x,y),(dx,dy)))

x, y = random.randrange(screenrect.w), random.randrange(screenrect.h)
dx, dy = 1+random.random()*5, 1+random.random()*5
Run.objects.append(balls.RollBallFinal("ball.gif",(x,y),(dx,dy)))

x, y = random.randrange(screenrect.w), random.randrange(screenrect.h)
dx, dy = 1+random.random()*5, 1+random.random()*5
Run.objects.append(balls.GravityRollBall("ball.gif",(x,y),(dx,dy)))

Game.Start()
Run.Init()
again = True
while again:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        again = False
    Run.Events(event)
    Run.Logic(screen)
    Run.Draw(screen)
    pygame.display.flip()
Game.Finish()
pygame.quit()
