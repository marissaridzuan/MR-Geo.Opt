import Rhino.Geometry as rg
import math

#create a sun vector

#1. create a Sphere at point (0,0,0) with radius 1 and output it to a
#output the sphere to a

a = rg.Sphere(rg.Point3d(0,0,0),1.0)

#2. evaluate a point in the sphere using rg.Sphere.PointAt() at coordintes x and y
#the point should only be on the upper half of the sphere (upper hemisphere)
#the angles are in radians, so you might want to use math.pi for this
#output the point to b

b = a.PointAt(x*2*math.pi, y*math.pi)

#create a vector from the origin  and reverse the vector
#keep in mind that Reverse affects the original vector
#output the vector to c

vector = rg.Vector3d(b)

vector.Reverse()

print(vector)

c = vector