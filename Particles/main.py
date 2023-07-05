
import pygame
import OpenGL
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def main(pxLength):

    dim = 10

    pygame.init()
    display = (pxLength,pxLength)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    # 2D camera and size
    gluOrtho2D(-1.05*dim, 
                1.05*dim,
               -1.05*dim,
                1.05*dim)

    # 3D camera and translation
    #gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    #glTranslatef(0.0,0.0,-5)

    simTime = 0
    simStep = 0.01
    scale = dim/pxLength

    nParticles = 5
    pxSize = 25
    
    damping = 0.25
    friction = 0.05
    vmax_initial = 100
    
    particles = []
    for n in range(nParticles):
        x = -dim + np.random.random()*2*dim
        y = -dim + np.random.random()*2*dim
        z = 0
        vx = -vmax_initial + 2*vmax_initial*np.random.random()
        vy = -vmax_initial + 2*vmax_initial*np.random.random()
        vz = 0
        p = Particle(x,y,z,vx,vy,vz,n,pxSize)
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

        # Clear the interacted particles list
        for p in particles:
            p.interacted = []

        # Search for boundary conditions and collisions
        for p in particles:

            # Apply gravity
            p.vel.y += -9.8*simStep
            p.pos.y += p.vel.y*simStep
            p.pos.x += p.vel.x*simStep

            # Check boundary
            if(p.pos.x <= -dim + p.size*scale):
                p.vel.x *= -1*(1-damping)
                p.pos.x = -dim + p.size*scale
            if(p.pos.x >= dim - p.size*scale):
                p.vel.x *= -1*(1-damping)
                p.pos.x = dim - p.size*scale
            if(p.pos.y <= -dim + p.size*scale):
                p.vel.y *= -1*(1-damping)
                p.vel.x *= (1-friction)
                p.pos.y = -dim + p.size*scale
            if(p.pos.y >= dim - p.size*scale):
                p.vel.y *= -1*(1-damping)
                p.pos.y = dim - p.size*scale

            # Check for collisions
            for p_ in particles:
                
                # No self interactions
                if (p.id == p_.id):
                    continue

                # Prevent duplicate interactions
                if(p.id in p_.interactions and p_.id in p_interactions):
                    continue
                
                # handle collisions
                d = np.sqrt((p.pos.x/scale - p_.pos.x/scale)**2 + (p.pos.y/scale - p_.pos.y/scale)**2)
                
                if(d <= p.size*2):
                    p.vel.x *= -1
                    p.vel.y *= -1
                    p_.vel.x *= -1
                    p_.vel.y *= -1

                    # Store that these particles have interacted already
                    p.interacted.append(p_.id)
                    p_.interacted.append(p.id)


        # Update screen
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        drawBoundary(dim, dim)
        for p in particles:
            drawParticle(p, 1,1,1)
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


def drawParticle(p, r, b, g):
    glEnable(GL_POINT_SMOOTH)
    glPointSize(p.size)
    glBegin(GL_POINTS)
    glColor3d(r,b,g)
    glVertex3d(p.pos.x,p.pos.y,p.pos.z)
    glEnd()
   
class Particle:
    def __init__(self,x,y,z,vx,vy,vz,id,size):
        self.id = id
        self.size = size
        self.pos = Position()
        self.vel = Velocity()
        self.pos.x = x
        self.pos.y = y
        self.pos.z = z
        self.vel.x = vx
        self.vel.y = vy
        self.vel.z = vz
        self.interactions = []

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
    main(800)
    print("Finished...")