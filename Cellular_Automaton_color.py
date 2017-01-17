#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 10:36:18 2016

@author: zhoulinn
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cellular Automaton trial 1
with rule 

Created on Fri Dec  2 18:25:55 2016

@author: zhoulinn
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
import random 
import matplotlib.animation as animation
import sys


rows = 50
columns = 50

board = np.zeros((rows,columns))
#board = np.zeros((10,10))

choice = input ('2 random starting point? [Y/N]')

if (choice == 'Y'):
    #start with two random points on board
    x1 = np.random.randint(0,rows-1)
    y1 = np.random.randint(0,columns-1)
    
    x2 = np.random.randint(0,rows-1)
    y2 = np.random.randint(0,columns-1)

elif (choice == 'N'):
    x1 = int (input ('first x (integer 0 - ' + str(rows-1) + '):'))
    y1 = int (input ('first y (integer 0 - ' + str(columns-1) + '):'))
    x2 = int (input ('second x (integer 0 - ' + str(rows-1) + '):'))
    y2 = int (input ('second y (integer 0 - ' + str(columns-1) + '):'))
    
else:
    print ('error input!')

board [x1][y1] = 1
board [x2][y2] = 1
 
#cycles = 20
cycles = input ('And how many cycles would u like to see? (default = 30)')
if (cycles == ''):
    cycles = 30
else:
    pass

cycles = int (cycles)        

def rule2d (left, right, up, down):
    if (left + right + up + down == 0):
        return 0
    elif (left + right + up + down == 1):
        return 1
    elif (left + right + up + down == 2):
        return 0
    elif (left + right + up + down == 3):
        return 0
    elif (left + right + up + down == 4):
        return 0
    else:
        return 1
        #print ('hey there s sth wrong with the code..')        


        
# print the board according to values 
count = 1
fig = plt.figure()

User = input('Enter to start the program!')

while (count < cycles):    

    for i in range (rows-1):
        for j in range (columns-1):
            left = board [i-1][j]
            right = board [i+1][j]
            up = board [i][j-1]
            down = board [i][j+1]
            middle = board [i][j]
            
            board[i][j] += rule2d (left, right, up, down)
            if (board[i][j] >= 10):
                board[i][j] -= 13
            else:
                pass

            #board[i][j][color] = eRule126 (left, middle, right)

    color = random.randint(0,2)
    print (count)
    #plt.matshow(board)
    img = plt.matshow(board, cmap='spectral')
    #img = plt.matshow(count * board, cmap='spectral')
    plt.colorbar(img, orientation='vertical')
    img.set_clim(vmin=0, vmax=10)
    
    
    if (count < 10):
        plt.savefig('images/img00'+str(count)+'.jpg')
    elif (10 <= count < 100):
        plt.savefig('images/img0'+str(count)+'.jpg')
    elif (100 <= count < 1000):
        plt.savefig('images/img'+str(count)+'.jpg')
    else:
        pass
    
    plt.show()
    time.sleep(0.05) # delays for 0.5 seconds
    count += 1 
       
# let user to exit the program            
    #if User == 'e':
        #break
    
'''    
ani = animation.FuncAnimation(fig,300,interval=30)
writer = animation.writers['ffmpeg'](fps=30)

ani.save('demo.mp4',writer=writer,dpi=dpi)
#return ani

#mencoder
'''

'''
problems (solved): 
    1. displaying array with color: RGB --> spectrum & setting limits
    2. input datatype: str --> int
    3. 
    
    (unsolved)
    1. more realistic rules (e.g. considering previous events)
    2. export as video 
    
'''