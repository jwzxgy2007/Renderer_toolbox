import numpy as np
class Mesh:
    """
    docstring
    """
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.transform_list = []

    def applyScale(self, s):
        self.transform_list.app
    def applyRot(self, rot):
        self.__r = rot
    def applyTrans(self, trans):
        self.__t = trans

    def getScale(self):
        return self.__s
    def getRot(self):
        return self.__r
    def getTrans(self):
        return self.__t




class Camera:
    """
    docstring
    """
    def __init__(self, position = [0, 0, 1], look_at = [0, 0, 0], up = [0, 1, 0]):
        self.__position = position
        self.__look_at = look_at
        self.__up = up

    def setLookat(self, look_at):
        self.__look_at = look_at
    def getLookat(self):
        return self.__look_at

    def setPosition(self, position):
        self.__position = position
    def getPosition(self):
        return self.__position

    def setUp(self, up):
        self.__up = up
    def getUp(self):
        return self.__up

