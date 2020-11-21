class Scene():
    def __init__(self):
        self.__meshes = []
        self.__cam = None
    def addCam(self, cam):
        self.__cam = cam
    def addMesh(self, mesh):
        self.__meshes.append(mesh) 
    def getCam(self):
        return self.__cam
    def getMeshes(self):
        return self.__meshes
    def setCamGUI(self):
        import open3d as o3d
        import numpy as np
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        for obj in self.__meshes:
            mesh = o3d.io.read_triangle_mesh(obj.filename)
            mesh.compute_vertex_normals()
            vis.add_geometry(mesh)

        ctr = vis.get_view_control()
        ctr.change_field_of_view(step=-5)

        vis.run()
        param = ctr.convert_to_pinhole_camera_parameters()
        R = param.extrinsic[:3,:3]
        T = param.extrinsic[:3,3]

        self.__cam.setPosition(R.T @ ([0,0,0] - T))

        self.__cam.setLookat(R[2,:3])
        self.__cam.setUp(-R[1,:3])

        vis.destroy_window()
