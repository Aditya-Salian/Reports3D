import bpy
import sys
argv = sys.argv
argv = argv[argv.index("--") + 1:]
id = argv[0]

brain_filepath = 'C://Users//Parin//transcend1//transcend1//brain.stl'
tumour_filepath = 'C://Users//Parin//transcend1//transcend1//tumour.stl'

bpy.ops.import_mesh.stl(filepath=brain_filepath)
bpy.ops.import_mesh.stl(filepath=tumour_filepath)

ob = bpy.context.scene.objects["Brain"]       # Get the object
bpy.ops.object.select_all(action='DESELECT') # Deselect all objects
bpy.context.view_layer.objects.active = ob   # Make the cube the active object 
ob.select_set(True)

brain = bpy.data.materials.new(name="brain")
ob.data.materials.append(brain)

bpy.ops.object.editmode_toggle()
bpy.ops.mesh.decimate()
bpy.ops.mesh.decimate(ratio=0.08)
bpy.ops.object.editmode_toggle()


ob = bpy.context.scene.objects["Tumour"]
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.objects.active = ob 
ob.select_set(True)

tumour = bpy.data.materials.new(name="tumour")
ob.data.materials.append(tumour)

bpy.context.object.location[0] = 240
bpy.context.object.location[2] = 155
bpy.context.object.rotation_euler[0] = -1.5708
bpy.context.object.rotation_euler[1] = 1.5708

path = "C://Users//Parin//transcend1//transcend1//static//" + id +"modelnew.gltf"
bpy.ops.object.editmode_toggle()
bpy.ops.export_scene.gltf(export_format = "GLTF_EMBEDDED", filepath = path, export_materials = True)
