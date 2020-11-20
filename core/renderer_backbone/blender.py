from core import Renderer
try:
    import bpy, mathutils
except:
    print('Cannot find blender, please install')

class Blender_renderer(Renderer):
    def __init__(self, width = 512, height = 512):
        self.scene = bpy.context.scene
        self.scene.render.engine = 'CYCLES'
        self.scene.world.light_settings.use_ambient_occlusion = True
        self.scene.world.light_settings.ao_factor = 2
        self.scene.cycles.samples = args.sample
        self.scene.render.film_transparent=True
        self.scene.view_layers["View Layer"].cycles.use_denoising = True
        self.scene.cycles.film_transparent = True
        self.scene.render.resolution_x = width
        self.scene.render.resolution_y = height
        self.scene.render.resolution_percentage = 100
        self.scene.cycles.use_adaptive_sampling = True
        self.scene.cycles.adaptive_threshold = 0.01
        self.scene.cycles.device = 'GPU'
        self.scene.render.image_settings.file_format = 'PNG'
        self.scene.render.image_settings.color_mode = 'RGBA'
        bpy.data.worlds['World'].use_nodes = True

        

    def render(self, savepath, scene):
        for obj in bpy.data.objects:
                if not obj.name =='Camera':
                    bpy.data.objects.remove(obj)
        meshes = scene.getMeshes()
        cam = scene.getCam()
        for idx, obj in enumerate(meshes):
            obj_path = obj.filename
            if '.ply' in obj_path:
                bpy.ops.import_mesh.ply(filepath=obj_path)
            elif '.obj' in obj_path:
                bpy.ops.import_scene.obj(filepath = obj_path)
        

        bpy.ops.object.select_all(action='DESELECT')

        MSH_OBJS = [m for m in bpy.data.objects if m.type == 'MESH']
        for obj in MSH_OBJS:
            obj.select_set(state=True)
            bpy.context.view_layer.objects.active = obj
        bpy.ops.object.join()


        MSH_OBJS = [m for m in bpy.data.objects if m.type == 'MESH']
        for obj in MSH_OBJS:
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

            obj.location = mathutils.Vector((0.0, 0.0, 0.0))
            bpy.ops.object.transform_apply(scale=True)

        

        cam = self.scene.objects['Camera']
        cam.location = cam.getPosition()
        point_at(cam, cam.getLookat)

        

        self.scene.render.filepath = (savepath)
        bpy.ops.render.render(write_still = True)