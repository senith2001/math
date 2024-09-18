import pygame
import math
#undamped free vibration

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
uy=0
v=0
g=100
k=10000
m=10000
t = 0
ls = []
while running:
    dt = clock.tick(60)  /1000
    t+=dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    pygame.draw.circle(screen,(255,0,0),(640,300+uy),50)
    pygame.draw.line(screen,(0,0,0),(200,50),(1080,50),4)
    pygame.draw.line(screen,(255,255,255),(640,50),(640,300+uy),2)
    uy = (g*m/k)*math.sin(((k/m)**(1/2)) * t)
    ls.insert(1,[640,300+uy])
    for i in ls:
        pygame.draw.circle(screen,(0,0,255),i,2)
    for p in range(len(ls)):
        ls[p][0] +=  ((k/m)**(1/2))*20*dt
    pygame.display.flip()
    
   

pygame.quit()