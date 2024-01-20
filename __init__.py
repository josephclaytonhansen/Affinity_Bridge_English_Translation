# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Affinity_Bridge",
    "author": "Hattori_Kaoru( t0rry_ )",
    "description": "Launches AffinityPhoto2 from Blender",
    "blender": (4, 0, 0),
    "version": (0, 6, 0),
    "location": "Image Editor >> Property Panel",
    "warning": "This version is experimental",
    "support": "COMMUNITY",
    "category": "User",
    "doc_url": "https://github.com/t0rry/Affinity_Bridge"
}

if "bpy" in locals():
    import imp
    imp.reload(ot)
    imp.reload(ui)
else:
    from . import ot
    from . import ui
    
import bpy
from bpy.props import (
    BoolProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    PointerProperty,
    StringProperty
)

class AffinityBridgeProp(bpy.types.PropertyGroup):
    file_format: EnumProperty(
        name='File Format',
        description='Choose the file format',
        items=[('PNG', 'PNG', 'PNG file format'),
               ('JPEG', 'JPEG', 'JPEG file format'),
               ('OPEN_EXR', 'Open_EXR', 'OpenEXR file format'),
               ('OPEN_EXR_MULTILAYER', 'Open EXR Multilayer', 'OpenEXR Multilayer file format')]
    )
    
    color_mode: EnumProperty(
        name='Color Mode',
        description='Choose the color mode',
        items=[('BW', "Black & White", 'Black & White color mode'),
               ('RGB', 'RGB', 'RGB color mode'),
               ('RGBA', 'RGBA', 'RGBA color mode')]
    )
    
    file_name: StringProperty(
        name='File Name',
        description='Name to use for saved image',
        default='AffinityBridge'
    )
    
    path_str: StringProperty(
        name='Path String',
        description='Display of saved image path',
        default=''
    )    
    
    is_change_name: BoolProperty(
        name='Change Name',
        description='Use to input original name',
        default=False
    )

    is_used_affinityphoto: BoolProperty(
        name='Use AffinityPhoto',
        description='Launch AffinityPhotoV2 when using AffinityBridge',
        default=True
    )
    # maybe don't use old_ff, old_cm
    
    old_ff: StringProperty(
        name='Old File Format',
        description='To change parameter when saving image'
    )
    
    old_cm: StringProperty(
        name='Old Color Mode',
        description='To change parameter when saving image'        
    )
    
class AFFINITYBRIDGE_MT_CompositPanel(bpy.types.Menu):
    
    bl_idname = "AFFINITYBRIDGE_MT_SetOpenExrSelected"
    bl_label = "AffinityBridge"
    bl_description = "Panel that works on the Compositor"
    
    def draw(self, context):
        layout = self.layout
        ui_type = context.area.ui_type
        if ui_type == "CompositorNodeTree":
            layout.operator(ot.AFFINTYBRIDGE_OT_SetOpenEXR_Selected.bl_idname, icon='NODETREE')  
            layout.operator(ot.AFFINITYBRIDGE_OT_SetOpenEXR_RenderLayer.bl_idname, icon='NODETREE')               

class AFFINITYBRIDGE_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

        
    option_image_editing_exe: StringProperty(
        name="Specify Image Editing Software",
        subtype="FILE_PATH",
        default=""
    )
    
    is_display_filepath: BoolProperty(
        name="Display file path of exe file on UI",
        default=False
    )
    
    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.prop(self, 'option_image_editing_exe')
        box.prop(self, 'is_display_filepath', text="Enable editing exe file on the image editor")
        box.label(icon='ERROR', text='It is recommended to disable this, as the file path will be displayed on the image editor.')
        
def menu_register_func(cls, context):
    
    ui_type = context.area.ui_type
    if ui_type == "CompositorNodeTree":
        cls.layout.separator()
        cls.layout.menu(AFFINITYBRIDGE_MT_CompositPanel.bl_idname, icon='NODETREE')
        
classes = [
    AffinityBridgeProp,
    AFFINITYBRIDGE_Preferences,
    AFFINITYBRIDGE_MT_CompositPanel,
    ot.AFFINITYBRIDGE_OT_SetOpenEXR_RenderLayer,
    ot.AFFINITYBRIDGE_OT_SetOpenEXR_Selected,
    ot.AFFINITYBRIDGE_OT_Photo,
    ot.AFFINITYBRIDGE_OT_Reload,
    ui.AFFINITYBRIDGE_PT_Panel,
    ui.AFFINITYBRIDGE_PT_RenderSettingPanel,
    ui.AFFINITYBRIDGE_PT_InformationPanel
]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.affinitybridge = bpy.props.PointerProperty(type=AffinityBridgeProp)
    bpy.types.NODE_MT_context_menu.append(menu_register_func)
    
def unregister():
    bpy.types.NODE_MT_context_menu.remove(menu_register_func)
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.affinitybridge
