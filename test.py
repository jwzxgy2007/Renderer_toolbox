import open3d as o3d
import numpy as np


# from core import Obj


mesh = o3d.io.read_triangle_mesh("cube.obj")
mesh.compute_vertex_normals()

vis = o3d.visualization.Visualizer()
vis.create_window()
vis.add_geometry(mesh)
ctr = vis.get_view_control()

vis.run()
param = ctr.convert_to_pinhole_camera_parameters()
print(param.extrinsic)
R = param.extrinsic[:3,:3]
T = param.extrinsic[:3,3]
cam_pos = R.T @ ([0,0,0] - T)
cam_look_at = R.T @ ([0,0,1] - T) - cam_pos
cam_up = R.T @ ([0,-1,0] - T) - cam_pos
print(cam_pos, cam_look_at, cam_up)
vis.destroy_window()
