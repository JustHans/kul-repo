print("CHECK")

import math as m
import pygame as pg
import random as rng

clock = pg.time.Clock()

global_size_mod = 4
wWidth = 100*global_size_mod
wHeight = 100*global_size_mod
window = pg.display.set_mode([wWidth, wHeight])

class Scene():
        current_scene = None
        def __init__(self):
            Scene.current_scene = self
        def check_empty(self, x, y):
            if (x,y) in self.coordinates:
                if self.coordinates[(x,y)] == 0:
                    return True
            return False
        def check_water(self,x,y):
            if (x,y) in self.coordinates:
                if self.coordinates[(x,y)] == 1:
                    return True
            return False
        def update(self):
            self.coordinates = {}
            x = 0
            y = 0
            while y < 100:
                while x < 99:
                    self.coordinates[(x,y)] = 0
                    x += 1
                self.coordinates[(x,y)] = 0
                y += 1
                x = 0
            for inst in WaterDrop.instances:
                self.coordinates[(inst.x,inst.y)] = 1

class Block():
    instances = []
    def __init__(self, size_mod, pos_x, pos_y, windowobject):
        Block.instances.append(self)
        self.size_mod = size_mod
        self.x = pos_x
        self.y = pos_y
        self.window_x = self.x*self.size_mod
        self.window_y = self.y*self.size_mod
        self.windowobject = windowobject
    def draw(self):
        surface = pg.Surface((1*self.size_mod,1*self.size_mod))
        surface.fill((255,255,255))
        rect = surface.get_rect()
        rect.center = self.window_x, self.window_y
        self.windowobject.blit(surface,rect)
    def load(self):
        Scene.current_scene.coordinates[(self.x,self.y)] = 1
    def unload(self):
        Scene.current_scene.coordinates[(self.x,self.y)] = 0

class BlockPyramid():
    def __init__(self, pos_x, pos_y, width, height):
        self.x = pos_x
        self.y = pos_y
        self.w = width
        self.h = height
        self.points = []
    
    def load(self):
        for i in range(self.h):
            if self.w-2*i > 0:
                for y in range(self.w-2*i):
                    self.points.append(((self.x+m.floor(self.w/2))-i-y,self.y-i))
            else:
                break
    
    def build(self):
        for i in self.points:
            x, y = i
            klass = Block
            instance = klass(global_size_mod,x,y,window)

class WaterDrop():
    instances = []
    def __init__(self, size_mod, start_pos_x, start_pos_y, windowobject):
        WaterDrop.instances.append(self)
        self.size_mod = size_mod
        self.x = start_pos_x
        self.y = start_pos_y
        self.window_x = self.x*self.size_mod
        self.window_y = self.y*self.size_mod
        self.windowobject = windowobject
        self.vel_x = 0
        self.vel_y = 0
        Scene.current_scene.coordinates[(self.x,self.y)] = 1
    
    def draw(self):
        surface = pg.Surface((1*self.size_mod,1*self.size_mod))
        surface.fill((0,0,255))
        rect = surface.get_rect()
        rect.center = self.window_x, self.window_y
        self.windowobject.blit(surface,rect)
    
    def check_move(self):
        scene = Scene.current_scene
        if scene.check_empty(self.x, self.y+1) == True:
            self.vel_y = 1
        elif scene.check_empty(self.x + 1, self.y + 1) == True:
            self.vel_x = 1
            self.vel_y = 1
        elif scene.check_empty(self.x - 1, self.y + 1) == True:
            self.vel_x = -1
            self.vel_y = 1
        else:
            rightDist = -3
            leftDist = -3
            if(scene.check_empty(self.x + 1, self.y) == True):
                rightDist = self.check_overflow(1)
            if(scene.check_empty(self.x - 1, self.y) == True):
                leftDist = self.check_overflow(-1)
            
            if(rightDist > 0 and leftDist > 0):
                if(rightDist < leftDist):
                    self.vel_x = 1
                elif(rightDist > leftDist):
                    self.vel_x = -1
                else:
                    self.vel_x = rng.choice([-1,1])
            else:
                if(rightDist > 0):
                    self.vel_x = 1
                elif(leftDist > 0):
                    self.vel_x = -1
    
    def check_overflow(self, xDir):
        scene = Scene.current_scene
        xCur = xDir
        
        while len(scene.coordinates) - 1 > self.x + xCur > 1:
            if scene.check_empty(self.x + xCur, self.y + 1):
                return abs(xCur)
            elif scene.check_empty(self.x + xCur + xDir, self.y) != True and scene.check_water(self.x + xCur + xDir, self.y) != True:
                return -1
            else:
                xCur = xCur + xDir
        return -2



    def move(self):
        previous_pos = (self.x, self.y)
        self.y += self.vel_y
        self.x += self.vel_x
        self.window_x = self.x*self.size_mod
        self.window_y = self.y*self.size_mod
        self.vel_x = 0
        self.vel_y = 0
        if (self.x, self.y) != previous_pos:
            Scene.current_scene.coordinates[previous_pos] = 0
            Scene.current_scene.coordinates[(self.x,self.y)] = 1
    
scene = Scene()
scene.update()
#drop1 = WaterDrop(global_size_mod,20,20,window)
pyramid1 = BlockPyramid(50,99,40,60)
pyramid1.load()
print(scene.check_empty(50,70))
pyramid1.build()

[inst.load() for inst in Block.instances]

contgame = True
while contgame == True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            contgame = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mx, my = pg.mouse.get_pos()
            mx = m.floor(mx/global_size_mod)
            my = m.floor(my/global_size_mod)
            for i in range(10):
                for y in range(10):
                    klass = WaterDrop
                    instance = klass(global_size_mod,mx-1+y,my-1+i,window)
    window.fill((0,0,0))

    for inst in WaterDrop.instances:
        inst.check_move()
        inst.move()
        inst.draw()
   
    [inst.draw() for inst in Block.instances]
   
    pg.display.flip()
    clock.tick(60)

pg.quit()