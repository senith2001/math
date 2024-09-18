import pygame
import math
import numpy as np
from decimal import Decimal
pygame.init()
pygame.display.set_caption("coastal hydraulics")
screen = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()
running = True
pls = []
d = -360
T = 1
L = 700
k = 2*math.pi/L
f = 2*math.pi/T
t = 0
a =20
# for i in range(128):
#     ls = []
    
#     for k in range(72):
#         ls.append([10*(i),360+(k)*10])
#     pls.append(ls)
# pls = [
#         [[0,360],[64,360],[128,360],[192,360],[256,360],[320,360],[384,360],[448,360],[512,360],[576,360],[640,360],[704,360],[768,360],[832,360],[896,360],[960,360],[1024,368],[1088,360],[1152,360],[1216,360],[1280,360]],
#         [[0,500],[64,500],[128,500],[192,500],[256,500],[320,500],[384,500],[448,500],[512,500],[576,500],[640,500],[704,500],[768,500],[832,500],[896,500],[960,500],[1024,500],[1088,500],[1152,500],[1216,500],[1280,500]]

#     ]
pls2 = []
for r in range(21):
    ls2 = []
    for b in range(10):
        
        ls2.insert(1,[64*r,360+36*b])
    pls2.append(ls2)
while running:
    dt = clock.tick(60) / 1000
    t+=dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")
  
    for i in pls2:
        for j in i:
            Y= j[0]+(a*(math.sinh(k*(d+j[1])))/(math.sinh(k*d)))*(math.sin(f*t-k*j[0]))
            X = -(j[1]+(-a*(math.cosh(k*(d+j[1])))/(math.sinh(k*d)))*(math.cos(f*t-k*j[0])))+720+340
            print(X,Y)
            pygame.draw.circle(screen,'white',(Y,X),10)
  

    pygame.display.flip()
pygame.quit()