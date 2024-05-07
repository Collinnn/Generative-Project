
import numpy as np
from matplotlib import pyplot as plt
import math
import scipy
import skimage
import copy
import os
import PIL
ARR_SIZE = 10
FINAL_SIZE = ARR_SIZE*2**5 # 100*2^5 = 3200

class GridMap:
    def __init__(self):
        self.connections = {}
    def add_point(self, x,y):
        self.connections[(x,y)] = []
    def get_connections(self, x,y):
        return self.connections[(x,y)]
    #check if a point is already in the map
    def check_point(self, x,y):
        return self.connections.get((x,y)) is not None
    def delete_point_before_connection(self, x,y): #Only used before connection is made
        del self.connections[(x,y)] 
    def point_to_string(self, x,y):
        str(self.connections[(x,y)]) + ", " + str(x) + "," + str(y)
    def num_of_connections(self,x,y): # 0 or 1
        return len(self.connections[(x,y)])
    def num_of_connections_to_self(self, x,y):
        amount = 0
        if (self.check_point(x-1,y)):
            if self.connections[x-1,y] == (x,y):
                amount += 1
        if (self.check_point(x-1,y)):
            if self.connections[x-1,y] == (x,y):
                amount += 1
        if (self.check_point(x,y-1)):
            if self.connections[x,y-1] == (x,y):
                amount += 1
        if (self.check_point(x,y+1)):
            if self.connections[x,y+1] == (x,y):
                amount += 1
        return amount
    def move_point(self, x,y,x2,y2):
        self.connections[(x2,y2)] = self.connections[(x,y)]
        del self.connections[(x,y)]
    def add_connection(self, x1,y1,x2,y2):
        if (x2,y2) not in self.connections[(x1,y1)] and self.check_point(x2,y2):
            self.connections[(x1,y1)].append((x2,y2)) # one way connection


grid_map = GridMap()
final_size = 5120
final_map = np.zeros((final_size,final_size), dtype=float)
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
        #location = placeNewPixelBorders(size)
        location = placeNewPixel(size)

        movePixel(location,size)

        if(density(size) >= 0.4 or edgefound):#density reached  FYI: split in two to see which happens
            if(density(size) >= 0.4):
                print("Density reached")
            else:
                print("Edge found")
                edgefound = False
            upscaleandAddToFinal(getHeightMap(size),exponent)
            exponent += 1
            size = int(math.pow(2,exponent))
            upscaledMountain(size)


        if(exponent==4):
            print("final map")
            upscaleandAddToFinal(getHeightMap(size),exponent)
            break
 
    print("To Image")
    normalizeHeight()
    circleHeight()
    toImage()

def normalizeHeight():
    global final_map
    for i in range(final_map.shape[0]):
        for j in range(final_map.shape[1]):
            final_map[i,j] = 1-(1/(1+final_map[i,j]))
    return

def normalizedLength(length,min_cutt_off,max_length):
    return (length-min_cutt_off)/(max_length-min_cutt_off)

def circleHeight():
    length = final_map.shape[0]
    center = length//2
    hypotenous = math.sqrt((center**2)+(center**2))
    max_length = (hypotenous/2) - (hypotenous/3)
    for i in range(length):
        for j in range(length):
            distance = math.sqrt((center-i)**2+(center-j)**2)
            if(distance <= hypotenous/3):
                final_map[i,j] = 0	
            elif(distance <= hypotenous/2):
                normal = normalizedLength(distance,hypotenous/3,hypotenous/2)
                print(normal)
                final_map[i,j] = final_map[i,j]*normal

            if(final_map[i,j]<0):
                final_map[i,j] = 0
            
    
    return

def upscaleandAddToFinal(arr,exponent):
    global final_map
    arr = arrJitter(arr)
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
            #The squeeze stops the random float from being a 1d array
            rand = np.squeeze(np.random.rand(1)*2-1) # -2 to 2
            rand2 = np.squeeze(np.random.rand(1)*2-1) # -2 to 2
            value=arr[i,j] 
            #split over 9 pixels
            if(rand > 0.0):
                if(i+1<arr_shape[0]):
                    newarr[i,j] = value-value*rand
                    newarr[i+1,j] = value*rand
            else:
                if(i-1<0):
                    newarr[i,j] = value-value*abs(rand)
                    newarr[i-1,j] = value*abs(rand)
            if(rand2 > 0.0):
                if(j+1<arr_shape[1]):
                    newarr[i,j] = value-value*rand2
                    newarr[i,j+1] = value*rand2
            else:
                if(j-1<0):
                    newarr[i,j] = value-value*abs(rand2)
                    newarr[i,j-1] = value*abs(rand2)
   
    return newarr
                        
            

        
def upscaleblur(arr,expo):

    #get size of arr
    while True:
        csize = 2**(expo-1)
        #Linear interpolation
        new_arr = skimage.transform.resize(arr,(ARR_SIZE*csize,ARR_SIZE*csize), order=1)
        #new_arr = arrJitter(new_arr)
        #Radial blur
        new_arr = scipy.ndimage.gaussian_filter(new_arr, sigma=1)
        new_arr = scipy.ndimage.gaussian_filter(new_arr, sigma=1)
        new_arr = scipy.ndimage.gaussian_filter(new_arr, sigma=1)
        expo += 1
        
        arr = new_arr
        if expo >=11: #Temp, but not going to be
            break

    return arr

    

def placeNewPixelBorders(size):
    greatest=(ARR_SIZE*size)-2
    #OLD way, only edges
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

def placeNewPixel(size):
    greatest=(ARR_SIZE*size)-2
    while(True):
        greatest = (ARR_SIZE*size)-2
        x = np.random.randint(1,greatest)
        y = np.random.randint(1,greatest)
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
        if move == 0: #Left
            if x>2:
                if(grid_map.check_point(x-1,y)):
                    grid_map.add_connection(x,y,x-1,y)
                    break
                grid_map.delete_point_before_connection(x,y)
                x=x-1
                grid_map.add_point(x,y)
        elif move == 1: #Right
            if x<greatest:
                if grid_map.check_point(x+1,y):
                    grid_map.add_connection(x,y,x+1,y)
                    break
                grid_map.delete_point_before_connection(x,y)
                x=x+1
                grid_map.add_point(x,y)
        elif move == 2: #Up
            if y>2:
                if grid_map.check_point(x,y-1):
                    grid_map.add_connection(x,y,x,y-1)
                    break
                grid_map.delete_point_before_connection(x,y)
                y=y-1
                grid_map.add_point(x,y)
        elif move == 3:
            if y<greatest: #Down
                if grid_map.check_point(x,y+1):
                    grid_map.add_connection(x,y,x,y+1)
                    break
                grid_map.delete_point_before_connection(x,y)
                y=y+1
                grid_map.add_point(x,y)
        else:
            print("Error in moving pixel") # WILL NEVER HAPPEN
    if(x == 1 or x == greatest or y == 1 or y == greatest): #Check if on the edge
        pointdict[(x,y)] = 1
        if(len(pointdict) == 16): #a few edges found
            edgefound = True
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
        x_sized = x*2
        y_sized = y*2
        if not upscaled_map.check_point(x_sized, y_sized):
            upscaled_map.add_point(x*2, y*2)  # Add the scaled point itself
        
        # Get the connections of the current point
        connections = grid_map.get_connections(x, y)

        
        # Scale each connected point and add connections in the upscaled map
        for cx, cy in connections:
            # Scale the connected point
            if(x-1 == cx): #left
                upscaled_map.add_point(x_sized-1, y_sized)
                if not upscaled_map.check_point(x_sized-2, y_sized):
                    upscaled_map.add_point(x_sized-2, y_sized)
                upscaled_map.add_connection(x_sized, y_sized, x_sized-1, y_sized)
                upscaled_map.add_connection(x_sized-1, y_sized, x_sized-2, y_sized)

            elif(x+1 == cx): #right
                upscaled_map.add_point(x_sized+1, y_sized)
                if not upscaled_map.check_point(x_sized+2, y_sized):
                    upscaled_map.add_point(x_sized+2, y_sized)
                upscaled_map.add_connection(x_sized, y_sized, x_sized+1, y_sized)
                upscaled_map.add_connection(x_sized+1, y_sized, x_sized+2, y_sized)
            elif(y-1 == cy): #up
                upscaled_map.add_point(x_sized, y_sized-1)
                if not upscaled_map.check_point(x_sized, y_sized-2):
                    upscaled_map.add_point(x_sized, y_sized-2)
                upscaled_map.add_connection(x_sized, y_sized, x_sized, y_sized-1)
                upscaled_map.add_connection(x_sized, y_sized-1, x_sized, y_sized-2)
            elif(y+1 == cy): #down
                upscaled_map.add_point(x_sized, y_sized+1)
                if not upscaled_map.check_point(x_sized, y_sized+2):
                    upscaled_map.add_point(x_sized, y_sized+2)
                upscaled_map.add_connection(x_sized, y_sized, x_sized, y_sized+1)
                upscaled_map.add_connection(x_sized, y_sized+1, x_sized, y_sized+2)
            else:
                print("Error in upscaling")
    grid_map = upscaled_map
    


def getHeightMap(size):
    frontier = {}
    arr = np.zeros((ARR_SIZE*size, ARR_SIZE*size), dtype=int)
    for i in range(1, ARR_SIZE*size):
        for j in range(1, ARR_SIZE*size):
            if grid_map.check_point(i, j):  # Check if point is in the grid
                if grid_map.num_of_connections(i, j) == 1:
                    frontier[(i, j)] = 1
                    arr[(i, j)] = 1

    # Expand frontier until all points are filled 
    #TODO: REDO TO ALLOW FOR EDGE CONNECTIONS TO CHECK HEIGHEST
    max_val = 0

    while frontier:
        item, _ = min(frontier.items(), key=lambda x: x[1])
        i, j = item
        for x, y in grid_map.get_connections(i, j):
            if 0 <= x < ARR_SIZE*size and 0 <= y < ARR_SIZE*size:
                if(arr[(x,y)] < frontier[(i,j)]+1):
                    frontier[(x, y)] = frontier[(i, j)] + 1
                    arr[(x, y)] = frontier[(i, j)] + 1
                
                max_val = max(max_val, arr[(x, y)])

        frontier.pop((i, j))
    print("MAX:", max_val)
    return arr
    
def printArea(arr,i,j):
    if i-10 < 0:
        starti = 0
    else:
        starti = i-10
    if j-10 < 0:
        startj = 0
    else:
        startj = j-10
    if i+10 > ARR_SIZE-1:
        endi = ARR_SIZE-1
    else:
        endi = i+10
    if j+10 > ARR_SIZE-1:
        endj = ARR_SIZE-1
    else:
        endj = j+10
    for x in range(starti,endi):
        for y in range(startj,endj):
            print(arr[x,y], end = "  ")
        print("")


#Currently wont work
def toImage():

    global final_map
    #plot array
    plt.axis('off')  
    plt.imshow(final_map, cmap='gray')


    try:
        os.remove("mountain.png")
    except FileNotFoundError:
        print("No file to remove")
        
    plt.savefig("mountain.png", bbox_inches='tight', pad_inches=0)
    plt.show()


def printNeighbours(location):
    x,y = location
    string = "Neighbours of: " + str(location)
    if grid_map.check_point(x-1,y):
        string += " left "
    if grid_map.check_point(x+1,y):
        string += " right "
    if grid_map.check_point(x,y-1):
        string += " up "
    if grid_map.check_point(x,y+1):
        string += " down "
    print(string)


main()