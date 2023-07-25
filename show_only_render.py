import bpy
from bpy.app.handlers import persistent

bl_info = {
    'name': "Show Only Render",
    'description': "Toggle to show only rendered objects in the 3D Viewport.",
    'author': "Artell & Gatada",
    "version": (1, 12, 3),
    'blender': (2, 80, 0),
    'location': "3D Viewport > Sidebar (N) > View",
    'wiki_url': "",
    'category': "3D View",
    }


class OBJECT_OT_toggle_disable_in_viewport(bpy.types.Operator):
    bl_idname = "object.toggle_disable_in_viewport"
    bl_label = "Refresh Visibility"
    
    def execute(self, context):
        if context.scene.sor_show_only_render:
            for obj in bpy.context.scene.objects:
                obj.hide_set(obj.hide_render)
        return {'FINISHED'}
        

class SOR_PT_menu(bpy.types.Panel):
    bl_label = "Hide Disabled"
    # bl_options = set({'HIDE_HEADER'})
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'
    bl_category = "View"    

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context):
        layout = self.layout        
        layout.prop(context.scene, "sor_show_only_render", text="Show Only Render")
        
        # Add a box around the options
        box = layout.box()
        box.enabled = context.scene.sor_show_only_render
        
        row = box.row()
        #row.enabled = context.scene.sor_show_only_render
        row.operator("object.toggle_disable_in_viewport")
        
        row = box.row()
        #row.enabled = context.scene.sor_show_only_render
        row.prop(bpy.context.scene, "sor_refresh_with_frame", text="Refresh on Frame Change")


def update_show_only_render(self, context):
    if context.scene.sor_show_only_render:
        for obj in context.scene.objects:
            obj.hide_set(obj.hide_render)
    else:
        for obj in context.scene.objects:
            obj.hide_set(False)



classes = (
    SOR_PT_menu,
    OBJECT_OT_toggle_disable_in_viewport,
    )


@persistent
def frame_change_handler(self, context):
    # print("Frame changed:", context.scene.frame_current)
    if context.scene.sor_refresh_with_frame:
        # Call the update_show_only_render method with the current scene context
        update_show_only_render(self, bpy.context)
    
    
def register():   
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)
    
    bpy.types.Scene.sor_show_only_render = bpy.props.BoolProperty(name="Show Only Render", default = False, description="Show only renderable objects", update=update_show_only_render)
    
    bpy.types.Scene.sor_refresh_with_frame = bpy.props.BoolProperty(name="Refresh on Frame change", default = True, description="Refresh visibility when frame changes", update=frame_change_handler)
    
    bpy.app.handlers.frame_change_post.append(frame_change_handler)

    
def unregister():   
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
        
    bpy.app.handlers.frame_change_post.remove(frame_change_handler)
    
    del bpy.types.Scene.sor_show_only_render
    del bpy.types.Scene.sor_refresh_with_frame
