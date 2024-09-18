import pygame
import math

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720))
#main variables
running = True
FPS = 30
center = [640,360]
scale_factor = 1
scale_factor_ex =50
scale_factor_ex_y = 360
#==============================================   e^x function
def draw_ex():
    points = []
    for i in range(length+1):
        points.append([i,-(scale_factor_ex_y/math.e)*(math.e**((1/scale_factor_ex)*(i-center[0])))+height/2]) #260
    pygame.draw.lines(screen,'white',False,points,6)
#============================================== i th derivative of e^x

def diexdx(value,i):
    return math.e**(value)
#============================================== taylor series of e^x
def draw_taylor_series_ex(i,a,derivative):
    points = [] 
    ax =( a[0] - center[0])

    
    for k in range(length):
        y = math.e**(ax)
        deltaX =(((1/scale_factor_ex)*(k-center[0])) -ax) #k = 0 , deltaX = -640
        for m in range(i):
            y += (scale_factor_ex_y/math.e) *(deltaX**(m+1))*derivative(ax,m+1)/factorial(m+1) # m = 0 y = -639
        
        print(k,y)
        points.append([k,-y+height/2-360/math.e ])
    pygame.draw.lines(screen,"red",False,points,6)
#==============================================   sin function
def draw_sin(length,height,center,screen,scale_factor):
    points=[]
    for i in range(length):
        points.append([i,(-(height/4)*math.sin((i-center[0])*2*scale_factor*math.pi/length)+height/2)])
    
    pygame.draw.lines(screen,'white',False,points,6)
#=============================================    i th derivative of function sin
def disinxdx(i,value,height,length,scale_factor):
    scale = -height/4
    if i%2 == 0:
        return scale*math.cos(i*math.pi/2)*math.sin(value*2*scale_factor*math.pi/length)
    
    return scale*math.sin(i*math.pi/2)*math.cos(value*2*scale_factor*math.pi/length)
    
#==============================================   axes function
def drawAxes(center,screen):
    pygame.draw.line(screen,'white',(640,0),(640,720),3)
    pygame.draw.line(screen,'white',(0,360),(1280,360),3)
#=============================================== factorial function
def factorial(n):
    x = 1
    for i in range(n):
        x*=(i+1)
    return x
#===============================================   taylor series of sinx
def draw_taylor_series_sinx(a,center,length,height,i,derivative,n,scale_factor):
    #i = number of derivatives
    points = []
    ax = (a[0] -center[0])*2*scale_factor*math.pi/length
    
    

    for k in range(0,length):
        y = (height/4) *math.sin(ax)
        deltaX = (k-center[0])*2*scale_factor*math.pi/length - ax

        for h in range(i):
            y += -(deltaX**(h+1))*derivative(h+1,ax,height,length,scale_factor)/factorial(h+1)
        print(-y+height/2)
        points.append([k,-y+height/2])
    pygame.draw.lines(screen,"red",False,points,6)
    
a = [640,360]
length = 1280

height = 720

n =1280
t = 1
func = 2
while running:
    dt = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('black')
    drawAxes(center,screen)
    if func == 1:
        draw_sin(1280,720,center,screen,scale_factor)
        
        draw_taylor_series_sinx(a,center,length,height,t,disinxdx,n,scale_factor)
        scale_factor+=1
    elif func == 2:
        draw_ex()
        draw_taylor_series_ex(t,a,diexdx)
        
    # print(a)
    pygame.display.flip()
    t+=1
    
pygame.quit()