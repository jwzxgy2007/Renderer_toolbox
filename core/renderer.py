class Renderer():
    """
    docstring
    """
    def __init__(self, backbone):
        if backbone == 'blender':
            try:
                from core.renderer import Blender_renderer
                self.renderer = Blender_renderer()
            except:
                print('Cannot find blender, please install')
                pass
        elif backbone == 'blender':
            try:
                from core.renderer import Mitsuba_renderer
                self.renderer = Mitsuba_renderer()
            except:
                print('Cannot find mitsuba, please install')
                pass
        else:
            raise NotImplementedError
        pass
    def render(self):
        pass
