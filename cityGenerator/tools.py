import maya.cmds as cmds
import random, math

'''
List of procedures in the module:

    def convertToRgb(colour):
        Converts hue, saturation and brightness of a colour to corresponding RGB value.
    def getRandomValue(range):
        Picks a random value between a start point and endpoint, wrapping back to 0 
        when reaching 1.
    def makeShader(colour, materialName = "material", type = "blinn"):
        Creates a shader of the specified type and colour.
'''

def convertToRgb(colour):
    '''
    Converts hue, saturation and brightness of a colour to corresponding RGB value.
    
    colour: A triple with the hsv values where hue is given as a value between 0 and 360.
    On exit: Returns a triple with the RGB value corresponding to the given hsv value.
    '''
    chroma = colour[1] * colour[2]
    h = colour[0] / 60.0
    x = chroma * (1 - abs(h % 2 - 1))
    if 0 <= h < 1:
        point = (chroma, x, 0)
    elif 1 <= h <2:
        point = (x, chroma, 0)
    elif 2 <= h < 3:
        point = (0, chroma, x)
    elif 3 <= h < 4:
        point = (0, x, chroma)
    elif 4 <= h < 5:
        point = (x, 0, chroma)
    else:
        point = (chroma, 0, x)
    RGB = (point[0] + colour[2] - chroma, point[1] + colour[2] - chroma, point[2] + colour[2] - chroma)
    return RGB
    
def getRandomValue(range):
    '''
    Picks a random value between a start point and endpoint, wrapping back to 0 
    when reaching 1.
    
    range: A tuple defining the range from which the value will be picked.
    On exit: A random value between 0 and 1 has been picked so that the
             following is true: 
             range[0] <=  range[1] --> range[0] <= value <= range[1]
             range[1] < range[0] --> (value > range[0] or value < range[1])
             The random value is returned.
    '''
    if range[0] <= range[1]:
        randomValue = random.uniform(range[0],range[1])
    else:
        randomValue = random.uniform(range[0],1 + range[1])
        if randomValue > 1:
             randomValue = randomValue - 1
    return randomValue

def makeShader(colour, materialName = "material", type = "blinn"):
    '''
    Creates a shader of the specified type and colour.
    
    colour: A triple with values between 0 and 1, that define the rgb value for a colour.
    materialName: The name the material will be given.
    type: A string that specifies the type of the shader.
    On exit: A shader and shading group has been created and the specified 
             colour has been set for the shader. A tuple with the name of the material 
             and the name of the shading group is returned.
    '''
    shadingGroup = cmds.sets(name = materialName + "Group", renderable=True, empty=True)
    shader = cmds.shadingNode(type, asShader=True)
    cmds.setAttr(shader + ".color", colour[0], colour[1], colour[2])
    cmds.surfaceShaderList(shader, add=shadingGroup)
    shader = cmds.rename(shader, materialName)
    return (shader, shadingGroup)