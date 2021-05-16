import Rhino.Geometry as rg

#1.
#compute face normals using rg.Mesh.FaceNormals.ComputeFaceNormals()
#output the vectors to a

m.FaceNormals.ComputeFaceNormals()
a = m.FaceNormals
m.Flip(m, True, True, True)

# a = rg.Mesh.FaceNormals.GetValue()

#a = faceNormals

#2.
#get the centers of each faces using rg.Mesh.Faces.GetFaceCenter()
#store the centers into a list called centers 
#output that list to b

centers = []

for i in range(len(a)):
    center = m.Faces.GetFaceCenter(i)
    centers.append(center)
    
b = centers

#3.
#calculate the angle between the sun and each FaceNormal using rg.Vector3d.VectorAngle()
#store the angles in a list called angleList and output it to c

angle_list=[]

for i in a:
    angle = rg.Vector3d.VectorAngle(s,i)
    angle_list.append(angle)
c = angle_list

#4. explode the mesh - convert each face of the mesh into a mesh
#for this, you have to first copy the mesh using rg.Mesh.Duplicate()
#then iterate through each face of the copy, extract it using rg.Mesh.ExtractFaces
#and store the result into a list called exploded in output d

m_copy = rg.Mesh.Duplicate(m)
faces_number = m_copy.Faces.Count

exploded = []

for i in range(faces_number):
    mesh1 = m_copy.Faces.ExtractFaces([0])
    exploded.append(mesh1)

d = exploded

#after here, your task is to apply a transformation to each face of the mesh
#the transformation should correspond to the angle value that corresponds that face to it... 
#the result should be a mesh that responds to the sun position... its up to you!

## --- I want to create different size circular perforations depending on the sun angle interaction

## 1.REMAP ANGLES 

remaped_angles=[]
min_value=min_r
max_value=max_r
old_minimum = min(angle_list)
old_max=max(angle_list)

for i in angle_list:
    remaped_value=(((i - old_minimum) * (max_value - min_value)) / (old_max - old_minimum)) + max_value
    remaped_angles.append(remaped_value)

## 2. CREATE CIRCLES

circles= []

for i in range(len(centers)):
    circle = rg.Circle(centers[i], remaped_angles[i])
    circles.append(circle)

## 3. PROJECT CIRCLLES TO MESH

# 1. convert mesh to brep

brep_list = []
for i in exploded:
    brep= rg.Brep.CreateFromMesh(i, True)
    brep_list.append(brep)


# 2. Project circles to Brep (No need since we can trim with extruded planar circles)
"""
projected_circles = []

for i in range(len(circles)):
    curve = rg.Circle.ToNurbsCurve(circles[i])
    projected = rg.Curve.ProjectToMesh(curve, exploded[i], rg.Vector3d.ZAxis, 0.001)[0]
    projected_circles.append(projected)
"""

# 2. Extrude Circles
extruded=[]
for i in circles:
    curve = rg.Circle.ToNurbsCurve(i)
    extruded_geo=rg.Extrusion.Create(curve,1,True)
    brep_s=rg.Surface.ToBrep(extruded_geo)
    rg.Brep.Flip(brep_s) # Here we flip the extrusion so the trim works outwards
    extruded.append(brep_s)

# 3. Move extrusions down

for i in extruded:
    rg.Surface.Transform(i, rg.Transform.Translation(rg.Vector3d.ZAxis*-.5))

## 3. Trim

trimed_surfaces = []
for i in range(len(brep_list)):
    #cutter = rg.Surface.ToBrep(extruded[i])
    trimed = brep_list[i].Trim(extruded[i], 0.001)[0]
    trimed_surfaces.append(trimed)0