# Renderer_toolbox

This is a simple renderer script for beginners to use blender and / or mitsuba2 to render 3D objects. Please follow the instruction and see the examples.


### Install
I recommend using anaconda to install dependencies.

    conda create -n renderer python=3.8
    conda activate renderer
    conda install -c kitsune.one python-blender
    conda install -c open3d-admin open3d
    pip install addict matplotlib pandas plyfile pyyaml tqdm sklearn

Now, you can use blender to rendering! If you want to use mitsuba2, please follow the [mitsuba2](https://mitsuba2.readthedocs.io/en/latest/) to install mitsuba2, and don't forget add 'gpu_rgb' in `mitsuba.conf`.


### example

