#ok whatever i'm starting from scratch
import pygame as pg
import time

#initialises pygame
pg.init()
screen = pg.display.set_mode((640,640))
smiley = pg.image.load('game/you-are-an-idiot.png').convert_alpha()
clock = pg.time.Clock()

running = True
x=-500
while running:
    #sets the screen colour
    screen.fill((100,100,100))
    #caps the framerate at 60fps
    clock.tick(20)
    #sets smiley position
    screen.blit(smiley, (x, 0))
    x+=1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    pg.display.flip()
pg.quit()