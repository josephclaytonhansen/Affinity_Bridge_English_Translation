# AffinityBridge Addon V0.6.0

![export](https://github.com/t0rry/Affinity_Bridge/assets/78343605/2ee80440-f5a9-401a-8057-0c9a0b8b58a7)

## What is this addon?

It was created to strongly integrate Blender and AffinityPhotoV2.
Currently, updates are being made to enable collaboration with software other than AffinityPhotoV2.

## Features

### Launch RenderLayer and ViewerNode directly in the editor software

The standard "Edit in External Editor" in Blender does not support RenderLayer and ViewerNode, so this addon adds support.
Moreover, it supports PNG/JPEG/OpenEXR/OpenEXR(MultiLayer) with a powerful exporter.

By specifying an exe file, you can execute similar functions in editors other than AffinityPhotov2.

### Launch externally edited images that have been loaded into Blender

Naturally, you can launch images loaded into Blender in external editor software.

### Image Reload

Reloads images saved in the editor. Very useful for texture painting using external editor software.

### Automatically generates an Output node that outputs the selected node in OpenEXR(MultiLayer)

Automatically generates an Output node that outputs the selected node in OpenEXR (MultiLayer) in the Compositing node.
It is convenient when outputting elements in customized group nodes for personal use.

### Automatically generates an Output node that outputs the RenderLayer of the scene in OpenEXR(MultiLayer)

Automatically generates an Output node that outputs the valid paths of the scene's RenderLayer.
Useful when you want to output only pure paths in a scene where the node structure has become complicated due to generating for each RenderLayer.
