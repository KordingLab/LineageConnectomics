"""
This is a script to get the centers of all selected objects in a Blender file.

To use, select only the objects you care about, and then run this script.

Note that this relies upon Blender Python, and cannot be run outside of the
built-in Blender interpreter.

"""

import bpy
import json

# Get a list of all selected objects
selected_objects = bpy.context.selected_objects


# Get the center of all selected objects
def get_center(obj):
    """
    Get the center of an object.

    Args:
        obj: The object to get the center of.

    Returns:
        A tuple of the object's center.

    """
    return (obj.name, round(obj.location.x, 3), round(obj.location.y, 3), round(obj.location.z, 3))


# Get the center of all selected objects
centers = [get_center(obj) for obj in selected_objects]

print(json.dumps({k: [x, y, z] for k, x, y, z in centers}))
