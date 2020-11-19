

import argparse, sys, os

import igl

parser = argparse.ArgumentParser()
parser.add_argument('--scene_path', type=str, default='',
                    help='')
parser.add_argument('--save_path', type=str, default='',
                    help='')
parser.add_argument('--mode', type=str, default='gpu_rgb',
                    help='')
parser.add_argument('--size', type=int, default=512,
                    help='')
parser.add_argument('--sample', type=int, default=32,
                    help='')
parser.add_argument('--per_sample', type=int, default=16,
                    help='')
parser.add_argument('--max_depth', type=int, default=5,
                    help='')
parser.add_argument('--origin', nargs='+', type=float, default=[0, 10, 0],
                    help='')
parser.add_argument('--target', nargs='+', type=float, default=[0, 0, 0],
                    help='')
parser.add_argument('--up', nargs='+', type=float, default=[0, 0, -1],
                    help='')
parser.add_argument('--focal_length', type=int, default=30,
                    help='')


args = parser.parse_args()

import mitsuba
mitsuba.set_variant(args.mode)
from mitsuba.core import Thread
from mitsuba.core.xml import load_file
from mitsuba.core import Bitmap, Struct
from mitsuba_utils import *


if not os.path.exists(args.save_path):
    os.mkdir(args.save_path)

scene_list = os.listdir(args.scene_path)
for scene_name in scene_list:
    if not os.path.isdir(os.path.join(args.scene_path, scene_name)):
        continue
    total_trans = [0,0,0]
    room_list = os.listdir(os.path.join(args.scene_path, scene_name))
    # print(room_list)
    # cc()
    for room in room_list:
        
        # if not ('Living' in room or 'Dining' in room):
        #     continue
        mesh_list = []
        idx = 0
        # print(room)
        scene_xml = Scene(max_depth = args.max_depth, samples_per_pass = args.per_sample)
        # idx +=1
        if os.path.isfile(os.path.join(args.scene_path, scene_name, room)):
            continue
        for obj_name in os.listdir(os.path.join(args.scene_path, scene_name, room)):
            if not obj_name.endswith('.obj'):
                continue
            # if obj_name in ['mesh.obj','room_noceilling.obj','room_noceillingwithtexturedwall.obj']:
            #     continue
            if obj_name == 'mesh.obj':
                wall_v, _, _, wall_f, _, _  = igl.read_obj(os.path.join(args.scene_path, scene_name, room, obj_name))
                total_trans = (wall_v.max(0) + wall_v.min(0))/2
                # continue
            mesh_list.append(os.path.join(args.scene_path, scene_name, room, obj_name).replace('\\','/'))
        if not len(mesh_list):
            continue
        for obj_path in mesh_list:

            tex_path = obj_path.replace('obj','png').replace('\\','/')
            if os.path.exists(tex_path):
                obj = scene_xml.add_obj(obj_path, tex_path, 'tex' + str(idx), 'bsdf' + str(idx), twosided = True)
                idx = idx + 1
            else:
                obj = scene_xml.add_obj(obj_path)
            scene_xml.add_trans(obj, trans = [-total_trans[0], 0, -total_trans[2]])
    
        scene_xml.add_sensor(origin = args.origin, target = args.target, up = args.up, sample = args.sample, width = args.size, height = args.size, focal_length = args.focal_length)
        scene_xml.add_emitters()
        scene_xml.write("temp.xml")
        filename = "temp.xml"
        
        Thread.thread().file_resolver().append(os.path.dirname(filename))
        scene = load_file(filename)
        sensor = scene.sensors()[0]
        scene.integrator().render(scene, sensor)
        film = sensor.film()
        img = film.bitmap(raw=True).convert(Bitmap.PixelFormat.RGBA, Struct.Type.UInt8, srgb_gamma=True)
        img.write(os.path.join(args.save_path,scene_name+'_'+room+'.png'))