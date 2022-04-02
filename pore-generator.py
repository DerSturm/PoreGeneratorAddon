bl_info = {
    "name": "Pore Generator",
    "author": "Hannes Sturm",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Toolshelf",
    "description": "Adds pores to your high-res mesh",
    "warning": "",
    "doc_url": "",
    "category": "Add Pores",
}


from email.policy import default
import bpy
import bmesh
import random

class PoreGeneratorMainPanel(bpy.types.Panel):
    bl_label = "Pore Generator"
    bl_idname = "SHADER_PT_MAINPANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Pore Generator"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(context.scene, "pore_ratio_prop")
        row = layout.row()
        row.prop(context.scene, "pore_depth_prop")
        row = layout.row()
        row.prop(context.scene, "pore_size_prop")
        row = layout.row()
        row = layout.row()
        row.operator('object.pore_generator')
        
        
#Generate pores on a high-poly mesh
class GENERATOR_OT_PORES(bpy.types.Operator):
    bl_label = "Generate"
    bl_idname = 'object.pore_generator'
    
    def execute(self, context):

        scene = context.scene

        ratio = scene.pore_ratio_prop
        depth = scene.pore_depth_prop
        size = scene.pore_size_prop

        print(ratio)
        
        bpy.ops.object.mode_set(mode = 'EDIT') 

        context = bpy.context
        selected_verts = context.active_object.vertex_groups.new(name='pores')
        vertex_group_data = []

        #select random vertices....
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.mesh.select_random(ratio=ratio)

        #...and store them into our pores vertex group
        vertex_group_data = [i.index for i in context.active_object.data.vertices if i.select]
        bpy.ops.object.mode_set(mode = 'OBJECT') 
        selected_verts.add(vertex_group_data , 1.0, 'ADD')
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        obj = context.object
        verts = obj.data
        bm = bmesh.from_edit_mesh(context.edit_object.data)
        bm.verts.ensure_lookup_table()

        #move each selected vertex and its neighbours proportionally
        for idx in vertex_group_data:
            v = bm.verts[idx]
            v.select = True
            transform = -v.normal * depth
            bpy.ops.transform.translate(value=transform, 
                                constraint_axis=(False, False, False),
                                orient_type='GLOBAL',
                                use_proportional_edit=True,
                                mirror=False, 
                                proportional_edit_falloff='SHARP',
                                proportional_size=size)
            v.select = False

        pore_pairs = []

        #pair up pores
        for i in range(int(len(vertex_group_data)/2)):
            if(i * 2 < len(vertex_group_data)):
                pore_pairs.__add__([bm.verts[i * 2], bm.verts[i * 2 + 1]])

        #Find and select the shortest paths between pore pairs

        for pair in pore_pairs:
            bpy.ops.mesh.select_all(action='DESELECT')
            pair[0].select = True
            pair[1].select = True
            bpy.ops.mesh.shortest_path_select()


        bpy.ops.object.mode_set(mode = 'OBJECT') 

        return {'FINISHED'}


def register():
    bpy.utils.register_class(PoreGeneratorMainPanel)
    bpy.types.Scene.pore_ratio_prop = bpy.props.FloatProperty(name="Pore ratio", description="The pore ratio.", default=0.01, min=0, max=1)
    bpy.types.Scene.pore_depth_prop = bpy.props.FloatProperty(name="Pore depth", description="The pore depth.", default=0.01, min=0, max=1)
    bpy.types.Scene.pore_size_prop = bpy.props.FloatProperty(name="Pore radius", description="The pore radius.", default=0.01, min=0, max=1)
    bpy.utils.register_class(GENERATOR_OT_PORES)
    

def unregister():
    bpy.utils.unregister_class(PoreGeneratorMainPanel)
    del bpy.types.Scene.pore_ratio_prop
    del bpy.types.Scene.pore_depth_prop
    del bpy.types.Scene.pore_depthrdm_prop
    del bpy.types.Scene.pore_size_prop
    del bpy.types.Scene.pore_sizerdm_prop
    bpy.utils.unregister_class(GENERATOR_OT_PORES)


if __name__ == "__main__":
    register()