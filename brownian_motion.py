import pygame
from scipy.stats import norm

pygame.init()
pygame.display.set_caption("BROWNIAN MOTION")
screen =pygame.display.set_mode((600,1000))
clock = pygame.time.Clock()
running = True
delta = 5
positions = []
for i in range(0,600,60):
    for j in range(0,1000,100):
        positions.append([i,j])
dt = 0.1
while running:
    dt = clock.tick(60) /100
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")
    for p in positions:

        pygame.draw.circle(screen,"white",p,6)
        p[0] = p[0] + norm.rvs(scale = delta**2*dt)
        p[1] = p[1] + norm.rvs(scale = delta**2*dt)
    pygame.display.flip()
pygame.quit()
