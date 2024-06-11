import bpy

class EXPORTOBJ_PT_main_panel(bpy.types.Panel):
    bl_label = "Export Objects Panel"
    bl_idname = "EXPORTOBJ_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ExportObj"
    
    def draw(self, context):
        layout = self.layonut
        
def register():
    bpy.utils.register_class(EXPORTOBJ_PT_main_panel)
    
def unregister():
    bpy.utils.unregister_class(EXPORTOBJ_PT_main_panel)
    
if __name__ == "__main__":
    register()
    