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

import bpy
from . import set_smooth_group

def register():
    set_smooth_group.register()

def unregister():
    set_smooth_group.unregister()

if __name__ == "__main__":
    register()
