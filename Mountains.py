
import numpy as np
from matplotlib import pyplot as plt
ARR_SIZE = 10
FINAL_SIZE = ARR_SIZE*2^5 # 100*(2^5) = 3200  3200*3200 = 10240000 points
NUM=2




class GridMap:
    def __init__(self):
        self.connections = {}
    def add_point(self, x,y):
        self.connections[(x,y)] = []
    def add_connection(self, x1,y1,x2,y2):
        self.connections[(x1,y1)].append((x2,y2))
        self.connections[(x2,y2)].append((x1,y1)) 
    def get_connections(self, x,y):
        return self.connections[(x,y)]
    #check if a point is already in the map
    def check_point(self, x,y):
        return self.connections.get((x,y)) is not None
    def delete_point_before_connection(self, x,y): #Only used before connection is made
        del self.connections[(x,y)] 
    def point_to_string(self, x,y):
        str(self.connections[(x,y)]) + ", " + str(x) + "," + str(y)
    def num_of_connections(self, x,y):
        return len(self.connections[(x,y)])

grid_map = GridMap()
height_map = np.zeros((FINAL_SIZE,FINAL_SIZE), dtype=int)
final_map = np.zeros((FINAL_SIZE,FINAL_SIZE), dtype=int)
edgefound = False


def main ():
    global edgefound
    exponent = 0
    size = NUM^exponent
    print("mountain home:")
    # numpy 2d array
    setFirstPixel()
    while(True):
        location = placeNewPixel(size)
        #print(location)
        
        movePixel(location,size)
        
        if(density() >= 0.3):#density reached  FYI: split in two to see which happens
            print("Density reached")
            printMountain(size)
            exponent += 1
            size = 2^exponent	
            upscaledMountain(size)

        if(edgefound): #edge reached 
            print("Edge found")
            edgefound = False 
            printMountain(size)
            exponent += 1
            size = 2^exponent
            upscaledMountain(size)

        if(exponent==1):
            getHeightMap(size)
            break
        
            
    toImage(size)


def placeNewPixel(size):
    greatest=(ARR_SIZE*size)-2

    while (True):
        place = np.random.randint(0, 4)
        rand = np.random.randint(1,greatest)
        up = (1, rand)    
        down = (greatest,rand) 
        left = (rand,1)
        right = (rand,greatest)

        arr = [up,down,left,right]
        x,y = arr[place]
        if not grid_map.check_point(x,y):
            grid_map.add_point(x,y)
            return (x,y)


def checkPixelEdges(location):
    #  0
    # 0x0
    #  0
    #Check if border of array
    x,y = location
    if grid_map.check_point(x-1,y):
        grid_map.add_connection(x,y,x-1,y)
    elif grid_map.check_point(x+1,y):
        grid_map.add_connection(x,y,x+1,y)
    elif grid_map.check_point(x,y-1):
        grid_map.add_connection(x,y,x,y-1)
    elif grid_map.check_point(x,y+1):
        grid_map.add_connection(x,y,x,y+1)
    else:
        return False
    return True

  
#Location = (x,y) tuple
def movePixel(location,size):
    x,y = location
    global edgefound
    greatest = (ARR_SIZE-2)*size
    while True:
        move = randMove()
        if checkPixelEdges((x,y)): #Found a neighbour
            if(x == 1 or x == greatest or y == 1 or y == greatest): #Check if on the edge
                print("Edge reached")
                edgefound = True 
            break
        if move == 0:
            if x>2:
                grid_map.delete_point_before_connection(x,y)
                x=x-1
                grid_map.add_point(x,y)
        elif move == 1:
            if x<greatest:
                grid_map.delete_point_before_connection(x,y)
                x=x+1
                grid_map.add_point(x,y)
        elif move == 2:
            if y>2:
                grid_map.delete_point_before_connection(x,y)
                y=y-1
                grid_map.add_point(x,y)
        elif move == 3:
            if y<greatest:
                grid_map.delete_point_before_connection(x,y)
                y=y+1
                grid_map.add_point(x,y)
        else:
            print("Error") # WILL NEVER HAPPEN
    return

def randMove():
    # random move
    return  np.random.randint(0, 4)
   
    
# density of the mountain
def density():
    # density of the mountain
    amount = 0
    for i in range(1,ARR_SIZE-1):
        for j in range(1,ARR_SIZE-1):
            if(grid_map.check_point(i,j)):
                amount += 1
    
    density = amount / float((ARR_SIZE-2) * (ARR_SIZE-2))
    #print(density)
    return density


def setFirstPixel():
    x = (ARR_SIZE//2)-1
    y = (ARR_SIZE//2)-1
    # center of the array
    grid_map.add_point(x,y)
    

def printMountain(size):
    for i in range(ARR_SIZE*size):
        for j in range(ARR_SIZE*size):
            if not grid_map.check_point(i,j):
                print(" ", end = " ")
            else:
                print(u'\u25A1', end = " ")
        print("")

def upscaledMountain(size):
    upscaled_map = GridMap()
    global grid_map
    for elem in grid_map.connections.keys():
        x,y = elem
        arr = grid_map.get_connections(x,y)
        upscaled_map.add_point(x*size,y*size)
        for tup in arr:
            xd,yd = (tup[0]*size,tup[1]*size)
            upscaled_map.add_point(xd,yd)
            #Adds the point in between the two points
            if(xd == x*2):
                if(yd>y*2):
                    upscaled_map.add_point(xd,yd-1)
                    upscaled_map.add_connection(xd,yd,xd,yd-1)
                else:
                    upscaled_map.add_point(xd,yd+1)
                    upscaled_map.add_connection(xd,yd,xd,yd+1)
            else:
                if(xd>x*2):
                    upscaled_map.add_point(xd-1,yd)
                    upscaled_map.add_connection(xd,yd,xd-1,yd)
                else:
                    upscaled_map.add_point(xd+1,yd)
                    upscaled_map.add_connection(xd,yd,xd+1,yd)
            
    grid_map = upscaled_map


def printNeighbours(location):
    x,y = location
    string = "Neighbours of: " + str(location)
    if grid_map.check_point(x-1,y):
        string += " neighbour up"
    else:
        string += " no neighbour up"
    if grid_map.check_point(x+1,y):
        string += " neighbour down"
    else:
        string += " no neighbour down"
    if grid_map.check_point(x,y-1):
        string += " neighbour left"
    else:
        string += " no neighbour left"
    if grid_map.check_point(x,y+1):
        string += " neighbour right"
    else:
        string += " no neighbour right"
    print(string)

def getHeightMap(size):
    frontier = {}
    size_diff = transposeSize(size)
    arr = np.zeros((ARR_SIZE*size,ARR_SIZE*size), dtype=int)
    #Rotate inwards from the edge of the 2d array

    for i in range(1,ARR_SIZE*size):
        #Found point
        for j in range(1,ARR_SIZE*size):
            if(grid_map.check_point(i,j)):
                print("Found point: ", i,j)
                print("Connections: ", grid_map.get_connections(i,j))
                if(grid_map.num_of_connections(i,j) == 1):
                    frontier[(i,j)] = 1
    
        
    #Expand frontier until all points are filled 
    while frontier.keys() != {}:
        if(arr[(i,j)]!=0):
            arr[i,j] = frontier[(i,j)]
            for (x,y) in grid_map.get_connections(i,j):
                frontier[(x,y)] = frontier[(i,j)] + 1
        frontier.pop((i,j))
    print(arr)
    
        
#Gives the size difference        
def transposeSize(size):
    local_size = ARR_SIZE*size               
    return FINAL_SIZE//local_size


#Currently wont work
def toImage(size):

    arr = np.zeros((ARR_SIZE*size,ARR_SIZE*size), dtype=int)
    #Finds all corners
    for i in range(ARR_SIZE*size):
        for j in range(ARR_SIZE*size):
            if(grid_map.check_point(i,j)):
                arr[i,j] = 255
    
                



main()