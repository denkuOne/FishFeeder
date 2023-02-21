import bpy
import math
import datetime


def initialize():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.ops.wm.console_toggle()
    print(f"Run script at {datetime.datetime.now()}")

#initialize()

for item in bpy.data.meshes:
    bpy.data.meshes.remove(item)

def add_pipe(
    body_radius,
    hole_radius,
    depth,
    location,
    rotation,
    body_name,
    hole_name,
):
    # body
    bpy.ops.mesh.primitive_cylinder_add(
        radius = body_radius,
        depth = depth,
        location = location,
        rotation = rotation,
    )
    body = bpy.context.active_object
    body.name = body_name

    # hole
    bpy.ops.mesh.primitive_cylinder_add(
        radius = hole_radius,
        depth = depth,
        location = location,
        rotation = rotation,
    )
    hole = bpy.context.active_object
    hole.name = hole_name

    # Apply boolean modifier
    bool = body.modifiers.new(name="bool", type="BOOLEAN")
    bool.object = hole
    bool.operation = "DIFFERENCE"
    bpy.ops.object.modifier_apply(modifier="bool")
    hole.hide_set(True)
    
    return body


# Parameters

BODY_RADIUS = 16
HOLE_RADIUS = 4.2 # add 0.1 for margin.
BODY_DEPTH = 32
BODY_THICKNESS = 2.5
MOAT_DEPTH = 8
POLE_RADIUS = 2
POLE_ADJUST = 0.4
POCKET_SIZE = 14


# main

body = add_pipe(
    body_radius = BODY_RADIUS,
    hole_radius = HOLE_RADIUS,
    depth = BODY_DEPTH,
    location = (0, 0, 0),
    rotation = (0, 0, 0),
    body_name = "body",
    hole_name = "hole",    
)

moat = add_pipe(
    body_radius = BODY_RADIUS - BODY_THICKNESS,
    hole_radius = HOLE_RADIUS + BODY_THICKNESS,
    depth = MOAT_DEPTH,
    location = (0, 0, (BODY_DEPTH - MOAT_DEPTH)/2),
    rotation = (0, 0, 0),
    body_name = "moat",
    hole_name = "moat_hole",    
)
bool = body.modifiers.new(name="bool", type="BOOLEAN")
bool.object = moat
bool.operation = "DIFFERENCE"
bpy.ops.object.modifier_apply(modifier="bool")
moat.hide_set(True)


pocket = bpy.ops.mesh.primitive_cube_add(
    size = 1,
    scale = (BODY_RADIUS - HOLE_RADIUS, POCKET_SIZE, POCKET_SIZE),
    location = ((BODY_RADIUS + HOLE_RADIUS)/2 + BODY_THICKNESS, 0, -MOAT_DEPTH/2),
    rotation = (0, 0, 0),
)
pocket = bpy.context.active_object
pocket.name = "pocket"
bool = body.modifiers.new(name="bool", type="BOOLEAN")
bool.object = pocket
bool.operation = "DIFFERENCE"
bpy.ops.object.modifier_apply(modifier="bool")
pocket.hide_set(True)


# Define position parameter
xy_length = (BODY_RADIUS + HOLE_RADIUS)/2 + POLE_ADJUST
xy_rotation = math.pi / 9 #


# separator1
bpy.ops.mesh.primitive_cube_add(
    size = 1,
    scale = (BODY_THICKNESS, BODY_RADIUS - HOLE_RADIUS - BODY_THICKNESS, MOAT_DEPTH),
    location = (0, xy_length, (BODY_DEPTH - MOAT_DEPTH)/2),
    rotation = (0, 0, 0),
)
sep1 = bpy.context.active_object
sep1.name = "sep1"

# separator2
bpy.ops.mesh.primitive_cube_add(
    size = 1,
    scale = (BODY_THICKNESS, BODY_RADIUS - HOLE_RADIUS - BODY_THICKNESS, MOAT_DEPTH),
    location = (0, -xy_length, (BODY_DEPTH - MOAT_DEPTH)/2),
    rotation = (0, 0, 0),
)
sep2 = bpy.context.active_object
sep2.name = "sep2"

# pole1
bpy.ops.mesh.primitive_cylinder_add(
    radius = POLE_RADIUS,
    depth = MOAT_DEPTH,
    location = (xy_length * math.sin(xy_rotation), xy_length * math.cos(xy_rotation), -(BODY_DEPTH + MOAT_DEPTH)/2),
    rotation = (0, 0, 0),
)
pole1 = bpy.context.active_object
pole1.name = "pole1"

# pole2
bpy.ops.mesh.primitive_cylinder_add(
    radius = POLE_RADIUS,
    depth = MOAT_DEPTH,
    location = (-xy_length * math.sin(xy_rotation), -xy_length * math.cos(xy_rotation), -(BODY_DEPTH + MOAT_DEPTH)/2),
#    location = (0, -(BODY_RADIUS + HOLE_RADIUS)/2, -(BODY_DEPTH + MOAT_DEPTH)/2),
    rotation = (0, 0, 0),
)
pole2 = bpy.context.active_object
pole2.name = "pole2"

bpy.ops.object.select_all(action='SELECT')