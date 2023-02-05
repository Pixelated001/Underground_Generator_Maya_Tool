'''

Randomly Generated Terrain
This program contains 5 major Functions:
    1. Creation of GUI and user inputs data 
    2. Adding constraints to tiles on the border
    3. Checking Bordering Tiles
    4. Placing Blcoks
    5. Train animation
    
'''

import maya.cmds as cmds
import functools
import random as rand
import math

class Block:
    
    def __init__(self, Object, Borders, Probability, Diffrence, PathList):
        
        '''
    
        Stores the information for a block to be placed on a Tile
        
        Object       : The name of the tile in the outliner
        Borders      : A array of the values assigned to each edge of the Block in order x-, top left, y+, top right, x+, bottom right, y-, bottom left
        Rotation     : The possible rotation of the Block ([0, 2, 4, 6] because when rotated the array shift by 2 places due to corners)
        Probability  : Stores the probability of the Block being chosen
        Diffrence    : The value that effects if a Block is more likely to be chosen the closer to the center the tile is
        PathList     : A list contining the possible paths a train could take on that Block 
        
        '''
        
        self.Object = Object 
        self.Borders = Borders 
        self.Rotation = [0,2,4,6]  
        self.Probability = Probability
        self.Diffrence = Diffrence
        self.PathList = [PathList]
        
    def remove_Rotation(self, Rotation): 
        
        '''
        
        Removes a rotation value from the array if it isnt possible anymore
        
        Rotation : The index of the rotation value to be removed
        
        '''
        
        self.Rotation.pop(Rotation) 
        

class Tile:
    
    def __init__(self, Possible_all, Picked):
        
        '''
        
        Stores the information for the tile
        
        Possible_all   : A array containing all of the possible Blocks for that Tile
        Constraint_all : A array containing all the border constraints bassed on neighbouring Tiles
        Picked         : Determins if a Block has been placed on the Tile         
        
        '''
        
        self.Possible_all = Possible_all[:]
        self.Constraint_all = [0,0,0,0,0,0,0,0] 
        self.Picked = Picked
    
    def remove_Possible(self, Possible):
        
        '''
        
        Removes a Block from the possible List if it isnt possible
        
        Possible : The index of the Block to be removed from the array 
        
        '''
        
        self.Possible_all.pop(Possible)
    
    def add_Constraint(self, Index, Constraint):
        
        '''
        
        Adds the new constraint value to the array in the correct index
        
        Index      : The index to add the new constraint
        Constraint : The Constraint to be added   
        
        '''
        
        self.Constraint_all.pop(Index)
        self.Constraint_all.insert(Index, Constraint)
        
class Train:
    
    def __init__(self, TrainName, Current):
        
        '''
        
        Contains all the information for a Train
        
        TrainName     : The name of the TrainMesh in the outliner
        Current       : The current tile the train is on
        Future        : The next tile the train is moving to 
        FutureBorder  : The border index the train will leave by
        CurrentBorder : The border index the train entered the tile 
        Time          : The current time the train is at in the timeline
        Speed         : The speed the train travels along the path        
        
        '''
        
        self.TrainName = TrainName
        self.Current = Current
        self.Future = "" 
        self.FutureBorder = ""
        self.CurrentBorder = ""
        self.Time = 0
        self.Speed = 1.0 
        
class Answers:
    
    def __init__(self):        
        
        '''
        
        Contains the users input for a custom Block
        
        CustomBlocks  : A array that stores all of the information for each of the custom Blocks
        Add_Name      : The name of the custom block
        Add_Border    : An array containing all borders for a custom Block
        Add_Prob      : The user inputted probability for the custom Block
        Add_Diffrence : The diffrence value for each Block
        Add_Path      : A array containing each of the names for each path on that Block        
        
        '''
        
        self.CustomBlocks = []
        self.Add_Name = 0
        self.Add_Border = 0
        self.Add_Prob = 0
        self.Add_Diffrence = 0
        self.Add_Path = 0 
   
    def ArrayFormat(self):     
       
        '''
        
        Converts the string values for Paths and Border into arrays and then appends all of the Block information into an array to be stores in CustomBlocks
        
        arrayTmp     : The temp array to format all of the Block information before adding it to array
        Path_array   : The array that contains the paths that have been converted from string to array
        Border_Array : The array that contains the borders in form of array not string
        word         : The array that contains 1 border to be added to the Border_Array
        CustomBlocks : A array that stores all of the information for a each of the custom blocks         
        
        '''
        
        arrayTmp = []
        Path_array = []
        
        for x in range(len(self.Add_Path)):
            if x % 4 == 0:
                Path_array.append(self.Add_Path[x:x+3])
                
        for x in range(len(Path_array)):
            if cmds.objExists(Path_array[x]) == False and Path_array[x] != "":
                print(Path_array[x] + " this path does not exist!")
                self.addMeshesV2()
                return 0
                
        
        
        Border_Array = []
        word = []
        for letter in range(len(self.Add_Border)):
            if self.Add_Border[letter] == " ":
                Border_Array.append(word)
                word = []
                continue
            elif letter == (len(self.Add_Border)-1):
                if len(word)==1:
                    word[0] = (word[0] + self.Add_Border[letter])
                else:
                    word.append(self.Add_Border[letter])
                Border_Array.append(word)
                break 
            if len(word)==1:
                word[0] = (word[0] + self.Add_Border[letter])
            else:
                word.append(self.Add_Border[letter])           
        
        if len(Border_Array) != 8:
            print("There should be 8 values for the border")
            self.addMeshesV2()
            return 0
            
        
        arrayTmp.append(self.Add_Name)
        arrayTmp.append(Border_Array)
        arrayTmp.append(self.Add_Prob)
        arrayTmp.append(self.Add_Diffrence)
        arrayTmp.append(Path_array)
        
        self.CustomBlocks.append(arrayTmp)
                  
    
    def Values(self, pName, pBorder, pProb, pDiffrence, pPath):

        '''
        
        Takes the values that the user inputted into these GUI systems and assigns them to variables
        
        Add_Name      : The name of the custom block
        Add_Border    : An string containing all of the users inputted borders
        Add_Prob      : The user inputted probability
        Add_Diffrence : The diffrence value for each block
        Add_Path      : A array containing each of the names for each path on that Block 
        
        ArrayFormat() : Converts the string values for Paths and Border into arrays and then appends all of the Block information into an array to be stores in CustomBlocks
        
        '''
        
        
        self.Add_Name = str(cmds.textFieldGrp( pName, query=True, text = True))
        if cmds.objExists(self.Add_Name) == False:
            print(self.Add_Name + " cant be found!")
            self.addMeshesV2()
            return 0           
        
        self.Add_Border = str(cmds.textFieldGrp( pBorder, query=True, text = True))        
        self.Add_Prob = int(cmds.intFieldGrp(pProb, query=True, value=True)[0])
        if self.Add_Prob < 1 or self.Add_Prob > 100:
            print(str(self.Add_Prob) + "This value is to high (max is 100) or low (min is 1)")
            self.addMeshesV2()
            return 0
            
        self.Add_Diffrence = float(cmds.floatFieldGrp(pDiffrence, query=True, value=True)[0])
        if self.Add_Diffrence > 2 or self.Add_Diffrence < 0:
            print(str(self.Add_Diffrence) + " this value is to high (max is 2) or low (min is 0)")
            self.addMeshesV2()
            return 0
        self.Add_Path = str(cmds.textFieldGrp(pPath, query=True, text = True))
        
        self.ArrayFormat()
        
    def addMeshesV2(self):
        
        '''
        
        Creates a window and inputs GUI elements for the user to input values for there Custom Block
        
        window    : The window created to hold the GUI elements
        Name      : Stores the GUI element to enter name
        Border    : Stores the GUI element to enter Border
        Prob      : Stores the GUI element to enter Prob
        Diffrence : Stores the GUI element to enter Diffrence
        Path      : Stores the GUI element to enter Path 
        
        '''
    
        windowID1 = "Custom"
        
        if cmds.window(windowID1, exists=True):
            cmds.deleteUI(windowID1)
        
        cmds.window(windowID1, widthHeight=(400, 300))
        
        cmds.columnLayout( adjustableColumn=True )
        Name = cmds.textFieldGrp( label='Name')
        Border = cmds.textFieldGrp( label='Border' )
        Prob = cmds.intFieldGrp( label='Probabilty')
        Diffrence = cmds.floatFieldGrp( label='Diffrence' )
        Path = cmds.textFieldGrp( label='Path' )
    
        cmds.button(label = "Add", command = lambda x: self.Values(Name, Border, Prob, Diffrence, Path) ) 
        
        cmds.button(label = "Finish", command = lambda *args: cancelProc(window))
        
        cmds.showWindow( )
        
        cmds.window(windowID1, e=True, widthHeight=(400, 300)) 


def actionProc(windowID, width, height, MeshTypes, CustomBlocks, Time):
    
    '''
    
    Closes the inputted window and runs the main Program    
    
    windowID  : Refrence to the window    
    width     : The user inputed value from the GUI for the width of the Board    
    height    : The user inputed value from the GUI for the height of the Board    
    MeshTypes : Stores 1 2 3. 1 is for train track to be generated, 2 is for Environment and 3 is for custom    
    array     : A array storing the Custom blocks
    
    main() : The main function of the program   
    
    '''
    
    if int(width[0]) < 1 or int(height[0]) < 1 or int(width[0]) > 20 or int(height[0]) > 20:
        print("Please enter a width or height between 1 and 20")
        createUI()
        return
    if int(Time[0]) < 0:
        print("Time must be higher then 0")
        createUI()
        return
        
    if MeshTypes == 0:
        print("Please select a Block mesh")
        createUI()
        return
        
    if MeshTypes == 1 or MeshTypes == 2:            
        if cmds.objExists("Block") == False:
            print("please import the Defult Models")  
            createUI()
            return
            
        if cmds.objExists("StraightGroup") == False:
            print("please import the Defult Models")  
            createUI()
            return   
    
    main(width, height, MeshTypes, CustomBlocks, Time) 
    
def cancelProc(windowID, *pArgs):
    
    '''
    
    Closes the inputed window
    
    windowID : Refrence to the window
    
    '''
    
    cmds.deleteUI(windowID)

def createUI():
    
    '''
    
    Creates the main window of my GUI to take information before calling main()
    
    windowID : Refrence to the window created
    
    Answers1.addMeshesV2() : Called if the custom Block button pressed for the user to add there own custom Blocks
    
    '''
    
    windowID = "Generator"
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
        
    cmds.window(windowID, title="Random Terain Generator",sizeable = False, widthHeight=(300, 527) )
    cmds.columnLayout( adj=True )
    imagePath = cmds.internalVar(upd = True) +"icons/v2.jpg"
    
    #User needs to change this directory to there own
    location = "C:/Users/matth/OneDrive/Desktop"
    cmds.image( image= location + "/Matthew_Fraser_Scripting/artefacts/Textures/Front_Image.JPG" )
    
    cmds.separator(h =10)
    cmds.text("Radom Terrain Generator")
    cmds.separator(h =10)
    
    Width = cmds.intFieldGrp( label='Width')
    Height = cmds.intFieldGrp( label='Height')
    Answers1 = Answers()
    MeshTypes = cmds.radioButtonGrp( label='Block Meshs', labelArray3=['Train Track', 'Environment', 'Custom'], numberOfRadioButtons=3, onCommand3 = lambda x: Answers1.addMeshesV2(), vertical = True )
    Time = cmds.intFieldGrp( label='Animation length' )
    cmds.button(label = "Run", command = lambda *args: actionProc(windowID, cmds.intFieldGrp( Width,  query=True, value=True), cmds.intFieldGrp( Height,  query=True, value=True), cmds.radioButtonGrp( MeshTypes, query=True, select=True), Answers1.CustomBlocks, cmds.intFieldGrp( Time,  query=True, value=True)) )
    cmds.button(label = "Import Defult Models", command = lambda *args: ImportModels())
    cmds.button(label = "Cancel", command = lambda *args: cancelProc(windowID))
    
    cmds.showWindow(windowID ) 
    cmds.window(windowID, e=True, width=300, height=527) 

def ImportModels():
    
    '''
    
    Imports the models from my main maya file into the current file
    
    '''
   
    #User needs to change this directory to there own
    location = "C:/Users/matth/OneDrive/Desktop"
    cmds.file(new=True, force=True)
    cmds.file(location + "/Matthew_Fraser_Scripting/artefacts/MayaScene/Block_Meshs_Scene.mb", i=True)
    



def Inputed_Tiles():
    
    '''
    
    Contains a List with all of the Blocks in to generate train tracks 
    
    return : The list full of Blocks  
    
    '''  
    
    list = []
    list.append( Block("StraightGroup",         (1,2,2,2,1,2,2,2), 10 , 1.1, ("P04", "")           ) )
    list.append( Block("AngleGroup",            (1,2,2,2,2,2,1,2), 10 , 1.1, ("P06", "")           ) )
    list.append( Block("EmptyGroup",            (2,2,2,2,2,2,2,2), 1  , 0.8, ("")                  ) )
    list.append( Block("StationGroup",          (1,2,2,2,2,2,2,2), 25  , 2  , ("P0")               ) )        
    list.append( Block("DiaganalGroup",         (2,1,2,2,2,1,2,2), 10 , 1.1, ("P15", "")           ) )        
    list.append( Block("Curve1Group",           (1,2,2,2,2,1,2,2), 10 , 1.1, ("P05", "")           ) )        
    list.append( Block("Curve2Group",           (1,2,2,1,2,2,2,2), 10 , 1.1, ("P03", "")           ) )
    list.append( Block("DiaganalStationGroup",  (2,1,2,2,2,2,2,2), 1  , 2  , ("P1")                ) )
    list.append( Block("BranchGroup",           (2,1,2,2,2,1,1,2), 50 , 1.1, ("P16", "P65", "P15") ) )
    list.append( Block("Branch1Group",          (1,1,2,2,2,1,2,2), 50 , 1.1, ("P01", "P05", "P15") ) )
    list.append( Block("TwoIntoOneGroup",       (2,1,2,2,1,2,2,1), 10 , 1.1, ("P17", "P74", "P14") ) )
    list.append( Block("StraightCorner1Group",  (1,2,2,2,1,2,2,1), 10 , 1.1, ("P74", "P07", "P04") ) )
    list.append( Block("StraightCorner2Group",  (1,2,2,2,1,1,2,2), 10 , 1.1, ("P05", "P54", "P04") ) )
    list.append( Block("DiaganalCornerGroup",   (2,1,2,1,2,1,2,2), 10 , 1.1, ("P13", "P35", "P15") ) )
    return list


def Inputed_Tiles1():
    
    '''
    
    Contains list with blocks to generate environment 
    
    return : The list full of Blocks  
    
    '''    
    
    list = []
    list.append( Block("Block",       (1,1,1,1,1,1,1,1), 10 , 1, ("") ) )
    list.append( Block("Corner",      (2,2,2,2,1,1,1,2), 10 , 1, ("") ) )
    list.append( Block("Wall_Ground", (2,2,1,1,1,1,1,2), 10 , 1, ("") ) )                
    list.append( Block("RightAngle",  (1,2,1,1,1,1,1,1), 10 , 1, ("") ) )        
    list.append( Block("Empty1",      (2,2,2,2,2,2,2,2), 1  , 1, ("") ) )
    return list
    
    
def Inputed_Tiles2(array):
    
    '''
    
    Contains list with blocks to generate environment, blocks that where stated as custom in the UI
    
    return : The list full of Blocks  
    
    '''    
    
    list = []
    for x in range(len(array)):
        list.append( Block(array[x][0], (int(array[x][1][0][0]), int(array[x][1][1][0]), int(array[x][1][2][0]), int(array[x][1][3][0]), int(array[x][1][4][0]), int(array[x][1][5][0]), int(array[x][1][6][0]), int(array[x][1][7][0])), array[x][2], array[x][3], array[x][4] ) )
    return list    
    

    
    
def Border_Constraints(x, Board, width, height, Environment):
    
    '''
    
    Adds Constraint values to tiles on the borders of the Board so that tracks dont run of the side of the Board.
    If the user has chosen to generate a environment then it adds constraints to the floor to make sure there is only ground
    
    x           : The index of the Tile
    Board       : A array containing all of the Tiles
    width       : The width of the Board 
    height      : The height of the Board
    Environment : Bool to determine if Environment has been chosen  
    
    '''    
    
    # If the Tile is at the top of the Board
    if (x < width):
        Board[x].add_Constraint(2, 2)
        Board[x].add_Constraint(1, 2)
        Board[x].add_Constraint(3, 2)
        check(Board, x)
    # If the Tile is at the Bottom of the Board
    if (x >= ((width*height) - width)): 
        if Environment == 1:        
            Board[x].add_Constraint(6, 1)
            Board[x].add_Constraint(5, 1)
            Board[x].add_Constraint(7, 1)
            check(Board, x)
        else:
            Board[x].add_Constraint(6, 2)
            Board[x].add_Constraint(5, 2)
            Board[x].add_Constraint(7, 2)
            check(Board, x)
    # If the Tile is on the Left of the Board
    if (x%width == 0):
        if (x >= ((width*height) - width) and Environment == 1):
            Board[x].add_Constraint(0, 1)
            Board[x].add_Constraint(1, 2)
            Board[x].add_Constraint(7, 1)
            check(Board, x)
        else:             
            Board[x].add_Constraint(0, 2)
            Board[x].add_Constraint(1, 2)
            Board[x].add_Constraint(7, 2)
            check(Board, x)
    # If the Tile is on the right of the Board
    if (x%width == width-1):
        if (x >= ((width*height) - width) and Environment == 1):
            Board[x].add_Constraint(4, 1)
            Board[x].add_Constraint(3, 2)
            Board[x].add_Constraint(5, 1)
            check(Board, x)
        else:            
            Board[x].add_Constraint(4, 2)
            Board[x].add_Constraint(3, 2)
            Board[x].add_Constraint(5, 2)
            check(Board, x)
            
def check(Board, input): 
    
    '''
    
    Loops through all of the Possible Borders for a Tile and checks if the Block can be placed at the tile by comparing the Blocks borders against the Constraint on the tile and repeating for each possible rotation.
    If the Rotation of the Block is not possible at that tile then it calls the function in the Block class to remove that rotation form the array.
    If no Rotations are possible then it calls the function in the Tile class to remove that Block from the Possible_all array
    
    Board : A array containing all of the Tiles
    input : The index of tile being checked
    b     : The offset needed if a Block is removed from the array as the length of the array has changed
    x     : The number of succsesfull comparisons between the Blocks Border and Constraints 
    f     : The offset needed if a Rotation is removed from the array as the length of the array has changed
    
    '''    
    
    b = 0
    for y in range(len(Board[input].Possible_all)):      
        y = y - b
        f = 0
        for i in range(len(Board[input].Possible_all[y].Rotation)):
            i = i - f
            x = 0
            for z in range(len(Board[input].Possible_all[y].Borders)*2):
                if Board[input].Possible_all[y].Borders[(Board[input].Possible_all[y].Rotation[i]+z)%8] == Board[input].Constraint_all[z] or Board[input].Constraint_all[z] == 0:
                    x = x+1
                else:
                    Board[input].Possible_all[y].remove_Rotation(i)
                    f = f + 1
                    break
                if (x == len(Board[input].Possible_all[y].Borders)):
                    break
        if len(Board[input].Possible_all[y].Rotation) == 0:
            Board[input].remove_Possible(y)
            b = b + 1 
            
        
def Random_Tile_Pick(Lowest, Board, width, height):
    
    '''
    
    Selects a random Tile out of all the Tiles with the least choice in the Board and assigns it a Block determined by my random() function and a random possible rotation and turns Picked to true
    
    Lowest   : A array that keeps record of all the Tiles with the lowest amount of Possible Blocks. The first value contains the number of Blocks possible for all of the index that follow
    random   : A random index with in the length of Lowest 
    Board    : A array containing all of the Tiles
    width    : The width of the Board 
    height   : The height of the Board
    
    Random() : Picks a random Block from the possible Blocks that can be placed at that tile. Takes into account probability of each tile when picking randomly and the diffrence based on how far the Tile is from the center of the Board
    
    return : The function returns the index of the Lowest array that was chosen
    
    '''    
    
    # If this is the first Tile pick then it just picks a random Tile index and assigns it to the array 
    if len(Lowest) == 0:
        Lowest.append("")
        Lowest.append(rand.randint(0, (width*height)-1)) 
        random = 1
    else:
        random = rand.randint(1, (len(Lowest)-1))
        
    if(len(Board[Lowest[random]].Possible_all) == 0):
        print(Board[Lowest[random]].Constraint_all)
    
    Board[Lowest[random]].Possible_all = [Random(Board[Lowest[random]], Lowest[random], width)]    
    Board[Lowest[random]].Picked = 1    
    Board[Lowest[random]].Possible_all[0].Rotation = [Board[Lowest[random]].Possible_all[0].Rotation[rand.randint(0, len(Board[Lowest[random]].Possible_all[0].Rotation)-1)]]   
    
    return random
    
    
def Tile_Checker(Lowest, Board, width, height, random, Environment):
    
    '''
    
    Checks all of the Tiles bordering a Tile thats just been assigned a Block and assigns them a Constraint on the border they share (also checks diagonals as well as up, down, right, left)
    Before it adds a constraint it checks to see if the Tile is on a Border and in that case skip becuase it cant add a constraint to a Tile the is out of the Board relative to the direction its checking.
    It also checks if the Border tile has been picked before because if it has there is no point adding a constraint to it.
    Then calls check() to see if the newly added constraint value on the bordering Tile has reduced any of there possible blocks.
    
    Lowest      : A array that keeps record of all the Tiles with the lowest amount of Possible Blocks. The first value contains the number of Blocks possible for all of the index that follow
    Board       : A array containing all of the Tiles
    width       : The width of the Board 
    height      : The height of the Board    
    random      : The index of the Tile which has just had a Block placed
    Environment : Bool to determine if Environment has been chosen       
    
    '''
       
    # Checks if the Tile is on the left Border
    if (Lowest[random])% width != 0 and Board[Lowest[random]-1].Picked != 1:          
        
        if Board[Lowest[random]].Possible_all[0].Borders[ ( 0 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] is str:
            if 'a' in Board[Lowest[random]].Possible_all[0].Borders[ ( 0 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ]:
                array[x] = array[0][0] + 'b'
            if 'b' in array[0]:
                array[x] = array[0][0] + 'a'
                
        
        Board[Lowest[random]-1].add_Constraint(4, Board[Lowest[random]].Possible_all[0].Borders[ ( 0 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] ) # below 
                
        if Environment == 1:
            
            Board[Lowest[random]-1].add_Constraint(3, Board[Lowest[random]].Possible_all[0].Borders[ ( 1 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] ) # above left
            
            Board[Lowest[random]-1].add_Constraint(5, Board[Lowest[random]].Possible_all[0].Borders[ ( 7 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] ) # below left        
                 
        
        check(Board, Lowest[random]-1)
    
    
    # Checks if the Tile is on the right Border
    if (Lowest[random])% width != (width-1) and Board[Lowest[random]+1].Picked != 1: 
        
        Board[Lowest[random]+1].add_Constraint(0, Board[Lowest[random]].Possible_all[0].Borders[ ( 4 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] )# forward
        
        
        if Environment == 1:
            
            Board[Lowest[random]+1].add_Constraint(1, Board[Lowest[random]].Possible_all[0].Borders[ ( 3 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] ) # above right
        
            Board[Lowest[random]+1].add_Constraint(7, Board[Lowest[random]].Possible_all[0].Borders[ ( 5 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] ) # below right
        
               
        check(Board, Lowest[random]+1)
    
    
    # Checks if the Tile is on the bottom Border
    if (Lowest[random]+width) < (width*height) and Board[Lowest[random]+width].Picked != 1:   
        
        Board[Lowest[random]+width].add_Constraint(2, Board[Lowest[random]].Possible_all[0].Borders[ ( 6 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] ) # below 
        
        
        if Environment == 1:
            
            Board[Lowest[random]+width].add_Constraint(1, Board[Lowest[random]].Possible_all[0].Borders[ ( 7 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] ) # below left
        
            Board[Lowest[random]+width].add_Constraint(3, Board[Lowest[random]].Possible_all[0].Borders[ ( 5 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] ) # below right
             

        check(Board, Lowest[random]+width)
    
    
    # Checks if the Tile is on the top Border
    if (Lowest[random]-width) >= 0 and Board[Lowest[random]-width].Picked != 1:
        
        Board[Lowest[random]-width].add_Constraint(6, Board[Lowest[random]].Possible_all[0].Borders[ ( 2 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] ) # above
        
        
        if Environment == 1:
            
            Board[Lowest[random]-width].add_Constraint(7, Board[Lowest[random]].Possible_all[0].Borders[ ( 1 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] ) # above left
        
            Board[Lowest[random]-width].add_Constraint(5, Board[Lowest[random]].Possible_all[0].Borders[ ( 3 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] ) # above right
        
                    
        check(Board, Lowest[random]-width)
        
    
    # Checks if the Tile is not on the top or right border because its adding constraint top right direction
    if (Lowest[random]-width) >= 0 and (Lowest[random])% width != width-1 and Board[(Lowest[random]-width)+1].Picked != 1: # above right
    
        Board[(Lowest[random]-width)+1].add_Constraint(7, Board[Lowest[random]].Possible_all[0].Borders[ ( 3 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] )
        
        check(Board, (Lowest[random]-width)+1)
    
    # Checks if the Tile is not on the top or left border because its adding constraint top left direction
    if (Lowest[random]-width) >= 0 and (Lowest[random])% width != 0 and  Board[(Lowest[random]-width)-1].Picked != 1: # above left
    
        Board[(Lowest[random]-width)-1].add_Constraint(5, Board[Lowest[random]].Possible_all[0].Borders[ ( 1 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] )
        
        check(Board, (Lowest[random]-width)-1)
    
    # Checks if the Tile is not on the bottom or right border because its adding constraint top right direction
    if (Lowest[random]+width) < (width*height) and (Lowest[random])% width != (width-1) and Board[(Lowest[random]+width)+1].Picked != 1: # below right
    
        Board[(Lowest[random]+width)+1].add_Constraint(1, Board[Lowest[random]].Possible_all[0].Borders[ ( 5 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] )
        
        check(Board, (Lowest[random]+width)+1)
    
    # Checks if the Tile is not on the bottom or left border because its adding constraint top right direction
    if (Lowest[random]+width) < (width*height) and (Lowest[random])% width != 0 and Board[(Lowest[random]+width)-1].Picked != 1: # below left
    
        Board[(Lowest[random]+width)-1].add_Constraint(3, Board[Lowest[random]].Possible_all[0].Borders[ ( 7 + Board[Lowest[random]].Possible_all[0].Rotation[0] ) % 8 ] )
        
        check(Board, (Lowest[random]+width)-1)
        
                
def Move_Tiles(StationList, Lowest, random, Board, width):
    
    '''
    
    Creates a instance of the only possible block and moves it relative to its possition in the Board array then Rotates relative to the only Rotation value left
    If the object i add i to an array to be used when dealing with trains
    
    StationList : A List containing all the index's of the Station Tiles
    Lowest      : A array that keeps record of all the Tiles with the lowest amount of Possible Blocks. The first value contains the number of Blocks possible for all of the index that follow
    random      : The index of the Tile which has just had a Block placed
    Board       : A array containing all of the Tiles
    width       : The width of the Board
    
    '''
    
    mesh = cmds.instance(Board[Lowest[random]].Possible_all[0].Object)
        
    if Board[Lowest[random]].Possible_all[0].Object == "StationGroup" or Board[Lowest[random]].Possible_all[0].Object == "DiaganalStationGroup":
        StationList.append(Lowest[random]) 
    
    Board[Lowest[random]].Possible_all[0].Object = mesh[0]
    
    cmds.move(Lowest[random] % width , 0 , round(Lowest[random] / width), mesh)        
    cmds.rotate(0, (90 * ((Board[Lowest[random]].Possible_all[0].Rotation[0])/2)), 0, mesh, os=True) 
    cmds.showHidden(mesh)        
    cmds.select(mesh, add=True)
    
    cmds.refresh()


def Lowest_Tile(Lowest, Board, width, height):   
        
    '''
    
    Checks all of the Tiles on the Board and searches for the tiles with the lowest number of possible Blocks
    
    Lowest   : A array that keeps record of all the Tiles with the lowest amount of Possible Blocks. The first value contains the number of Blocks possible for all of the index that follow
    Board    : A array containing all of the Tiles
    width    : The width of the Board 
    height   : The height of the Board
    x        : The index of the Tile in Board
    
    '''   
    
    for x in range(width*height):           
        if Board[x].Picked == 1:
            continue            
        # If its the first Loop just add the first tile's information
        elif len(Lowest) == 0:
            Lowest.append(len(Board[x].Possible_all)) 
            Lowest.append(x) 
            continue                
        # If the the Tile has same number as possibilites as the lowest then add to array
        if len(Board[x].Possible_all) == Lowest[0]:
            Lowest.append(x)
            continue
        # If the Tile being checked has less possibilites then clear array add new lowest block value and add the index after
        if len(Board[x].Possible_all) < Lowest[0]:
            del Lowest[:]
            Lowest.append(len(Board[x].Possible_all))
            Lowest.append(x)
            continue
        else:
            continue           


def Random(Tile, Location, width):
    
    '''
    
    Picks a random Block from the possible Blocks that can be placed at the tile index inputted. Takes into account probability of each tile when picking randomly and the diffrence based on how far the Tile is from the center of the Board
    
    Tile            : The Tile information
    Location        : The index of the Tile in Board
    width           : The width of the Board
    RandomSelection : A array to contain multiple Blocks dependant on the Probability value becuase the imported modeule random doesnt have a weighted function
    
    returns : The randomly selected Block
    
    '''   
    
    RandomSelection = []
    
    CenterLocation = (abs( math.floor(width / 2) - ( Location % width) ) + abs( math.floor(width / 2) - (Location / width))) + 1
    
    for x in range(len(Tile.Possible_all)):

        RandomSelection.extend([Tile.Possible_all[x]] * int(math.ceil(Tile.Possible_all[x].Probability / ((Tile.Possible_all[x].Diffrence ** CenterLocation))))) 
        
    return rand.choice(RandomSelection)
    

def main(Width, Height, MeshTypes, array, time):
    
    '''
    
    The main function that calls the above functions to complete each step
    
    width       : The width of the Board
    height      : The height of the Board
    Environment : Bool to determine if Environment has been chosen 
    Board       : A array containing all of the Tiles
    Lowest      : A array that keeps record of all the Tiles with the lowest amount of Possible Blocks. The first value contains the number of Blocks possible for all of the index that follow
    StationList : A List containing all the index's of the Station Tiles
    
    Border_Constraints() : Adds Constraint values to tiles on the borders of the Board so that tracks dont run of the side of the Board.
    Random_Tile_Pick()   : Selects a random Tile out of all the Tiles with the least choice in the Board and assigns it a Block determined by my random() function and a random possible rotation and turns Picked to true
    Tile_Checker()       : Checks all of the Tiles bordering a Tile thats just been assigned a Block and assigns them a Constraint on the border they share
    Move_Tiles()         : Creates a instance of the only possible block and moves it relative to its possition in the Board array then Rotates relative to the only Rotation value left
    Lowest_Tile()        : Checks all of the Tiles on the Board and searches for the tiles with the lowest number of possible Blocks
    TrainAnimation()     : This function is the main part of the trains animation that places trains at station and then loops through each train and determins what it should do relative to its position and Tile.     
    
    '''
        
    cmds.select(cmds.ls(typ="transform"), visible = True)
    cmds.delete()
    
    width = int(Width[0])
    height = int(Height[0])
    
    
    Environment = int(MeshTypes - 1)
    Board = [] 
    Lowest = []
    StationList = []
    
    
    for x in range(width*height):
        
        if Environment == 1:
            Board.append(Tile(Inputed_Tiles1()[:], 0)) 
        
            Border_Constraints(x, Board, width, height, Environment)
            
        elif Environment == 0:
            Board.append(Tile(Inputed_Tiles()[:], 0))
            Border_Constraints(x, Board, width, height, Environment)
   
        elif Environment == 2:
            Board.append(Tile(Inputed_Tiles2(array)[:], 0))
            Border_Constraints(x, Board, width, height, Environment)
    
    for x in range(width*height):
        
        random = Random_Tile_Pick(Lowest, Board, width, height)
        
        Tile_Checker(Lowest, Board, width, height, random, Environment)           
        
        Move_Tiles(StationList, Lowest, random, Board, width)
        
        Lowest=[]
        
        Lowest_Tile(Lowest, Board, width, height)
    
    if Environment == 0:
        TrainAnimation(Board, StationList, width, int(time[0]))
           
     
def BorderTile(current, BorderIndex, width):
    
    '''
    
    This function returns the index of the Tile in the direction of the border index inputted
    
    current     : The Tile index 
    BorderIndex : The Border index
    width       : The width of the Board
    
    return : The index of the tile in the borders direction. (eg if border is on the left returns the index of the tile to the left)    
    
    '''
    
    if BorderIndex == 0: 
        return (current - 1) 
    elif BorderIndex == 1:
        return ((current - width) - 1)
    elif BorderIndex == 2:
        return (current - width)
    elif BorderIndex == 3:
        return (current - (width - 1))
    elif BorderIndex == 4:
        return (current + 1)
    elif BorderIndex == 5:
        return (current + (width + 1))
    elif BorderIndex == 6:
        return (current + width)
    elif BorderIndex == 7:
        return (current + (width - 1)) 
              

def Train_Animation(Board, x, z, TrainList, reverse, name):
    
    '''
    
    This function animates the train inputted along the path inputted either forwards or in reverse
    
    Board     : A array containing all of the Tiles
    x         : The index of the train to be moved with in the train list
    z         : The index of the path to animate the train along 
    TrainList : A list containing all of the trains
    reverse   : Determines weather the train should be animated forwards along the path or in reverse
    name      : Determines weather Tile has more then 1 path optional 
    
    
    PathName           : The location of the path and the name of the path that the train is following. Combination of the name of the tile group that the Train is currently on and the name of the path inputted
    Empty              : Is used to animate along the path that the train will follow so the key frames can then be copied across to the train. Allows the train not to be parented to anything
    TrainList[x].Time  : The time on the timeline that the train is currently
    TrainList[x].Speed : The speed that the train needs to travel across the path    
    
    '''
 
    if name == 0:
        PathName = (Board[TrainList[x].Current].Possible_all[0].Object)+ "|" + (Board[TrainList[x].Current].Possible_all[0].PathList[0])
    else:                    
        PathName = (Board[TrainList[x].Current].Possible_all[0].Object)+ "|" + (Board[TrainList[x].Current].Possible_all[0].PathList[0][z])
    
    Empty = cmds.spaceLocator()                   
    
    if reverse == 1:
        cmds.reverseCurve(PathName, ch = 1, rpo = 1)   

    cmds.pathAnimation(Empty[0], c = PathName, stu = TrainList[x].Time, etu = TrainList[x].Time+(10/TrainList[x].Speed), f = True)    
    cmds.bakeResults( Empty[0] , simulation = True, t = (TrainList[x].Time,TrainList[x].Time+(10/TrainList[x].Speed)), disableImplicitControl = True, preserveOutsideKeys = True, sparseAnimCurveBake = False, removeBakedAttributeFromLayer = False, removeBakedAnimFromLayer = False, bakeOnOverrideLayer = False, minimizeRotation = True, controlPoints = True, shape = True)     
    cmds.copyKey( Empty[0], time=(TrainList[x].Time,TrainList[x].Time+(10/TrainList[x].Speed)), attribute=['tx', 'ty', 'tz', 'rx', 'ry', 'rz'])    
    cmds.pasteKey(TrainList[x].TrainName, time=(TrainList[x].Time,TrainList[x].Time), attribute=['tx', 'ty', 'tz', 'rx', 'ry', 'rz'])
    
    if reverse == 1:
        cmds.reverseCurve(PathName, ch = 1, rpo = 1)
    
    cmds.delete(Empty)
    
    TrainList[x].Time = TrainList[x].Time + (10/TrainList[x].Speed)


def Train_Speed(TrainList, x):
    
    '''
    
    This function determines weather the train needs to slow down in order for another train to pass with out colliding
    
    x         : The index of the train to be moved with in the train list
    TrainList : A list containing all of the trains
    
    '''    
    
    # Loops through all of the trains to check if there future tile is the same as the current train
    for i in range(len(TrainList)):                                          
    
        if i == x:
            continue
         
        if x > i:                        
            if TrainList[i].Future == TrainList[x].Future:
                TrainList[x].Speed = TrainList[x].Speed / 2.0 
                break
            
def CurrentBorder_Correction(CurrentBorder):
    
    '''
    
    Converts the Border inputted to the index of the neighbouring border
    
    CurrentBorder : The border inputted
    
    returns : The index of the border that neighbours the inputed border
    
    '''    
    
    if CurrentBorder < 4:
        
        return CurrentBorder + 4
    
    else:
        
        return CurrentBorder - 4           

def Iteration(Board, Tile, Border, width, TrainList, x, Two, Trigger):
    
    '''
    
    This function is used to check all of the tiles along a track until a train is located traveling towards the train beign checked or until a tile with more then one exit is on the track
    This function is used recursively each time begin called with the updated arguments to check the next tile on the track
    
    Board     : A array containing all of the Tiles  
    Tile      : The index of the Tile being checked with in Board array
    width     : The width of the Board
    TrainList : A list containing all of the trains
    x         : The index of the train to be moved with in the train list
    Two       : Determines whether trains need to be checked on the track
    Trigger   : Determines whether a train has been on the track heading the same direction as the fucntion is checking incase the function ends at a station
    
    Exits      : Records the number of possible exits on the Tile the function is checking
    Length     : The value returned if the Tile checked has more then one exit. This value is larger then any of the indexs in the array so the program doesnt get confused with it being the index of a station to remove
    TileBorder : The index of the border that the train would exit out of
    
    BorderTile()               : Used to calcuate the next tile to be checked when the function is called again
    CurrentBorder_Correction() : Converts the exit border index to the enter border index on the next tile to be checked 
    Iteration()                : Calls this function again with updated information to check the next tile on the track
    
    return result : Returns the result of the next tile checked
    return False  : Returns False to show this track is not possible to send a train down
    return Tile   : Returns the index of the station the function ends on when checking which station to start trains on, if a Tile with 2 exits hasnt been checked inbetween
    return length : Returns a int larger then any index on the board if there is more then 1 possible exit on the tile being checked          
    
    '''   
   
    Exits = 0
    
    length = len(Board) + 1
    
    # Loops thorugh all the Borders to establich which border is the exit border
    for z in range(len(Board[Tile].Possible_all[0].Borders)):
    
        Tile1 = ( z + (Board[Tile].Possible_all[0].Rotation[0])) % 8        
        
        if Border != z and Board[Tile].Possible_all[0].Borders[Tile1] == 1:
            
            Exits = Exits + 1
            
            TileBorder = z   
    
    # Checks if a train is on the tile and if its heading towrds or away from the curent train 
    if Two == 1:  
        
        for i in range(len(TrainList)):
                                        
            if i == x:
                continue
                            
            if TrainList[i].Current == Tile and Exits == 0:
                return False
            #elif TrainList[i].Speed == 0.5: 
            elif Exits > 1 and x < i and TrainList[i].Current == Tile and TrainList[i].FutureBorder == Border:
                return False
            elif Exits > 1 and x > i and  TrainList[i].Current == Tile and TrainList[i].FutureBorder == Border:
                return False                  
            elif Exits  == 1 and TrainList[i].Current == Tile and TrainList[i].CurrentBorder != Border:
                return False
            elif Exits == 1 and TrainList[i].Current == Tile and TrainList[i].CurrentBorder == Border:
                Trigger = 1
            
    if Exits == 1:
        NextTile = BorderTile(Tile, TileBorder, width)
        Border = CurrentBorder_Correction(TileBorder) 
        result = Iteration (Board, NextTile, Border, width, TrainList, x, Two, Trigger)
        return result
    elif Exits == 0 and Trigger == 1:
        return False    
    elif Exits == 0 and Two == 0: 
        return Tile     
    else:            
        return length

def FillTrainList(StationList, Board, width):
    
    '''
    
    This function places trains at possible stations and records information about them as classes with in the TrainList array
    
    StationList : A array that contains the index of all of the stations on the Board    
    Board       : A array containing all of the Tiles     
    width       : The width of the Board
    
    TrainList : A list containing all of the trains
    Difrrent1 : The offset needed incase a element is removed from StationList
    TrainName : Name of the train + the itertaion number (eg train1, train2)
    
    Iteration() : Check all of the tiles along a track until a tile with more then one exit is on the track if not returns the index of the station it stops at
    
    '''   
    
    TrainList = []
    Difrrent1 = 0
    
    for x in range(len(StationList)):
        
        if x == len(StationList):
            break
        
        # This checks whether there is a Tile with more then one exit before a station is reached on the track if not then remove the station for possible stations to start trains at
        Result = Iteration(Board, StationList[x], "", width, "", "", 0, 0)
        
        if Result != len(Board) + 1:
            StationList.remove(Result)
            Difrrent1 = Difrrent1 + 1
        
        TrainName = "Train" + str(x)
        cmds.sphere(r = 0.1, name = TrainName)                         
        TrainList.append( Train( TrainName , StationList[x]))
        
    return TrainList
    

def UpdateTrain(TrainList, CurrentStation):
    
    '''
    
    This function updates all of the trains so that there current, future and current borders are up to date for there new positions after being animated along paths
    
    TrainList      : A list containing all of the trains
    CurrentStation : A array of all of the previouse tile Indexs 
    
    CurrentBorder_Correction() : Converts the exit border index to the enter border index on the next tile 
    
    '''
    
    for i in range(len(TrainList)):            
    
        CurrentStation.append(TrainList[i].Current)                
        
        if TrainList[i].Speed == 0.5:
            continue
        
        TrainList[i].Current = TrainList[i].Future 
                
        TrainList[i].CurrentBorder = CurrentBorder_Correction(TrainList[i].FutureBorder)
    

def EnitialMoveOff(Board, TrainList, x, width):
    
    '''
    
    Animates the train for the first time on the station Tile it was started on
    
    Board     : A array containing all of the Tiles 
    TrainList : A list containing all of the trains
    x         : The index of the train to be moved with in the train list
    width     : The width of the Board 
    
    BorderTile()    : This function tells which Tile is in the direction of the border index inputted
    Train_Speed()   : This function determines weather the train needs to slow down in order for another train to pass with out colliding
    Train_Animation : This function animates the train inputted along the inputted path either forwards or in reverse
    
    '''
    
    for z in range(len(Board[TrainList[x].Current].Possible_all[0].Borders)): 
    
        Tile1 = ( z + (Board[TrainList[x].Current].Possible_all[0].Rotation[0])) % 8 
        
        if Board[TrainList[x].Current].Possible_all[0].Borders[Tile1] == 1: 
                                    
            TrainList[x].FutureBorder = z  
            
            TrainList[x].Future = BorderTile( TrainList[x].Current, TrainList[x].FutureBorder, width )                        
            
            Train_Speed(TrainList, x)
            
            break
    
    Train_Animation(Board, x, z, TrainList, 0, 0)



def PossibleBordersCheck(PossibleBorders, width, TrainList, x, Board):
        
    '''
    
    Checks the tracks along each possible border direction and see if its possible for the train to travel down it
    
    PossibleBorders : A array of possible border exits the train could take on the tile
    width           : The width of the Board 
    x               : The index of the train to be moved with in the train list
    Board           : A array containing all of the Tiles
    
    w        : The offset of the index checked in the array incase a border was removed
    NextTile : The Tile index of the first tile on the track based of the possible border picked
    Border   : The entrance border on the next tile
    
    BorderTile()               : This function tells which Tile is in the direction of the border index inputted
    CurrentBorder_Correction() : Converts the exit border index to the enter border index on the next tile    
    Iteration()                : Check all of the tiles along a track until a train is located traveling towards the train beign checked or until a tile with more then one exit is on the track
    
    '''   
    
    w = 0
    
    for z in range (len(PossibleBorders)):

        z = z - w
        
        NextTile = BorderTile(TrainList[x].Current, PossibleBorders[z], width)
       
        Border = CurrentBorder_Correction(PossibleBorders[z])
        
        result = Iteration(Board, NextTile, Border, width, TrainList, x, 1, 0)
    
        if result != len(Board) + 1:
            PossibleBorders.remove(PossibleBorders[z])
            w = w+ 1 
    return PossibleBorders  


def MoveTrain(Board, TrainList, x):
    
    '''
    
    This function takes the possible borders and curent border and compares them to the name of the paths to determine which path to follow and weather it needs to be reverse or not    
    
    Board     : A array containing all of the Tiles
    TrainList : A list containing all of the trains
    x         : The index of the train to be moved with in the train list
    
    Path : This is a array that stores the borders indexs in the paths name 
    
    Train_Animation() : This function animates the train inputted along the path inputted either forwards or in reverse 
    
    '''
    
    
    for z in range(len(Board[TrainList[x].Current].Possible_all[0].PathList[0])):
    
        Path = []                    
        
        for letter in range(len(Board[TrainList[x].Current].Possible_all[0].PathList[0][z])):
                                  
            # Ignore the P becuase only the border indexs are wanted for comparison
            if Board[TrainList[x].Current].Possible_all[0].PathList[0][z][letter] == 'P':
                
                continue
            # Add border indexs to array to be compared
            else:
                Path.append(( int(Board[TrainList[x].Current].Possible_all[0].PathList[0][z][letter]) + (8 - Board[TrainList[x].Current].Possible_all[0].Rotation[0])) % 8)
                
        
        if [TrainList[x].CurrentBorder, TrainList[x].FutureBorder] == Path:
            
            Train_Animation(Board, x, z, TrainList, 0, 1)
            
            break
        
        elif [TrainList[x].FutureBorder, TrainList[x].CurrentBorder] == Path:
            
            Train_Animation(Board, x, z, TrainList, 1, 1)
            
            break


def TrainAnimation(Board, StationList, width, time):
    
    '''
    
    This function is the main part of the trains animation that places trains at station and then loops through each train and determins what it should do relative to its position and number of exits on the Tile. 
    This is repeated a number of times until the inputted time has been meet.
    
    Board       : A array containing all of the Tiles 
    StationList : A array that contains the index of all of the stations
    width       : The width of the Board
    
    TrainList       : A array containing all of the trains placed on the board and there information
    CurrentStation  : A array of all of the previouse tile Indexs
    PossibleBorders : A array of possible border exits the train could take on the tile  
    
    
    FillTrainList()        : This function places trains at possible stations and records information about them as class with in the TrainList array    
    UpdateTrain()          : This function updates all of the trains so that there current, future, current borders are right for there new positions after being animated along the path
    EnitialMoveOff()       : Animates the train for the first time on the station Tile it was started on
    PossibleBordersCheck() : Checks the tracks along each possible border direction and see if its possible for the train to travel down it
    TrainAnimation()       : This function animates the train inputted along the path inputted either forwards or in reverse
    Train_Speed()          : This function determines weather the train needs to slow down in order for another train to pass with out colliding
    MoveTrain()            : This function takes the possible borders and curent border and compares them to the name of the paths to determine which path to follow and weather it needs to be reverse or not

    '''  
    
    TrainList = FillTrainList(StationList, Board, width)
 
    for k in range(int(time/10)):
        
        CurrentStation = []
        
        if k != 0:
            
            UpdateTrain(TrainList, CurrentStation)        
        
        
        for x in range(len(TrainList)):
            
            # If the train was traveling slow skip this check becuase its still moving and reset speed to normal
            if TrainList[x].Speed == 0.5:
                TrainList[x].Speed = 1.0
                continue
            
            # If the Train is moving for the first time
            if TrainList[x].Future == "": 
                
                EnitialMoveOff(Board, TrainList, x, width)        
            
            else:
                
                PossibleBorders = []                
                
                # Cycle through borders of the tile skiping the border bordering the past tile, add all the other possible exits to PossibleBorders
                for z in range(len(Board[TrainList[x].Current].Possible_all[0].Borders)):   
                    
                    Tile = ( z + (Board[TrainList[x].Current].Possible_all[0].Rotation[0])) % 8
                    
                    if z == TrainList[x].CurrentBorder:
                        continue
                        
                    if Board[TrainList[x].Current].Possible_all[0].Borders[Tile] == 1:
                        PossibleBorders.append(z)
               
                # If more then one border was added to PossibleBorders (meaning there are 2 exits)
                if len(PossibleBorders) > 1:
                    
                    PossibleBorders = PossibleBordersCheck(PossibleBorders, width, TrainList, x, Board)
                        
                    if len(PossibleBorders) == 0:
    
                        StationList.pop(x-1)
                        
                        for q in range(len(TrainList)):
                            cmds.delete(TrainList[q].TrainName)                       
                        
                        TrainAnimation(Board, StationList, width, time)
                        
                        return False
                                           
                    TrainList[x].FutureBorder = rand.choice(PossibleBorders)
                    
                    TrainList[x].Future = BorderTile(TrainList[x].Current, TrainList[x].FutureBorder, width) 

                    Train_Speed(TrainList, x)
                    
                # If only one possible exit    
                elif len(PossibleBorders) == 1: 
                    
                    TrainList[x].FutureBorder = PossibleBorders[0] 
                     
                    TrainList[x].Future = BorderTile(TrainList[x].Current ,TrainList[x].FutureBorder, width)  
                    
                    Train_Speed(TrainList, x)
                
                
                # If no possible exits = station
                elif len(PossibleBorders) == 0:
                    
                    TrainList[x].Future = CurrentStation[x]
                    
                    TrainList[x].FutureBorder = TrainList[x].CurrentBorder                  
                    
                    TrainList[x].Speed = 2.0
                    
                    Train_Speed(TrainList, x)
                    
                    Train_Animation(Board, x, z, TrainList, 1, 0)
                    
                    Train_Animation(Board, x, z, TrainList, 0, 0)
                    
                    if TrainList[x].Speed == 2:                        
                        TrainList[x].Speed = 1.0                    
                    else:
                        TrainList[x].Speed = 0.5
                
                MoveTrain(Board, TrainList, x)
                    
                    
if __name__ == '__main__':
    createUI()    
        