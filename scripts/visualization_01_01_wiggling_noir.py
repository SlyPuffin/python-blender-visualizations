import bpy
import math

# Note:
# This was created almost entirely with the help of ChatGTP3.5
# Only minor adjustments have been made.

# Add a new sphere object to the scene
bpy.ops.mesh.primitive_uv_sphere_add(location=(0,0,0))

# Add a wave modifier to the sphere
sphere = bpy.context.active_object
sphere.rotation_euler = (0, 0, 270 * 0.0174533) # Rotate by 270 degrees in radians
wave_mod = sphere.modifiers.new(name='Wave', type='WAVE')
wave_mod.time_offset = 0.0
wave_mod.height = 0.1
wave_mod.width = 1.0

# Add a Simple Deform modifier to the sphere
deform_mod = sphere.modifiers.new(name='Deform', type='SIMPLE_DEFORM')
deform_mod.deform_method = 'BEND'
deform_mod.angle = 0.0

# Animate the wave and Simple Deform modifiers
for i in range(0, 120):
    t = i / 5.0 # Time in seconds
    offset = math.sin(t) * 2.0 # Time offset for wave modifier
    wave_mod.time_offset = offset
    wave_mod.keyframe_insert(data_path='time_offset', frame=i)

    angle = math.sin(t) * math.pi / 2.0 # Angle for Simple Deform modifier
    deform_mod.angle = angle
    deform_mod.keyframe_insert(data_path='angle', frame=i)

# Add a camera object to the scene
camera_location = (0, -5, 2) # Camera location (x,y,z)
camera_rotation = (math.pi/3, 0, math.pi/2) # Camera rotation (x,y,z)
bpy.ops.object.camera_add(location=camera_location, rotation=camera_rotation)

# Set the camera to point at the sphere
camera = bpy.context.active_object
track_constraint = camera.constraints.new(type='TRACK_TO')
track_constraint.target = sphere
track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
track_constraint.up_axis = 'UP_Y'

# Add a light source to the scene
light_location = (2, -2, 2) # Light location (x,y,z)
light_rotation = (math.pi/4, 0, 0) # Light rotation (x,y,z)
bpy.ops.object.light_add(type='POINT', location=light_location, rotation=light_rotation)

# Set the light to shine on the sphere from the upper-right
light = bpy.context.active_object
light_constraint = light.constraints.new(type='TRACK_TO')
light_constraint.target = sphere
light_constraint.track_axis = 'TRACK_NEGATIVE_Z'
light_constraint.up_axis = 'UP_X'
light.data.energy = 150.0 # Increase the light's brightness
