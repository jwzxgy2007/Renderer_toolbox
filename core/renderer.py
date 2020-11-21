class Renderer():
    
    def __init__(self, backbone, **kwargs):

        if backbone == 'blender':
            from core.renderer_backbone import Blender_renderer
            self.renderer = Blender_renderer(**kwargs)
        elif backbone == 'mitsuba':
            from core.renderer_backbone import Mitsuba_renderer
            self.renderer = Mitsuba_renderer(**kwargs)
        else:
            raise NotImplementedError
        
    def render(self, savepath, scene):
        self.renderer.render(savepath, scene)
        
