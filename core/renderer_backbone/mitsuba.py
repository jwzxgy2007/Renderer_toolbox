

import mitsuba, os





from core import Renderer

mitsuba.set_variant('packet_rgb')# packet_rgb gpu_rgb
from mitsuba.core import Thread
from mitsuba.core.xml import load_file
from mitsuba.core import Bitmap, Struct
from core.renderer_backbone.utils import *

class Mitsuba_renderer(Renderer):
    def __init__(self, max_depth = 5, per_sample = 2, sample = 512, width = 512, height = 512, focal_length = 50):
        self.max_depth = max_depth
        self.per_sample = per_sample
        self.sample = sample
        self.width = width
        self.height = height
        self.focal_length = focal_length

    def render(self, savepath, scene):
        
        scene_xml = Scene(max_depth = self.max_depth, samples_per_pass = self.per_sample)
        meshes = scene.getMeshes()
        cam = scene.getCam()
        for idx, obj in enumerate(meshes):
            obj_path = obj.filename
            tex_path = obj_path.replace('obj','png').replace('\\','/')
            if os.path.exists(tex_path):
                obj = scene_xml.add_obj(obj_path, tex_path, 'tex' + str(idx), 'bsdf' + str(idx), twosided = True)
                idx = idx + 1
            else:
                obj = scene_xml.add_obj(obj_path)
        
        scene_xml.add_sensor(origin = cam.getPosition(), target = cam.getLookat(), up = cam.getUp(), sample = self.sample, width = self.width, height = self.height, focal_length = self.focal_length)
        scene_xml.add_emitters()
        scene_xml.write("temp.xml")
        filename = "temp.xml"
        
        Thread.thread().file_resolver().append(os.path.dirname(filename))
        scene = load_file(filename)
        sensor = scene.sensors()[0]
        scene.integrator().render(scene, sensor)
        film = sensor.film()
        img = film.bitmap(raw=True).convert(Bitmap.PixelFormat.RGBA, Struct.Type.UInt8, srgb_gamma=True)
        img.write(savepath)


