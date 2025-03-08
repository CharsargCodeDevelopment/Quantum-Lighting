import SDF
import math
import turtle

class HitData:
    def __init__(self,distance = None,normal = None,collision = None):
        self.distance = distance
        self.normal = normal
        self.collision = collision
        self.pos = (0,0)
        self.collision_index = None
class BaseRay:
    def __init__(self,max_distance=512,angle=0,step_size = 0.1,position = (0,0)):
        self.max_distance = 128
        self.angle = 0
        self.step_size = 0.1
        self.pos = position
        self.cast_ray = self.__castRay__
        self.collision_sdf = []
        self.hit_data = HitData()
    def __castRay__(self):
        x,y = self.pos
        rayAngle = self.angle
        dx,dy = math.sin(math.radians(self.angle)),math.cos(math.radians(self.angle))
        d=0
        self.hit_data = HitData(distance=d,collision = False)
        #turtle.penup()
        #turtle.goto(x,y)
        #turtle.pendown()
        
        while d < self.max_distance:
            d+= self.step_size
            x = x+dx*self.step_size
            y +=dy*self.step_size
            values = [0 for _ in self.collision_sdf]
            i = 0
            collision = False
            for sdf in self.collision_sdf:
                sdf_out = sdf._computeFunction(x,y)
                #df_out = 0
                if sdf_out < 1:
                    collision = True
                    collisionIndex = i
                    break
                values[i] = sdf_out
                i+=1
                #values.append(sdf_out)
            #print(values)
            #turtle.goto(x,y)
            
                
            if min(values) < 1 and not collision:
                collision = True
                collisionIndex = values.index(min(values))
            if collision:
                self.hit_data.collision = True
                self.hit_data.pos = (x,y)
                self.hit_data.collision_index = collisionIndex
                self.hit_data.distance = d
                break
        self.hit_data.pos = (x,y)



        
        
            
        


__ShapeSize__ = 20
__PixelSize__ = 10

turtle.shape("square")
turtle.shapesize(__PixelSize__/__ShapeSize__)

ray = BaseRay()


SDFs = []
#SDFs.append(SDF.BaseSDF(center = (20,0),r = 10))

ray.collision_sdf = SDFs

target_point = SDF.BaseSDF(center = (-20,0),r = 10)
ray.collision_sdf.append(target_point)
#turtle.tracer(False)
turtle.penup()



pixels = [[0 for _ in range(100)] for _ in range(100)]



import tqdm

for x in tqdm.tqdm(range(-50,50,5)):
    for y in (range(-50,50,5)):
        target_point.center = (x,y)
        prob_dirX = 0
        prob_dirY = 0

        
        #turtle.goto(x*__PixelSize__,y*__PixelSize__)
        #turtle.tracer(False)
        for i in range(0,360,45):
            ray.angle = i
            ray.__castRay__()
            if ray.hit_data.collision:
                #print(ray.hit_data.distance)
                if ray.hit_data.collision_index == 0:
                    prob_dirX+=math.sin(math.radians(ray.hit_data.distance))
                    prob_dirY+=math.cos(math.radians(ray.hit_data.distance))
        
        probability = prob_dirX**2 + prob_dirY **2
        b = (probability/10)
        b = min(1,b)
        #print(prob_dirX,prob_dirY,b)
        #turtle.color(b,b,b)
        #turtle.stamp()
        pixels[x+50][y+50] = b
        #turtle.dot()
    #turtle.update()
pixels = blur_nested_list(pixels)
turtle.tracer(False)
for i in range(len(pixels)):
    for j in range(len(pixels[i])):
        x,y = i,j
        b = pixels[i][j]
        turtle.color(b,0,0)
        turtle.goto(x*__PixelSize__,y*__PixelSize__)
        turtle.stamp()
    turtle.update()
turtle.mainloop()
        

