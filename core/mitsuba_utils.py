import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def add_indent(text,n):
  sp = " "*n
  lsep = chr(10) if text.find(chr(13)) == -1 else chr(13)+chr(10)
  lines = text.split(lsep)
  for i in range(len(lines)):
    spacediff = len(lines[i]) - len(lines[i].lstrip())
    if spacediff: lines[i] = sp*spacediff + lines[i] 
  return lsep.join(lines)

def defElement2(parent, type, dict_input = {}):
    return ET.SubElement(parent, type, dict_input)
def defElement(parent, type, name, value):
    return ET.SubElement(parent, type, {'name': name, 'value': str(value)})

def defString(parent, name, value):
    return defElement(parent, 'string', name, value)

def defInt(parent, name, value):
    return defElement(parent, 'integer', name, value)

def defFloat(parent, name, value):
    return defElement(parent, 'float', name, value)

def defBool(parent, name, value):
    assert value in ['true', 'false']
    return defElement(parent, 'boolean', name, value)

def defVector(parent, name, value):
    return defElement(parent, 'vector', name, str(value[0])+ ',' + str(value[1]) + ',' + str(value[2]))

def defPoint(parent, name, value):
    return defElement(parent, 'point', name, str(value[0]) + ',' + str(value[1]) + ',' + str(value[2]))

def defColor(parent, name, value):
    return defElement(parent, 'rgb', name, str(value[0]) + ',' + str(value[1]) + ',' + str(value[2]))
def attach_bsdf(mesh_xml, bsdf_id):
    ET.SubElement(mesh_xml, 'ref', {'id': bsdf_id})



class Transform:
    def __init__(self,scale = None, rot = None, trans = None):
        self.scale = scale
        self.rot = rot
        self.trans = trans
    def apply(self, parent):
        transform = ET.SubElement(parent, 'transform', {'name': 'to_world'})
        if not self.scale is None:
            defElement2(transform, 'scale', {'x': str(self.scale[0].item()),'y': str(self.scale[1].item()),'z': str(self.scale[2].item())})
        if not self.rot is None:
            defElement2(transform, 'rot', {'value': rot[:3].tolist(),'angle':rot[3].item()})
        if not self.trans is None:
            defElement2(transform, 'translate', {'x': str(self.trans[0]),'y': str(self.trans[1]),'z': str(self.trans[2])})
        return transform





class Film:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def apply(self, parent):
        film = ET.SubElement(parent, 'film', {'type': 'hdrfilm'})
        defInt(film, 'width', self.width)
        defInt(film, 'height', self.height)
        return film


class Texture:
    def __init__(self, type = 'bitmap', id = 'my_texture', filename = 'texture.png', filter_type = 'bilinear', wrap_mode = 'repeat', raw = 'false', to_uv = None, rgb=None):
        self.type = type
        self.id = id
        self.filename = filename
        self.filter_type = filter_type
        self.wrap_mode = wrap_mode
        self.raw = raw
        self.to_uv = to_uv
        if rgb is not None:
            self.rgb = str(rgb[0]) + ', ' + str(rgb[1]) + ', ' + str(rgb[2])
    def apply(self,parent):
        if self.type == 'bitmap':
            texture = ET.SubElement(parent, 'texture', {'type': self.type, 'id': self.id})
        elif self.type == 'rgb':
            texture = ET.SubElement(parent, 'rgb', {'name': self.type, 'id': self.id, 'value': self.rgb})
        if self.filename is not None:
            defString(texture, 'filename', self.filename)
        return texture
class Bsdf:
    def __init__(self, type = 'diffuse', id = 'my_material', tex_id = 'my_texture', twosided = False):
        self.type = type
        self.id = id
        self.tex_id = tex_id
        self.twosided = twosided
    def apply(self, parent):
        if self.twosided:
            parent = ET.SubElement(parent, 'bsdf', {'type': 'twosided','id': self.id})
            texture = ET.SubElement(parent, 'bsdf', {'type': self.type})
        else:
            texture = ET.SubElement(parent, 'bsdf', {'type': self.type, 'id': self.id})

        ref = ET.SubElement(texture, 'ref', {'name': 'reflectance', 'id': self.tex_id})
        return texture

class Emitters:
    def __init__(self, type = 'constant', radiance = 1):
        self.type = type
        self.radiance = radiance
    def apply(self, parent):
        emitters = ET.SubElement(parent, 'emitter', {'type': self.type})
        ET.SubElement(emitters, 'spectrum', {'name': 'radiance', 'value': str(self.radiance)})


class Sensor:
    def __init__(self, type = 'perspective', focal_length = 50, origin = None, target = None, up = None, near_clip = 0.01, far_clip = 10000, sample = 32, width = 256, height = 256):
        self.origin = str(origin[0]) + ', ' + str(origin[1]) + ', ' + str(origin[2])
        self.target = str(target[0]) + ', ' + str(target[1]) + ', ' + str(target[2])
        self.up = str(up[0]) + ', ' + str(up[1]) + ', ' + str(up[2])
        self.type = type
        self.focal_length = focal_length
        self.near_clip = near_clip
        self.far_clip  = far_clip
        self.sample = sample
        self.film = Film(width, height)

    def apply(self, parent):
        sensor = ET.SubElement(parent, 'sensor', {'type': self.type})
        defString(sensor, 'focal_length', str(self.focal_length))
        trans = ET.SubElement(sensor, 'transform', {'name': 'to_world'})
        if self.target is not None:
            ET.SubElement(trans, 'lookat', {'origin': self.origin, 'target': self.target, 'up': self.up})

        sampler = ET.SubElement(sensor, 'sampler', {'type': 'independent'})
        defInt(sampler, 'sample_count', self.sample)

        self.film.apply(sensor)

        return sensor


class Object:
    def __init__(self, obj_path):
        self.obj_path = obj_path
    def apply(self, parent):
        shape = ET.SubElement(parent, 'shape', {'type':'obj'})
        defString(shape, 'filename', self.obj_path)
        return shape

class Scene:
    def __init__(self, max_depth=-1, samples_per_pass = 32):
        self.scene = ET.Element('scene',{'version':'2.0.0'})
        integrator = ET.SubElement(self.scene, 'integrator', {'type':'path'})
        samples_per_pass  = ET.SubElement(integrator, 'integer', {'name':'samples_per_pass', 'value':str(samples_per_pass)})
        max_depth  = ET.SubElement(integrator, 'integer', {'name':'max_depth', 'value':str(max_depth)})
        ET.SubElement(integrator, 'boolean', {'name':'hide_emitters', 'value':'true'})

    def add_obj(self, obj_path, tex_path = None, tex_id = None, bsdf_id = None, twosided = False):
        mesh = Object(obj_path).apply(self.scene)
        if tex_path is not None:
            texture = Texture(filename = tex_path, id = tex_id)
            texture.apply(self.scene)
            bsdf = Bsdf(tex_id = tex_id, id = bsdf_id, twosided=twosided)
            bsdf.apply(self.scene)
            attach_bsdf(mesh, bsdf_id)
        return mesh
    def add_trans(self,obj, scale = None, rot = None, trans = None):
        transform = Transform(scale, rot, trans)
        transform.apply(obj)
        return transform

    def add_emitters(self):
        Emitters().apply(self.scene)

    def add_sensor(self, origin = [0, 0, 5], target = [0, 0, 0], up = [0, 1, 0], focal_length = 50, sample = 32, width = 256, height = 256):
        sensor = Sensor(origin = origin, target = target, up = up, focal_length = focal_length, sample = sample, width = width, height = height).apply(self.scene)
    def write(self,filename):
        tree = ET.tostring(self.scene,encoding='utf-8').decode()
        tree = BeautifulSoup(tree, "xml").prettify()
        tree = add_indent(tree,4)

        with open(filename, "w") as f:
            f.write(tree)
