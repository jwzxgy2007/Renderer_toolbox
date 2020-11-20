class Renderer():

    def __init__(self, backbone, **kwargs):

        if backbone == 'blender':
            try:
                from core.renderer_backbone import Blender_renderer
                self.renderer = Blender_renderer(**kwargs)
            except:
                print('Cannot find blender, please install')
                
        elif backbone == 'mitsuba':
            try:
                from core.renderer_backbone import Mitsuba_renderer
                self.renderer = Mitsuba_renderer(**kwargs)
            except:
                print('Cannot find mitsuba, please install')
                
        else:
            raise NotImplementedError
        
    def render(self, savepath, scene):
        self.renderer.render(savepath, scene)
        
