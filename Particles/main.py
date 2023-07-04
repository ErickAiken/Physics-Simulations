
import pygame
import OpenGL
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def main(pxWidth, pxHeight):

    dimx = 100
    dimy = 100

    pygame.init()
    display = (pxWidth,pxHeight)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    # 2D camera and size
    gluOrtho2D(-1.05*dimx, 
                1.05*dimx,
               -1.05*dimy,
                1.05*dimy)

    # 3D camera and translation
    #gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    #glTranslatef(0.0,0.0,-5)

    simTime = 0
    simStep = 0.01

    nParticles = 100
    
    damping = 0.50
    friction = 0.05
    vmax_initial = 50
    
    particles = []
    for n in range(nParticles):
        x = -dimx + np.random.random()*2*dimx
        y = -dimy + np.random.random()*2*dimy
        z = 0
        vx = -vmax_initial + 2*vmax_initial*np.random.random()
        vy = -vmax_initial + 2*vmax_initial*np.random.random()
        vz = 0
        p = Particle(x,y,z,vx,vy,vz)
        particles.append(p)

    isRunning = True
    while isRunning:

        # Check for close window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                isRunning = False
                return

        # Main simulation
        for p in particles:
            p.vel.y += -9.8*simStep
            p.pos.y += p.vel.y*simStep
            p.pos.x += p.vel.x*simStep

            # Check boundary
            if(p.pos.x <= -dimx):
                p.vel.x *= -1*(1-damping)
                p.pos.x = -dimx
            if(p.pos.x >= dimx):
                p.vel.x *= -1*(1-damping)
                p.pos.x = dimx
            if(p.pos.y <= -dimy):
                p.vel.y *= -1*(1-damping)
                p.vel.x *= (1-friction)
                p.pos.y = -dimy
            if(p.pos.y >= dimy):
                p.vel.y *= -1*(1-damping)
                p.pos.y = dimy

        # Update screen
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        drawBoundary(dimx, dimy)
        for p in particles:
            drawParticle(p.pos, 1,1,1)
        pygame.display.flip()

        # Update time
        simTime += simStep
        print("Simulation Time: ", simTime)
        pygame.time.wait(int(simStep * 1000))

def drawBoundary(dimx, dimy):
    glColor3d(1,1,1)
    glBegin(GL_LINE_LOOP)
    glVertex2d(dimx, dimy)
    glVertex2d(dimx, -dimy)
    glVertex2d(-dimx, -dimy)
    glVertex2d(-dimx, dimy)
    glEnd()


def drawParticle(pos, r, b, g):
    glEnable(GL_POINT_SMOOTH)
    glPointSize(0.1)
    glBegin(GL_POINTS)
    glColor3d(r,b,g)
    glVertex3d(pos.x,pos.y,pos.z)
    glEnd()
   
class Particle:
    def __init__(self,x,y,z,vx,vy,vz):
        self.pos = Position()
        self.vel = Velocity()
        self.pos.x = x
        self.pos.y = y
        self.pos.z = z
        self.vel.x = vx
        self.vel.y = vy
        self.vel.z = vz

class Position:
    def __init__(self):
        self.x = 0
        self.y = 0 
        self.z = 0

class Velocity:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

def simulate():
    print("simulating")

def update():
    print("updating")


if __name__ == "__main__":
    print("Starting...")
    main(1200, 800)
    print("Finished...")