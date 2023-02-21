import bpy
import math
import datetime

def delete_all(
    scene_object:bool=False,
    data_object:bool=True,
    data_mesh:bool=True,
    data_material:bool=True
):
    """ Delete all items by default.
    If set args to False, that kinds of items will not be deleted.
    """
    if scene_object:
        for item in bpy.context.scene.objects:
            bpy.context.scene.objects.unlink(item)

    if data_object:
        for item in bpy.data.objects:
            bpy.data.objects.remove(item)

    if data_mesh:
        for item in bpy.data.meshes:
            bpy.data.meshes.remove(item)
    
    if data_material:
        for item in bpy.data.materials:
            bpy.data.materials.remove(item)

def toggle_console():
    """ Show console to see print massage.
    """
    bpy.ops.wm.console_toggle()

def initialize():
    """ Iinitialize design space.
    """
    delete_all()
    toggle_console()
    
    print(f"Run script at {datetime.datetime.now()}")


initialize()

########## Parameters ##########

# Clip
CLIP_X = 32 # X axis is along with aquarium edge.
CLIP_TOP_Y = 16
CLIP_BOT_Y = 20
CLIP_Z = 14 # Z axis is width of clip
CLIP_THICKNESS = 2.5 # Thickness of z axis
CLIP_HOLE_RADIUS = 4.0 # No margin to fix wood pole *** this parmeter depends on [ HOLE_RADIUS ] ***
EDGE_SPACE_Y = CLIP_BOT_Y # Measured value is 13
EDGE_SPACE_Z = 9 # Measured value is 9.0, no margin (polish if needed)
EDGE_SLIT_Y = 1.3 # Measured value is 1.2, add 0.1 is margin.
EDGE_SLIT_Z = 1.1 # Measured Value is 1.0, add 0.1 is margin.
EDGE_SLIT_DZ = 2.1 # 1.9 1 6.1 -> 2.4, 6.6 -> dz = 2.1 

################################


# clip
bpy.ops.mesh.primitive_cube_add(
    size = 1,
    scale = (
        CLIP_X, 
        CLIP_TOP_Y + CLIP_BOT_Y, 
        CLIP_Z
    ),
    location = (0, 0, 0),
    rotation = (0, 0, 0),
)
clip = bpy.context.active_object
clip.name = "clip"


# clip_hole
bpy.ops.mesh.primitive_cylinder_add(
    radius = CLIP_HOLE_RADIUS,
    depth = CLIP_Z - CLIP_THICKNESS,
    location = (0, (CLIP_TOP_Y + CLIP_BOT_Y)/2 - 8, CLIP_THICKNESS/2),
    rotation = (0, 0, 0),
)
clip_hole = bpy.context.active_object
clip_hole.name = "clip_hole"


# edge_space
bpy.ops.mesh.primitive_cube_add(
    size = 1,
    scale = (
        CLIP_X, 
        EDGE_SPACE_Y,
        EDGE_SPACE_Z
    ),
    location = (0, -(CLIP_TOP_Y + CLIP_BOT_Y)/2 + EDGE_SPACE_Y/2, 0),
    rotation = (0, 0, 0),
)
edge_space = bpy.context.active_object
edge_space.name = "edge_space"


# edge_slit
bpy.ops.mesh.primitive_cube_add(
    size = 1,
    scale = (
        CLIP_X, 
        EDGE_SLIT_Y, 
        EDGE_SLIT_Z
    ),
    location = (0, -(CLIP_TOP_Y + CLIP_BOT_Y)/2 + EDGE_SPACE_Y + EDGE_SLIT_Y/2, EDGE_SLIT_DZ),
    rotation = (0, 0, 0),
)
edge_slit = bpy.context.active_object
edge_slit.name = "edge_slit"


def apply_modifier_diff(base_object, bool_object):
    """ Apply boolean modifier "DIFFERENCE"
    """
    bool = base_object.modifiers.new(name="bool", type="BOOLEAN")
    bool.object = bool_object
    bool.operation = "DIFFERENCE"
    bpy.ops.object.modifier_apply(modifier="bool")
    bool_object.hide_set(True)
    return None

# Apply DIFFERENCE
apply_modifier_diff(clip, clip_hole)
apply_modifier_diff(clip, edge_space)
apply_modifier_diff(clip, edge_slit)


bpy.ops.object.select_all(action='SELECT')