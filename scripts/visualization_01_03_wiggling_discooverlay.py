import bpy
import math

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

# Add a metallic texture to the sphere
material = bpy.data.materials.new(name='Metallic')
sphere.data.materials.append(material)

# Set the material's nodes to create a metallic and reflective texture
material.use_nodes = True
nodes = material.node_tree.nodes

# Clear the default nodes
for node in nodes:
    nodes.remove(node)
    
# Add a Principled BSDF node and connect it to the Material Output node
principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
output_node = nodes.new(type='ShaderNodeOutputMaterial')
material.node_tree.links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])

# Set the Principled BSDF node properties to create a metallic and reflective texture
principled_node.inputs['Base Color'].default_value = (1.0, 1.0, 1.0, 1.0)
principled_node.inputs['Metallic'].default_value = 0.75
principled_node.inputs['Roughness'].default_value = 0.0
principled_node.inputs['Specular'].default_value = 0.75

# Animate the wave and Simple Deform modifiers
for i in range(0, 385):
    t = i / 5.0 # Time in seconds
    offset = math.sin(t) * 2.0 # Time offset for wave modifier
    wave_mod.time_offset = offset
    wave_mod.keyframe_insert(data_path='time_offset', frame=i)

    angle = math.sin(t) * math.pi / 2.0 # Angle for Simple Deform modifier
    deform_mod.angle = angle
    deform_mod.keyframe_insert(data_path='angle', frame=i)
    
# Animate the Principled BSDF node's base color
for i in range(0, 95):
    t = i / 5.0 # Time in seconds
    r_sin = math.sin(t) * 0.5 + 0.5 # Red channel value
    r_cos = math.cos(t) * 0.5 * 0.5
    g_cos = math.cos(t) * 0.5 + 0.5 # Green channel value
    g_sin = math.sin(t) * 0.5 + 0.5
    b_sin = math.sin(t) * 0.5 + 0.5 # Red channel value
    b_cos = math.cos(t) * 0.5 + 0.5
    principled_node.inputs['Base Color'].default_value = (r_sin, g_cos, 1, 1)
    principled_node.inputs['Base Color'].keyframe_insert(data_path='default_value', frame=i)
    principled_node.inputs['Base Color'].default_value = (r_sin, 1, b_cos, 1)
    principled_node.inputs['Base Color'].keyframe_insert(data_path='default_value', frame=i+95)
    principled_node.inputs['Base Color'].default_value = (1, g_sin, b_cos, 1)
    principled_node.inputs['Base Color'].keyframe_insert(data_path='default_value', frame=i+190)
    principled_node.inputs['Base Color'].default_value = (r_cos, g_sin, b_sin, 1)
    principled_node.inputs['Base Color'].keyframe_insert(data_path='default_value', frame=i+285)
        
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

# Add an environment texture to the scene
world = bpy.context.scene.world
env_texture = world.node_tree.nodes.new('ShaderNodeTexEnvironment')
background = world.node_tree.nodes['Background']
world.node_tree.links.new(env_texture.outputs['Color'], background.inputs['Color'])

# Set the environment texture to an HDR image
# Free HDR downloaded from: https://polyhaven.com/hdris
env_texture.image = bpy.data.images.load('/Path/To/HDR/Folder/the_sky_is_on_fire_4k.hdr')

bpy.context.scene.render.film_transparent = True
