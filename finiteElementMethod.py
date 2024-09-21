import pygame
import math
import numpy as np
from operator import itemgetter

pygame.init()
S_W=1280
S_H = 720
screen = pygame.display.set_mode((S_W,S_H))
pygame.display.set_caption("finiteElementMethod")
clock = pygame.time.Clock()
running = True
FPS = 250

class FiniteElementMethod:
    def __init__(self,elements):
        self.elements = elements
    
    def solve(self,p):
        e = self.elements[0]
        print("displacements : ",np.linalg.solve(e.getKe(),e.NodelForces(p)))
        return np.linalg.solve(e.getKe(),e.NodelForces(p))
        
      

class TNElement:
    
    def __init__(self,L,E,I,position,udl):
        self.v1 = None
        self.t1 = None
        self.v2 = None
        self.t2 = None
        self.f1 = None
        self.f1 = None
        self.c1 = None
        self.c2 = None
        self.p = udl
        self.pos = position
        self.E = E
        self.I = I
        self.L = L
        self.scalar = self.E*self.I/(self.L**3)
        self.ke = np.array([
            [12,6*self.L,-12,6*self.L],
            [6*self.L,4*(self.L**2),-6*self.L,2*(self.L**2)],
            [-12,-6*self.L,12,-6*self.L],
            [6*self.L,2*(self.L**2),-6*self.L,4*(self.L**2)]
        ])*self.scalar
        
    
    def getDisplacements(self):
        return [self.v1[0],self.t1[0],self.v2[0],self.t2[0]] #0 for applying boundry conditions
    
    def getKe(self):
        return self.ke
    
    def calculateS(self,x):
        return (x-self.pos[0])/self.L
    
    def N1(self,s):
        return (1-3*(s**2)+2*(s**3))
    
    def N2(self,s):
        return (self.L*(s-2*(s**2)+s**3))
    
    def N3(self,s):
        return (3*(s**2) - 2*(s**3))
    
    def N4(self,s):
        return (self.L*(-(s**2) + s**3))
    
    def NodelForces(self,p):
        self.p = p
        self.f1 = self.p*self.L / 2
        self.f2 = -self.p*self.L / 2
        self.c1 = self.p *(self.L**2) /12
        self.c2 = -self.p *(self.L**2) /12
        return [[self.f1],[self.c1],[self.f2],[self.c2],[0]]

    def setDisplacements(self,displacements):
        self.v1 = displacements[0]
        self.t1 = displacements[1]
        self.v2 = displacements[2]
        self.t2 = displacements[3]
    
    def s(self,x):
        return (x - self.pos[0] )/self.L

class BEAM:
    def __init__(self,E,I,L,origin,udl) :
        self.E = E
        self.I = I
        self.L = L
        self.origin = origin
        self.points = []
        self.maximumDeflection = 0
        self.udl = udl
        self.element = TNElement(self.L,self.E,self.I,(0,0),self.udl)
        self.arrLength = 100
        self.method = None
        for i in range(self.L):
            self.points.append([i,0])
    def setP(self,t):
        # self.element.p= self.udl * (math.sin(t)**2+1)
        # self.element = TNElement(self.L,self.E,self.I,self.origin,self.udl)
        return self.udl * (math.sin(t)+1)
    def calculateKg(self,boundryConditions):
        self.element.ke = np.append(self.element.ke,boundryConditions,axis=0)
        
        matrixEdgeConditons = [[boundryConditions[0][0]],[boundryConditions[0][1]],[boundryConditions[0][2]],[boundryConditions[0][3]],[0]]
        
        self.element.ke = np.append(self.element.ke,matrixEdgeConditons,axis = 1)
        self.method=FiniteElementMethod([self.element])

    def color(self,deflection):

        ls = sorted(self.points,key = itemgetter(1))
        if abs(ls[-1][0]) >= abs(ls[0][0]):
            self.maximumDeflection = abs(ls[-1][1])
        else :
            self.maximumDeflection = abs(ls[0][1])
        if self.maximumDeflection == 0:
            return (0,0,255)
        color = (255*(abs(deflection)/self.maximumDeflection),0,255*(1-(abs(deflection)/self.maximumDeflection)))
        print("color is : ",color)
        return color
    def drawArrow(self,color,p):
        pygame.draw.line(screen,color,(p[0]+self.origin[0],self.origin[1]-self.arrLength),(p[0]+self.origin[0],p[1]+self.origin[1]))
        #pygame.draw.circle(screen,color,(p[0]+self.origin[0],p[1]+self.origin[1]),5)

    def drawForces(self):
        pygame.draw.line(screen,"black",(self.origin[0],self.origin[1]-self.arrLength ),(self.points[-1][0]+self.origin[0],self.origin[1]-self.arrLength),5)
        for i in range(0,len(self.points),5):
            self.drawArrow(self.color(self.points[i][1]),self.points[i])
        


    def drawBeam(self):
        for p in range(len(self.points)-1):
            print((self.points[p][0]+self.origin[0],self.points[p][1]+self.origin[1]))
            pygame.draw.line(screen,self.color(self.points[p][1]),(self.points[p][0]+self.origin[0],self.points[p][1]+self.origin[1]),(self.points[p+1][0]+self.origin[0],self.points[p+1][1]+self.origin[1]),20)

    def drawFixedEnd(self):
        pygame.draw.line(screen,"black",(self.origin[0],self.origin[1]-100),(self.origin[0],self.origin[1]+100),10)

    def draw(self):
        self.drawFixedEnd()
        self.drawBeam()
        self.drawForces()

    def solve(self,t):
        p = self.setP(t)
        #self.method=FiniteElementMethod([self.element])
        self.element.setDisplacements(self.method.solve(p))
        print(self.element.getDisplacements())
        for i in range(len(self.points)):
            self.points[i][1] = 0*self.element.getDisplacements()[0]*self.element.N1(self.element.s(self.points[i][0]))+ 0*self.element.getDisplacements()[1]*self.element.N2(self.element.s(self.points[i][0]))+ self.element.getDisplacements()[2]*self.element.N3(self.element.s(self.points[i][0])) + self.element.getDisplacements()[3]*self.element.N4(self.element.s(self.points[i][0]))
        

beam = BEAM(1000000000000,100000000000,900,(190,360),-0.1)

boundryConditions = [[1,1,0,0]]
beam.calculateKg(boundryConditions)
t = 0
while running:
    dt = clock.tick(FPS)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    beam.draw()
    beam.solve(t)
    pygame.display.flip()
    t+=dt
    
pygame.quit()
