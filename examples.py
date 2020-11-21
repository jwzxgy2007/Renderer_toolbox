import sys
sys.path.append('.')
from core import Mesh, Camera, Scene
from core import Renderer



def example_1():
    scene = Scene()

    cam = Camera(position=[1, 1, 1], look_at = [0, 0, 0], up = [0, 1, 0])
    scene.addCam(cam)

    mesh_cube = Mesh('cube.obj')
    scene.addMesh(mesh_cube)
    renderer = Renderer('blender',sample=32, weigh = 512, height = 512)
    renderer.render('/path/to/save',scene)

def example_2():
    import os
    scene = Scene()

    cam = Camera(position=[0, 50, 0], look_at = [0, 0, 0], up = [0, 0, 1])
    scene.addCam(cam)
    scene_path = './example/0018b6c8-c3b6-4fb8-a640-4b9b0b763254'
    room_list = os.listdir(scene_path)
    for room in room_list:
        if os.path.isfile(os.path.join(scene_path, room)):
            continue
        for obj_name in os.listdir(os.path.join(scene_path, room)):
            if not obj_name.endswith('.obj'):
                continue
            mesh = Mesh(os.path.join(scene_path, room, obj_name))
            scene.addMesh(mesh)
    scene.setCamGUI()
    
    renderer = Renderer('mitsuba',sample=32, weigh = 512, height = 512, per_sample = 2)
    renderer.render('D:/zlx/Renderer_toolbox/test2.png',scene)

example_2()
