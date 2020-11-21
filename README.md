# Renderer_toolbox

This is a simple renderer script for beginners to use blender and / or mitsuba2 to render 3D objects. Please follow the instruction and see the examples.


### Install
I recommend using anaconda to install dependencies.

    conda create -n renderer python=3.8
    conda activate renderer
    conda install -c kitsune.one python-blender
    conda install -c open3d-admin open3d
    pip install addict matplotlib pandas plyfile pyyaml tqdm sklearn

Now, you can use blender to rendering! If you want to use mitsuba2, please follow the [mitsuba2](https://mitsuba2.readthedocs.io/en/latest/) to install mitsuba2, and *don't forget add 'gpu_rgb' in `mitsuba.conf` if you want to use GPU to rendering*.


### examples

You can see the examples.py to know how to use.

First, you need to inital a scene

`scene = Scene()`

Next, you need to add a camera, and set `position, look_at, up` vector.

    cam = Camera(position=[1, 1, 1], look_at = [0, 0, 0], up = [0, 1, 0])
    scene.addCam(cam)

Or, you can add `scene.setCamGUI()` to use open3d's GUI to specify a camera params.

Then, you can add objects you like

    mesh_cube = Mesh('cube.obj')
    scene.addMesh(mesh_cube)

Finally, you can render through

    renderer = Renderer('blender',sample=32)
    renderer.render('path/to/save(absolute path)',scene)

### TODO

This is a initial script now, some features need to be added in the future

- [ ] Documents
- [ ] Object transform
- [ ] Lighting
- [ ] Normal, depth rendering
