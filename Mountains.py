
import numpy as np
from matplotlib import pyplot as plt
ARR_SIZE = 100


def main ():
    print("mountain home:")
    mountain_arr = [ARR_SIZE*ARR_SIZE]
    mountain_arr = np.zeros(mountain_arr)
    
    setFirstPixel(mountain_arr)
    while(True):
        mountain_arr, location = placeNewPixel(mountain_arr)
        mountain_arr = movePixel(mountain_arr, location)
        if(density(mountain_arr) >= 0.5):
            break
    #printMountain(mountain_arr) # Finished mountain
    toImage(mountain_arr)
    
    


def placeNewPixel(mountain_arr):
    
    while (True):
        location = np.random.randint(0, ((ARR_SIZE-1)*(ARR_SIZE-1)))
        if mountain_arr[location] == 0:
            mountain_arr[location] = 1
            return mountain_arr, location

    

    

def movePixel(mountain_arr,location):

    while True:
        move = randMove()
        
        if move == 0:
            # move up
            if location - ARR_SIZE < 0: # out of bounds
                continue
            if mountain_arr[location - ARR_SIZE] == 1: # found pixel
                break
            
            mountain_arr[location] = 0
            mountain_arr[location - ARR_SIZE] = 1
        elif move == 1:
            # move down
            if location + ARR_SIZE > (ARR_SIZE * ARR_SIZE): # out of bounds
                continue
            if mountain_arr[location + ARR_SIZE] == 1: # found pixel
                break
            
            mountain_arr[location] = 0
            mountain_arr[location + ARR_SIZE] = 1
        elif move == 2:
            # move left
            if location % ARR_SIZE == 0: # out of bounds
                continue
            if mountain_arr[location + 1] == 1: # found pixel
                break

            mountain_arr[location] = 0
            mountain_arr[location - 1] = 1
        else:
            # move right
            if location % ARR_SIZE == ARR_SIZE - 1: # out of bounds
                continue
            if mountain_arr[location - 1] == 1: # found pixel
                break
            mountain_arr[location] = 0
            mountain_arr[location + 1] = 1
    return mountain_arr

def randMove():
    # random move
    move = np.random.randint(0, 3)
    return move
    
    
    
# density of the mountain
def density(mountain_arr):
    # density of the mountain
    amount = 0
    for i in range(ARR_SIZE):
        for j in range(ARR_SIZE):
            amount += mountain_arr[j+(i*ARR_SIZE)]
    
    density = amount / float((ARR_SIZE * ARR_SIZE))
    print(density)
    return density


def setFirstPixel(mountain_arr):
    center = (ARR_SIZE//2) * (ARR_SIZE//2)
    # center of the array
    print(center)
    mountain_arr[center] = 1
    
    return mountain_arr
    

def printMountain(mountain_arr):
    print(mountain_arr)
    for i in range(ARR_SIZE):
        for j in range(ARR_SIZE):
            if mountain_arr[j+(i*ARR_SIZE)] == 0:
                print(" ", end = " ")
            else:
                print(u'\u25A1', end = " ")
        print("")
        
def toImage(mountain_arr):
    # convert array to image
    plt.imshow(mountain_arr, cmap='gray')
    plt.show()
    
    
def rescaleMountain(mountain_arr):
    newArr = [(ARR_SIZE*ARR_SIZE*4)] # 4 times the size of the original array
    newArr = np.zeros(newArr)
    
    #Nearest neighbor interpolation

    
    

    


    return mountain_arr


main()