"""Provides a scripting component.
    Inputs:
        mesh: a mesh
        sph_vec: sun vector
    Output:
        a: List of Vectors
        b: List of Points
        c: list of angles
        d: exploded mesh
        ----------------
        e: circles
        f: remap circles
        g: projected
        """
        
import Rhino.Geometry as rg
import math
import ghpythonlib as ghc
import rhinoscriptsyntax as rs

#1.
#compute face normals using rg.Mesh.FaceNormals.ComputeFaceNormals()
#output the vectors to a
m = mesh
m.FaceNormals.ComputeFaceNormals()

a = m.FaceNormals
m.Flip(m, True, True, True)

#2.
#get the centers of each faces using rg.Mesh.Faces.GetFaceCenter()
#store the centers into a list called centers 
#output that list to b

centers = []

for i in range(len(a)):
    center = m.Faces.GetFaceCenter(i)
    centers.append(center)
    
b = centers
print type(len(centers))

#3.
#calculate the angle between the sun and each FaceNormal using rg.Vector3d.VectorAngle()
#store the angles in a list called angleList and output it to c

angle_list=[]

for i in a:
    angle = rg.Vector3d.VectorAngle(sph_vec,i)
    angle_list.append(angle)

c = angle_list

#4. explode the mesh - convert each face of the mesh into a mesh
#for this, you have to first copy the mesh using rg.Mesh.Duplicate()
#then iterate through each face of the copy, extract it using rg.Mesh.ExtractFaces
#and store the result into a list called exploded in output d

mesh_copy = rg.Mesh.Duplicate(m)
face_count = mesh_copy.Faces.Count

exploded = []
for i in range(face_count):
    face = mesh_copy.Faces.ExtractFaces([0])
    exploded.append(face)

d = exploded

#after here, your task is to apply a transformation to each face of the mesh
#the transformation should correspond to the angle value that corresponds that face to it... 
#the result should be a mesh that responds to the sun position... its up to you!


circles = []
for i in range(len(b)):
    circle = rg.Circle(b[i],0.5)
    circles.append(circle)
e = circles

#im still working on this!! it takes quite some time to go through the library and understand things
#trying to create circles with radius that respond to angle 
#need to remap c = angle list
#mesh to surface
#project circles to surface