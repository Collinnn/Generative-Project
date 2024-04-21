
import numpy as np
from matplotlib import pyplot as plt
ARR_SIZE = 100
FINAL_SIZE = ARR_SIZE*2^5 # 100*(2^5) = 3200  3200*3200 = 10240000 points





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

grid_map = GridMap()
final_map = np.zeros((FINAL_SIZE,FINAL_SIZE), dtype=int)
edgefound = False


def main ():
    global edgefound
    exponent = 1
    size = 2^exponent
    print("mountain home:")
    # numpy 2d array
    setFirstPixel()
    while(True):
        location = placeNewPixel()
        #print(location)
        
        movePixel(location)
        
        if(density() >= 0.3):#density reached  FYI: split in two to see which happens
            print("Density reached")
            printMountain()
            upscaledMountain(size)
            exponent += 1
            size = 2^exponent	
        if(edgefound): #edge reached 
            print("Edge found")
            edgefound = False 
            printMountain()
            upscaledMountain(size)
            exponent += 1
            size = 2^exponent
        
        if(exponent==3):
            break
        
            
    toImage(0)


def placeNewPixel():
    
    while (True):
        place = np.random.randint(0, 4)
        rand = np.random.randint(1,ARR_SIZE-1)
        up = (1, rand)    
        down = (ARR_SIZE-2,rand) 
        left = (rand,1)
        right = (rand,ARR_SIZE-2)

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
def movePixel(location):
    x,y = location
    global edgefound
    while True:
        move = randMove()
        if checkPixelEdges((x,y)): #Found a neighbour
            if(x == 1 or x == ARR_SIZE-2 or y == 1 or y == ARR_SIZE-2): #Check if on the edge
                print("Edge reached")
                edgefound = True 
            break
        if move == 0:
            if x>2:
                grid_map.delete_point_before_connection(x,y)
                x=x-1
                grid_map.add_point(x,y)
        elif move == 1:
            if x<ARR_SIZE-2:
                grid_map.delete_point_before_connection(x,y)
                x=x+1
                grid_map.add_point(x,y)
        elif move == 2:
            if y>2:
                grid_map.delete_point_before_connection(x,y)
                y=y-1
                grid_map.add_point(x,y)
        elif move == 3:
            if y<ARR_SIZE-2:
                grid_map.delete_point_before_connection(x,y)
                y=y+1
                grid_map.add_point(x,y)
        else:
            print("Error")
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
    if(density >= 0.1):
        printMountain()
    #print(density)
    return density


def setFirstPixel():
    x = (ARR_SIZE//2)-1
    y = (ARR_SIZE//2)-1
    # center of the array
    grid_map.add_point(x,y)
    

def printMountain():
    for i in range(ARR_SIZE):
        for j in range(ARR_SIZE):
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
            #Adds the point in between the two points
            if(xd == x*2):
                if(yd>y*2):
                    upscaled_map.add_point(xd,yd-1)
                else:
                    upscaled_map.add_point(xd,yd+1)
            else:
                if(xd>x*2):
                    upscaled_map.add_point(xd-1,yd)
                else:
                    upscaled_map.add_point(xd+1,yd)
            upscaled_map.add_point(xd,yd)
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

def toImage(size):
    arr = np.zeros((ARR_SIZE*2^size,ARR_SIZE*2^size), dtype=int)
    for i in range(ARR_SIZE*2^size):
        for j in range(ARR_SIZE*2^size):
            if(grid_map.check_point(i,j)):
                arr[i][j] = 1
    
    plt.imshow(arr, cmap='gray', interpolation='nearest')
    plt.show()
                



main()