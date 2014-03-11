import maya.cmds as cmds
import random
import cityGenerator.cityGenerator as cityGenerator

'''
List of procedures in the module:
    def createGUI(): 
        Creates a user interface for the city generator script.
    def defaultButtonPush(args):
        Calls the procedure cityGenerator.city(...) with the user specified 
        arguments.
    def changeMaxHeight(args):
        Changes the maximum house height if it is smaller than the minimum house height.
    def changeMinHeight(args):
        Changes the minimum house height if it is larger than the maximum house height.
    def changeMaxWidth(args):
        Changes the maximum house width so that it is at least 10 units larger 
        than the minimum house height.
    def changeMinWidth(args):
        Changes the minimum house width so that it is at least 10 units smaller 
        than the maximum house height.
    def windows(args):
        Changes the booleans checkbox to be disabled and unchecked when the windows 
        checkbox is unchecked.
    def booleans(args):
        Opens a confirm window, to let the user know the risk of enabling booleans.
    def nighttime(args):
        Changes the city image and the environment colour to match the daytime/nighttime 
        checkboxes. Also uncheckes the daytime checkbox when nighttime is checked and checkes
        it when nighttime is unchecked.
    def daytime(args):
        Changes the city image and the environment colour to match the daytime/nighttime 
        checkboxes. Also uncheckes the nighttime checkbox when daytime is checked and checkes
        it when daytime is unchecked.
    def hueChange1(args):
        Updates the canvas colours for the start of the colour range when the hue is changed.
    def saturationChange1(args):
        Updates the canvas colours for the start of the colour range when the
        saturation is changed.
    def valueChange1(args):
        Updates the canvas colours for the start of the colour range when the 
        value is changed.
    def hueChange2(args):
        Updates the canvas colours for the end of the colour range when the hue
        is changed.
    def saturationChange2(args):
        Updates the canvas colours for the end of the colour range when 
        the saturation is changed.
    def valueChange2(args):
        Updates the canvas colours for the end of the colour range when the value
        is changed.
    def randomize(args):
        Randomizes the hue, saturation and value for both the start
        and the end of the colour range.
    def clearScene(arg):
        Deletes all objects and shaders in the scene.
'''

def createGUI(): 
    '''
    Creates a user interface for the city generator script.
    
    On exit: A window with the user interface has been created.
    '''    
    GUIwindow = cmds.window( title = "City Generator")
    layout0 = cmds.columnLayout()
    imageNum = random.randint(1,19)
    cmds.image("cityImage", image="cityImages/dayImage" + str(imageNum) + ".jpg", width = 800, height = 288 )
    layout1 = cmds.rowLayout(nc = 2, parent = layout0)
    layout2 = cmds.columnLayout(parent = layout1, rs = 3)
    cmds.rowLayout(nc = 2, parent = layout2, cw2 = [140,250])
    cmds.text(label = "City name")
    cmds.textField("cityName", width = 240)
    cmds.intSliderGrp("cityWidth", field=True, label="City width", minValue=50, maxValue=200, fieldMinValue=50, fieldMaxValue=200, value=100, cal = [1,"left"],parent = layout2)
    cmds.intSliderGrp("cityDepth", field=True, label="City depth", minValue=50, maxValue=200, fieldMinValue=50, fieldMaxValue=200, value=100, cal = [1,"left"],parent = layout2)
    cmds.intSliderGrp("minHeight", field=True, label="Minimum house height", minValue=4, maxValue=40, fieldMinValue=4, fieldMaxValue=40, value=4, cal = [1,"left"],parent = layout2, dc = changeMaxHeight)
    cmds.intSliderGrp("maxHeight", field=True, label="Maximum house height", minValue=4, maxValue=40, fieldMinValue=4, fieldMaxValue=40, value=30, cal = [1,"left"],parent = layout2, dc = changeMinHeight)
    cmds.intSliderGrp("minWidth", field=True, label="Minimum house width", minValue=2, maxValue=20, fieldMinValue=2, fieldMaxValue=20, value=5, cal = [1,"left"],parent = layout2, dc = changeMaxWidth)
    cmds.intSliderGrp("maxWidth", field=True, label="Maximum house width", minValue=12, maxValue=30, fieldMinValue=12, fieldMaxValue=30, value=20, cal = [1,"left"],parent = layout2, dc = changeMinWidth)
    cmds.checkBoxGrp("features", numberOfCheckBoxes=3, label1="Windows", label2 = "Booleans", label3="Deformers", v1=True, v2 = False, v3 = True, cc1 =  windows, cc2 = booleans, cal = [1,"left"],parent = layout2,cw = [1,140])
    cmds.checkBoxGrp("time", numberOfCheckBoxes=3, label1="Daytime", label2="Nighttime", label3 = "All windows glow", v1=True, v2 = False, v3 = False, enable3 = False, cal = [1,"left"], parent = layout2,cw = [1,140], cc1 = daytime, cc2 = nighttime )
    cmds.colorSliderGrp("environment", label="Environment colour", hsv=(204, 0.451, 1), parent = layout2, cal = [1,"left"] )
    layout3 = cmds.columnLayout(parent = layout1)
    cmds.text("Set the colour range for the houses by selecting the ranges separately for hue,\nsaturation and value.", align  = "left")
    cmds.text("\nStart of range:", align = "left")
    cmds.rowLayout( numberOfColumns=2, parent = layout3, cw2 = [70,200])
    cmds.canvas("hueCanvas1", hsvValue=(0, 1, 1), width=70, height=15)
    cmds.intSliderGrp("hue1", field=True, label="Hue", minValue=0, maxValue=360, fieldMinValue=0, fieldMaxValue=360, value=0,cw3 = [70,70,170], dc = hueChange1 )
    cmds.rowLayout( numberOfColumns=2, parent = layout3, cw2 = [70,200])
    cmds.canvas("saturationCanvas1", hsvValue=(0, 1, 1), width=70, height=15)
    cmds.floatSliderGrp("saturation1", field=True, label="Saturation", minValue=0, maxValue=1, fieldMinValue=0, fieldMaxValue=1, value=1,cw3 = [70,70,170], dc = saturationChange1, step = 0.01)
    cmds.rowLayout( numberOfColumns=2, parent = layout3, cw2 = [70,200])
    cmds.canvas("valueCanvas1", hsvValue=(0, 1, 1), width=70, height=15)
    cmds.floatSliderGrp("value1", field=True, label="Value", minValue=0, maxValue=1, fieldMinValue=0, fieldMaxValue=1, value=1,cw3 = [70,70,170], dc = valueChange1, step = 0.01)
    cmds.text("End of range:", align =  "left", parent = layout3)
    cmds.rowLayout( numberOfColumns=2, parent = layout3, cw2 = [70,200])
    cmds.canvas("hueCanvas2", hsvValue=(0, 1, 1), width=70, height=15)
    cmds.intSliderGrp("hue2", field=True, label="Hue", minValue=0, maxValue=360, fieldMinValue=0, fieldMaxValue=360, value=0,cw3 = [70,70,170], dc = hueChange2 )
    cmds.rowLayout( numberOfColumns=2, parent = layout3, cw2 = [70,200])
    cmds.canvas("saturationCanvas2", hsvValue=(0, 1, 1), width=70, height=15)
    cmds.floatSliderGrp("saturation2", field=True, label="Saturation", minValue=0, maxValue=1, fieldMinValue=0, fieldMaxValue=1, value=1,cw3 = [70,70,170], dc = saturationChange2, step = 0.01)
    cmds.rowLayout( numberOfColumns=2, parent = layout3, cw2 = [70,200])
    cmds.canvas("valueCanvas2", hsvValue=(0, 1, 1), width=70, height=15)
    cmds.floatSliderGrp("value2", field=True, label="Value", minValue=0, maxValue=1, fieldMinValue=0, fieldMaxValue=1, value=1,cw3 = [70,70,170], dc = valueChange2, step = 0.01)
    cmds.button(label = "Randomize", command = randomize, parent = layout3)
    layout4 = cmds.rowLayout(numberOfColumns=2, parent = layout0, cw2 = [690,110])
    cmds.button(label="Generate City", command = defaultButtonPush, parent = layout4, w = 685, h = 50)
    cmds.button(label="Clear Scene", command = clearScene, parent = layout4, w = 110, h = 50)
    cmds.showWindow()

def defaultButtonPush(args):
    '''
    Calls the procedure cityGenerator.city(...) with the user specified 
    arguments.
    
    args: Dummy argument needed to satisfy the command interface.
    On exit: The cityGenerator.city(...) procedure has been called with
             the arguments specified by the user. 
    '''
    Name_ = cmds.textField("cityName", query = True, text = True)
    if Name_ == "":
        Name_ = "Helsinki"
    cityWidth = cmds.intSliderGrp("cityWidth", query = True, value = True)
    cityDepth = cmds.intSliderGrp("cityDepth", query = True, value = True)
    minHeight = cmds.intSliderGrp("minHeight", query = True, value = True)
    maxHeight = cmds.intSliderGrp("maxHeight", query = True, value = True)
    minWidth = cmds.intSliderGrp("minWidth", query = True, value = True)
    maxWidth = cmds.intSliderGrp("maxWidth", query = True, value = True)
    windows = cmds.checkBoxGrp("features", query = True, v1 = True)
    booleans = cmds.checkBoxGrp("features", query = True, v2 = True)
    deformers = cmds.checkBoxGrp("features", query = True, v3 = True)
    dayTime = cmds.checkBoxGrp("time", query = True, v1=True)
    glow = cmds.checkBoxGrp("time", query = True, v3=True)
    environment = cmds.colorSliderGrp("environment", query = True, rgbValue = True)
    colourRangeStart = (cmds.intSliderGrp("hue1", query = True, value = True),
    cmds.floatSliderGrp("saturation1", query = True, value = True), 
    cmds.floatSliderGrp("value1", query = True, value = True))
    colourRangeEnd = (cmds.intSliderGrp("hue2", query = True, value = True),
    cmds.floatSliderGrp("saturation2", query = True, value = True), 
    cmds.floatSliderGrp("value2", query = True, value = True))
    cityGenerator.city(Name_, (cityWidth,cityDepth),(minHeight,maxHeight),
    (minWidth,maxWidth), windows, booleans, deformers, dayTime, glow, environment,(colourRangeStart,colourRangeEnd))    

def changeMaxHeight(args):
    '''
    Changes the maximum house height if it is smaller than the minimum house height.
    
    args: Dummy argument needed to satisfy the command interface.
    On exit: If the value of "maxHeight" was smaller than the value of 
             "minHeight", "maxHeight" has been changed to have the same value
             as "minHeight".
    '''
    minHeight = cmds.intSliderGrp("minHeight", query = True, value = True)
    maxHeight = cmds.intSliderGrp("maxHeight", query = True, value = True)
    if maxHeight < minHeight:
        cmds.intSliderGrp("maxHeight", edit = True, value = minHeight)

def changeMinHeight(args):
    '''
    Changes the minimum house height if it is larger than the maximum house height.
    
    args: Dummy argument needed to satisfy the command interface.
    On exit: If the value of "minHeight" was larger than the value of 
             "maxHeight", "minHeight" has been changed to have the same value
             as "maxHeight".
    '''
    minHeight = cmds.intSliderGrp("minHeight", query = True, value = True)
    maxHeight = cmds.intSliderGrp("maxHeight", query = True, value = True)
    if minHeight > maxHeight:
        cmds.intSliderGrp("minHeight", edit = True, value = maxHeight)

def changeMaxWidth(args):
    '''
    Changes the maximum house width so that it is at least 10 units larger 
    than the minimum house height.
    
    args: Dummy argument needed to satisfy the command interface.
    On exit: If the value of "maxWidth" was less than ten units larger than 
             the value of "minWidth", "maxWidth" has been changed to be ten 
             units larger than "minWidth"
    '''
    minWidth = cmds.intSliderGrp("minWidth", query = True, value = True)
    maxWidth = cmds.intSliderGrp("maxWidth", query = True, value = True)
    if maxWidth < (minWidth + 10):
        cmds.intSliderGrp("maxWidth", edit = True, value = minWidth + 10)

def changeMinWidth(args):
    '''
    Changes the minimum house width so that it is at least 10 units smaller 
    than the maximum house height.
    
    args: Dummy argument needed to satisfy the command interface.
    On exit: If the value of "minWidth" was less than ten units smaller than 
             the value of "maxWidth", "minWidth" has been changed to be ten 
             units smalle than "maxWidth"
    '''
    minWidth = cmds.intSliderGrp("minWidth", query = True, value = True)
    maxWidth = cmds.intSliderGrp("maxWidth", query = True, value = True)
    if minWidth > (maxWidth - 10):
        cmds.intSliderGrp("minWidth", edit = True, value = maxWidth - 10)
        
def windows(args):
    '''
    Changes the booleans checkbox to be disabled and unchecked when the windows 
    checkbox is unchecked.
    
    args: Dummy argument needed to satisfy the command interface.
    On exit: If the windows checkbox is checked the booleans checkbox has been enabled.
             If it is unchecked, the booleans checkbox has been unchecked and disabled.
    '''
    windows = cmds.checkBoxGrp("features", query = True, v1 = True)
    if windows == False:
        cmds.checkBoxGrp("features", edit = True, v2 = False, enable2 = False)
    else:
        cmds.checkBoxGrp("features", edit = True, enable2 = True)
        
def booleans(args):
    '''
    Opens a confirm window, to let the user know the risk of enabling booleans.
    
    args: Dummy argument needed to satisfy the command interface.
    On exit: If the booleans checkbox is checked, a window has been opened asking the
             user if he really wants to enabled the booleans. If the "Yes" button
             was pressed, the booleans checkbox remained checked and if the "No" button
             was pressed or if the window was dismissed, the booleans box has been unchecked.
    '''
    booleans = cmds.checkBoxGrp("features", query = True, v2 = True)
    if booleans == True:
        confirm = cmds.confirmDialog( title="Confirm", message="Enabling the booleans can cause" +
        " maya to crash for large cities that have houses with many windows. Are you sure you" + 
        " want enable them?", button=["Yes","No"], defaultButton="Yes", cancelButton="No", 
        dismissString="No" )
        if confirm == "No":
            cmds.checkBoxGrp("features", edit = True, v2 = False)

def nighttime(args):
    '''
    Changes the city image and the environment colour to match the daytime/nighttime 
    checkboxes. Also uncheckes the daytime checkbox when nighttime is checked and checkes
    it when nighttime is unchecked.
    
    args: Dummy argument needed to satisfy the command interface.
    On exit: If nighttime was checked, the daytime checkbox has been unchecked. The cityimage 
             has also been changed to a nighttime image and the environment colour updated to
             suit a nighttime city.
             If nighttime was unchecked, daytime has been checked and the image and environment
             colour has been updated accordingly.
    '''
    night = cmds.checkBoxGrp("time", query = True, v2 = True)
    if night == True:
        cmds.checkBoxGrp("time", edit = True, v1 = False, enable3 = True)
        imageNum = random.randint(1,15)
        cmds.image("cityImage", edit = True, image = "cityImages/nightImage" + str(imageNum) + ".jpg")
        cmds.colorSliderGrp("environment", edit = True, hsv = (204, 0.451, 0.054))
    else:
        cmds.checkBoxGrp("time", edit = True, v1 = True, v3 = False, enable3 = False)
        imageNum = random.randint(1,19)
        cmds.image("cityImage", edit = True, image = "cityImages/dayImage" + str(imageNum) + ".jpg")
        cmds.colorSliderGrp("environment", edit = True, hsv = (204, 0.451, 1))
    
def daytime(args):
    '''
    Changes the city image and the environment colour to match the daytime/nighttime 
    checkboxes. Also uncheckes the nighttime checkbox when daytime is checked and checkes
    it when daytime is unchecked.
    
    args: Dummy argument needed to satisfy the command interface.
    On exit: If daytime was checked, the  nighttime checkbox has been unchecked. The cityimage 
             has also been changed to a daytime image and the environment colour updated to
             suit a daytime city.
             If daytime was unchecked, nighttime has been checked and the image and environment
             colour has been updated accordingly.
    '''
    day = cmds.checkBoxGrp("time", query = True, v1 = True)
    if day == True:
        cmds.checkBoxGrp("time", edit = True, v2 = False, v3 = False,  enable3 = False)
        imageNum = random.randint(1,19)
        cmds.image("cityImage", edit = True, image = "cityImages/dayImage" + str(imageNum) + ".jpg")
        cmds.colorSliderGrp("environment", edit = True, hsv = (204, 0.451, 1))
    else: 
        cmds.checkBoxGrp("time", edit = True, v2 = True,  enable3 = True)
        imageNum = random.randint(1,15)
        cmds.image("cityImage", edit = True, image = "cityImages/nightImage" + str(imageNum) + ".jpg")
        cmds.colorSliderGrp("environment", edit = True, hsv = (204, 0.451, 0.054))
    
def hueChange1(args):
    '''
    Updates the canvas colours for the start of the colour range when the 
    hue is changed.
    
    args: Dummy argument needed to satisfy the command interface.  
    On exit: The hue, saturation and value canvases have been 
    updated to reflect the change in hue. 
    '''
    newHue = cmds.intSliderGrp("hue1", query = True, value = True)
    cur = cmds.canvas("valueCanvas1", query = True, hsvValue = True)
    cmds.canvas("hueCanvas1", edit = True, hsvValue = (newHue,1,1))
    cmds.canvas("saturationCanvas1", edit = True, hsvValue = (newHue, cur[1],1))    
    cmds.canvas("valueCanvas1", edit = True, hsvValue = (newHue, cur[1],cur[2]))    

    
def saturationChange1(args):
    '''
    Updates the canvas colours for the start of the colour range when the
    saturation is changed.
    
    args: Dummy argument needed to satisfy the command interface.   
    On exit: The saturation and value canvases have been updated
    to reflect the change in saturation.
    '''
    newSaturation = cmds.floatSliderGrp("saturation1", query = True, value = True)
    cur = cmds.canvas("valueCanvas1", query = True, hsvValue = True)
    cmds.canvas("saturationCanvas1", edit = True, hsvValue = (cur[0]*360, newSaturation,1))    
    cmds.canvas("valueCanvas1", edit = True, hsvValue = (cur[0]*360, newSaturation,cur[2]))    

    
def valueChange1(args):
    '''
    Updates the canvas colours for the start of the colour range when the 
    value is changed.
    
    args: Dummy argument needed to satisfy the command interface.
    On exit: The value canvas has been updated
    to reflect the change in value.
    '''
    newValue = cmds.floatSliderGrp("value1", query = True, value = True)
    cur = cmds.canvas("valueCanvas1", query = True, hsvValue = True)    
    cmds.canvas("valueCanvas1", edit = True, hsvValue = (cur[0]*360, cur[1],newValue))
    
def hueChange2(args):
    '''
    Updates the canvas colours for the end of the colour range when the hue
    is changed.
    
    args: Dummy argument needed to satisfy the command interface. 
    On exit: The hue, saturation and value canvases have been 
    updated to reflect the change in hue. 
    '''
    newHue = cmds.intSliderGrp("hue2", query = True, value = True)
    cur = cmds.canvas("valueCanvas2", query = True, hsvValue = True)
    cmds.canvas("hueCanvas2", edit = True, hsvValue = (newHue,1,1))
    cmds.canvas("saturationCanvas2", edit = True, hsvValue = (newHue, cur[1],1))    
    cmds.canvas("valueCanvas2", edit = True, hsvValue = (newHue, cur[1],cur[2]))    


    
def saturationChange2(args):
    '''
    Updates the canvas colours for the end of the colour range when the
    saturation is changed.
    
    args: Dummy argument needed to satisfy the command interface.  
    On exit: The saturation and value canvases have been updated
    to reflect the change in saturation.
    '''
    newSaturation = cmds.floatSliderGrp("saturation2", query = True, value = True)
    cur = cmds.canvas("valueCanvas2", query = True, hsvValue = True)
    cmds.canvas("saturationCanvas2", edit = True, hsvValue = (cur[0]*360, newSaturation,1))    
    cmds.canvas("valueCanvas2", edit = True, hsvValue = (cur[0]*360, newSaturation,cur[2]))    

    
def valueChange2(args):
    '''
    Updates the canvas colours for the end of the colour range when the value
    is changed.
    
    args: Dummy argument needed to satisfy the command interface.
    On exit: The value canvas has been updated
    to reflect the change in value.
    '''
    newValue = cmds.floatSliderGrp("value2", query = True, value = True)
    cur = cmds.canvas("valueCanvas2", query = True, hsvValue = True)    
    cmds.canvas("valueCanvas2", edit = True, hsvValue = (cur[0]*360, cur[1],newValue))

def randomize(args):
    '''
    Randomizes the hue, saturation and value for both the start
    and the end of the colour range.
    
    args: Dummy argument needed to satisfy the command interface.
    On exit: Random values for hue, saturation and value have been
    picked for both the start and the end of the colour range. The 
    canvases and the sliders have been updated accordingly.
    '''
    rhue1 = random.randint(0,360)
    rsaturation1 = random.uniform(0,1)
    rvalue1 = random.uniform(0,1)
    rhue2 = random.randint(0,360)
    rsaturation2 = random.uniform(0,1)
    rvalue2 = random.uniform(0,1)
    cmds.intSliderGrp("hue1", edit = True, value = rhue1)
    cmds.floatSliderGrp("saturation1", edit = True, value = rsaturation1)
    cmds.floatSliderGrp("value1", edit = True, value = rvalue1)
    cmds.canvas("hueCanvas1", edit = True, hsvValue = (rhue1,1,1))
    cmds.canvas("saturationCanvas1", edit = True, hsvValue = (rhue1, rsaturation1,1))    
    cmds.canvas("valueCanvas1", edit = True, hsvValue = (rhue1, rsaturation1,rvalue1)) 
    cmds.intSliderGrp("hue2", edit = True, value = rhue2)
    cmds.floatSliderGrp("saturation2", edit = True, value = rsaturation2)
    cmds.floatSliderGrp("value2", edit = True, value = rvalue2)
    cmds.canvas("hueCanvas2", edit = True, hsvValue = (rhue2,1,1))
    cmds.canvas("saturationCanvas2", edit = True, hsvValue = (rhue2, rsaturation2,1))    
    cmds.canvas("valueCanvas2", edit = True, hsvValue = (rhue2, rsaturation2,rvalue2)) 
    
def clearScene(arg):
    '''
    Deletes all objects and shaders in the scene.
    
    args: Dummy argument needed to satisfy the command interface.
    On exit: All objects and shaders in the scene have been deleted, and the active camera
             has been changed to the default "persp" camera.
    '''
    cmds.select(all = True)
    cmds.delete()
    cmds.lookThru("persp")
    
createGUI()

