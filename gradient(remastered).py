import pygame
import numpy as np
from threading import Thread
import queue
import math

def Transformation(x,y,t,A):
    A = [[255/280,-255/280],[0,255/360],[255/640,0]]
    X = [x,y]

    return np.matmul(A,X)


def ScalarMultiplication(X):
    scalar = [256,256,256]
    return np.mod(X,scalar)

def draw(part,t,A) :
    T = 0
    T = t.get()
    for y in range(part[0][1],part[1][1]):
        
        for x in range(part[0][0],part[1][0]):
            
            pygame.draw.circle(screen,ScalarMultiplication(Transformation(x,y,T,A)),(x,y),1)

def linearGradient(m,q):
        # t1 = Thread(target=draw,args=[[(0,0),(S_W//2,S_H//2)],q,[[255/120,-255/640],[0,0],[0,0]]])
    # t2 = Thread(target=draw,args=[[(S_W//2 ,0),(S_W,S_H//2)],q,[[0,0],[255/600,(255/600)*(320/180)],[0,0]]])
    # t3 = Thread(target=draw,args=[[(0,S_H//2),(S_W//2,S_H)],q,[[0,0],[0,0],[-255/920,-255/640]]])
    # t4 = Thread(target=draw,args=[[(S_W//2,S_H//2),(S_W,S_H)],q,[[0,0],[0,0],[0,0]]])
    # t1 = Thread(target=draw,args=[[(0,0),(S_W//2,S_H//2)],q,[[255/1280,0],[(255-720*m)/1280,m],[255/720,0]]])
    # t2 = Thread(target=draw,args=[[(S_W//2 ,0),(S_W,S_H//2)],q,[[255/1280,0],[(255-720*m)/1280,m],[255/720,0]]])
    # t3 = Thread(target=draw,args=[[(0,S_H//2),(S_W//2,S_H)],q,[[255/1280,0],[(255-720*m)/1280,m],[255/720,0]]])
    # t4 = Thread(target=draw,args=[[(S_W//2,S_H//2),(S_W,S_H)],q,[[255/1280,0],[(255-720*m)/1280,m],[255/720,0]]])
    t1 = Thread(target=draw,args=[[(0,0),(S_W//2,S_H//2)],q,[[255/1280,0],[(255-720*m)/1280,m],[255/720,0]]])
    t2 = Thread(target=draw,args=[[(S_W//2 ,0),(S_W,S_H//2)],q,[[255/1280,0],[(255-720*m)/1280,m],[255/720,0]]])
    t3 = Thread(target=draw,args=[[(0,S_H//2),(S_W//2,S_H)],q,[[255/1280,0],[(255-720*m)/1280,m],[255/720,0]]])
    t4 = Thread(target=draw,args=[[(S_W//2,S_H//2),(S_W,S_H)],q,[[255/1280,0],[(255-720*m)/1280,m],[255/720,0]]])
    t1.start()
    t2.start()
    t3.start()
    t4.start()


def circularRedGradient(start,end):
    global stop_threads
    for x in range(start[0],end[0],1):
        if stop_threads:
            break
        for y in range(start[1],end[1],1):
            if stop_threads:
                break
            if (((x-720)**2) + ((y-360)**2)) <= 120**2 :
                pygame.draw.circle(screen,(((x-720)**2)/((120**2 )/255 )  + ((y-360)**2)/((120**2)/255),((x-720)**2)/((120**2 )/255 )  + ((y-360)**2)/((120**2)/255),((x-720)**2)/((120**2 )/255 )  + ((y-360)**2)/((120**2)/255)),(x,y),5)
            

def threadsForCircularGradient():
    t1 = Thread(target=circularRedGradient,args=[(0,0),(640,360)])
    t2 = Thread(target=circularRedGradient,args=[(640,0),(1280,360)])
    t3 = Thread(target=circularRedGradient,args=[(0,360),(640,720)])
    t4 = Thread(target=circularRedGradient,args=[(640,360),(1280,720)])
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    return [t1,t2,t3,t4]

def helixGradient():
    global stop_threads
    for x in range(S_W):
        if stop_threads:
            break
        for y in range(S_H):
            if stop_threads:
                break
            if (x*S_H )==  (S_W*y):
                pygame.draw.circle(screen,((255*2)/math.pi *math.acos(x/S_W),(255*2)/math.pi *math.acos(x/S_W),(255*2)/math.pi *math.acos(x/S_W)),(x*2,y),20)


def threadsForHelixGradient():
    t1 = Thread(target=helixGradient)
    t2 = Thread(target=helixGradient)
    t3 = Thread(target=helixGradient)
    t4 = Thread(target=helixGradient)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    return [t1,t2,t3,t4]


def myGradient(start,end,q,state,steps):
    global stop_threads
    global thState
    
    
    
    radius = q.get()
    for x in range(start[0],end[0],steps[0]):
        if stop_threads:
            break
        for y in range(start[1],end[1],steps[1]):
            if stop_threads:
                break
            pygame.draw.circle(screen,(radius*math.cos(math.pi*x/2/S_W),radius*math.sin(math.pi*x/2/S_W)*math.sin(math.pi*y/2/S_H),radius*math.sin(math.pi*x/2/S_W)*math.cos(math.pi*y/2/S_H)),(x,y),1)
    thState[state]       = True


def threadsForMygradient(q):
    global thState
    t1 = Thread(target=myGradient,args=[(0,0),(640,360),q,0,[1,1]])
    t2 = Thread(target=myGradient,args=[(1280,360),(640,0),q,1,[-1,1]])
    t3 = Thread(target=myGradient,args=[(0,360),(640,720),q,2,[1,-1]])
    t4 = Thread(target=myGradient,args=[(1280,720),(640,360),q,3,[-1,-1]])
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    # thState = [False,False,False,False]
    return [t1,t2,t3,t4]

def main(running):
    t = 0
    # m = -100
    q  = queue.Queue()
    global stop_threads
    global thState 
    thState=  [True,True,True,True]
    radius = 255
    q.put(radius)
    FPS = 250
    screen.fill("white")
    ths = threadsForMygradient(q)
    while running:
        dt = clock.tick(FPS)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        # linearGradient(m,q)   
        
        
        pygame.display.flip()
        # for t in ths:
        #     t.join()
        

    
        
        
        
    stop_threads = True
    
    for i in ths:
        i.join()
    pygame.quit()


    
                
stop_threads = False

if __name__ == "__main__":
    pygame.init()
    S_W = 1280
    S_H = 720
    screen = pygame.display.set_mode((S_W,S_H))
    pygame.display.set_caption("gradient creating using vector spaces and linear transformation")
    clock = pygame.time.Clock()
    running = True
    



    main(running)