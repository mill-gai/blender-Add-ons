import bpy
from random import randint, uniform
from math import radians    

def generateCubes(number, location, material):
    for i in range(number):
        bpy.ops.mesh.primitive_cube_add(location=(uniform(-location, location), uniform(-location, location), uniform(-location, location)), scale=(uniform(0.01, 0.2), uniform(0.01, 0.2), uniform(0.01, 0.2)))
        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].segments = randint(1, 4)
        bpy.context.object.modifiers["Bevel"].width = uniform(0.005, 0.1)
        bpy.context.object.active_material = materin
   
    
def generateColor(color, hasRandomHue, hasRandomSaturation):
    new_material = bpy.data.materials.new(name="Color")
    new_material.use_nodes = True
    
    principled_node = new_material.node_tree.nodes.get('Principled BSDF')
    
    # add hue/saturation node
    hueSaturation_node = new_material.node_tree.nodes.new('ShaderNodeHueSaturation')
    hueSaturation_node.location = (-200,0) 
    hueSaturation_node.inputs[4].default_value = color
    
    # add object info node
    objectInfo_node = new_material.node_tree.nodes.new('ShaderNodeObjectInfo')
    objectInfo_node.location = (-450, 0)
    
    link = new_material.node_tree.links.new
    # connect output of the node to the input base color of Principled BSDF
    link(hueSaturation_node.outputs[0], principled_node.inputs[0])
    if(hasRandomHue):
        link(objectInfo_node.outputs[4], hueSaturation_node.inputs[0])
    if(hasRandomSaturation):
        link(objectInfo_node.outputs[4], hueSaturation_node.inputs[1])
    
    return new_material


def GlassMaterial(input_material):
    principled_node = input_material.node_tree.nodes.get('Principled BSDF')
    # roughness
    principled_node.inputs[9].default_value = 0
    # transmission
    principled_node.inputs[17].default_value = 1
    
def MetalMaterial(input_material):
    principled_node = input_material.node_tree.nodes.get('Principled BSDF')
    # roughness
    principled_node.inputs[9].default_value = 0
    # metallic
    principled_node.inputs[6].default_value = 1
   
# ========================================================================================
 
class CubeProperties(bpy.types.PropertyGroup):
    color : bpy.props.FloatVectorProperty(name="Color", subtype='COLOR_GAMMA',size=4, default=(0.6,1,0.9,1))
    number : bpy.props.IntProperty(name="Number of cube", soft_min=1, soft_max=50, default=10)
    locationRadius : bpy.props.FloatProperty(name="Range of cube", soft_min=0.5, soft_max=5, default=0.5)
    randomHue : bpy.props.BoolProperty(name="RandomHue")
    randomSaturation: bpy.props.BoolProperty(name="RandomSaturation")
    texture : bpy.props.EnumProperty(
        name="Material Option",
        description="description",
        items=[ ('default_material', "Default", ""),
                ('glass_material', "Glass", ""),
                ('metal_material', "Metal", "")
        ]
    )
    
    
class COLORFULCUBES_PT_main_panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Colorful Cubes Panel"
    bl_idname = "COLORFULCUBES_PT_main_panel"
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "ColorfulCubes"

    def draw(self, context):
        layout = self.layout
        
        # access CubeProperties
        scene = context.scene
        cube_property = scene.cube_property 
        
        layout.prop(cube_property, "color")
        layout.prop(cube_property, "number")
        layout.prop(cube_property, "locationRadius")
        layout.prop(cube_property, "randomHue")
        layout.prop(cube_property, "randomSaturation")
        layout.prop(cube_property, "texture")
        
        row = layout.row()
        row.operator("colorfulcubes.generatecube_operator")

class COLORFULCUBES_OT_generate_cube(bpy.types.Operator):
    bl_label = "Generate Cubes"    
    bl_idname = "colorfulcubes.generatecube_operator"  
    
    def execute(self, context):  
        # access Cube Properties
        scene = context.scene
        cube_property = scene.cube_property 
        material = generateColor(cube_property.color, cube_property.randomHue, cube_property.randomSaturation)
        if(cube_property.texture == 'glass_material'):
            GlassMaterial(material)
        elif(cube_property.texture == 'metal_material'):
            MetalMaterial(material)
        
        location = cube_property.locationRadius
        
        # generate cubes
        for i in range(cube_property.number):
            bpy.ops.mesh.primitive_cube_add(location=(uniform(-location, location), uniform(-location, location), uniform(-location, location)), scale=(uniform(0.01, 0.2), uniform(0.01, 0.2), uniform(0.01, 0.2)))
            
            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.context.object.modifiers["Bevel"].segments = randint(1, 4)
            bpy.context.object.modifiers["Bevel"].width = uniform(0.005, 0.1)
            bpy.context.object.active_material = material
            

        return {'FINISHED'}

        

classes = [CubeProperties, COLORFULCUBES_PT_main_panel, COLORFULCUBES_OT_generate_cube]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.cube_property = bpy.props.PointerProperty(type=CubeProperties) 


def unregister():
     for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.cube_property


if __name__ == "__main__":
    register()
