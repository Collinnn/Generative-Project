
import numpy as np
from matplotlib import pyplot as plt
import math
import scipy
import skimage
import copy
ARR_SIZE = 20
FINAL_SIZE = ARR_SIZE*2**4 # 100*2^5 = 3200

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
    def move_point(self, x,y,x2,y2):
        self.connections[(x2,y2)] = self.connections[(x,y)]
        del self.connections[(x,y)]


grid_map = GridMap()
height_map = np.zeros((FINAL_SIZE,FINAL_SIZE), dtype=int)
final_map = np.zeros((2560,2560), dtype=float)
edgefound = False
pointdict = {}

def main ():
    global grid_map
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
            upscaleandAddToFinal(getHeightMap(size),exponent)
            exponent += 1
            size = int(math.pow(2,exponent))


            jitterMap(size)
            upscaledMountain(size)
  
        if(edgefound): #edge reached 
            print("Edge found")
            upscaleandAddToFinal(getHeightMap(size),exponent)
            edgefound = False
            exponent += 1

            size = int(math.pow(2,exponent))

            jitterMap(size)
            upscaledMountain(size)


        if(exponent==5):
            print("Heightmap")
            print(size)
            arr = getHeightMap(size)
            upscaleandAddToFinal(arr,exponent)
            break
        
            
    toImage()

def upscaleandAddToFinal(arr,exponent):
    global final_map
    arr = arrJitter(arr)
    expo = exponent
    expo += 1
    arr = upscaleblur(arr,expo)

    final_map += arr

def arrJitter(arr):
    arr_shape = arr.shape
    newarr = np.zeros((arr_shape[0], arr_shape[1]), dtype=float)
    
    for i in range(arr_shape[0]):
        for j in range(arr_shape[1]):
            rand = np.random.rand(1)*2-1#-1 to 1
            rand2 = np.random.rand(1)*2-1 
            value=arr[i,j]
            #split over 9 pixels
            if(rand > 0.0):
                if(i+1<arr_shape[0]):
                    newarr[i,j] = value-value*rand
                    newarr[i+1,j] = value*rand
            else:
                if(i-1<0):
                    newarr[i,j] = value-value*math.fabs(rand)
                    newarr[i-1,j] = value*math.fabs(rand)
            if(rand2 > 0.0):
                if(j+1<arr_shape[1]):
                    newarr[i,j] = value-value*rand2
                    newarr[i,j+1] = value*rand2
            else:
                if(j-1<0):
                    newarr[i,j] = value-value*math.fabs(rand2)
                    newarr[i,j-1] = value*math.fabs(rand2)
   
    return newarr
                        
            

        
def upscaleblur(arr,expo):

    #get size of arr
    while True:
        csize = 2**(expo-1)
        #Linear interpolation
        new_arr = skimage.transform.resize(arr,(ARR_SIZE*csize,ARR_SIZE*csize), order=1)

        #Radial blur
        new_arr = scipy.ndimage.gaussian_filter(new_arr, sigma=1)
        expo += 1
        
        arr = new_arr
        if expo >= 9: #Temp, but not going to be
            break

    return arr

    

            


def placeNewPixel(size):
    greatest=(ARR_SIZE*size)-2

    while (True):
        place = np.random.randint(0, 4) #0 = up, 1 = down, 2 = left, 3 = right
        small = np.random.randint(1,10*size) # 1 to 4*size-1
        rand = np.random.randint(1,greatest) # 1 to greatest-1
        up = (small, rand)    
        down = (greatest,rand) 
        left = (rand,small)
        right = (rand,greatest)

        arr = [up,down,left,right]
        x,y = arr[place]
        if not grid_map.check_point(x,y) and pointdict.get((x,y)) is None:
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
    greatest = (ARR_SIZE-1)*size
    while True:
        move = randMove()
        if checkPixelEdges((x,y)): #Found a neighbour
            if(x == 1 or x == greatest or y == 1 or y == greatest): #Check if on the edge
                pointdict[(x,y)] = 1
                if(len(pointdict) == 16): #a few edges found
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
            print("Error in moving pixel") # WILL NEVER HAPPEN
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
    x = (ARR_SIZE//2)
    y = (ARR_SIZE//2)
    # center of the array
    grid_map.add_point(x,y)
    

def printMountain(size):
    for i in range(ARR_SIZE*size):
        for j in range(ARR_SIZE*size):
            if not grid_map.check_point(i,j):
                print("0", end = " ")
            else:
                print("x", end = " ")
        print("")

def stepDown(size):
    return int(size*(2**(-1)))

def jitterMap(size):
    global grid_map
    grid = copy.deepcopy(grid_map)
    for x,y in grid.connections.keys():
        rand = np.random.randint(0,5) #0 = up, 1 = down, 2 = left, 3 = right, 4 = stay
        if rand == 0:
            if(y-1 >= 0 and not grid_map.check_point(x,y-1)):
                grid_map.move_point(x,y,x,y-1)
        elif rand == 1:
            if(y+1 <= ARR_SIZE-1*size  and not grid_map.check_point(x,y+1)):
                grid_map.move_point(x,y,x,y+1)
        elif rand == 2:
            if(x-1 >= 0  and not grid_map.check_point(x-1,y)):
                grid_map.move_point(x,y,x-1,y)
        elif rand == 3:
            if(x+1 <= ARR_SIZE-1*size and not grid_map.check_point(x+1,y)):
                grid_map.move_point(x,y,x+1,y)
        else:
            continue
    return
        
        

def upscaledMountain(size):
    global grid_map
    pointdict.clear()
    upscaled_map = GridMap()
    for x, y in grid_map.connections.keys():
        upscaled_map.add_point(x*2, y*2)  # Add the scaled point itself
        
        # Get the connections of the current point
        connections = grid_map.get_connections(x, y)
        x_sized = x*2
        y_sized = y*2
        
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
                print("Error in upscaling")
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
def toImage():

    global final_map
    #plot array
    plt.imshow(final_map, cmap='gray')
    plt.show()


def printNeighbours(location):
    x,y = location
    string = "Neighbours of: " + str(location)
    if grid_map.check_point(x-1,y):
        string += " neighbour found left"
    else:
        string += " no neighbour up"
    if grid_map.check_point(x+1,y):
        string += " neighbour found right"
    else:
        string += " no neighbour down"
    if grid_map.check_point(x,y-1):
        string += " neighbour found up"
    else:
        string += " no neighbour left"
    if grid_map.check_point(x,y+1):
        string += " neighbour found down"
    else:
        string += " no neighbour right"
    print(string)


main()