import bpy

class ExportProperties(bpy.types.PropertyGroup):
    filePath: bpy.props.StringProperty(default="")
    fileName: bpy.props.StringProperty(default="untitled")
    checkExisting: bpy.props.BoolProperty(default=True)
    selectObjOnly: bpy.props.BoolProperty(default=True)
    axisForward: bpy.props.EnumProperty(default="Y", items=[('X', "X", ""),
                                               ('Y', "Y", ""),
                                               ('Z', "Z", ""),
                                               ('-X', "-X", ""),
                                               ('-Y', "-Y", ""),
                                               ('-Z', "-Z", "")])
    axisUp: bpy.props.EnumProperty(default="Z", items=[('X', "X", ""),
                                               ('Y', "Y", ""),
                                               ('Z', "Z", ""),
                                               ('-X', "-X", ""),
                                               ('-Y', "-Y", ""),
                                               ('-Z', "-Z", "")])
                                               

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
        
        row = layout.row()
        
        export_property = context.scene.export_property
        layout.prop(export_property, "filePath")
        layout.prop(export_property, "checkExisting")
        layout.prop(export_property, "selectObjOnly")
        layout.prop(export_property, "axisForward")
        layout.prop(export_property, "axisUp")
        
        row = layout.row()
        
        row.operator("exportobj.exportasfbx_operator")
        
        
class EXPORTOBJ_OT_toggle_face_orien(bpy.types.Operator):
    bl_label = "Toggle Face Orientation"
    bl_idname = "exportobj.togglefaceorien_operator"
  
    def execute(self, context):
        # toggle show face orientation
        prevVal = bpy.context.space_data.overlay.show_face_orientation
        bpy.context.space_data.overlay.show_face_orientation = not prevVal
        
        return {'FINISHED'}

class EXPORTOBJ_OT_export_as_fbx(bpy.types.Operator):
    bl_label = "Export As FBX"
    bl_idname = "exportobj.exportasfbx_operator"
    
    def execute(self, context):
        export_property = context.scene.export_property
#        filePath = export_property.filePath + export_property.fileName + ".fbx"
        bpy.ops.export_scene.fbx(filepath=export_property.filePath,
                                 check_existing=export_property.checkExisting,
                                 use_selection=export_property.selectObjOnly,
                                 axis_forward=export_property.axisForward,
                                 axis_up=export_property.axisUp,
                                 path_mode='AUTO'
                                 )
        return {'FINISHED'}
    
        
classes = [EXPORTOBJ_PT_main_panel, EXPORTOBJ_OT_toggle_face_orien, ExportProperties, EXPORTOBJ_OT_export_as_fbx]
        
def register():
#    bpy.utils.register_class(EXPORTOBJ_PT_main_panel)
#    bpy.utils.register_class(EXPORTOBJ_OT_calculate_normal)
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.export_property = bpy.props.PointerProperty(type=ExportProperties) 


def unregister():
#    bpy.utils.unregister_class(EXPORTOBJ_PT_main_panel)
#    bpy.utils.unregister_class(EXPORTOBJ_OT_calculate_normal)

    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.export_property
        
if __name__ == "__main__":
    register()
    