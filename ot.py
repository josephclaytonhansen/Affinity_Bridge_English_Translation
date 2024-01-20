from typing import Set
import bpy
import subprocess
import os
from bpy.types import Context

class AFFINITYBRIDGE_OT_SetOpenEXR_Selected(bpy.types.Operator):
    """
    Automatically sets up the OpenEXR (MultiLayer) output node for the selected node (supports group nodes).
    """
    
    bl_idname = "affinity_bridge.setopenexr_selectednode"
    bl_label = "Set OpenEXR Output for Selected Node"    
    
    def add_output_node(self, overlap):
        # Method to add the output node
        # Check for overlap
        if overlap:
            try:
                scene = bpy.context.scene
                scene.node_tree.nodes['export_openexr_AB']
            except KeyError:
                pass
            else:
                # Remove the node
                node = scene.node_tree.nodes['export_openexr_AB']
                scene.node_tree.nodes.remove(node)
            finally:
                bpy.ops.node.add_node(use_transform=True, type="CompositorNodeOutputFile")
                output_node = bpy.context.scene.node_tree.nodes.active
                # Output node settings (ID, visual)
                output_node.name = "export_openexr_AB"
                output_node.label = "Export_OpenEXR(MultiLayer)"
                output_node.use_custom_color = True
                output_node.color = (0.6, 0.3, 0.5)
                # Output node settings (file settings)
                output_node.format.file_format = "OPEN_EXR_MULTILAYER"    

                add_node = scene.node_tree.nodes['export_openexr_AB']   
        else:
            bpy.ops.node.add_node(use_transform=True, type="CompositorNodeOutputFile")
            output_node = bpy.context.scene.node_tree.nodes.active
            # Output node settings (ID, visual)
            output_node.name = "export_openexr_selected_AB"
            output_node.label = "Export_OpenEXR(MultiLayer)"
            output_node.use_custom_color = True
            output_node.color = (0.6, 0.3, 0.5)
            # Output node settings (file settings)
            output_node.format.file_format = "OPEN_EXR_MULTILAYER"               

            add_node = bpy.context.scene.node_tree.nodes.active
                
        return add_node
    
    def setting_export_node(self, input_node):
        # Method to set up the output node based on the input node properties
        input_node_1 = input_node
        socket_counts = len(input_node_1.outputs)
        
        for num in range(socket_counts - 1):
            bpy.ops.node.output_file_add_socket()
            
        return socket_counts

    def connecting_nodes(self, count, output_node, input_node):
        # Method to connect input node and output node
        scene = bpy.context.scene
        node_tree = scene.node_tree
        socket_count = count
        export_node = output_node
        selected_node = input_node
        
        print(socket_count)
        for i in range(socket_count):
            node_tree.links.new(export_node.inputs[i],
                                selected_node.outputs[i])
        # Socket names cannot be changed (ReadOnly)
        
    def node_location(self, output_node, input_node):
        # Method to adjust the node positions
        export_node = output_node
        select_node = input_node
            
        x = select_node.location.x
        export_node.location.x = x + 300
            
        y = select_node.location.y
        export_node.location.y = y - 20        
        
    def execute(self, context):
        # Get the input node
        input_node = bpy.context.scene.node_tree.nodes.active
        # If the target node is a render layer, don't proceed
        if not input_node.type == "R_LAYERS":
            # Set up the output node        
            output_node = self.add_output_node(overlap=False)
            socket_count = self.setting_export_node(input_node)
            
            # Connect the nodes
            self.connecting_nodes(socket_count, output_node, input_node)

            # Adjust node positions
            self.node_location(output_node, input_node)
            self.report({'INFO'}, 'Success!: Set OpenEXR(MultiLayer)') 
        else:
            self.report({'ERROR'}, 'Cannot be used for Render Layers') 
        return {'FINISHED'}

class AFFINITYBRIDGE_OT_SetOpenEXR_RenderLayer(bpy.types.Operator):
    """
    Automatically sets up the OpenEXR (MultiLayer) output node connected to the active socket for the RenderLayer of the scene.
    """
    
    bl_idname = "affinity_bridge.setopenexr"
    bl_label = "Set OpenEXR Output for RenderLayer"
    
    def add_output_node(self):
        # Check for overlap
        try:
            scene = bpy.context.scene
            scene.node_tree.nodes['export_openexr_AB']
        except KeyError:
            pass
        else:
            # Remove the node
            node = scene.node_tree.nodes['export_openexr_AB']
            scene.node_tree.nodes.remove(node)
        finally:
            bpy.ops.node.add_node(use_transform=True, type="CompositorNodeOutputFile")
            output_node = bpy.context.scene.node_tree.nodes.active
            # Output node settings (ID, visual)
            output_node.name = "export_openexr_AB"
            output_node.label = "Export_OpenEXR(MultiLayer)"
            output_node.use_custom_color = True
            output_node.color = (0.6, 0.3, 0.5)
            # Output node settings (file settings)
            output_node.format.file_format = "OPEN_EXR_MULTILAYER"    
            
            return scene.node_tree.nodes['export_openexr_AB']

    def add_input_node(self):
        # Check for overlap
        try:
            scene = bpy.context.scene
            scene.node_tree.nodes['input_openexr_AB']
        except KeyError:
            pass
        else:
            # Remove the node
            node = scene.node_tree.nodes['input_openexr_AB']
            scene.node_tree.nodes.remove(node)
        finally:
            bpy.ops.node.add_node(use_transform=True, type="CompositorNodeRLayers")
            input_node = bpy.context.scene.node_tree.nodes.active
            # Input node settings (ID, visual)
            input_node.name = "input_openexr_AB"
            input_node.label = "Input_OpenEXR(MultiLayer)"
            input_node.use_custom_color = True
            input_node.color = (0.6, 0.3, 0.5)
            # Input node settings (file settings)   
            
            return scene.node_tree.nodes['input_openexr_AB']
    
    def get_render_pass_dict(self, output_node, input_node):
        scene = bpy.context.scene
        node_tree = scene.node_tree
        
        export_node = output_node
        render_layer = input_node
        
        output_sockets = len(render_layer.outputs)
        output_sockets_name = []
        output_sockets_enable = []
        output_sockets_dict = {}
        
        # Get all sockets of the node (including hidden ones)
        for i in range(output_sockets):
            names = render_layer.outputs[i].name
            output_sockets_name.append(names)
            
            enables = render_layer.outputs[i].enabled
            output_sockets_enable.append(enables)
        output_sockets_dict = dict(zip(output_sockets_name, output_sockets_enable))
        
        # Extract only the visible ones from

 all sockets of the node
        for name, enable in list(output_sockets_dict.items()):
            if enable == False:
                output_sockets_dict.pop(name)
        
        # Dictionary structure
        # {Socket name: True or False}
        # For RenderLayer, checking outputs refers to both visible and hidden sockets
        # So, all outputs are first referred to, and then a dictionary is created for only the valid nodes
        return output_sockets_dict
                    
    def setting_export_node(self, pathdata_dict):
        for i in range(len(pathdata_dict) - 1):
            bpy.ops.node.output_file_add_socket()
            
    def connecting_nodes(self, pathdata_dict, output_node, input_node):
        scene = bpy.context.scene
        node_tree = scene.node_tree
        
        export_node = output_node
        render_layer = input_node
        
        for i in range(len(pathdata_dict)):
            node_tree.links.new(export_node.inputs[i],
                                render_layer.outputs[i])
        # Socket names cannot be changed (ReadOnly)
        
    def node_location(self, output_node, input_node):
        export_node = output_node
        render_layer = input_node
        
        x = export_node.location.x
        render_layer.location.x = x - 300
        
    def execute(self, context):
        # Add and set up the output node
        input_node = self.add_input_node()      
        output_node = self.add_output_node()
        
        # Get output path information from the view layer
        pathdata_dict = self.get_render_pass_dict(output_node, input_node)
        
        # Apply path information to the nodes
        self.setting_export_node(pathdata_dict)
        
        # Connect the nodes
        self.connecting_nodes(pathdata_dict, output_node, input_node)
        
        # Adjust the node positions
        self.node_location(output_node, input_node)
        
        self.report({'INFO'}, 'Success!: Set OpenEXR(MultiLayer)') 
        return {'FINISHED'}
    
class AFFINITYBRIDGE_OT_Reload(bpy.types.Operator):
    """
    Reloads the image.
    (Please execute this after saving the image in the image editing software)
    """    
    bl_idname = "affinity_bridge.reload_affinity_photo"
    bl_label = "Reload in Affinity Photo"
    
    def execute(self, context):
        bpy.ops.image.reload()
        self.report({'INFO'}, 'Success!: Reloaded image!') 
        return {'FINISHED'}
    
class AFFINITYBRIDGE_OT_Photo(bpy.types.Operator):
    """
    Opens the image in Affinity Photo V2.
    * When AffinityBridge is disabled, the specified image editing software will be launched.
    """    
    bl_idname = "affinity_bridge.open_affinity_photo"
    bl_label = "Open in Affinity Photo V2"

    def convert_fileformat(self, file_format):
        
        file_format = 'EXR' if file_format == 'OPEN_EXR' else file_format
        file_format = 'EXR' if file_format == 'OPEN_EXR_MULTILAYER' else file_format
        
        return file_format

    def save_render_setting(self):
        img_stg = bpy.context.scene.render.image_settings
        old_ff = img_stg.file_format
        old_cc = img_stg.color_mode
        
        old_setting = [old_ff, old_cc]
        
        return old_setting

    def undo_render_setting(self, old_setting):
        img_stg = bpy.context.scene.render.image_settings    
        img_stg.file_format = old_setting[0]
        img_stg.color_mode = old_setting[1]
        
    def open_affinity_photo(self, file_path, is_ap, other_path):
        # Path to Affinity Photo
        if is_ap:
            users_path = os.path.expanduser('~')
            ap2_path = '\AppData\Local\Microsoft\WindowsApps\AffinityPhoto2.exe'
            affinity_photo2_path = users_path + ap2_path    
            
            subprocess.Popen([affinity_photo2_path, file_path], shell=True)
            
        else:
            subprocess.Popen([other_path, file_path], shell=True)
                    
        return 

    def execute(self, context):
        # Can only be used when there is only one IMAGE_EDITOR on the screen

        is_exist_filepath = True
        # True when the file path exists, False when it doesn't
    
        try:
            # Get the file path
            file_path = context.space_data.image.filepath_from_user(image_user=None)
            file_name = context.space_data.image.name
            
        except:
            # Exception handling
            self.report({'ERROR'}, 'No valid image selected') 
            
        else:
            # When the file path doesn't exist
            if file_path == '':
                is_exist_filepath = False
                bl_path = os.path.dirname(bpy.data.filepath)
                save_dir = bl_path + "\AffinityBridge"
            
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                    self.report({'INFO'}, 'Folder created:' + save_dir) 
                
            else:
                # When the file path exists
                is_exist_filepath = True
                save_dir = file_path
                    
            # Temporarily save rendering settings
            old_render_setting = self.save_render_setting()
            
            # Use only data with no existing file paths
            if not is_exist_filepath:
                # Overwrite rendering settings
                # file_mode, color_mode
                afy_brg = context.scene.affinitybridge
                context.scene.render.image_settings.file_format = afy_brg.file_format
                context.scene.render.image_settings.color_mode = afy_brg.color_mode
                
            else:
                pass
            
            # Convert to EXR
            file_format = self.convert_fileformat(context.scene.render.image_settings.file_format)
            
            # Save
            if not is_exist_filepath:
                        
                if context.scene.affinitybridge.is_change_name:
                    file_name_change = afy_brg.file_name
                    saved_path = save_dir + "\\" + file_name_change + '.' + file_format.lower()                            
                    
                else:
                    file_name_change = file_name
                    saved_path = save_dir + "\\" + file_name_change + '.' + file_format.lower()
                    
                    # Save the image
                    bpy.data.images[file_name].save_render(saved_path, scene=bpy.context.scene)

                    # Reload the saved image
                    bpy.ops.image.open(filepath=saved_path)
                    
            else:
                saved_path = file_path
                
            # Bridge to the image editing software
            is_ap = context.scene.affinitybridge.is_used_affinityphoto
            
            prefs = context.preferences.addons['Affinity_Bridge'].preferences
            other_file_path = prefs.option_image_editing_exe
            self.open_affinity_photo(saved_path, is_ap, other_file_path)
        
            # Display the file path in the UI
            context.scene.affinitybridge.path_str = saved_path
            
            # Restore rendering settings
            self.undo_render_setting(old_render_setting)
            
            self.report({'INFO'}, 'Success!:' + saved_path) 
    
        return {'FINISHED'}
