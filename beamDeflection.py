import pygame
import math

class SimplySupportedBeam:
    def __init__(self,position,length,E,A,I):
        self.position = position
        self.length = length
        self.E = E
        self.A = A
        self.I = I
        self.xcoordinates = [i for i in range(length)]
        self.ycoordinates = [0 for i in range(length)]
        self.pinSupport = [position,[position[0]+20,position[1]+20],[position[0]-20,position[1]+20]]
        self.floorpin = [[position[0]+60,position[1]+20],[position[0]-60,position[1]+20]]
        self.rollerSupport = [[position[0]+length,position[1]],[position[0]+length+20,position[1]+20],[position[0]+length-20,position[1]+20]]
        self.rollers = [[position[0]+length-10,position[1]+20+10],[position[0]+length+10,position[1]+20+10]]
        self.floorroller = [[position[0]+length-60,position[1]+40],[position[0]+length+60,position[1]+40]]
        self.defAtP = 0

    def Location(self):
        return self.position
    
    def L(self):
        return self.length
    
    def create_points(self):
        points = []
        for i in range(self.length):
            points.append([self.position[0]+self.xcoordinates[i],self.position[1]-self.ycoordinates[i]])
        return points

    def draw_beam(self,screen,beamcolor,width,supportcolor,rollercolor,floorcolor):
        pygame.draw.polygon(screen,supportcolor,self.pinSupport)

        pygame.draw.polygon(screen,supportcolor,self.rollerSupport)
        pygame.draw.circle(screen,rollercolor,self.rollers[0],10)
        pygame.draw.circle(screen,rollercolor,self.rollers[1],10)
        pygame.draw.line(screen,floorcolor,self.floorpin[0],self.floorpin[1],5)
        pygame.draw.line(screen,floorcolor,self.floorroller[0],self.floorroller[1],5)
        pygame.draw.lines(screen,beamcolor,False,self.create_points(),width)
        
    def deflect(self,force,location):
        for x in self.xcoordinates:
            if x < location[0]:
            
                self.ycoordinates[x] = (force*(self.length-location[0])*x/(6*self.length*self.E*self.I))*(2*self.length*location[0] - location[0]**2 - x**2)
            else:
                self.ycoordinates[x] = (force*location[0]*(self.length-x)/(6*self.length*self.E*self.I))*(2*self.length*x - location[0]**2 - x**2)
                if x == location[0]:
                    self.defAtP = self.ycoordinates[x]
            

    def deflectAtP(self,force,location):
        return force*(self.length- location)*location*(2*self.length*location - 2*location**2 )/(6*self.length*self.E*self.I)
    
pygame.init()
pygame.display.set_caption("RAYLEIGH-RITZ METHOD")
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
running = True
t=0
FPS = 60
g = 10
w = 0.001
beamColor  = (82, 64, 21)
supporColor = (153, 43, 91)
screenColor = (224, 175, 58)
rollercolor = (33, 17, 24)
floorcolor = (0,0,0)
ballColor = (62, 85, 87)
beam = SimplySupportedBeam((300,360),600,10000000,50,0.01)
P=-2
ballRadius = 20
while running:
    dt = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False

    screen.fill(screenColor)
    beam.deflect(P,[(beam.L()/2)*math.cos(w*t)+beam.L()/2,0])
    beam.draw_beam(screen,beamColor,9,supporColor,rollercolor,floorcolor)
    pygame.draw.circle(screen,ballColor,((beam.Location()[0]+(beam.L()/2)*math.cos(w*t)+beam.L()/2),beam.Location()[1]+-beam.deflectAtP(P,(beam.L()/2)*math.cos(w*t)+beam.L()/2)-ballRadius),ballRadius)
    pygame.display.flip()
    t+=dt
pygame.quit()