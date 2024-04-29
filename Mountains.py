
import numpy as np
from matplotlib import pyplot as plt
import math
import scipy
import skimage
ARR_SIZE = 10
FINAL_SIZE = ARR_SIZE*2**5 # 100*(2^5) = 3200  3200*3200 = 10240000 points

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
    size = int(math.pow(2,exponent)) 
    print("mountain home:")
    # numpy 2d array
    setFirstPixel()
    while(True):
        location = placeNewPixel(size)

        
        movePixel(location,size)

        if(density(size) >= 0.3):#density reached  FYI: split in two to see which happens
            print("Density reached")
            exponent += 1

            size = int(math.pow(2,exponent)) 
            upscaledMountain(size)
  
        if(edgefound): #edge reached 
            print("Edge found")
            edgefound = False
            exponent += 1
            print("size: ", size)
            size = int(math.pow(2,exponent))
            
            upscaledMountain(size)
            print(size)
   
        if(exponent==2):
            print("Heightmap")
            print(size)
            arr = getHeightMap(size)
            upscaleandAddToFinal(arr,exponent)
            break
        
            
    toImage(size)

def upscaleandAddToFinal(arr,exponent):
    customSize = 2^exponent

    while(True):
        if(customSize*ARR_SIZE >= FINAL_SIZE):
            break
        
        exponent += 1
        customSize = 2^exponent
        upscaleblur(arr,customSize)
        

        
        
def upscaleblur(arr,size):
    #get size of arr
    #TODO: REDO INTERPOLATION
    print(size)
    print(len(arr))
    new_arr = skimage.transform.resize(arr,(ARR_SIZE*size,ARR_SIZE*size), order=1)
    print(arr)
    print(new_arr)
            


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
    return  np.random.randint(0, 4)
   
    
# density of the mountain
def density(size):
    # density of the mountain
    amount = 0
    for i in range(1,ARR_SIZE-1*size):
        for j in range(1,ARR_SIZE-1*size):
            if(grid_map.check_point(i,j)):
                amount += 1
    
    density = amount / float((ARR_SIZE-2)*size * (ARR_SIZE-2)*size)
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
                print("0", end = " ")
            else:
                print(grid_map.num_of_connections(i,j), end = " ")
        print("")

def upscaledMountain(size):
    global grid_map

    upscaled_map = GridMap()

    for x, y in grid_map.connections.keys():
        upscaled_map.add_point(x * size, y * size)  # Add the scaled point itself
        
        # Get the connections of the current point
        connections = grid_map.get_connections(x, y)
        x_sized = x * size
        y_sized = y * size
        
        # Scale each connected point and add connections in the upscaled map
        for cx, cy in connections:
            # Scale the connected point
            if(x-1 == cx): #left
                upscaled_map.add_point(x_sized-1, y_sized)
                upscaled_map.add_connection(x_sized, y_sized, x_sized-1, y_sized)

                if(upscaled_map.check_point(x_sized-2, y_sized)): #Exists to check if extended also connnects to another point
                    upscaled_map.add_connection(x_sized-1, y_sized, x_sized-2, y_sized)
            elif(x+1 == cx): #right
                upscaled_map.add_point(x_sized+1, y_sized)
                upscaled_map.add_connection(x_sized, y_sized, x_sized+1, y_sized)

                if(upscaled_map.check_point(x_sized+2, y_sized)):
                    upscaled_map.add_connection(x_sized+1, y_sized, x_sized+2, y_sized)
            elif(y-1 == cy): #up
                upscaled_map.add_point(x_sized, y_sized-1)
                upscaled_map.add_connection(x_sized, y_sized, x_sized, y_sized-1)

                if(upscaled_map.check_point(x_sized, y_sized-2)):
                    upscaled_map.add_connection(x_sized, y_sized-1, x_sized, y_sized-2)
            elif(y+1 == cy): #down
                upscaled_map.add_point(x_sized, y_sized+1)
                upscaled_map.add_connection(x_sized, y_sized, x_sized, y_sized+1)

                if(upscaled_map.check_point(x_sized, y_sized+2)):
                    upscaled_map.add_connection(x_sized, y_sized+1, x_sized, y_sized+2)
            else:
                print("Error")       
    grid_map = upscaled_map
    


def getHeightMap(size):
    frontier = {}
    arr = np.zeros((ARR_SIZE*size,ARR_SIZE*size), dtype=int)
    for i in range(1,ARR_SIZE*size):
        for j in range(1,ARR_SIZE*size):
            if(grid_map.check_point(i,j)): #Check if point is in the grid
                if(grid_map.num_of_connections(i,j) == 1):
                    frontier[(i,j)] = 1
                    arr[(i,j)] = 1

    #Expand frontier until all points are filled 
    while True:
        if not frontier:
            break
        item,_= min(frontier.items(), key=lambda x: x[1])
        i,j = item

        for (x,y) in grid_map.get_connections(i,j):
            if(x >= 0 and x <= ARR_SIZE*size-1 and y >= 0 and y <= ARR_SIZE*size-1):
                if(arr[(x,y)] == 0):
                    frontier[(x,y)] = frontier[(i,j)] + 1
                    arr[(x,y)] = frontier[(i,j)] + 1

        frontier.pop((i,j))
        
    return arr
    


#Currently wont work
def toImage(size):

    arr = np.zeros((ARR_SIZE*size,ARR_SIZE*size), dtype=int)
    #Finds all corners
    for i in range(ARR_SIZE*size):
        for j in range(ARR_SIZE*size):
            if(grid_map.check_point(i,j)):
                arr[i,j] = 255


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


main()