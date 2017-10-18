import bpy
import bpy_extras
import csv

outputfile = '/Users/Guy/Desktop/centroid-actual.csv'

f = open(outputfile, "w+")

count = 0.0

for frame in range(1,3000):
	bpy.context.scene.frame_set(frame)
	scene = bpy.context.scene
	obj = bpy.context.object
	co = bpy.data.objects['Galileo Small'].location

	co_2d = bpy_extras.object_utils.world_to_camera_view(scene, obj, co)
	
	render_scale = scene.render.resolution_percentage / 100
	render_size = (int(scene.render.resolution_x * render_scale),int(scene.render.resolution_y * render_scale))
	
	if(int(scene.frame_current)%15 == 0):
		count+=0.5
		f.write(str(count) + "," + str((round(co_2d.x * render_size[0]),round(co_2d.y * render_size[1])))+"\n")

f.close() 