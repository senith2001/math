import pygame
import math
from decimal import Decimal

pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
pygame.display.set_caption("FUNCTIONS OF GRADIENT")
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
running = True


def gradient_curve1(x,y):
    R = 255*math.cos((math.pi*x)/(2*SCREEN_WIDTH))
    G = 255*math.sin((math.pi*x)/(2*SCREEN_WIDTH))*math.sin((math.pi*y)/(2*SCREEN_HEIGHT))
    B = 255*math.sin((math.pi*x)/(2*SCREEN_WIDTH))*math.cos((math.pi*y)/(2*SCREEN_HEIGHT))


    return (R,G,B)

def gradient_curve2(x,y):
    shi =((math.pi)/(2*math.e ))* (math.e**(x/SCREEN_WIDTH)) - (math.pi) /(2*math.e )
    theta = ((math.pi)/(2 *math.e ))* (math.e**(y/SCREEN_HEIGHT)) - (math.pi)/(2 *math.e )
    R = 255*math.cos(shi)
    G = 255*math.sin(shi)*math.sin(theta)
    B = 255*math.sin(shi)*math.cos(theta)
    print(R,G,B)
    return (R,G,B)




x = None
y = None
clicked_points = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_points.append(pygame.mouse.get_pos())
    # screen.fill("white")
    for p in clicked_points:
        pygame.draw.circle(screen,gradient_curve2(p[0],p[1]),p,20)




    pygame.display.flip()
    print('')



pygame.quit()