import bpy
import bmesh

bl_info = {
    "name": "Set Smooth Group",
    "author": "Viktor Kom",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Mesh > Normals",
    "description": "Set smooth group with sharp edges for selected faces",
    "warning": "",
    "wiki_url": "https://x.com/Viktorcor",
    "category": "Mesh",
}

class MESH_OT_set_smooth_group(bpy.types.Operator):
    """Set Smooth Group"""
    bl_idname = "mesh.set_smooth_group"
    bl_label = "Set Smooth Group"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        set_smooth_group()
        return {'FINISHED'}

def set_smooth_group():
    obj = bpy.context.active_object
    if obj is None or obj.type != 'MESH':
        print("No mesh object selected.")
        return
    
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Get currently selected faces
    bm = bmesh.from_edit_mesh(obj.data)
    selected_faces = [f for f in bm.faces if f.select]
    
    # Remove duplicate vertices within a distance of 0.00001 meters
    bpy.ops.mesh.remove_doubles(threshold=0.00001)
    
    # Clear sharp edges
    bpy.ops.mesh.mark_sharp(clear=True)
    
    # Apply smoothing to selected faces
    bpy.ops.mesh.faces_shade_smooth()
    
    # Select boundary edges for the selected faces
    bpy.ops.mesh.region_to_loop()
    
    # Mark boundary edges as sharp
    bpy.ops.mesh.mark_sharp()
    
    # Restore the selection of faces
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.mesh.select_all(action='DESELECT')
    for face in selected_faces:
        face.select = True
    
    # Switch to Face Select mode
    bpy.ops.mesh.select_mode(type='FACE')
    
    print("Operation completed successfully.")

def menu_func(self, context):
    self.layout.operator(MESH_OT_set_smooth_group.bl_idname)

def register():
    bpy.utils.register_class(MESH_OT_set_smooth_group)
    # Add the operator to the Mesh > Normals menu
    bpy.types.VIEW3D_MT_edit_mesh_normals.append(menu_func)
    # Add the hotkey
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    kmi = km.keymap_items.new(MESH_OT_set_smooth_group.bl_idname, 'G', 'PRESS', alt=True)

def unregister():
    bpy.utils.unregister_class(MESH_OT_set_smooth_group)
    # Remove the operator from the Mesh > Normals menu
    bpy.types.VIEW3D_MT_edit_mesh_normals.remove(menu_func)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps['Mesh']
    for kmi in km.keymap_items:
        if kmi.idname == MESH_OT_set_smooth_group.bl_idname:
            km.keymap_items.remove(kmi)
            break

if __name__ == "__main__":
    register()
