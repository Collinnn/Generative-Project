
import numpy as np
from matplotlib import pyplot as plt
ARR_SIZE = 10

def main ():
    print("mountain home:")
    # numpy 2d array
    mountain_arr = np.zeros((ARR_SIZE, ARR_SIZE))
    setFirstPixel(mountain_arr)
    while(True):
        mountain_arr, location = placeNewPixel(mountain_arr)
        print(mountain_arr)
        return
        mountain_arr = movePixel(mountain_arr, location)
        if(density(mountain_arr) >= 0.3):
            break
    ##printMountain(mountain_arr) # Finished mountain
    #toImage(mountain_arr)
    
    


def placeNewPixel(mountain_arr):
    
    while (True):
        place = np.random.randint(0, 4)
        rand = np.random.randint(1,ARR_SIZE-1)
        print(rand)
             #y   , x
        up = (1, rand)    
        down = (rand,ARR_SIZE-2) 
        left = (1,rand)
        right = (ARR_SIZE-1,rand)

        arr = [up,down,left,right]
        x,y = arr[place]
        print(place,x,y)
        if mountain_arr[x,y] == 0:
            mountain_arr[x,y] = 1
            return mountain_arr, (x,y)


def checkPixelEdges(mountain_arr, location):
    # 000
    # 0x0
    # 000
    #Check if border of array
    printNeighbours(mountain_arr, location)
    up = mountain_arr[location-ARR_SIZE]
    down = mountain_arr[location+ARR_SIZE]
    left = mountain_arr[location-1]
    right = mountain_arr[location+1]
    upleft = mountain_arr[location-ARR_SIZE-1]
    upright = mountain_arr[location-ARR_SIZE+1]
    downleft = mountain_arr[location+ARR_SIZE-1]
    downright = mountain_arr[location+ARR_SIZE+1]
    if (up == 1 or down == 1 or left == 1 or right == 1 or upleft == 1 or upright == 1 or downleft == 1 or downright == 1) :
        return True
    return False

  
#Location = (x,y) tuple
def movePixel(mountain_arr,location):
    while True:
        move = randMove()
        if checkPixelEdges(mountain_arr, location): #Found a neighbour
            #print("break out")
            break
        
        print("move: ", move)
        if move == 0:
            # move up
            if location - ARR_SIZE < ARR_SIZE: #  top of the array
                continue
            else:
                mountain_arr[location] = 0
                mountain_arr[location - ARR_SIZE] = 1
                location = location - ARR_SIZE
        elif move == 1:
            # move down
            print(location, ARR_SIZE*(ARR_SIZE-1))
            if location + ARR_SIZE >= ARR_SIZE*(ARR_SIZE-1): # Bottom
                continue
            else:
                mountain_arr[location] = 0
                mountain_arr[location + ARR_SIZE] = 1
                location = location + ARR_SIZE
        elif move == 2:
            # move left
            if location -1 % ARR_SIZE == 0: # Left
                continue
            else:
                mountain_arr[location] = 0
                mountain_arr[location - 1] = 1
                location = location - 1
        else:
            # move right
            if location % ARR_SIZE == ARR_SIZE - 1: # Right
                continue
            else:
                mountain_arr[location] = 0
                mountain_arr[location + 1] = 1
                location = location+1
    #printMountain(mountain_arr)
    return mountain_arr

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


def setFirstPixel(mountain_arr):
    x = (ARR_SIZE//2)-1
    y = (ARR_SIZE//2)-1
    # center of the array
    mountain_arr[x,y] = 1
    return mountain_arr
    

def printMountain(mountain_arr):
    for i in range(ARR_SIZE):
        for j in range(ARR_SIZE):
            if mountain_arr[j+(i*ARR_SIZE)] == 0:
                print(" ", end = " ")
            else:
                print(u'\u25A1', end = " ")
        print("")
        
def toImage(mountain_arr):
    # convert array to image
    mountain_arr = np.reshape(mountain_arr, (ARR_SIZE, ARR_SIZE))
    plt.imshow(mountain_arr, cmap='gray')
    plt.show()
    
    
def rescaleMountain(mountain_arr):
    newArr = [(ARR_SIZE*ARR_SIZE*4)] # 4 times the size of the original array
    newArr = np.zeros(newArr)
    
    #Nearest neighbor interpolation

    
    

    


    return mountain_arr


def printNeighbours(mountain_arr, location):
    up = mountain_arr[location-ARR_SIZE]
    down = mountain_arr[location+ARR_SIZE]
    left = mountain_arr[location-1]
    right = mountain_arr[location+1]
    upleft = mountain_arr[location-ARR_SIZE-1]
    upright = mountain_arr[location-ARR_SIZE+1]
    downleft = mountain_arr[location+ARR_SIZE-1]
    downright = mountain_arr[location+ARR_SIZE+1]
    print(upleft, up, upright,"\n", left,mountain_arr[location],right, "\n", downleft, down, downright,"\n")
  

main()