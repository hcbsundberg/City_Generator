import maya.cmds as cmds
import random, math
import streets
import trafficLight
import park
import tools

'''
List of procedures in the module:
    class House:
        A House object represents a house in the city.
        def __init__(self, name_, type, height, width, depth):
            Initializes a House object with the given parameters.
        def addDeformer(self):
            Adds one or two deformers to a house.
        def moveHouse(self, newCoor):
            Moves house to new Coordinates.
        def makeWindows(self, name_, windowShaders, booleans):
            Creates windows for a cylinder or pipe house. 
    class BoxHouse(House):
        Subclass of the class House, which represents houses based on the polygon 
        primitive box.
        def __init__(self, name_, height, width, depth, shader):
            Initializes a BoxHouse object, and creates a polygonal house object based on a
            box primitive.
        def makeWindows(self, name_, windowShaders, booleans):
            Creates windows for a box house.
    class CylinderHouse(House):
        Subclass of the class House, which represents houses based on the polygon 
        primitive cylinder.
        def __init__(self, name_, height, radius, sides, shader):
            Initializes a CylinderHouse object, and creates a polygonal house object based on a
            cylinder primitive.
    class PipeHouse(House):
        Subclass of the class House, which represents houses based on the polygon 
        primitive pipe.
        def __init__(self, name_, height, radius, sides, thickness, shader):
            Initializes a PipeHouse object, and creates a polygonal house object based on a
            pipe primitive.
        def addDeformer(self):
            Adds one or two deformers to a pipe house.
    class Block:
        A Block object repesents a block in the city.
        def __init__(self, width, depth, center):
            Initializes a Block object and creates a pavement on the block.
    def makeWindowColumn(windowWidth, windowHeight, num, floorHeight):
        Creates a column with the specified number of windows.
    def assignWindowShaders(window, windowNum, shaders):
        Assigns shaders to all the windows for a house.
    def makeHouseShaders(num, colourRange):
        Creates a number of shaders for houses.
    def makeNecessaryShaders(daytime):
        Creates shaders that are needed for the city.
    def makeWindowShaders(daytime, glow, environment):
        Creates shaders for windows.
    def makeLights(daytime, name_):
        Creates lights for the city.
    def makeCamera(name_, environment):
        Creates a camera with the given background colour. 
    def makeZoneHeihgts(size, houseHeightInt):
        Creates a list of six different height ranges for the houses in the city.
    def makeHouse(name_, heightInt, wxd, houseShaders, treeShaders, windowShaders, windows, booleans, deformer):
        Creates a house.
    def city(name_, size, houseHeightInt, houseWidthInt, windows, booleans, deformers, daytime, glow, environment, colourRange):
        Generates the city.       
'''

class House:
    '''
    A House object represents a house in the city. This class is used solely as a
    superclass for its subclasses BoxHouse, CylinderHouse or PipeHouse. No 
    objects of this class are ever created. 
    
    Attributes:
        name: String with the name of the polygon object owned by the House object.
        type: String with the type of the house ("box", "cylinder" or "pipe").
        height: The height of the house.
        width: The width of the house.
        depth: The depth of the house.
        flare: If a flare deformer has been added to the house this is a tuple containing the 
               deformer driver name and the deformer handle transform name.
        twist: If a twist deformer has been added to the house this is a tuple containing the 
               deformer driver name and the deformer handle transform name.
    '''
    def __init__(self, name_, type, height, width, depth):
        '''
        Initializes a House object with the given parameters.
        
        self: Object that is to be initialized.
        name_: See Attributes.
        type: See Attributes.
        height: See Attributes.
        width: See Attributes.
        depth: See Attributes.
        On exit: A house object has been initialized. Note that the attributes
                 flare and twist are initialized as None.
        '''
        self.name = name_
        self.type = type
        self.height = height
        self.width = width
        self.depth = depth
        self.flare = None
        self.twist = None
        
    def addDeformer(self):
        '''
        Adds one or two deformers to a house.
        
        self : Object of the class House.       
        On exit : A flare deformer has been added to the object house.name. 
        A twist deformer is occasionally added on top of that. 
        Some of the deformers' attributes have been randomly set.
        '''
        cmds.select(self.name)
        self.flare = cmds.nonLinear(type = "flare")
        moveFlare = random.choice(["Yes", "No"])
        if (moveFlare == "Yes"): 
            cmds.xform(self.flare, translation = (0, random.uniform(self.height / 2.0, self.height + self.height / 4.0), 0))
        endFlare = random.uniform(0.3, 1.5)
        cmds.setAttr(self.flare[0] + ".endFlareX", endFlare)
        cmds.setAttr(self.flare[0] + ".endFlareZ", endFlare)
        cmds.setAttr(self.flare[0] + ".curve", random.uniform(-0.4, min((self.height/min(self.width, self.depth)) * 0.3, 0.9)))
        cmds.xform(self.flare, scale = (0,self.height / 2, 0))
        twist = random.randint(0, 6)
        if (twist == 0):
            if not(self.type == "box" and (self.width/self.depth > 1.5 or self.depth/self.width > 1.5)):
                cmds.select(self.name)
                self.twist = cmds.nonLinear(type = "twist")
                cmds.setAttr(self.twist[0] + ".endAngle", random.randint(-90, 90))
                cmds.xform(self.twist, scale = (0,self.height / 2, 0))
            
    def moveHouse(self, newCoor):
        '''
        Moves house to new Coordinates.
        
        self: Object of the class House.
        newCoor: coordinates to which the house will be moved    
        On exit: The house along with it's deformers has been moved
        to the new coordinates. 
        '''
        cmds.select(self.name)
        cmds.move(newCoor[0],newCoor[1], x = True, z = True)
        if (self.flare != None):
            cmds.select(self.flare)
            cmds.move(newCoor[0], newCoor[1], x = True, z = True)
        if (self.twist != None):
            cmds.select(self.twist)
            cmds.move(newCoor[0], newCoor[1], x = True, z = True)
        
    def makeWindows(self, name_, windowShaders, booleans):
        '''
        Creates windows for a cylinder or pipe house. 
        
        self: Object of the class House.
        name_: A string with the name the polygonal house object will have.
        windowShader: A list with shaders for the windows.
        booleans: A boolean variable which determines whether the windows should be 
                  combined with the house using boolean difference or not. 
        On exit: Columns of windows are created using makeWindowColumn(...) and these
                 are then duplicated around the house. The windows are assigned shaders
                 using assignWindowShaders(...), and are then combined with the 
                 house. The House object's name attribute is updated.        
        '''
        windowHeight = random.uniform(0.5,1.9)
        # Make sure the window height is not too close to 1.6 since the window edge
        # in that case will be too close to a edge loop on the house and the boolean
        # operation will fail.
        if booleans and (windowHeight > 1.59 and windowHeight < 1.61):
            windowHeight = random.choice([1.59, 1.61])
        floorHeight = int(math.ceil(windowHeight))
        heightNum = int((self.height - (1 + floorHeight/2.0))/floorHeight)
        if heightNum == 0:
            return
        angleR = 2.0 * math.pi / self.sides
        angleD = math.degrees(angleR)
        distance = math.cos(angleR / 2.0) * self.radius
        sideWidth = 2.0 * self.radius * math.sin(angleR / 2.0)
        windowWidth = random.uniform((sideWidth -0.2)/ 2.0, sideWidth - 0.2)
        if windowWidth <= 0.1:
            return
        windowColumn = makeWindowColumn(windowWidth, windowHeight, heightNum, floorHeight)
        cmds.rotate(90 - angleD / 2.0, windowColumn[0], y = True)
        for j in range(self.sides): # Copy the column faces around the house. 
            cmds.polyChipOff(windowColumn[0] + ".f[0:" + str((heightNum * 6) - 1) + "]", dup = True, kft = True, 
                             translate = (math.sin(math.pi/2.0 - angleR/2.0 + angleR * j) * distance,0,math.cos(math.pi/2.0 - angleR/2.0 + angleR * j) *  distance))
            cmds.select(windowColumn[0] + ".f[0:" + str((heightNum * 6) - 1) + "]")
            cmds.rotate(angleD, y = True)
            cmds.delete(all = True, ch = True)
            cmds.refresh()
        cmds.delete(windowColumn[0] + ".f[0:" + str((heightNum * 6) - 1) + "]")
        windowNum = self.sides * heightNum
        assignWindowShaders(windowColumn, windowNum, windowShaders)
        cmds.select(windowColumn[0] + ".f[0:" + str(windowNum * 6 - 1) +"]")
        cmds.polySubdivideFacet()
        if booleans == True:
            result = cmds.polyBoolOp(self.name,windowColumn[0], op = 2, n = name_)
        else:
            result = cmds.polyUnite(self.name,windowColumn[0], n = name_)
        self.name = result[0]
        cmds.delete(all = True, ch = True)
        
class BoxHouse(House):
    '''
    Subclass of the class House, which represents houses based on the polygon 
    primitive box.
    
    Attributes: 
        Same as for a House object.
    '''
    def __init__(self, name_, height, width, depth, shader):
        '''
        Initializes a BoxHouse object, and creates a polygonal house object based on a
        box primitive.
        
        self: Object that is to be initialized.
        name_: name_: A string with the name the polygonal house object will have.
        height: The height of the house.
        width: The width of the house.
        depth: The depth of the house.
        shader: Shader that will be assigned to the house. 
        On exit: A BoxHouse object has been initialized and a polygonal house has 
                 been created out of a box primitive. A foundation for the house has
                 also been created and united with the box. The given shader has been 
                 assigned to the house. 
        '''
        House.__init__(self, name_, "box", height, width, depth)
        n = cmds.polyCube(n = "house_", w = width, h = height, d = depth, sy = height)
        cmds.xform(n[0], translation = (0, height/2.0, 0))
        f = cmds.polyCube(n = "foundation", w = width + 0.3, h = 0.8, d = depth + 0.3)
        cmds.xform(f[0], translation = (0,0.4,0))
        n = cmds.polyUnite(n[0],f[0], n = name_)
        self.name = n[0]
        cmds.sets(n[0], edit=True, forceElement= shader[1])
        cmds.delete(self.name, ch = True)
  
    def makeWindows(self, name_, windowShaders, booleans):
        '''
        Creates windows for a box house. 
        
        self: Object of the class BoxHouse.
        name_: A string with the name the house will have.
        windowShader: A list with shaders for the windows.
        booleans: A boolean variable which determines whether the windows should be 
                  combined with the house using boolean difference or not. 
        On exit: Columns of windows are created using makeWindowColumn(...) and these
                 are then duplicated around the house. The windows are assigned shaders
                 using assignWindowShaders(...), and are then combined with the 
                 house. The House object's name attribute is updated.        
        '''
        windowHeight = random.uniform(0.5,1.9)
        # Make sure the window height is not too close to 1.6 since the window edge
        # in that case will be too close to a edge loop on the house and the boolean
        # operation will fail.
        if booleans and (windowHeight > 1.59 and windowHeight < 1.61):
            windowHeight = random.choice([1.59, 1.61])
        windowWidth = random.uniform(1, 3)
        floorHeight = int(math.ceil(windowHeight))
        heightNum = max(0,int((self.height - (1 + floorHeight/2.0))/floorHeight))
        if heightNum == 0:
            return
        widthNum = max(0,int((self.width - 0.3) / (windowWidth)))
        if (widthNum != 0):
            # Makes it possible for houses to have less windows or no windows on a side.
            widthNum = widthNum - random.randint(0, min(2, widthNum)) 
        # Space between window columns along the width of the house.
        widthSpace = (self.width - (widthNum * windowWidth)) /(widthNum + 1) 
        depthNum = max(0,int((self.depth - 0.3)/ windowWidth))
        if (depthNum != 0):
            # Makes it possible for houses to have less windows or no windows on a side.
            depthNum = depthNum - random.randint(0, min(2, depthNum))
        if (depthNum == 0) and (widthNum == 0):
            return
        # Space between window columns along the width of the house.
        depthSpace = (self.depth - (depthNum * windowWidth)) / (depthNum + 1)
        windowColumn = makeWindowColumn(windowWidth,windowHeight, heightNum, floorHeight)
        for j in range(widthNum):
            # Duplicates all the faces of the first window column and translates the duplicates along the width.
            cmds.polyChipOff(windowColumn[0] + ".f[0:" + str((heightNum * 6) - 1) + "]", dup = True, kft = True, 
                             translate = (-self.width/2.0 + windowWidth/2.0 + widthSpace + (windowWidth + widthSpace) * j,
                             0, self.depth/2.0))
            cmds.polyChipOff(windowColumn[0] + ".f[0:" + str((heightNum * 6) - 1) + "]", dup = True, kft = True, 
                             translate =  (-self.width/2.0 + windowWidth/2.0 + widthSpace + (windowWidth + widthSpace) * j, 
                             0, -self.depth/2.0))       
            cmds.delete(all = True, ch = True)   
            cmds.refresh()
        cmds.select(windowColumn[0] + ".f[0:" + str((heightNum * 6) - 1) + "]")
        cmds.rotate(90, y = True)
        for j in range(depthNum):
            # Duplicates all the faces of the first window column and translates the duplicates along the depth.
            cmds.polyChipOff(windowColumn[0] + ".f[0:" + str((heightNum * 6) - 1) + "]", dup = True, kft = True,
                             translate = (self.width/2.0, 0, -self.depth/2.0 + windowWidth/2.0 + depthSpace + (windowWidth + depthSpace) * j), ws = True)
            cmds.polyChipOff(windowColumn[0] + ".f[0:" + str((heightNum * 6) - 1) + "]", dup = True, kft = True,
                             translate = (-self.width/2.0, 0, -self.depth/2.0 + windowWidth/2.0 + depthSpace + (windowWidth + depthSpace) * j), ws = True)
            cmds.delete(all = True, ch = True)
            cmds.refresh()
        cmds.select(windowColumn[0] + ".f[0:" + str((heightNum * 6) - 1) + "]")
        cmds.delete()
        windowNum = widthNum * heightNum * 2 + depthNum * heightNum * 2 # Total number of windows.
        assignWindowShaders(windowColumn, windowNum, windowShaders)
        cmds.select(windowColumn[0] + ".f[0:" + str(windowNum * 6 - 1) +"]")
        cmds.polySubdivideFacet()
        if booleans:
            result = cmds.polyBoolOp(self.name,windowColumn[0], op = 2, n = name_)
        else:
            result = cmds.polyUnite(self.name,windowColumn[0], n = name_)
        self.name = result[0]
        cmds.delete(self.name, ch = True) 
        
class CylinderHouse(House):
    '''
    Subclass of the class House, which represents houses based on the polygon 
    primitive cylinder.    
    
    Attributes:
        A CylinderHouse object has all the attributes of a House object, and the
        additional attributes:
        radius: The radius of the original cylinder polygon object.
        sides: Number of sides the cylinder has. 
    '''
    
    def __init__(self, name_, height, radius, sides, shader):
        '''
        Initializes a CylinderHouse object, and creates a polygonal house object based on a
        cylinder primitive.
        
        self: Object that is to be initialized.
        name_: A string with the name the polygonal house object will have.
        height: The height of the house.
        radius: See Attributes.
        sides: See Attributes.
        shader: Shader that will be assigned to the house. 
        On exit: A CylinderHouse object has been initialized and a polygonal house has 
                 been created out of a cylinder primitive. A foundation for the house has
                 also been created and united with the box. The given shader has been 
                 assigned to the house. 
        '''
        House.__init__(self, name_, "cylinder", height, radius * 2, radius * 2)
        self.radius = radius
        self.sides = sides
        n = cmds.polyCylinder(n = name_, r = radius, h = height, sx = sides, sy = height)
        cmds.xform(n[0], translation = (0,height/2.0,0))
        f = cmds.polyCylinder(n = "foundation", r = radius + 0.15, height = 0.8, sx = sides)
        cmds.xform(f[0], translation = (0, 0.4, 0))
        n = cmds.polyUnite(n[0],f[0], n = name_)
        self.name = n[0]
        cmds.sets(n[0], edit=True, forceElement= shader[1])
        cmds.delete(self.name, ch = True)
        
class PipeHouse(House):
    '''
    Subclass of the class House, which represents houses based on the polygon 
    primitive pipe.    
    
    Attributes:
        A PipeHouse object has all the attributes of a House object, and the
        additional attributes:
        radius: The outer radius of the original pipe polygon object.
        sides: Number of sides the pipe has. 
        thickness: The thickness of the original pipe.
    '''
    
    def __init__(self, name_, height, radius, sides, thickness, shader):
        '''
        Initializes a PipeHouse object, and creates a polygonal house object based on a
        pipe primitive.
        
        self: Object that is to be initialized.
        name_: A string with the name the polygonal house object will have.
        height: The height of the house.
        radius: See Attributes.
        sides: See Attributes.
        thickness: See Attributes.
        shader: Shader that will be assigned to the house. 
        On exit: A PipeHouse object has been initialized and a polygonal house has 
                 been created out of a pipe primitive. A foundation for the house has
                 also been created and united with the box. The given shader has been 
                 assigned to the house. 
        '''
        House.__init__(self, name_, "pipe", height, radius * 2, radius * 2)
        self.radius = radius
        self.sides = sides
        self.thickness = thickness
        # The actual height of a pipe object in maya is half of the height it is given. Therefore here h = 2 * height.
        n = cmds.polyPipe(n = name_, r = radius, h = 2 * height, t = thickness, sa = sides, sh = height)
        cmds.xform(n[0], translation = (0,height/2.0,0))
        f = cmds.polyPipe(n = "foundation", r = radius + 0.15, height = 0.8 * 2, t = thickness + 0.3, sa = sides)
        cmds.xform(f[0], translation = (0, 0.4, 0))
        n = cmds.polyUnite(n[0],f[0], n = name_)
        self.name = n[0]
        cmds.sets(n[0], edit=True, forceElement=shader[1])
        cmds.delete(self.name, ch = True)
        
        
    def addDeformer(self):
        '''
        Adds one or two deformers to a pipe house.
        
        self : Object of the class PipeHouse.       
        On exit : A flare deformer has been added to the object house.name. 
        A twist deformer is occasionally added on top of that. Since in maya 
        the actual height of a pipe is half of the height it is given, the
        deformers have to be scaled up. Some of the deformers' attributes have 
        been randomly set.
        '''
        House.addDeformer(self)
        if (self.flare != None):
            cmds.select(self.flare)
            cmds.scale(self.height/2.0, y = True)
        if (self.twist != None):
            cmds.select(self.twist)
            cmds.scale(self.height/2.0, y = True)
        
class Block:
    '''
    A Block object repesents a block in the city. The street lights are placed 
    based on the city blocks.
    
    Attributes:
        width: The width of the block.
        depth: The depth of the block.
        center: Tuple with the center coordinates for the block.
        obj: Polygonal object forming the pavement on the block        
    '''
    def __init__(self, width, depth, center):
        '''
        Initializes a Block object and creates a pavement on the block.
        
        self: Object that is to be initialized.
        width: See Attributes.
        depth: See Attributes.
        center: See Attributes.
        On exit: The Block object has been initialized and a pavement has
                 been created on the block. A shader has been assigned to
                 the pavement.        
        '''
        self.width = width
        self.depth = depth
        self.center = center
        self.obj = cmds.polyCube(n = "block", w = width, h = 0.2, d = depth) 
        cmds.xform(self.obj, translation = (center[0], 0.1,center[1]))    
        cmds.sets(self.obj[0], edit=True, forceElement="pavementMaterialGroup")

def makeWindowColumn(windowWidth, windowHeight, num, floorHeight):
    '''
    Creates a column with the specified number of windows.
    
    windowWidth: The width of the windows.
    windowHeight: The height of the windows.
    num = The number of windows in the column.
    floorHeight: The height of one floor.
    On exit: A column of windows of the given size has been created.
    '''
    window = cmds.polyCube(w = windowWidth, h = windowHeight, d = 0.1)
    cmds.xform(window, translation = (0, 0.8 + floorHeight,0))
    for i in range(1,num):
        cmds.polyChipOff(window[0] + ".f[0:5]", dup = True, kft = True, translate = (0,(i * floorHeight),0))
    cmds.delete(all = True, ch = True)
    cmds.refresh()
    return window    
        
def assignWindowShaders(window, windowNum, shaders):
    '''
    Assigns shaders to all the windows for a house.
    
    window: The polygonal object whose faces form the windows.
    windowNum: The number of windows in the object window.
    shaders: A list of shaders for the windows.
    On exit: A shader has been assigned seperately to every window
             in the window object. 
    '''
    for i in range(windowNum):
        light = random.random()
        if light < 0.2:
            shader = random.choice(shaders)
        else:
            shader = shaders[0]
        cmds.sets(window[0] + ".f[" + str(i * 6) + ":" + str((i + 1) * 6) + "]", edit=True, forceElement= shader[1])
        
def makeHouseShaders(num, colourRange):
    '''
    Creates a number of shaders for houses.
    
    num: The number of shaders that will be created.
    colourRange: A tuple containing two triples with hsv colour values. These 
                 colour values gives the range for the hue, saturation and value 
                 the shaders will have.
    On exit: The specified number of shaders have been created and added to a list. 
             All the shaders have colours within the given colour range. The list
             is returned.
    '''
    shaderList = []    
    for i in range(num):
        hue = tools.getRandomValue((colourRange[0][0]/360.0,colourRange[1][0]/360.0))
        saturation = tools.getRandomValue((colourRange[0][1],colourRange[1][1]))
        value = tools.getRandomValue((colourRange[0][2],colourRange[1][2]))
        RGB = tools.convertToRgb((hue*360, saturation, value))
        shader = tools.makeShader((RGB[0], RGB[1], RGB[2]))
        cmds.setAttr(shader[0] + ".reflectivity", 0.000)
        cmds.setAttr(shader[0] + ".specularColor", 0.120, 0.120, 0.120)
        shaderList.append(shader)
    return shaderList

def makeNecessaryShaders(daytime):
    '''
    Creates shaders that are needed for the city. 
    
    daytime: Boolean variable which is true if it is day and false if it is night.
    On exit: Shaders for streets, pavement, parks, traffic lights and street lights
             have been created.
    '''
    streetShader = tools.makeShader((0.145,0.145,0.145), "streetMaterial", "lambert")
    pavementShader = tools.makeShader((0.701,0.628,0.594), "pavementMaterial", "lambert")
    park.makeParkShaders()
    trafficLight.makeLightShaders(daytime)
    
def makeWindowShaders(daytime, glow, environment):
    '''
    Creates shaders for windows.
    
    daytime: Boolean variable which is true if it is day and false if it is night.
    glow: Boolean variable which specifies if all windows will glow if daytime is false, 
          or if some windows will be dark.
    environment: Triple containing the colour value the environment windows will be given
                 if daytime is true.
    On exit: A list of shaders is returned. If daytime is true this list contains only one
             shader. 
    '''
    shaderList = []
    if daytime == True:
        windowShader = tools.makeShader((environment[0],environment[1],environment[2]), "glassMaterial")
        cmds.setAttr("glassMaterial.reflectivity",1.000)
        cmds.setAttr("glassMaterial.eccentricity",0.291)
        cmds.setAttr("glassMaterial.specularColor",0.863,0.863,0.863)
        shaderList.append(windowShader)
    else:
        if glow == False:
            for i in range(1):
                windowShader = tools.makeShader((0,0,0),"glassMaterial")
                cmds.setAttr(windowShader[0] + ".reflectivity",1.000)
                shaderList.append(windowShader)
        for i in range(4):            
            windowShader = tools.makeShader((1.0,0.75,0),"glassMaterial")
            inc = random.uniform(0.1,0.6)
            incR = inc * 1
            incG = inc * 0.922
            incB = inc * 0.399
            cmds.setAttr(windowShader[0] + ".glowIntensity", 0.05)
            cmds.setAttr(windowShader[0] + ".incandescence", incR,incG,incB)
            shaderList.append(windowShader)
    return shaderList
    
def makeLights(daytime, name_):
    '''
    Creates lights for the city.
    
    daytime: Boolean variable which is true if it is day and false if it is night.
    On exit: A directional light has been created and rotated randomly. If daytime
             is true a ambient light has also been created.    
    '''
    light = cmds.directionalLight(name = name_ + "directionalLight", rs = True)
    rotatex = random.randint(-90,0)
    rotatey = random.randint(0,360)
    cmds.xform(name_ + "directionalLight", rotation = (rotatex,rotatey,0), translation = (0,50,0),relative = True, ws = True)
    if daytime == False:
        cmds.setAttr(light + ".intensity", 0.05)
    else:
        light2 = cmds.ambientLight(name = name_ + "ambientLight",intensity = 0.5)
        cmds.xform(name_ + "ambientLight", translation = (0,50,0))
    
def makeCamera(name_, environment):
    '''
    Creates a camera with the given background colour. 
    
    name_: The name the camera is given.
    environment: The colour the backround for the camera will have.
    On exit: A camera with the given background colour has been created and 
             made active.
    '''
    camera_ = cmds.camera(n = name_)
    cmds.setAttr(camera_[1] + ".backgroundColor", environment[0], environment[1],environment[2])
    cmds.camera(camera_[0], edit = True, position = [0,100,250], rotation = [-23,0,0])
    cmds.lookThru(camera_[0])
    
def makeZoneHeights(size, houseHeightInt):
    '''
    Creates a list of six different height ranges for the houses in the city.
    
    size: Tuple defining the size of the city.
    houseHeightInt: Tuple determining the minimum and the maximum height for the houses in the city.
    On exit: A list containing six tuples specifying the height range for houses in the city zones 
             is returned. The first element in the list is the height range for the central zone, 
             while the last element is the height range for the zone furthest away from the city
             center.
    '''
    heightChange = (houseHeightInt[1] - houseHeightInt[0]) / 9.0
    heightIntList = [] 
    heightIntList.append((houseHeightInt[1] - (heightChange * 2), houseHeightInt[1]))
    heightIntList.append((houseHeightInt[1] - (heightChange * 4), houseHeightInt[1] - (heightChange * 2)))
    heightIntList.append((houseHeightInt[1] - (heightChange * 6), houseHeightInt[1] - (heightChange * 4)))
    heightIntList.append((houseHeightInt[1] - (heightChange * 7), houseHeightInt[1] - (heightChange * 6)))
    heightIntList.append((houseHeightInt[1] - (heightChange * 8), houseHeightInt[1] - (heightChange * 6)))
    heightIntList.append((houseHeightInt[1] - (heightChange * 9), houseHeightInt[1] - (heightChange * 8)))
    return heightIntList
    
    
def makeHouse(name_, heightInt, wxd, houseShaders, treeShaders, windowShaders, windows, booleans, deformer):
    '''
    Creates a house.
    
    name_: Name the house will be given.
    heightInt: The range for the height of the house.
    wxd: A tuple defining the width and the depth of the house.
    houseShaders: A list of shaders for the house.
    treeShaders: A list of shaders for the tree crowns.
    windowShaders: A list of shaders for the windows.
    windows: A boolean variable which specifies if the house should have windows.
    booleans: A boolean variable which determines whether the windows should be 
              combined with the house using boolean difference or not. 
    deformers: A boolean variable which determines whether deformers will be 
               added to the house or not.
    On exit: A house of either the class BoxHouse, CylinderHouse or PipeHouse has
             been created and wanted features added. The House object is returned.
    
    '''
    shader = random.choice(houseShaders)
    houseShape = random.choice(["box", "cylinder", "pipe"])
    height = int(random.uniform(heightInt[0], heightInt[1]))
    if (houseShape == "box"):
        width = wxd[0]
        depth = wxd[1]
        h = BoxHouse(name_, height, width, depth, shader)
    if (houseShape == "cylinder"):
        radius = min(wxd[0], wxd[1])  / 2.0
        sides = random.randint(3, 20)
        h = CylinderHouse(name_, height, radius, sides, shader)
    if (houseShape == "pipe"):
        radius = min(wxd[0], wxd[1])  / 2.0
        sides = random.randint(3, 20)
        thickness = random.uniform(min(1, radius - 0.2), max(radius - 2, min(1.1, radius - 0.5)))
        h = PipeHouse(name_, height, radius, sides, thickness, shader) 
    if (windows == True):
        h.makeWindows(name_, windowShaders, booleans)
    if (deformer == True):
        h.addDeformer()
    if (houseShape == "cylinder") or (houseShape == "pipe"):
        park.placeStreetTrees(h, wxd, treeShaders)
    cmds.refresh()
    return h
    


def city(name_, size, houseHeightInt, houseWidthInt, windows, booleans, deformers, daytime, glow, environment, colourRange):
    '''
    Generates the city.
    
    name_: String specifying the name of the city.
    size: Tuple defining the size of the city.
    houseHeightInt: Tuple determining the minimum and the maximum height for the houses in the city.
    houseWidthInt: Tuple determining the minimum and the maximum width for the houses in the city.
    windows: A boolean variable which specifies if the houses should have windows.
    booleans: A boolean variable which determines whether the windows should be 
              combined with the houses using boolean difference or not. 
    deformers: A boolean variable which determines whether deformers will be 
               added to the houses or not.
    daytime: Boolean variable which is true if it is day and false if it is night.
    glow: Boolean variable which specifies if all windows will glow if daytime is false, 
          or if some windows will be dark.
    environment: Triple specifying the colour value the environment will have.
    colourRange: A tuple containing two triples with hsv colour values. These 
                 colour values gives the range for the hue, saturation and value 
                 the house shaders will have.
    On exit: A city with houses, trees, parks, traffic lights and street lights has been 
             generated. The height of the houses decrease the further away from the city center
             they are. 
    '''
    cmds.flushUndo()
    houseShaders = makeHouseShaders(40,colourRange)
    makeNecessaryShaders(daytime)
    treeShaders = park.makeTreeShaders(10)   
    windowShaders = makeWindowShaders(daytime, glow, environment)
    makeCamera(name_+ "RenderCam", environment)
    makeLights(daytime, name_)
    ground = cmds.polyPlane(n = "Ground", w = size[0], h = size[1])
    cmds.sets(ground[0], edit=True, forceElement="streetMaterialGroup")
    streetLightGeom = trafficLight.makeStreetLight()
    dir = random.choice(["horisontal","vertical"])
    # Make the binary tree forming the street structure for the city
    if (dir == "horisontal"):
        firstSplit = random.uniform(-size[1] / 2.0 + houseWidthInt[0] + 8 ,size[1] / 2.0  -houseWidthInt[0] - 8)
    else:
        firstSplit = random.uniform(-size[0] / 2.0 + houseWidthInt[0] + 8 ,size[0] / 2.0  -houseWidthInt[0] - 8)
    cityStreets = streets.Street((dir,firstSplit), (-size[0] / 2.0,-size[1] / 2.0), (size[0] / 2.0, size[1] / 2.0))
    cityStreets.split_((-size[0] / 2.0,-size[1] / 2.0), (size[0] / 2.0, size[1] / 2.0), houseWidthInt[1] + 8, houseWidthInt[0] + 8)
    list = []
    areas = cityStreets.listAreas((-size[0] / 2.0,-size[1] / 2.0), (size[0] / 2.0, size[1] / 2.0),list)
    heightIntList = makeZoneHeights(size, houseHeightInt) # Make a list with 6 different height ranges for the houses.
    maxCenterDistance = math.sqrt(math.pow((size[0] / 2.0), 2) + math.pow((size[1] / 2.0), 2))
    zoneWidth = maxCenterDistance/6 # The thickness of each circular zone.
    blockList = []
    cmds.group(n = "houses", empty = True)
    cmds.group(n = "parks", empty = True)
    for i in areas:
        centerx = (i[0][0] + i[1][0]) / 2.0
        centerz = (i[0][1] + i[1][1]) / 2.0
        width = (i[1][0] - i[0][0]) - 4
        depth = (i[1][1] - i[0][1]) - 4
        blockList.append(Block(width, depth, (centerx, centerz))) # Create Block object. 
        centerDistance = math.sqrt(math.pow(centerx, 2) + math.pow(centerz, 2))
        blockType = random.random() # Determine if house or park should be created.
        if blockType < 0.8:
            zone = int(math.floor(centerDistance / zoneWidth)) # Check which zone the house is in.
            house = makeHouse(name_ + "House", heightIntList[zone], (width - 4,depth - 4), houseShaders, treeShaders, windowShaders, windows, booleans, deformers)
            house.moveHouse((centerx,centerz))
            cmds.delete(house.name, ch = True)
            cmds.parent(house.name, "houses")
        elif blockType < 0.9:
            park_ = park.makeFountainPark((width - 3,depth - 3), treeShaders, daytime, streetLightGeom)
            cmds.xform(park_[0], translation = (centerx,0,centerz), r = True)
            cmds.parent(park_[0], "parks")
        else:
            park_ = park.makePark((width - 3,depth - 3), treeShaders, daytime, streetLightGeom)
            cmds.xform(park_[0], translation = (centerx,0,centerz), r = True)
            cmds.parent(park_[0], "parks")
    trafficLight.placeStreetLight(blockList,daytime,streetLightGeom)
    trafficLight.trafficLights(cityStreets,size,daytime)
    cmds.hide(streetLightGeom[0])
    # Group all blocks together.
    cmds.group(n = "blocks", empty = True)
    for i in blockList:
        cmds.parent(i.obj[0], "blocks")
        