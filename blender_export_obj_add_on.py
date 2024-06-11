import bpy

class EXPORTOBJ_PT_main_panel(bpy.types.Panel):
    bl_label = "Export Objects Panel"
    bl_idname = "EXPORTOBJ_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ExportObj"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("exportobj.togglefaceorien_operator")
        
        
class EXPORTOBJ_OT_toggle_face_orien(bpy.types.Operator):
    bl_label = "Toggle Face Orientation"
    bl_idname = "exportobj.togglefaceorien_operator"
#    bl_space_type = "VIEW_3D"
#    bl_region_type = "UI"
#    bl_category = "ExportObj"
#    bl_parent_id = "ExportObjMainPanel"
#    
    def execute(self, context):
        layout = self.layout
        
#        # toggle show face orientation
        prev = bpy.context.space_data.overlay.show_face_orientation
        bpy.context.space_data.overlay.show_face_orientation = not prev
        
        return {'FINISHED'}
        
classes = [EXPORTOBJ_PT_main_panel, EXPORTOBJ_OT_toggle_face_orien]
        
def register():
#    bpy.utils.register_class(EXPORTOBJ_PT_main_panel)
#    bpy.utils.register_class(EXPORTOBJ_OT_calculate_normal)
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
#    bpy.utils.unregister_class(EXPORTOBJ_PT_main_panel)
#    bpy.utils.unregister_class(EXPORTOBJ_OT_calculate_normal)
     for cls in classes:
        bpy.utils.unregister_class(cls)
    
if __name__ == "__main__":
    register()
    