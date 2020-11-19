from core import Mesh, Camera, Scene





Scene = Scene()
cam = Camera(position=[0, 0, 5], look_at = [0, 0, 0], up = [0, 1, 0])
Scene.add_cam(cam)
mesh_cube = Mesh('cube.obj')
Scene.add_mesh(mesh_cube)

render = Render()