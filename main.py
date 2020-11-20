from core import Mesh, Camera, Scene
from core import Renderer



def example_1():
    scene = Scene()

    cam = Camera(position=[10, 10, 10], look_at = [0, 0, 0], up = [0, 1, 0])
    scene.addCam(cam)

    mesh_cube = Mesh('cube.obj')
    scene.addMesh(mesh_cube)

    renderer = Renderer('mitsuba',sample=32)

    renderer.render('test.png',scene)

example_1()
