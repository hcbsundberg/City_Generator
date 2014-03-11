import maya.cmds as cmds
import random, math
import trafficLight
import tools

'''
List of procedures in the module:

    def makeParkShaders():
        Creates the shaders that are necessary for creating parks.
    def makeTreeShaders(num):
        Creates a number of shaders suitable for trees.
    def makePark(wxd, treeShaders, daytime, lightGeom):
        Creates a park block with trees, paths, fences and street lights.
    def makeFountainPark(wxd, treeShaders, daytime, lightGeom):
        Creates a park with a fountain in the middle.
    def makeFence(startPoint, endPoint, axis):
        Creates a fence between two points along either the x-axis or the z-axis.
    def makeFountain():
        Creates a fountain.
    def fountainTop(fountain):
        Creates a top decoration for a fountain.
    def makeTree(shaders):
        Creates a tree.
    def placeTreesInSquare(squareBbox, shaders):
        Places trees randomly in a given square.
    def makeStreetTree(shaders):
        Creates a tree on a circular platform and with a circular fence around it.
    def makeRowOfStreetTrees(num, coor, shaders, dir):
        Makes a row with the specified number of street trees. 
    def placeStreetTrees(house, wxd, treeShaders):
        Places trees on empty areas around a cylinder or pipe houses.
'''

def makeParkShaders():
    '''
    Creates the shaders that are necessary for creating parks.
    On exit: Shaders for fences, fountains and grass has been created.
    '''
    fountainShader = tools.makeShader((0.691,0.683,0.596), "fountainMaterial")
    cmds.setAttr("fountainMaterial.reflectivity",0)
    cmds.setAttr("fountainMaterial.specularColor",0.179,0.179,0.179)
    grassShader = tools.makeShader((0.043,0.392,0.008), "grassMaterial")
    cmds.setAttr("grassMaterial.reflectivity",0)
    cmds.setAttr("grassMaterial.specularColor",0.137,0.137,0.137)
    fenceShader = tools.makeShader((0.373,0.269,0.168), "fenceMaterial")
    cmds.setAttr("fenceMaterial.reflectivity",0)
    cmds.setAttr("fenceMaterial.specularColor",0.137,0.137,0.137)    

def makeTreeShaders(num):
    '''
    Creates a number of shaders suitable for trees.
    
    num: The number of different green coloured shaders that will be created.
    On exit: Creates a shader for the tree trunk, and returns a list with the
             specified number of shaders with different green colours.
    '''
    trunkShader = tools.makeShader((0.124,0.043,0.000), "trunkMaterial")
    cmds.setAttr("trunkMaterial.reflectivity", 0)
    cmds.setAttr("trunkMaterial.specularColor", 0, 0, 0)
    l =[]
    for i in range(num):
        hue = random.randint(75, 120)
        saturation = random.uniform(0.6, 1)
        value = random.uniform(0.15, 0.6)
        RGB = tools.convertToRgb((hue, saturation, value))
        treeShader = tools.makeShader((RGB[0], RGB[1], RGB[2]), "treeMaterial")
        cmds.setAttr(treeShader[0] + ".reflectivity", 0)
        cmds.setAttr(treeShader[0] + ".specularColor", 0, 0, 0)
        l.append(treeShader)
    return l
    
def makePark(wxd, treeShaders, daytime, lightGeom):
    '''
    Creates a park block with trees, paths, fences and street lights.
    
    wxd: A tuple containing the width and the depth of the park.
    treeShaders: A list of shaders for the tree crowns.
    daytime: Boolean variable which is true if it is day and false if it is night.
    lightGeom: Tuple containing the object name and node name for a polygonal object,
               in this case a street light.
    On exit: A park with three randomly placed paths has been created and street 
             lights placed using trafficLights.placeLights(...) at the intersection of 
             these paths. Trees and fences have also been created using 
             placeTreesInSquare(...) and makeFence(...). Everything has been combined 
             into a single polygonal object except the lights, which are instead parented
             to this object. The park object is returned as a tuple containing the 
             object name and node name.
    '''
    # Decide if the first path should be horisontal (along the x-axis) or vertical (along the z-axis).
    dir = random.choice(["horisontal", "vertical"]) 
    if dir == "horisontal":
        path1 = random.uniform(-wxd[1]/2 + 2, wxd[1]/2 - 2) # z-coordinate for the first path.
        path2 = random.uniform(-wxd[0]/2 + 2, wxd[0]/2 - 2) # x-coordinate for the second path.
        path3 = random.uniform(-wxd[0]/2 + 2, wxd[0]/2 - 2) # x-coordinate for the third path.
        # Place squares with grass and trees around the paths.
        square1 = placeTreesInSquare(((-wxd[0]/2.0, -wxd[1]/2.0), (path2 - 0.5, path1 - 1)), treeShaders)
        square2 = placeTreesInSquare(((-wxd[0]/2.0, path1 + 1), (path3 - 0.5, wxd[1]/2.0)), treeShaders)
        square3 = placeTreesInSquare(((path2 + 0.5, -wxd[1]/2.0), (wxd[0]/2.0, path1 - 1)), treeShaders)
        square4 = placeTreesInSquare(((path3 + 0.5, path1 + 1), (wxd[0]/2.0, wxd[1]/2.0)), treeShaders)
        # Make fences around the park.
        fence1 = makeFence((-wxd[0]/2.0,-wxd[1]/2.0), (path2 -0.5,-wxd[1]/2.0), "x")
        fence2 = makeFence((path2 + 0.5,-wxd[1]/2.0), (wxd[0]/2.0,-wxd[1]/2.0), "x")
        fence3 = makeFence((wxd[0]/2.0,-wxd[1]/2.0), (wxd[0]/2.0,path1 - 1), "z")
        fence4 = makeFence((wxd[0]/2.0,path1 + 1), (wxd[0]/2.0,wxd[1]/2.0), "z")
        fence5 = makeFence((wxd[0]/2.0,wxd[1]/2.0), (path3 + 0.5,wxd[1]/2.0), "x")
        fence6 = makeFence((path3 - 0.5,wxd[1]/2.0), (-wxd[0]/2.0,wxd[1]/2.0), "x")
        fence7 = makeFence((-wxd[0]/2.0,wxd[1]/2.0), (-wxd[0]/2.0,path1 + 1), "z")
        fence8 = makeFence((-wxd[0]/2.0,path1 - 1), (-wxd[0]/2.0,-wxd[1]/2.0), "z")
        # Create and place instances of street lights
        light1 = cmds.instance(lightGeom[0])
        trafficLight.placeLight(light1[0], (path3 - 1.5,path1 + 0.9), daytime)
        light2 = cmds.instance(lightGeom[0])
        trafficLight.placeLight(light2[0], (path3 + 1.5,path1 + 0.9), daytime)
        light3 = cmds.instance(lightGeom[0])
        trafficLight.placeLight(light3[0], (path2 - 1.5,path1 - 0.9), daytime)
        light4 = cmds.instance(lightGeom[0])
        trafficLight.placeLight(light4[0], (path2 + 1.5,path1 - 0.9), daytime)
    if dir == "vertical":
        path1 = random.uniform(-wxd[0]/2 + 2, wxd[0]/2 - 2) # x-coordinate for the first path.
        path2 = random.uniform(-wxd[1]/2 + 2, wxd[1]/2 - 2) # z-coordinate for the second path.
        path3 = random.uniform(-wxd[1]/2 + 2, wxd[1]/2 - 2) # z-coordinate for the third path.
        # Place squares with grass and trees around the paths.
        square1 = placeTreesInSquare(((-wxd[0]/2.0, -wxd[1]/2.0), (path1 - 1, path2 - 0.5)), treeShaders)
        square2 = placeTreesInSquare(((-wxd[0]/2.0, path2 + 0.5), (path1 - 1, wxd[1]/2.0)), treeShaders)
        square3 = placeTreesInSquare(((path1 + 1, -wxd[1]/2.0), (wxd[0]/2.0, path3 - 0.5)), treeShaders)
        square4 = placeTreesInSquare(((path1 + 1, path3 + 0.5), (wxd[0]/2.0, wxd[1]/2.0)), treeShaders)
        # Make fences around the park.
        fence1 = makeFence((-wxd[0]/2.0,-wxd[1]/2.0), (path1 -1,-wxd[1]/2.0), "x")
        fence2 = makeFence((path1 + 1,-wxd[1]/2.0), (wxd[0]/2.0,-wxd[1]/2.0), "x")
        fence3 = makeFence((wxd[0]/2.0,-wxd[1]/2.0), (wxd[0]/2.0,path3 - 0.5), "z")
        fence4 = makeFence((wxd[0]/2.0,path3 + 0.5), (wxd[0]/2.0,wxd[1]/2.0), "z")
        fence5 = makeFence((wxd[0]/2.0,wxd[1]/2.0), (path1 + 1,wxd[1]/2.0), "x")
        fence6 = makeFence((path1 - 1,wxd[1]/2.0), (-wxd[0]/2.0,wxd[1]/2.0), "x")
        fence7 = makeFence((-wxd[0]/2.0,wxd[1]/2.0), (-wxd[0]/2.0,path2 + 0.5), "z")
        fence8 = makeFence((-wxd[0]/2.0,path2 - 0.5), (-wxd[0]/2.0,-wxd[1]/2.0), "z")
        # Create and place instances of street lights
        light1 = cmds.instance(lightGeom[0])
        trafficLight.placeLight(light1[0], (path1 + 0.9,path3 - 1.5), daytime)
        light2 = cmds.instance(lightGeom[0])
        trafficLight.placeLight(light2[0], (path1 + 0.9,path3 + 1.5), daytime)
        light3 = cmds.instance(lightGeom[0])
        trafficLight.placeLight(light3[0], (path1 - 0.9,path2 - 1.5), daytime)
        light4 = cmds.instance(lightGeom[0])
        trafficLight.placeLight(light4[0], (path1 - 0.9,path2 + 1.5), daytime)
    park = cmds.polyUnite(square1,square2,square3,square4,fence1, fence2, fence3,
                          fence4, fence5, fence6, fence7, fence8)
    cmds.delete(park, ch = True)
    cmds.parent((light1[0],light2[0],light3[0],light4[0]),park[0])
    return park
    
def makeFountainPark(wxd, treeShaders, daytime, lightGeom):
    '''
    Creates a park with a fountain in the middle.
    
    wxd: A tuple containing the width and the depth of the park.
    treeShaders: A list of shaders for the tree crowns.
    daytime: Boolean variable which is true if it is day and false if it is night.
    lightGeom: Tuple containing the object name and node name for a polygonal object,
               in this case a street light.
    On exit: A park with trees (placeTreesInSquare(...)), fences (makeFence(...)) 
             and street lights (trafficLight.placeLight(...)) has been created and
             a fountain has been created in the middle of the park using 
             makeFountain(...). Everything has been combined into a single polygonal 
             object except the lights, which are instead parented to this object. 
             The park object is returned as a tuple containing the object name and 
             node name.
    '''
    # Make fences around the park.
    fence1 = makeFence((-wxd[0]/2.0,wxd[1]/2.0), (-1,wxd[1]/2.0), "x")
    fence2 = makeFence((1,wxd[1]/2.0), (wxd[0]/2.0,wxd[1]/2.0), "x")
    fence3 = makeFence((wxd[0]/2.0,wxd[1]/2.0), (wxd[0]/2.0,1), "z")
    fence4 = makeFence((wxd[0]/2.0,-1), (wxd[0]/2.0,-wxd[1]/2.0), "z")
    fence5 = makeFence((wxd[0]/2.0,-wxd[1]/2.0), (1,-wxd[1]/2.0), "x")
    fence6 = makeFence((-1,-wxd[1]/2.0), (-wxd[0]/2.0,-wxd[1]/2.0), "x")
    fence7 = makeFence((-wxd[0]/2.0,-wxd[1]/2.0), (-wxd[0]/2.0,-1), "z")
    fence8 = makeFence((-wxd[0]/2.0,1), (-wxd[0]/2.0,wxd[1]/2.0), "z")
    fountain = makeFountain()
    # Place squares with grass and trees around the paths.
    square1 = placeTreesInSquare(((-wxd[0]/2.0, -wxd[1]/2.0), (-1,-1)), treeShaders)
    square2 = placeTreesInSquare(((-wxd[0]/2.0, 1),(-1, wxd[1]/2.0)), treeShaders)
    square3 = placeTreesInSquare(((1, -wxd[1]/2.0),(wxd[0]/2.0, -1)), treeShaders)
    square4 = placeTreesInSquare(((1,1),(wxd[0]/2.0, wxd[1]/2.0)), treeShaders)
    park = cmds.polyUnite(fence1, fence2, fence3, fence4, fence5, fence6, fence7,
                          fence8, fountain, square1, square2, square3, square4)
    cmds.delete(park, ch = True)
    # Create and place instances of street lights
    light1 = cmds.instance(lightGeom[0])
    trafficLight.placeLight(light1[0], (-1.5,-0.9), daytime)
    light2 = cmds.instance(lightGeom[0])
    trafficLight.placeLight(light2[0], (-1.5,0.9), daytime)
    light3 = cmds.instance(lightGeom[0])
    trafficLight.placeLight(light3[0], (1.5,-0.9), daytime)
    light4 = cmds.instance(lightGeom[0])
    trafficLight.placeLight(light4[0], (1.5,0.9), daytime)
    cmds.parent((light1[0],light2[0],light3[0],light4[0]),park[0])
    return park


    
def makeFence(startPoint, endPoint, axis):
    '''
    Creates a fence between two points along either the x-axis or the z-axis.
    
    startPoint: Tuple with the coordinates where the fence will start.
    endPoint: Tuple with the coordinates where the fence will end.
    axis: String that specifies along which axis the fence will be created.
    On exit: A fence polygonal object has been created between the specified points 
             and a shader has been assigned to it. The fence object is returned as
             a tuple with the object name and the node name.
    '''
    if axis == "x":
        length = abs(startPoint[0] - endPoint[0])
        poleNumber = int(length / 0.8)
        if poleNumber != 0:
            distance = float(endPoint[0] - startPoint[0]) / poleNumber
        else:
            distance = 0
        bar = cmds.polyCube(name = "bar", h = 0.05, w = length, d = 0.05)
        cmds.xform(bar,translation = (startPoint[0] + (endPoint[0] - startPoint[0])/2.0,0.8,startPoint[1]))
        bar2 = cmds.duplicate(bar[0])
        cmds.xform(bar2, translation = (0,-0.3,0), r = True)
        fence = cmds.polyUnite(bar,bar2)
        for i in range(poleNumber + 1):
            pole = cmds.polyCube(name = "pole", h = 0.7, w = 0.1, d = 0.05)
            cmds.xform(pole[0], translation = (startPoint[0] + i * distance,0.55,startPoint[1]))
            fence = cmds.polyUnite(pole,fence)
    else:
        length = abs(startPoint[1] - endPoint[1])
        poleNumber = int(length / 0.8)
        if poleNumber != 0:
            distance = float(endPoint[1] - startPoint[1]) / poleNumber
        else:
            distance = 0
        bar = cmds.polyCube(name = "bar", h = 0.05, w = 0.05, d = length)
        cmds.xform(bar,translation = (startPoint[0],0.8,startPoint[1]+ (endPoint[1] - startPoint[1])/2.0))
        bar2 = cmds.duplicate(bar[0])
        cmds.xform(bar2, translation = (0,-0.3,0), r = True)
        fence = cmds.polyUnite(bar,bar2)
        for i in range(poleNumber + 1):
            pole = cmds.polyCube(name = "pole", h = 0.7, w = 0.05, d = 0.1)
            cmds.xform(pole[0], translation = (startPoint[0],0.55,startPoint[1] + i * distance))
            fence = cmds.polyUnite(pole,fence)
    cmds.sets(fence[0], edit=True, forceElement="fenceMaterialGroup")
    return fence

def makeFountain():
    '''
    Creates a fountain.
    
    On exit: A fountain shaped polygonal object has been created, assigned a shader
             and is returned as a tuple with the object name and node name. The 
             procedure uses random numbers in order to create different looking fountains
             every time it is called.
    '''
    steps = random.randint(1,3)
    fountain = cmds.polyCylinder(name = "Fountain", h = 0.1)
    cmds.xform(fountain, translation = (0, 0.25, 0))
    cmds.select(fountain[0] + ".f[40:59]")
    for i in range(steps):
        scale_ = random.uniform(0.6, 0.95) 
        cmds.polyExtrudeFacet(scale = (scale_, scale_, scale_))
        translation = random.uniform(0.1, 0.6)
        cmds.polyExtrudeFacet(translate = (0, translation, 0))
    cmds.polyExtrudeFacet(scale = (0.9,0.9,0.9))
    cmds.polyExtrudeFacet(translate = (0, -0.3,0))
    scale_ = random.uniform(0.3,0.6)
    cmds.polyExtrudeFacet(scale = (scale_,scale_,scale_))
    translation = random.uniform(0.2,0.4)
    cmds.polyExtrudeFacet(translate = (0,translation,0))
    stepsUp = random.randint(1,3)
    for i in range(stepsUp):
        scale_ = random.uniform(0.4,0.9) 
        cmds.polyExtrudeFacet(scale = (scale_,scale_,scale_))
        translation = random.uniform(0.05,1)
        cmds.polyExtrudeFacet(translate = (0,translation,0))
    top = fountainTop(fountain) # Create a top for the fountain.
    fountain = cmds.polyUnite(top[0],fountain)
    cmds.sets(fountain[0], edit=True, forceElement="fountainMaterialGroup")
    return fountain


def fountainTop(fountain):
    '''
    Creates a top decoration for a fountain.
    
    fountain: A object the top decoration will be placed on.
    On exit: A top decoration has been created by adding a deformer to a 
             basic polygonal object. The top is returned as a tuple
             with the object name and node name.
    '''
    height = random.uniform(0.1,0.6)
    # Decide which type of object will form the top.
    type = random.choice(["cube", "cylinder", "prism", "cone", "sphere"])
    if type == "cube":
        top = cmds.polyCube(name = "top", h = height, w = 0.2, d = 0.2, sy = 10)
    if type == "cylinder":
        top = cmds.polyCylinder(name = "top",h = height, r = 0.1, sy = 10)
    if type == "prism":
        top = cmds.polyPrism(name = "top", l = height, w = 0.1, sh = 10)
    if type == "cone":
        top = cmds.polyCone(name = "top", h = height, r = 0.1, sy = 10)
    if type == "sphere":
        top = cmds.polySphere(name = "top",r = height/2.0) 
    bbox = cmds.exactWorldBoundingBox(fountain)
    cmds.xform(top, translation = (0,bbox[4]+ height/2.0,0))
    flare = random.choice([0,1])
    if flare == 1:
        cmds.select(top[0])
        flare = cmds.nonLinear(type = "flare")
        cmds.setAttr(flare[0] + ".curve", random.uniform(-3,3))
    twist = random.choice([0,1])
    if type == "cube" or type == "prism":
        if twist == 1:
            cmds.select(top[0])
            twist = cmds.nonLinear(type = "twist")
            cmds.setAttr(twist[0] + ".endAngle", random.randint(-500, 500))
    return top
    
def makeTree(shaders):
    '''
    Creates a tree.
    
    shaders: A list of shaders for the tree crown.
    On exit: A tree has been modeled, and is returned as a tuple 
             containing the object name and the node name. Some of the
             variables are chosen randomly to create different results.
    '''
    height = random.uniform(0.3,1.5)
    trunk = cmds.polyCylinder(name = "trunk", h = height, r = 0.07)
    cmds.sets(trunk[0], edit=True, forceElement="trunkMaterialGroup")
    cmds.xform(trunk, translation = (0,height/2.0 + 0.2,0))
    crown = cmds.polySphere(name = "crown", r = 0.5)
    cmds.xform(crown, translation = (0,height + 0.6,0))
    cmds.softSelect(sse = True, ssd = 0.86)
    cmds.select(crown[0] + ".vtx[381]")
    translation = random.uniform(0.3,1.5)
    cmds.move(translation, y = True, r = True)
    cmds.softSelect(sse = False)
    shader = random.choice(shaders)
    scale_ = random.uniform(0.7,1.8)
    cmds.select(crown)
    cmds.scale(scale_, scale_, scale_, pivot = (0,height,0))
    cmds.sets(crown[0], edit=True, forceElement= shader[1])
    tree = cmds.polyUnite(trunk[0],crown[0])
    cmds.delete(tree[0], ch = True)
    return tree
    
def placeTreesInSquare(squareBbox, shaders):
    '''
    Places trees randomly in a given square.
    
    squareBbox: A list of two tuples containing the x- and z-coordinates for the
                bounding box of a square.
    shaders: A list of shaders for the tree crowns.
    On exit: A cube of the same size as the square been created and assigned a green
             shader in order to make it look like grass. Trees have created using 
             makeTree(...), and placed randomly using a dart throwing algorithm which 
             gives up after six failed attempts. Everything is united into one object
             which is returned as a tuple with the object name and the node name.             
    '''
    treeList = []
    width = squareBbox[1][0] - squareBbox[0][0]
    depth = squareBbox[1][1] - squareBbox[0][1]
    grass = cmds.polyCube(name = "grass", h = 0.3, w = width, d = depth)
    cmds.xform(grass, translation = (squareBbox[0][0] + 0.5 * width,0.15,squareBbox[0][1] + 0.5 * depth))
    cmds.sets(grass[0], edit=True, forceElement="grassMaterialGroup")
    while True:
        failCount = 0
        tree = makeTree(shaders)
        treeList.append(tree)
        bbox1 = cmds.exactWorldBoundingBox(tree[0])
        radius = (bbox1[3] - bbox1[0]) / 2.0
        coorx = random.uniform(squareBbox[0][0] + radius, squareBbox[1][0] - radius)
        coorz = random.uniform(squareBbox[0][1] + radius, squareBbox[1][1] - radius)
        cmds.xform(tree[0], translation = (coorx, 0, coorz))
        while True:
            failed = False
            for j in treeList:
                bbox1 = cmds.exactWorldBoundingBox(tree[0])
                bbox2 = cmds.exactWorldBoundingBox(j[0])
                # Check if the tree intersects with element j in treeList.
                xinters = (bbox1[0] < bbox2[3] and bbox1[0] > bbox2[0])\
                       or (bbox2[0] < bbox1[3] and bbox2[0] > bbox1[0])                
                zinters = (bbox1[2] < bbox2[5] and bbox1[2] > bbox2[2])\
                       or (bbox2[2] < bbox1[5] and bbox2[2] > bbox1[2])
                if xinters and zinters:
                    coorx = random.uniform(squareBbox[0][0] + radius, squareBbox[1][0] - radius)
                    coorz = random.uniform(squareBbox[0][1] + radius, squareBbox[1][1] - radius)
                    cmds.xform(tree[0], translation = (coorx, 0, coorz))               
                    failCount = failCount + 1
                    failed = True
                    break               
            if (failed == False) or (failCount > 5): 
                break
        if (failCount > 5) or (len(treeList) == 10):
            break
    cmds.delete(tree[0]) # Delete the last tree that was not successfully placed.         
    treeList.pop() 
    for i in treeList:
        grass = cmds.polyUnite(grass[0], i[0])
    return grass
    
def makeStreetTree(shaders):
    '''
    Creates a tree on a circular platform and with a circular fence around it.
    
    shaders: A list of shaders for the tree crowns.
    On exit: A tree has been created using makeTree(...), a circular platform
             has been created underneath it and a fence around it. Appropriate 
             shaders have been assigned. Everything is united into one polygonal
             object and returned as a tuple with the object name and the node 
             name.
    '''
    tree = makeTree(shaders)
    platform = cmds.polyCylinder(name = "platform",h = 0.1, r = 0.8)
    cmds.move(0.25, y = True)
    cmds.sets(platform[0], edit=True, forceElement="fountainMaterialGroup")
    pole = cmds.polyCube(name = "pole", h = 0.6, w = 0.04, d = 0.04)
    cmds.xform(pole, t = (0.7,0.45,0))
    angle = 360/10.0
    for i in range(1,10):
        pole1 = cmds.polyCube(name = "pole", h = 0.6, w = 0.04, d = 0.04)
        cmds.rotate(angle * i, y = True)
        cmds.move(0.7,0.45,0, os = True)
        pole = cmds.polyUnite(pole, pole1)
    bar = cmds.polyPipe(name = "bar", h = 0.1, r = 0.65, t = 0.04)
    cmds.move(0.65, y = True)
    bar1 = cmds.duplicate(bar[0])
    cmds.move(-0.2, y = True, r = True)
    fence = cmds.polyUnite(pole, bar, bar1)
    cmds.sets(fence[0], edit=True, forceElement="blackMetalGroup")
    streetTree = cmds.polyUnite(tree,platform, fence)
    cmds.delete(streetTree, ch = True)
    return streetTree
    
def makeRowOfStreetTrees(num, coor, shaders, dir):
    '''
    Makes a row with the specified number of street trees. 
    
    num: Number of street trees in the row.
    coor: A tuple with the x- and z- coordinates the center of the row of trees
          will be located at.
    shaders: A list of shaders for the tree crowns.
    dir: String which specifies if the trees should be placed along the x-axis
         (horisontal) or along the z-axis (vertical).
    On exit: The specified number of trees has been created using makeStreetTree(...),
             and placed in a row at the given coordinates. All of the trees are 
             combined and the resulting object is returned as a tuple with the 
             object name and node name.
    '''
    start =  -(num - 1)/2.0 * 2.8
    tree = makeStreetTree(shaders)
    cmds.xform(tree[0], t = (start, 0, 0), ws = True)
    for i in range(1,num):
        tree1 = makeStreetTree(shaders)
        cmds.xform(tree1[0], t = (start + i * 2.8, 0, 0), ws = True)
        tree = cmds.polyUnite(tree[0], tree1[0])
    cmds.xform(tree[0], centerPivots = True)
    if dir == "vertical":
        cmds.rotate(90, y = True)
    cmds.xform(tree[0], translation = (coor[0], 0,coor[1]), ws = True)
    return tree

def placeStreetTrees(house, wxd, treeShaders):
    '''
    Places trees on empty areas around a cylinder or pipe houses.
    
    house: Object of the class House by which the trees will be created.
    wxd: Tuple containing the width and depth of the area the house and
         the trees will take up. 
    treeShaders: A list of shaders for the tree crowns.
    On exit: If there is a lot of empty space on the same block as the house,
             two rows of trees have been created using makeRowsOfStreetTrees(...)
             and placed outside the house. The trees are parented to the house.
    '''
    if wxd[0]/wxd[1] >= 1.5: # Check if there is too much empty space on the block.
        distance = (wxd[0] - wxd[1]) / 2.0 # distance between the house and the street.
        if distance > wxd[1]:
            num = int((distance + 1.5) / 2.8)
            tree1 = makeRowOfStreetTrees(num,((wxd[1] + distance)/ 2.0 + 1,0), treeShaders, "horisontal")
            tree2 = makeRowOfStreetTrees(num,((-wxd[1] - distance)/ 2.0 - 1,0), treeShaders, "horisontal")
        else:
            num = int((wxd[1] + 3)/ 2.8)
            tree1 = makeRowOfStreetTrees(num,((wxd[1] + distance)/ 2.0 + 1,0), treeShaders, "vertical")
            tree2 = makeRowOfStreetTrees(num,((-wxd[1] - distance)/ 2.0 - 1,0), treeShaders, "vertical")
        cmds.parent((tree1[0],tree2[0]), house.name)        
    if wxd[1]/wxd[0] >= 1.5: # Check if there is too much empty space on the block.
        distance = (wxd[1] - wxd[0]) / 2.0 # distance between the house and the street.
        if distance > wxd[0]:
            num = int((distance + 1.5) / 2.8)
            tree1 = makeRowOfStreetTrees(num,(0,(wxd[0] + distance)/ 2.0 + 1), treeShaders, "vertical")
            tree2 = makeRowOfStreetTrees(num,(0, (-wxd[0] - distance)/ 2.0 - 1), treeShaders, "vertical")
        else:
            num = int((wxd[0] + 3)/ 2.8)
            tree1 = makeRowOfStreetTrees(num,(0,(wxd[0] + distance)/ 2.0 + 1), treeShaders, "horisontal")
            tree2 = makeRowOfStreetTrees(num,(0, (-wxd[0] - distance)/ 2.0 - 1), treeShaders, "horisontal")
        cmds.parent((tree1[0],tree2[0]), house.name)
        