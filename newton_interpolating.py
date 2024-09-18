import pygame
from operator import itemgetter
import numpy as np
import math

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("NEWTON INTERPLATING POLYNOMIAL")
running = True
FPS = 250
x,y = None,None
A = []
coords = []
marks = []
points = []
drawn = True
N = 255
def draw_axes():
    pygame.draw.line(screen,"black",(SCREEN_WIDTH/2,0),(SCREEN_WIDTH/2,SCREEN_HEIGHT),5)
    pygame.draw.line(screen,"black",(0,SCREEN_HEIGHT/2),(SCREEN_WIDTH,SCREEN_HEIGHT/2),5)

def remove_partial_duplicate_rows(matrix):
    # Use a set to track seen elements
    seen_elements = set()
    unique_rows = []
    
    for row in matrix:
        # Check if any element in the current row is already in seen_elements
        if any(element in seen_elements for element in row):
            continue  # Skip this row if a partial match is found
        
        # Add all elements of the current row to the seen_elements set
        seen_elements.update(row)
        unique_rows.append(row)
    
    return unique_rows

def interpolate(coordinates):
    A.clear()
    for i in range(len(coordinates)):
        p = [1 for i in range(i+1)]
        for n in range(len(coordinates)-1,len(p)-1,-1):
            p.append(0)
        A.append(p)

    for k in range(1,len(A),1):
        for j in range(1,k+1):
            A[k][j] *= A[k][j-1]
            for m in range(j-1,k):
                A[k][j]*=(coordinates[k][0] - coordinates[m][0])
               
                
    
    
    
def create_polynomial_points(x,coordinates):
    points.clear()
    for i in range(-SCREEN_WIDTH//2,SCREEN_WIDTH//2,1):
        y = x[0]
        for j in range(1,len(x)):
            
            b = 1
            for k in range(j):
                b*= (i-coordinates[k][0])
            b*= x[j]
            y+= b
        if (y <= SCREEN_HEIGHT/2 ) and (y >= -SCREEN_HEIGHT/2 ):
            points.append([i+SCREEN_WIDTH/2,-y+SCREEN_HEIGHT/2])



    

def solve_matrix(matB):
    interpolate(coords)
    
    x = np.linalg.solve(A,matB)
    
    return  x

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawn = False
            x,y = pygame.mouse.get_pos()

    
        
    

    screen.fill("white")
    draw_axes()
    if not drawn:
        
        marks.append((x,y))
        if x>=SCREEN_WIDTH/2 and y <= SCREEN_HEIGHT/2:
            coords.append([x-SCREEN_WIDTH/2,SCREEN_HEIGHT/2 - y])
        elif x<=SCREEN_WIDTH/2 and y <= SCREEN_HEIGHT/2:
            coords.append([-(SCREEN_WIDTH/2 - x),SCREEN_HEIGHT/2 - y])
        elif x<= SCREEN_WIDTH/2 and y >= SCREEN_HEIGHT/2 :
            coords.append([-(SCREEN_WIDTH/2 - x),-(y-SCREEN_HEIGHT/2)])
        elif x >= SCREEN_WIDTH/2 and y >= SCREEN_HEIGHT/2:
            coords.append([x-SCREEN_WIDTH/2,-(y-SCREEN_HEIGHT/2)])

    
    
    
    if len(coords) >=2:
       
        coords = remove_partial_duplicate_rows(coords)
        coords = sorted(coords,key = itemgetter(0))
    if len(coords) >=2 and not drawn:
        
        create_polynomial_points(solve_matrix([y for (x,y) in coords]),coords)
        
    if len(points) >=2:
        for i in range(len(points)-1):
            R = N*math.sin((math.pi/2)*points[i][0]/SCREEN_WIDTH)*math.cos((math.pi/2)*points[i][1]/SCREEN_HEIGHT)
            G = N*math.sin((math.pi/2)*points[i][0]/SCREEN_WIDTH)*math.sin((math.pi/2)*points[i][1]/SCREEN_HEIGHT)
            B = N*math.cos((math.pi/2)*points[i][0]/SCREEN_WIDTH)
            print(R,G,B)
            if abs(points[i][0]-points[i+1][0]) ==1 :
                pygame.draw.line(screen,(R,G,B),points[i],points[i+1],10)
    for i in marks:
        pygame.draw.circle(screen,"red",i,10)
        pygame.draw.circle(screen,"white",i,5)
    drawn = True
   
    pygame.display.flip()
pygame.quit()
