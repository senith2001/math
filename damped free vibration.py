import pygame
import math
#damped free vibration

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
uy=0

v=0
x=640
g=100
k=10000
m=100000
u0 = g*m/k
t = 0
c=10000
ccr = 2*((m*k)**(1/2))
wn = ((k/m)**(1/2))
dr = c/ccr
wd = wn*(1-dr**2)**(1/2)
ls = []
while running:
    dt = clock.tick(250)  /1000
    t+=dt
    x+=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    pygame.draw.circle(screen,(255,0,0),(640,300+uy),50)
    pygame.draw.line(screen,(0,0,0),(200,50),(1080,50),4)
    pygame.draw.line(screen,(255,255,255),(640,50),(640,300+uy),2)
    uy = math.e**(-dr*wn*t)*(math.sin(t*wd)*(dr*wn*u0)/wd)
    print(uy)
    ls.insert(1,[640,300+uy])
    for i in ls:
        pygame.draw.circle(screen,(0,255,0),i,2)
    for p in range(len(ls)):
        ls[p][0] += wd*50*dt
    pygame.display.flip()

   

pygame.quit()