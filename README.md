How to run the city generator script:

1. Copy over the folder cityGenerator to your maya scripts folder. 

2. Copy over the folder cityImages to your maya prefs/icons folder.

3. Open the file cityGui.py in your script editor and run it. 

How to use:

After you run the script a GUI window will open. Specify how you want the
city to look, and press "Generate City". If you want to clear your scene,
press "Clear Scene". This will clear all elements in your scene, not only
the generated city. Below is an explanation of all the controls in the 
user interface.

City name: The name of the city. Certain objects in the scene will
	be named based on this. If no name is given the city will have
	the default name "Helsinki".
City width & City depth: Specify the size of the city in x- and 
	z-direction.
Minimum house height & maximum house height: Determine the maximum
	and the minimum height the houses in the city can have.
Minimum house width & maximum house width: Determine the maximum
	and the minimum width the houses in the city can have. Note that
	the maximum width is always at least 10 units larger than the
	minimum width. 
Windows: Specifies whether the houses in the city should have windows.
Booleans: Determines if the windows should be attached to the house 
	using boolean difference or by simply combining the meshes. 
	If the booleans are enabled it gives a nicer result, but there 
	is a chance that maya will crash if large cities are created, 
	or if many cities are generated during the same maya session. 
	This is due to maya not beeing able to perform too many boolean 
	operations.
Deformers: Determines if deformers should be added to the houses.
Daytime & Nigttime: Allows the user to decide if the generated city 
	should be a daytime or a nighttime city.
All windows glow: If nighttime is checked, this determines whether all
	of the windows in the city should glow, or if some of them should
	be dark.
Environment colour: Sets the colour of the environment. The background for
	for the camera will be set to have this colour, and during 
	daytime the windows will also have the same colour.
Colour range sliders: Determines the range for the hue, saturation and 
	value of the colours the houses will have. It is possible to set 
	a higher value for the start of the range than for the end of the 
	range. If the start point for the hue range is set to 120 for 
	example and the end point is set to 40 the colours will have hues 
	between 0 and 40, and between 120 and 360.
Randomize: Randomizes the ranges for the hue, saturation and value.
 