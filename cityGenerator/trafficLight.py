import maya.cmds as cmds
import random, math
import tools

'''
List of procedures in the module:

    def makeLightShaders(daytime):
        Creates shaders for traffic lights and street lights.
    def makeTrafficLight(glow):
        Creates a traffic light.
    def trafficLights(street,size,daytime):
        Creates traffic lights for the city.
    def placeTrafficLights(street,trafficLights, size):
        Creates instances of traffic lights and places them throughout the city.
    def makeStreetLight():
        Creates a street light.
    def placeStreetLight(blockList,daytime,lightGeom):
        Places street light instances on every block in the city.
    def placeLight(light, xz, daytime):
        Places a street light and if it is night creates and parents a spotlight to it.  
'''

def makeLightShaders(daytime):
    '''
    Creates shaders for traffic lights and street lights.
    
    daytime: Boolean variable which is true if it is day and false if it is night.
    On exit: Shaders for the traffic and street lights have been created, and
             appropriate names have been given to them.
    '''
    blackMetal = tools.makeShader((0.090, 0.090, 0.090), "blackMetal")
    cmds.setAttr("blackMetal.reflectivity", 0)
    green = tools.makeShader((0.0, 0.4, 0.0), "green")
    red = tools.makeShader((0.6, 0.0, 0.0), "red")
    yellow = tools.makeShader((0.6,0.6,0.0), "yellow")
    greenLight = tools.makeShader((0.0, 1.0, 0.0), "greenLight")
    redLight = tools.makeShader(( 1.0, 0.0, 0.0), "redLight")
    yellowLight = tools.makeShader((1.0,1.0,0.0), "yellowLight")
    whiteLight = tools.makeShader((0.474, 0.487, 0.334), "whiteLight")
    cmds.setAttr("whiteLight.reflectivity", 0)
    cmds.setAttr("green.reflectivity", 0)
    cmds.setAttr("red.reflectivity", 0)
    cmds.setAttr("yellow.reflectivity", 0)
    cmds.setAttr("greenLight.reflectivity", 0)
    cmds.setAttr("redLight.reflectivity", 0)
    cmds.setAttr("yellowLight.reflectivity", 0)
    if daytime == False:
        cmds.setAttr("whiteLight.incandescence", 0.4,0.4,0.4)
        cmds.setAttr("whiteLight.glowIntensity", 0.3)
        cmds.setAttr("greenLight.incandescence", 0.0,0.812,0.0)
        cmds.setAttr("greenLight.glowIntensity", 0.3)
        cmds.setAttr("redLight.incandescence", 1.0, 0.0, 0.0)
        cmds.setAttr("redLight.glowIntensity", 0.3)
        cmds.setAttr("yellowLight.incandescence", 0.725, 0.532, 0.0)
        cmds.setAttr("yellowLight.glowIntensity", 0.3)
    else:
        cmds.setAttr("whiteLight.transparency", 0.7,0.7,0.7)
        cmds.setAttr("greenLight.incandescence", 0.0,0.128,0.0)
        cmds.setAttr("greenLight.glowIntensity", 0.1)
        cmds.setAttr("redLight.incandescence", 1.0, 0.118, 0.118)
        cmds.setAttr("redLight.glowIntensity", 0.1)
        cmds.setAttr("yellowLight.incandescence", 0.12, 0.09, 0.0)
        cmds.setAttr("yellowLight.glowIntensity", 0.1)

def makeTrafficLight(glow):
    '''
    Creates a traffic light.
    
    glow: String that determines what colour should be glowing on the traffic
          light. Valid values are "R", "G", "Y" and "RY".
    On exit: A traffic light has been created and the right shaders have been
             assigned to it. The traffic light polygonal object is returned as a
             tuple containing the object name and node name.
    '''
    pole = cmds.polyCube(n = "pole", w = 0.1,d = 0.1, h = 2)
    cmds.xform(pole, translation = (0, 1, 0))
    cmds.sets(pole[0], edit=True, forceElement="blackMetalGroup")
    box = cmds.polyCube(n = "box", w = 0.3, d = 0.3, h = 0.7)
    cmds.xform(box, translation = (0, 2.35, 0))
    cmds.sets(box[0], edit=True, forceElement="blackMetalGroup")
    lights = cmds.polyCylinder(n = "light", r = 0.1, h = 0.2, sx = 12)
    cmds.xform(lights, rotation = (90, 0, 0))
    cmds.xform(lights, translation = (0, 2.575, 0.15), ws = True)
    cmds.polyChipOff(lights[0] + ".f[0:13]" , dup = True, kft = True, 
                             translate = (0, -0.225,0))
    cmds.polyChipOff(lights[0] + ".f[0:13]" , dup = True, kft = True, 
                             translate = (0, -0.45,0))
    if glow == "R" or glow == "RY":
        cmds.sets(lights[0] + ".f[0:13]", edit=True, forceElement="redLightGroup")
    else:
        cmds.sets(lights[0] + ".f[0:13]", edit=True, forceElement="redGroup")
    if glow == "Y" or glow == "RY":
        cmds.sets(lights[0] + ".f[14:27]", edit=True, forceElement="yellowLightGroup")
    else:
        cmds.sets(lights[0] + ".f[14:27]", edit=True, forceElement="yellowGroup")
    if glow == "G":
        cmds.sets(lights[0] + ".f[28:43]", edit=True, forceElement="greenLightGroup")
    else:
        cmds.sets(lights[0] + ".f[28:43]", edit=True, forceElement="greenGroup")
    trafficLight = cmds.polyBoolOp(box[0], lights[0], op = 2)
    trafficLight = cmds.polyUnite(trafficLight[0], pole[0], n = "trafficLight")
    cmds.delete(trafficLight[0], ch = True)
    return trafficLight
    
def trafficLights(street,size,daytime):
    '''
    Creates traffic lights for the city.
    
    street: An object of the class Street, which is the root node of the binary
            tree that makes up the street structure for the city.
    size: Tuple that contains the x- and z-components for the size of the city.
    daytime: Boolean variable which is true if it is day and false if it is night.
    On exit: Traffic lights polygonal objects of each type ("R", "G", "Y", "RY") have 
             been created using makeTrafficLight(...) and instances placed using 
             placeTrafficLights(...). 
              
    '''
    RedLightGeom = makeTrafficLight("R")
    RedYellowLightGeom = makeTrafficLight("RY")
    YellowLightGeom = makeTrafficLight("Y")
    GreenLightGeom = makeTrafficLight("G")
    cmds.group(RedLightGeom[0], RedYellowLightGeom[0], YellowLightGeom[0], GreenLightGeom[0], name = "trafficLights")
    placeTrafficLights(street, [RedLightGeom,RedYellowLightGeom,YellowLightGeom,GreenLightGeom], size)
    cmds.hide(RedLightGeom[0],RedYellowLightGeom[0],YellowLightGeom[0],GreenLightGeom[0])
        
def placeTrafficLights(street,trafficLights, size):
    '''
    Creates instances of traffic lights and places them throughout the city.
    
    street: An object of the class Street.
    trafficLights: A list containing four traffic light objects of different type.
    size: Tuple that contains the x- and z-components for the size of the city.
    On exit: Traffic light instances have been placed at the start point and end point 
             of the street, except if this is at the edge of the city. The procedure is
             recursively called in order to place traffic lights for every street in the
             binary tree that makes up the street structure for the city. 
    '''
    #randomly pick which geometries should be instanced.
    num1 = random.random()
    if num1 > 0.6:
        geom1 = trafficLights[0]
    elif num1 > 0.2:
        geom1 = trafficLights[3]
    elif num1 > 0.1:
        geom1 = trafficLights[2]
    else:
        geom1 = trafficLights[1]
    num2 = random.random()
    if num2 > 0.6:
        geom2 = trafficLights[0]
    elif num2 > 0.2:
        geom2 = trafficLights[3]
    elif num2 > 0.1:
        geom2 = trafficLights[2]
    else:
        geom2 = trafficLights[1]
    if street.split[0] == "horisontal":
        if street.start[0] != -size[0]/2.0:            
            light1 = cmds.instance(geom1[0])
            light2 = cmds.instance(geom1[0])
            cmds.xform(light1, rotation = (0,90,0), translation = (street.start[0]+3, 0, street.start[1] + 2.2))
            cmds.xform(light2, rotation = (0,90,0), translation = (street.start[0]+3, 0, street.start[1] - 2.2))
        if street.end[0] != size[0]/2.0:
            light1 = cmds.instance(geom2[0])
            light2 = cmds.instance(geom2[0])
            cmds.xform(light1, rotation = (0,-90,0), translation = (street.end[0]-3, 0, street.end[1] + 2.2))
            cmds.xform(light2, rotation = (0,-90,0), translation = (street.end[0]-3, 0, street.end[1] - 2.2))
    else:
        if street.start[1] != -size[1]/2.0:
            light1 = cmds.instance(geom1[0])
            light2 = cmds.instance(geom1[0])
            cmds.xform(light1, translation = (street.start[0] + 2.2, 0, street.start[1] + 3))
            cmds.xform(light2, translation = (street.start[0] - 2.2, 0, street.start[1] + 3))
        if street.end[1] != size[1]/2.0:
            light1 = cmds.instance(geom2[0])
            light2 = cmds.instance(geom2[0])
            cmds.xform(light1, rotation = (0,180,0), translation = (street.end[0] + 2.2, 0, street.end[1] - 3))
            cmds.xform(light2, rotation = (0,180,0), translation = (street.end[0] - 2.2, 0, street.end[1] - 3))
    if street.smaller != None:
        placeTrafficLights(street.smaller, trafficLights, size)
    if street.larger != None:
        placeTrafficLights(street.larger, trafficLights, size)
        
def makeStreetLight():
    '''
    Creates a street light.
    
    On exit: A street light polygonal object has been created and appropriate 
             shaders have been assigned. The street light object is returned.
    '''
    streetLight = cmds.polyCube(name = "streetLight", w = 0.1, d = 0.1, h = 2.4)
    cmds.xform(streetLight, translation = (0, 1.2, 0))
    cmds.select(streetLight[0] + ".f[1]")
    cmds.polyExtrudeFacet(scale = (1.7,1.7,1.7))
    cmds.polyExtrudeFacet(scale = (2.2,2.2,2.2), translate = (0,0.2,0))
    cmds.polyExtrudeFacet(scale = (0.8,0.8,0.8), translate = (0,0.1,0))
    cmds.polyExtrudeFacet(scale = (0.6,0.6,0.6))
    cmds.polyExtrudeFacet(scale = (0.8,0.8,0.8), translate = (0,0.08,0))
    cmds.polyExtrudeFacet(scale = (0.6,0.6,0.6))
    cmds.polyExtrudeFacet(scale = (0.7,0.7,0.7), translate = (0,0.08,0))
    cmds.polyExtrudeFacet(scale = (0.5,0.5,0.5))
    cmds.polyExtrudeFacet(scale = (0.2,0.2,0.2), translate = (0,0.7,0))
    hole = cmds.polyCube(name = "hole", w = 0.16, d = 0.3, h = 0.22)
    cmds.select(hole[0] + ".f[1]")
    cmds.scale(1.9,1.9,1.9)
    cmds.xform(hole, translation = (0,2.59,0))
    hole2 = cmds.duplicate(hole[0])
    cmds.rotate(0,90,0, hole2[0])
    streetLight = cmds.polyBoolOp((streetLight[0],hole[0]),op = 2)
    streetLight = cmds.polyBoolOp((streetLight[0],hole2[0]),op = 2)
    cmds.sets(streetLight[0], edit=True, forceElement="blackMetalGroup")
    light = cmds.polyCube(name = "hole", w = 0.16, d = 0.16, h = 0.22)
    cmds.select(light[0] + ".f[1]")
    cmds.scale(1.9,1.9,1.9)
    cmds.xform(light, translation = (0,2.59,0))
    cmds.select(light)
    cmds.sets(light[0], edit=True, forceElement="whiteLightGroup")
    streetLight = cmds.polyUnite(light,streetLight)
    cmds.delete(streetLight, ch = True)
    cmds.group(streetLight[0], n = "streetLights")
    return streetLight
    
def placeStreetLight(blockList,daytime,lightGeom):
    '''
    Places street light instances on every block in the city.
    
    blockList: A list containing all the objects of the class Block.
    daytime: Boolean variable which is true if it is day and false if it is night.
    lightGeom: Tuple containing the object name and node name for a polygonal object,
               in this case a street light.
    On exit: The polygonal object (lightGeom) has been instanced and placed around
             every block in blockList using placeLight(...). 
    '''
    for i in blockList:
        widthNumber = int(i.width / 5.0 - 1) #number of objects placed along the width of the block
        widthDistance = i.width / (widthNumber + 1) #distance between every object
        depthNumber = int(i.depth / 5.0 - 1) #number of objects placed along the depth of the block
        depthDistance = i.depth / (depthNumber + 1) #distance between every object
        for j in range(widthNumber):
            light1 = cmds.instance(lightGeom[0])
            light2 = cmds.instance(lightGeom[0])
            placeLight(light1,(i.center[0] - i.width/2.0 + (j+1) * widthDistance, i.center[1] - i.depth/2.0 + 0.2), daytime)
            placeLight(light2,(i.center[0] - i.width/2.0 + (j+1) * widthDistance, i.center[1] + i.depth/2.0 - 0.2), daytime)
        for j in range(depthNumber):
            light1 = cmds.instance(lightGeom[0])
            light2 = cmds.instance(lightGeom[0])
            placeLight(light1, (i.center[0] - i.width/2.0 + 0.2, i.center[1] - i.depth/2.0 + (j+1) * depthDistance), daytime)
            placeLight(light2, (i.center[0] + i.width/2.0 - 0.2, i.center[1] - i.depth/2.0 + (j+1) * depthDistance), daytime)

def placeLight(light, xz, daytime):
    '''
    Places a street light and if it is night creates and parents a spotlight to it.
    
    light: object that is to be placed.
    xz: Tuple containing the x- and z-coordinates the object will be placed at.
    daytime: Boolean variable which is true if it is day and false if it is night.
    On exit: The object has been placed in the right position and if daytime is false,
             a spotlight has been positioned and parented to the object.
    '''
    cmds.xform(light, translation = (xz[0], 0, xz[1]))
    if daytime == False:
        spotLight = cmds.spotLight(intensity = 0.672, coneAngle = 125, penumbra = 10, dropOff = 4.286)
        cmds.move(xz[0], 2.6, xz[1])
        cmds.rotate(-90, x = True)
        cmds.parent("spotLight" + spotLight[14:], light)
        
