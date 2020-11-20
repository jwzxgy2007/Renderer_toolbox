class Scene():
    """
    docstring
    """
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
    