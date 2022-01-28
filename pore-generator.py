
import bpy
import bmesh
import random

RATIO = 0.0005
DEPTH = 0.0001
SIZE = 0.02

bpy.ops.object.mode_set(mode = 'EDIT') 

context = bpy.context
selected_verts = context.active_object.vertex_groups.new(name='pores')
vertex_group_data = []

#select random vertices....
bpy.ops.mesh.select_mode(type="VERT")
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.mesh.select_random(ratio=RATIO)

#...and store them into our pores vertex group
vertex_group_data = [i.index for i in context.active_object.data.vertices if i.select]
bpy.ops.object.mode_set(mode = 'OBJECT') 
selected_verts.add(vertex_group_data , 1.0, 'ADD')
bpy.ops.object.mode_set(mode = 'EDIT') 

bm = bmesh.from_edit_mesh(context.edit_object.data)
bm.verts.ensure_lookup_table()

#move each selected vertex and its neighbours proportionally
for idx in vertex_group_data:
    v = bm.verts[idx]
    v.select = True
    transform = -v.normal * DEPTH
    bpy.ops.transform.translate(value=transform, 
                        constraint_axis=(False, False, False),
                        orient_type='GLOBAL',
                        use_proportional_edit=True,
                        mirror=False, 
                        proportional_edit_falloff='SMOOTH',
                        proportional_size=SIZE)
    v.select = False