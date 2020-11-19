class Scene():
    """
    docstring
    """
    def __init__(self):
        self.__meshes = []
        self.__cam = None
    def add_cam(self, cam):
        self.__cam = cam
    def add_mesh(self, mesh):
        self.__meshes.append(mesh)
    