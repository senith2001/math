import pygame
import math
import decimal
import numpy as np

decimal.getcontext().prec = 100

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("orbital motion(remastered)")
screen = pygame.display.set_mode((1280,720))
running = True

G =1
#parameters of large mass
direction = [1,0] #-----> starting direction of large mass


Llocation = [640,360]
Lcolor = (207, 99, 23)
Lradius = 300

DensityL = 1
ML = (4/3)*math.pi*(Lradius**3)*DensityL
#parameters of small mass
Slocation = [940,360]


Sradius = 50
DensityS = 10
MS = (4/3)*math.pi*(Sradius**3)*DensityS
Scolor = (89, 142, 150)

#SURFACE VELOCITIES OF TWO MASSES
# VS = ML * ((2*G/(ML+MS))*((1/Lradius)-(1/((Llocation[0] - Slocation[0])**2 + (Llocation[1] - Slocation[1])**2)**(1/2))))**(1/2)
# VL = -MS * ((2*G/(ML+MS))*((1/Lradius)-(1/((Llocation[0] - Slocation[0])**2 + (Llocation[1] - Slocation[1])**2)**(1/2))))**(1/2)

#parameter of time when two masses reach each other
# T = None
# B = (G*MS*((1/Sradius**3)-(1/Lradius**3)))**(1/2)
# print(B)

#gloabal variables

FPS = 60

K = -G*(ML+MS)
Rt = (((Llocation[0] - Slocation[0])**2 + (Llocation[1] - Slocation[1])**2)**(1/2))
R = ((Llocation[0] - Slocation[0])**2 + (Llocation[1] - Slocation[1])**2)**(1/2)
# dRtdt = 0
# Pt = 0
# dPtdt = decimal.Decimal(K)/(Rt**2)
t = 0
#centroid of two masses
C = [Llocation[0] + R*MS/(MS+ML),Llocation[1]]

XL = R*MS/(ML+MS)
dXL2dt = None
XS = R*ML/(ML+MS)
dXSdt = 0
dXLdt = dXSdt*MS/ML
dXS2dt = None
graph = []
scale = 5
#K VALUES FOR INSIDE MOTION
# kS = (MS/Lradius**3)*G*MS*((1/Sradius**3)-(1/Lradius**3))
# kL = (MS/Sradius**3)*G*MS*((1/Sradius**3)-(1/Lradius**3))
# b1 = None
# b2 = None

#time step
# h = decimal.Decimal(0.01)
#matrix algebra 

#oppsite motion
# dydt = decimal.Decimal(G*(ML+MS)/(R**2))
# y = dRtdt

# a = np.array([[(G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*math.cos(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t)),-(G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*math.sin(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t))],
#                             [math.sin(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t)),math.cos(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t))]])
# b = np.array([float(dRtdt),R])
# x = np.linalg.solve(a,b)
# i = []
# j = []
# u = 0
while running:
    dt = (clock.tick(FPS) / 1000)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((235, 157, 226))

    #large mass
    earth = pygame.draw.circle(screen,(69, 5, 11),Llocation,Lradius)
    pygame.draw.circle(screen,Lcolor,Llocation,Lradius-4)
    
    #hole inside large mass
    pygame.draw.rect(screen,"black",pygame.Rect(Llocation[0]-Lradius,Llocation[1]-Sradius,2*Lradius,2*Sradius))

    #small mass
    ball = pygame.draw.circle(screen,(44, 49, 138),Slocation,Sradius)
    pygame.draw.circle(screen,Scolor,Slocation,Sradius-4)
    
    pygame.draw.line(screen,(61, 128, 73),(C[0],0),(C[0],720),5)
    pygame.draw.line(screen,(61, 128, 73),(0,360),(1280,360),5)
    pygame.draw.circle(screen,"white",C,5)
    if (Rt>0) and (Rt <= Lradius) and (XS > 0):
        
        dXS2dt = -4*G*DensityL*math.pi*Rt/3
        dXSdt = dXSdt + dXS2dt*dt
        XS = XS + dXSdt*dt
        print("inside the right half ",dXS2dt)
    elif Rt == 0:
        
        dXS2dt = 0
        dXSdt = dXSdt + dXS2dt*dt
        XS = XS + dXSdt*dt
        print("at the center",dXS2dt)
    elif (XS < 0 )and ((Rt<0) and (Rt>-Lradius)):
        
        dXS2dt = -4*G*DensityL*math.pi*Rt/3
        dXSdt = dXSdt + dXS2dt*dt
        XS = XS + dXSdt*dt
        print("inside the left half",dXS2dt)
    
    elif dXSdt <= 0 and XS > 0:
        XS = (ML/(ML+MS))*(R**(3/2) - (3/2)* (2*G*(ML+MS))**(1/2)*t )**(2/3)
        dXSdt = -(ML/(ML+MS))*((2*G*(ML+MS))**(1/2))/(R**(3/2) - (3/2)* (2*G*(ML+MS))**(1/2)*t )**(1/3)
    elif dXSdt >0 and XS < 0:
        dXS2dt = -G*ML/(Rt**2)
        dXSdt = dXSdt + dXS2dt*dt
        XS = XS + dXSdt*dt
    elif dXSdt < 0 and XS < 0:
        dXS2dt = -G*ML/(Rt**2)
        dXSdt = dXSdt + dXS2dt*dt
        XS = XS + dXSdt*dt
    elif dXSdt >=0 and XS <0:
        XS = (ML/(ML+MS))*(R**(3/2) - (3/2)* (2*G*(ML+MS))**(1/2)*t )**(2/3)
        dXSdt = -(ML/(ML+MS))*((2*G*(ML+MS))**(1/2))/(R**(3/2) - (3/2)* (2*G*(ML+MS))**(1/2)*t )**(1/3)
             

    print("velocity of small mass: ",dXSdt)
    XL = XS * (MS/ML) 

    Rt = XS+XL
    
    # print("radius ",Rt)
    # if not earth.collidepoint(Slocation[0],Slocation[1]):
        # Rt =(decimal.Decimal(Rt) + decimal.Decimal(Pt*h))
        # print("distance between masses",Rt)
        # dRtdt = Pt
        # print("rate of change of distance : ",dRtdt)
        # print("relative velocity between masses",Pt)
        # Pt =Pt + dPtdt*h
        # dPtdt = decimal.Decimal(K)/(Rt**2)
        # print("time is ",t)
        # print((R**(3/2) - ((3/2)*(2*G*(ML+MS))**(1/2))*t))
        #Rt = decimal.Decimal((R**(3/2) - ((3/2)*(2*G*(ML+MS))**(1/2))*t)**(2/3))
       
        
        
        #print(-(((2*G*(ML+MS))**(1/2))/((R**(3/2) - (3/2)*((2*G*(ML+MS))**(1/2))*t)**(1/3))))
        # if ( (dRtdt<=0) and Rt > Lradius):
        #     Rt = Rt + dRtdt*h
        #     i.append(u)
        #     if len(i) >=2:
        #         if (i[-1]-1) != i[-2]:
        #             t = 0
        #     dRtdt = decimal.Decimal(-((2*G*(ML+MS))**(1/2))/((R**(3/2) - (3/2)*((2*G*(ML+MS))**(1/2))*t)**(1/3)))
            
        # elif ((dRtdt<=0) and Rt < -Lradius):
        #     y = dRtdt
        #     y = y + decimal.Decimal(dydt*h)
        
                
        #     Rt = Rt - y*h

            # if Rt > Lradius:

            #     dRtdt = -y
            # elif Rt < -Lradius:
            #     dRtdt = y
            # Rt = Rt + dRtdt*h
        #     print("opposite velocity :",dRtdt)
        #     dydt = decimal.Decimal(G*(ML+MS))/(Rt**2)
        # print("distance at time t", Rt)
        # XL = decimal.Decimal(C[0])-(Rt*decimal.Decimal(MS/(MS+ML)))
        # XS = decimal.Decimal(C[0]) +(Rt*decimal.Decimal(ML/(MS+ML)))
        

        # XS = XS + dRtdt*(ML/(-MS+ML))*h
        # XL = XL + dRtdt*(-MS/(-MS+ML))*h
        # Llocation[0]= float(XL)
        # Slocation[0]= float(XS)

        # if abs(Rt) <= Lradius:
        #     T = 0
        #     t = 0
        #     a = np.array([[float(decimal.Decimal(T*B).exp()),float(decimal.Decimal(-T*B).exp())],
        #                     [float(decimal.Decimal(B)*(decimal.Decimal(T*B).exp())),float(-decimal.Decimal(B)*(decimal.Decimal(-T*B).exp()))]])
        #     b = np.array([float(decimal.Decimal(R)),float(decimal.Decimal(dRtdt))])
        #     x = np.linalg.solve(a,b)
            # a = np.array([[(G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*math.cos(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t)),-(G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*math.sin(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t))],
            #                 [math.sin(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t)),math.cos(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t))]])
            # b = np.array([float(dRtdt),R])
            # x = np.linalg.solve(a,b)
    #effective masss changing when small object go through large object
    # else :
        # Rt = G*MS*((1/Sradius**3)-(1/Lradius**3))*(math.e)**t
        
        # print(B)
        #Rt = (decimal.Decimal(x[0])*decimal.Decimal(t*B).exp() + decimal.Decimal(x[1])*decimal.Decimal(-t*B).exp())
        #dRtdt = decimal.Decimal(B)*(decimal.Decimal(x[0])*decimal.Decimal(t*B).exp() -decimal.Decimal(B)*decimal.Decimal(x[1])*decimal.Decimal(-t*B).exp())
        # print("radius after entering : ",Rt)
        # XL = decimal.Decimal(C[0])-np.sign(dRtdt)*(Rt*decimal.Decimal(MS/(MS+ML)))
        # XS = decimal.Decimal(C[0]) +np.sign(dRtdt)*(Rt*decimal.Decimal(ML/(MS+ML)))

        #Rt = decimal.Decimal(x[0]*math.sin(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t))) + decimal.Decimal(x[1]*math.cos(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t)))
        # dRtdt = decimal.Decimal(x[0]*(G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))* math.cos(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t))) - decimal.Decimal(x[1]*(G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*math.sin(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t)))
        # Rt = Rt + dRtdt * h
        # XL = decimal.Decimal(C[0])-(decimal.Decimal(Rt)*decimal.Decimal(MS/(MS+ML)))
        # XS = decimal.Decimal(C[0]) +(decimal.Decimal(Rt)*decimal.Decimal(ML/(MS+ML)))

        # ML = (4/3)*math.pi*(Rt**3)*Density
        # xl = kL*math.e**t + (VL-kL*T)*t +XL - kL*math.e**T -(VL-kL*math.e**T)*T 
        # xs = kS*math.e**t + (VS-kS*T)*t +XS  - kS*math.e**T - (VS-kS*math.e**T)*T

        #y = dRtdt
        # Llocation[0]= float(XL)
        # Slocation[0]= float(XS)
        # if Rt > Lradius:
        #     y = dRtdt
            
        # elif Rt < -Lradius:
        #     y = -dRtdt
            
        # elif Rt == -Lradius:
        #     y = dRtdt
        # elif Rt == Lradius:
        #     y = -dRtdt
        #dydt = decimal.Decimal(G*(ML+MS))/(Rt**2)

    # else:
    #     if Rt == -Lradius:
    #         if dRtdt > 0:
    #             dRtdt = decimal.Decimal(x[0]*(G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))* math.cos(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t))) - decimal.Decimal(x[1]*(G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*math.sin(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t)))
    #             Rt = Rt + dRtdt * h
                
    #         else:
    #             dydt = decimal.Decimal(G*(ML+MS))/(Rt**2)
    #             y = y + decimal.Decimal(dydt*h)
    #             dRtdt = -y

    #     if Rt == Lradius:
    #         if dRtdt < 0:
    #             dRtdt = decimal.Decimal(x[0]*(G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))* math.cos(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t))) - decimal.Decimal(x[1]*(G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*math.sin(((G*MS/((1/Sradius**3)-(1/Lradius**3))**(1/2))*t)))
    #             Rt = Rt + dRtdt * h
    #         else :
    #             dydt = decimal.Decimal(G*(ML+MS))/(Rt**2)
    #             y = y + decimal.Decimal(dydt*h)
    #             dRtdt = y


    # print("calculated distance between masses",abs(XS-XL))
    # XL = decimal.Decimal(C[0])-(decimal.Decimal(Rt)*decimal.Decimal(MS/(MS+ML)))
    # XS = decimal.Decimal(C[0]) +(decimal.Decimal(Rt)*decimal.Decimal(ML/(MS+ML)))
    Llocation[0]= C[0] - XL
    Slocation[0]=  C[0] + XS
    graph.append((Slocation[0],360+dXSdt/scale))
    if len(graph) >=2 :
        pygame.draw.lines(screen,(110, 73, 166),False,graph,5)
    pygame.display.flip()
    if len(graph) >= 100:
        #for i in range(50):
        graph.pop(0)
    t += dt    #calculating the time
    
pygame.quit()