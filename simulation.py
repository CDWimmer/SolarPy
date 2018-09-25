import math
import time
from graphics import *
## requires graphics.py
## http://mcsp.wartburg.edu/zelle/python/graphics.py

class Body():
    def __init__(self, name:str, mass, radius, initvector, initcoord):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.vector = initvector
        self.coord = initcoord
    def get_velocity(self):
        a = self.vector[0]
        b = self.vector[1]
        c = a**2 + b**2
        d = math.sqrt(c)
        return d
    def show_details(self, print_this:bool=False): 
        upper_name = self.name.upper()
        out = upper_name + "\nmass of: " + str(self.mass) + "\nradius: " + str(self.radius) + "\ncoordinates: " + str(self.coord) + "\nvelocity: " + str(self.get_velocity())
        if(print_this):
            print(out)
        return out


class Universe(): # holds constants and sim objects
    def __init__(self, name:str="Universe", timestep=0.1, grav_const=5):
        
        ## initialise variables
        self.name = name
        self.bodies = []
        self.points = []
        self.body_count = 0
        self.timestep = timestep
        self.grav_const = grav_const
        self.win = GraphWin(self.name, 500, 500)
    

    def add_body(self, new_body):

        self.bodies.append(new_body)
        self.points.append(Point(new_body.coord[0], new_body.coord[1]))
        self.points[self.body_count].draw(self.win) ## draw the new object 
        self.body_count += 1 ## we'll have an equal count of bodies/points so can refer to both with the same id/number later
        
    def print_all(self):
        for body in self.bodies:
            body.show_details(True)

    def distance_x(self, body1, body2):
        distx = body1.coord[0] - body2.coord[0]
        return distx
    def distance_y(self, body1, body2):
        disty = body1.coord[1] - body2.coord[1]
        return disty
    def distance(self, body1, body2):
        '''
        get the absolute distance between two bodies
        '''
        dist = (math.sqrt((body2.coord[0] - body1.coord[0])**2 + (body2.coord[1] - body1.coord[1])**2))
        print(dist)
        return dist
    def refresh_points(self):
        '''
        undraws and redraws all graphic points
        '''
        for pt in self.points:
            pt.undraw()
            pt.draw()

    def refresh_point(self, point_id):
        self.points[point_id].undraw()
        self.points[point_id].draw()

    def move_point(self, point_id, distx, disty):
        self.points[point_id].move(distx, disty)

    def step(self):
        '''
        The big one.
        Take a simulation step.
        '''
        for i in range(0, self.body_count):
            for j in range(0, self.body_count):
                if(i == j): # body cannot effect itself!
                    pass
                else:
                    bod_i = self.bodies[i]
                    bod_j = self.bodies[j]
                    ## calculate the effect of j on i
                    adj = self.distance_x(bod_i, bod_j)
                    opp = self.distance_y(bod_i, bod_j)
                    theta = math.atan(opp/adj)
                    
                    force = (self.grav_const * bod_i.mass * bod_j.mass)/(self.distance(bod_i, bod_j)**2)
                    force_x = math.cos(theta) * force
                    force_y = math.sin(theta) * force
                    
                    accel_x = force_x / bod_i.mass
                    accel_y = force_y / bod_i.mass

                    ## update vectors
                    bod_i.vector[0] = bod_i.vector[0] + accel_x * self.timestep
                    bod_i.vector[1] = bod_i.vector[1] + accel_y * self.timestep
                    
                    ## move body and graphic point with new vectors
                    distx = (self.timestep * bod_i.vector[0])
                    disty = (self.timestep * bod_i.vector[1])
                    self.move_point(i, distx, disty)
                    bod_i.coord[0] += distx
                    bod_i.coord[1] += disty

        ## check for collision ##### This is shit and doesn't work pls make good I can't be bothered with how many comparisons it'll take, thank u #####
##            for i in self.bodies:
##                for j in self.bodies:
##                    if(i!=j):
##                        if((i.coord[0] + i.radius > j.coord[0] - j.radius) or i.coord[0] - i.radius < j.coord[0] + j.radius): ## horizontal overlap
##                            if((i.coord[1] + i.radius > j.coord[1] - j.radius) or i.coord[1] - i.radius < j.coord[1] + j.radius): ## vertical overlap
##                                print("collision!")

    def run(self, step_lim, interval):
        '''
        run step() step_lim times with a time interval in seconds
        '''
        cur_step = 1
        while(cur_step <= step_lim):
            cur_step += 1
            self.step()
            time.sleep(interval)
    



## Create the universe
world = Universe("universe", 0.05, 5.5)
## add bodies
world.add_body(Body("Titan", 1300, 3, [0,0], [80,30])) # world.bodies[0]
world.add_body(Body("Europa", 1000, 2, [0,0], [10,10]))   # world.bodies[1]
world.add_body(Body("Fraztater", 1600, 4, [0,-1], [140, 140]))
world.add_body(Body("Sun", 50000, 7, [0,0], [250,250]))

## 


## show details of all bodies

world.run(300, 0.05)
