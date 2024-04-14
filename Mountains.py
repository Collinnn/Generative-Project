
import numpy as np
from matplotlib import pyplot as plt
ARR_SIZE = 10
pixel=0


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
        return (x,y) in self.connections

# Example usage
grid_map = GridMap()



def main ():
    print("mountain home:")
    # numpy 2d array
    setFirstPixel()
    while(True):
        location = placeNewPixel()
        print(location)
        
        movePixel(location)
        printMountain()
        return
        if(density(mountain_arr) >= 0.3):
            break
    ##printMountain(mountain_arr) # Finished mountain
    #toImage(mountain_arr)
    
    


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
    (x,y) = location
    #printNeighbours(location)
    
    if grid_map.check_point(x-1,y):
        grid_map.add_connection(x,y,x-1,y)
        return True
    elif grid_map.check_point(x+1,y):
        grid_map.add_connection(x,y,x+1,y)
        return True
    elif grid_map.check_point(x,y-1):
        grid_map.add_connection(x,y,x,y-1)
        return True
    elif grid_map.check_point(x,y+1):
        grid_map.add_connection(x,y,x,y+1)
        return True
    return False

  
#Location = (x,y) tuple
def movePixel(location):
    x,y = location
    while True:
        move = randMove()
        if checkPixelEdges(location): #Found a neighbour
            
            break
        if move == 0:
            if x>2:
                x=x-1
        elif move == 1:
            if x<ARR_SIZE-2:
                x=x+1
        elif move == 2:
            if y>2:
                y=y-1
        elif move == 3:
            if y<ARR_SIZE-2:
                y=y+1
        else:
            print("Error")
        print(x,y)
    return

def randMove():
    # random move
    return  np.random.randint(0, 3)
   
    
# density of the mountain
def density(mountain_arr):
    # density of the mountain
    amount = 0
    for i in range(ARR_SIZE):
        for j in range(ARR_SIZE):
            amount += mountain_arr[j+(i*ARR_SIZE)]
    
    density = amount / float((ARR_SIZE * ARR_SIZE))
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