import random

'''
List of procedures in the module:
    class Street:
        A Street object is a node in a binary tree that forms the street structure
        of the city.
        
        def __init__(self,split, minPoint, maxPoint):
            Initializes a Street object with the given parameters. 
        def listAreas(self, minPoint, maxPoint, list = []):
            Recursive procedure that creates a list of all the blocks formed by 
            the street structure.
        def split_(self, minPoint, maxPoint, maxSideLimit, minSideLimit):
            Procedure that creates a street structure by recursively splitting the city into
            rectangles.
        def splitRectangle(self, minPoint, maxPoint, minSideLimit, maxSideLimit):
            Creates a street that splits a rectangle in two.            
'''

class Street:
    '''
    A Street object is a node in a binary tree that forms the street structure
    of the city. The streets can either be horisontal (parallel with the x-axis)
    or vertical (parallel with the z-axis). 
    The root node of the tree splits the entire city in two rectangles. These
    rectangles may in turn be split by the children of the root. The grandchildren
    may then split their respective rectangles, and so on. The tree is constructed
    with the method split_(...). 
    
    Attributes:
        smaller: If not None, then it is an object of the class Street. This is the
                 child of self that represents the street splitting the rectangle
                 on the more negative side of self. 
        larger: If not None, then it is an object of the class Street. This is the
                 child of self that represents the street splitting the rectangle
                 on the more negative side of self. 
        split: This is a tuple containing a string with the direction of the street 
               ("horisontal" or "vertical") and the coordinate where the street splits the
               rectangle. If the direction is "horisontal" this is the z-coordinate for 
               the street, and if it is "vertical" it is the x-coordinate.
        start: Tuple with the coordinates for the start point of the street self.
        end: Tuple with the coordinates for the end point of the street self.
    
    '''
    def __init__(self,split, minPoint, maxPoint):
        '''
        Initializes a Street object with the given parameters. 
        
        self: Object that is to be intialized. 
        split: See attributes.
        minPoint: Tuple containing the minimum x- and z- coordinates of the
                  rectangle self is splitting.
        maxPoint: Tuple containing the maximum x- and z- coordinates of the
                  rectangle self is splitting.
        On exit: The Street object has been initialized with the correct parameters.
                 Note that both children are initialized as None.              
        '''
        self.smaller = None
        self.larger = None
        self.split = split 
        if (self.split[0] == "horisontal"):
            self.start = (minPoint[0], self.split[1])
            self.end = (maxPoint[0], self.split[1])
        else:
            self.start = (self.split[1], minPoint[1])
            self.end = (self.split[1], maxPoint[1])               

    def listAreas(self, minPoint, maxPoint, list = []):
        '''
        Recursive procedure that creates a list of all the blocks formed by 
        the street structure.
    
        self: An object of the class Street.
        minPoint: Tuple containing the minimum x- and z- coordinates of the
                  rectangle self is splitting.
        maxPoint: Tuple containing the maximum x- and z- coordinates of the
                  rectangle self is splitting.
        list: A list containing all the blocks that have already been listed.
        On exit: A list is returned that contains the bounding box coordinates
                 for every block in the city. Each element in the list is a 
                 tuple containing two tuples with the coordinates for the minimum
                 and the maximum points of the block. 
    '''
        if (self.smaller == None):
            list.append((minPoint,self.end))
        else:
            self.smaller.listAreas(minPoint, self.end, list)
        if (self.larger == None):
            list.append((self.start, maxPoint))
        else:
            self.larger.listAreas(self.start, maxPoint, list)
        return list
        
    def split_(self, minPoint, maxPoint, maxSideLimit, minSideLimit):
        '''
        Procedure that creates a street structure by recursively splitting the city into
        rectangles.

        self: Object of the class Street.
        minPoint: Tuple containing the minimum x- and z- coordinates of the
                  rectangle self is splitting.
        maxPoint: Tuple containing the maximum x- and z- coordinates of the
                  rectangle self is splitting.
        maxSideLimit: The maximum side length for the final rectangles.
        minSideLimit: The minimum side length for the final rectangles.
        On exit: A binary tree has been created with the self argument 
                 in the first procedure call as the root node. This tree 
                 forms the street structure for the city.
        '''
        self.smaller = self.splitRectangle(minPoint, self.end, minSideLimit, maxSideLimit)
        if self.smaller != None:
            self.smaller.split_(minPoint, self.end, maxSideLimit, minSideLimit)
        self.larger = self.splitRectangle(self.start, maxPoint, minSideLimit, maxSideLimit) 
        if self.larger != None:
            self.larger.split_(self.start, maxPoint, maxSideLimit, minSideLimit)
        
    def splitRectangle(self, minPoint, maxPoint, minSideLimit, maxSideLimit):
        '''
        Creates a street that splits a rectangle in two.
        
        self: Object of the class Street.
        minPoint: Tuple containing the minimum x- and z- coordinates of the
                  rectangle that is to be split by the new street.
        maxPoint: Tuple containing the maximum x- and z- coordinates of the
                  rectangle that is to be split by the new street.
        maxSideLimit: The maximum side length for the final rectangles.
        minSideLimit: The minimum side length for the final rectangles.
        On exit: A new Street object has been initialized to split the given
                 rectangle. With a probability of 80% the rectangle is split
                 across its longer side. A side will not be split if it is 
                 already shorter than the maximum side length.
        '''
        width = maxPoint[0] - minPoint[0]
        depth = maxPoint[1] - minPoint[1]
        if width <= maxSideLimit and depth <= maxSideLimit: 
            return None
        startSplitRange = minPoint[0]
        endSplitRange = maxPoint[0]
        dir = "vertical"
        if (width > maxSideLimit and depth > maxSideLimit):
            prob = random.random()
            if (prob > 0.8 and width >= depth) or (prob <= 0.8 and width < depth):  
                startSplitRange = minPoint[1]
                endSplitRange = maxPoint[1]
                dir = "horisontal"            
        elif (depth > maxSideLimit):
            startSplitRange = minPoint[1]
            endSplitRange = maxPoint[1]
            dir = "horisontal"     
        splitValue = random.uniform(startSplitRange + minSideLimit, endSplitRange - minSideLimit)                          
        return Street((dir, splitValue), minPoint, maxPoint)
        

