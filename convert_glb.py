import bpy
import sys
import os

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Get command line arguments
glb_path = sys.argv[-2]  # Second to last argument
blend_path = sys.argv[-1]  # Last argument

# Import GLB
bpy.ops.import_scene.gltf(filepath=glb_path)

# Save as blend file
bpy.ops.wm.save_as_mainfile(filepath=blend_path)
