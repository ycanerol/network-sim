#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 21:25:44 2017

@author: zhoulinn
first trail 
"""

"""
define the network: 1D 
node_info: 
rows[1&2]: 2 connection nodes
rows[3&4]: probabilities

"""
import numpy as np
import matplotlib.pyplot as plt
import math
import random
from random import randint
import time
import sys
from matplotlib import colors


row = 10
node_num = row * row   # a square number is preferred --> easier for visualizatio in 2D matrix later
connection_num = 4


t = 50 # number of steps
sigma = 1.0   # average number of nodes activated by one anscester 
activity_mode = False #True for "driven mode", False for "spontaneous mode"
initializing_node_num = 2 # for 'driven' mode: number of initializing nodes
p_spontaneous = 0.001 # for 'spontaneous' mode: probability of node being spontaneously active

print_img = False
save_img = False
analyze_avalanches = True



#%% functions

#determine whether a node will be activated. input_value (0,1)
def if_activate(input_value, probability): 
    if (input_value <= probability):
        return 1
    else:
        return 0

        
        
# split the 1D array into square 2D 
def split(array, n):
    two_d_array = []
    for i in range(0, len(array), n):
        two_d_array.append(list(array[i:i + n]))
        #print(i)
        
    return list(two_d_array)        

    
    
# get lengths of avalanches from active time steps
# step_size: define "continous"
def get_avalanche_lengths(data, step_size = 1):
    non_duplicate_data = list(set(data)) #remove duplicates from recorded active steps
    
    break_indeces = np.array((np.where(np.diff(non_duplicate_data) != step_size)))#array of index where steps stop being continous 
    avalanche_steps = np.array_split(non_duplicate_data, break_indeces[0]+1) #split the array at incontinueous points
    length_list = []
    
    for i in range(len(avalanche_steps)):
        length_list.append(len(avalanche_steps[i]))
    
    return length_list
    
#print(get_avalanche_lengths([1,1,1,2,3,6,6,7,8,10,11], 1))




# get avalanche sizes. i.e. # of active nodes during each avalanche
# step_size: define "continous", here >= 1 to include duplicates --> calculate size
def get_avalanche_sizes(data, step_size = 1):
    break_indeces = np.array((np.where(np.diff(data) > step_size)))#array of index where steps stop being continous 
   
    avalanche_steps = np.array_split(data, break_indeces[0]+1) # list steps in all avalanches, including duplicates
    
    size_list = []
    for i in range(len(avalanche_steps)):
        size_list.append(len(avalanche_steps[i])) #add up #of active nodes in each step
        
    return size_list
        
a = get_avalanche_sizes([1,1,1,2,3,6,6,7,8,10,11], 1)
print(a)


    
#%% setting up the network
    
if (node_num <= connection_num):
    print ('more nodes than connections, pls check ur network! Default: 9 nodes, 2 outgoing connections from each node')
    node_num = 9
    connection_num = 2

old_node_states = np.zeros(node_num) # records original statuss of nodes on = 1; off = 0
new_node_states = np.zeros(node_num) # records statuss of nodes after info transmission on = 1; off = 0
node_activities = []
node_connections = np.zeros([node_num,connection_num]) #indeces of connections made from each node
p_connections = np.zeros([node_num,connection_num]) # probabilities of each connection

#print ("connections: \n", node_connections)


#setting connections bewteen nodes, exlcuding duplicates and self-connections 
for i in range(0,node_num):
    random_list = random.sample(range(0, node_num), connection_num + 1) #generate a list of non-duplicated random connections for node i
    
    for j in range (0, connection_num): #put in the connections
            node_connections[i][j] = random_list[j]
            
            while (node_connections[i][j] == i):
                node_connections[i][j] = random_list[connection_num] # re-connect to exclude self-connections


#print ("connection matrix: \n", node_connections)
            
# setting probabilities for each connection, to make sigma = 1, sum p_connections from i should = 1!
count = 0
flag = True
while flag and count <= 1000:

    for i in range(node_num):
        #generate a list of probabilities with sum = sigma
        divider_list = list(np.sort(np.random.random_sample((connection_num - 1)) ))
        divider_list.insert(0,0)
        divider_list.append(1)
        divider_list = [i * sigma for i in divider_list]
        #divider_list = list(np.multiply(divider,sigma))
        #divider_list = divider_list.sort()
        
        for j in range (connection_num):
            p_connections[i][j] = divider_list[j+1] - divider_list[j]       

    #check if all probabilities are less than 1, if not: repeat & generate new probabilities
    all_less_than_one = True
    for i in range(node_num):
        for j in range (connection_num):
            if p_connections[i][j] > 1: 
                all_less_than_one = False
    
    if  all_less_than_one:
        flag = False
    count += 1

##print probability matrix generation results     
#if not all_less_than_one:
#    print ("failed to generate all probabilities after 1001 attempts, conside a smaller sigma/connection_num ratio.")   
#else:         
#    print ("<1 probabilities generated after " + str(count) + " rounds. \n")            
#print ("transmission probability matrix: \n", p_connections)
#




#%%
# to initialize the network:
# 'driven' mode: initializing the network with active nodes

if activity_mode: 

    active_nodes = random.sample(range(0, node_num), initializing_node_num) #array of 3 non-duplicate integers
    
    print (active_nodes)
    
    for i in active_nodes:
                old_node_states[i] = 1  #activate the network
                
    #new_node_states = old_node_states # get the new states ready
    #print ("original network: \n", old_node_states)
    
else:    
    
    #'spontaneous' mode: initializing each node with spontaneous active probability p_spontaneous
    
    for i in range(0,node_num):
        old_node_states[i] = if_activate(random.random(), p_spontaneous)
    
    #print ("original network: \n", old_node_states)


#%%
# network in action

connection_transmission = np.zeros([node_num,connection_num]) # transmission form node i to node_connections[i][j] = 1, no transmission = 0
count = 0
node_activities_step = []
node_activities_num = []


"""
newpath = '/Users/zhoulinn/python/network-sim-pics/' 
if not os.path.exists(newpath):
    os.makedirs(newpath)
else:
    pass
"""

# This is one experiment with t steps of network activity

while count < t: # iterate through t rounds of activity
    old_node_states = new_node_states    
    new_node_states = np.zeros(node_num)

    #assign connection transmission
    for j in range (0,connection_num):
        for i in range(0,node_num):
            connection_transmission[i][j] = if_activate(random.random(), p_connections[i][j])
            
    #print ("connection transmission: \n", connection_transmission)        
    
    
    #assign values to nodes after one round
#    node_activated = np.zeros (node_num) #record whether node has changed from 0 to 1 in the current round: Yes --> 1; No --> 0
    for j in range (0,connection_num):
        for i in range(0,node_num):
            
            if (old_node_states[i] == 1 and connection_transmission[i][j] == 1): 
                # if ancester state ==1 and transmission == 1 --> descendent = 1
                new_node_states[int(node_connections[i][j])] = 1
                node_activities_step.append(count) #record node activation events
                node_activities_num.append(node_connections[i][j])

#            elif (node_activated[node_connections[i][j]] == 1):
#                # a node has been changed from 0 to one by previous connections in step t --> it ramains 1
#                new_node_states[node_connections[i][j]] = 1

            elif (if_activate(random.random(), p_spontaneous) == 1): 
                #print ('node ' + str(node_connections[i][j]) + 'is spontaneously activated.')
                # if a neuron is sontaneously activated 
                new_node_states[int(node_connections[i][j])] = int(1)
                node_activities_step.append(count) #record node activation events
                node_activities_num.append(node_connections[i][j])
                
    count += 1
    #print ("network after " + str(t) + "rounds of activity transmission: \n", new_node_states)
    
    # split the 1D array into square 2D 
    def split(array, n):
        two_d_array = []
        for i in range(0, len(array), n):
            two_d_array.append(list(array[i:i + n]))
            #print(i)
        
        return list(two_d_array)
        
    network = split(new_node_states, row)
    #print(network)

    
    if print_img:
        #make a color map of fixed colors: 0 --> black; 1 --> white
        cmap = colors.ListedColormap(['black', 'white'])
        bounds=[0,0.5,1]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        
        #plot & save img for this round 
        img = plt.matshow(network, cmap=cmap, norm=norm)
        # make a color bar
        plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=[0, 1])
        
    
    if save_img:    
        
        if (count < 10):
            plt.savefig('/Users/zhoulinn/python/network-sim-pics/network00'+str(count)+'.jpg')
        elif (10 <= count < 100):
            plt.savefig('/Users/zhoulinn/python/network-sim-pics/network0'+str(count)+'.jpg')
        elif (100 <= count < 1000):
            plt.savefig('/Users/zhoulinn/python/network-sim-pics/network'+str(count)+'.jpg')
        else:
            pass
        
        plt.show()
        time.sleep(0.05) # delays for 0.5 seconds    

#print(node_activities)

#%%
if analyze_avalanches:
    #collect avalanches
    
    active_steps = [] #record steps when there's activity
    avalanche_sizes = []
    
    #get avalache lengths (# of steps in each avalanche)
    avalanche_lengths = get_avalanche_lengths(node_activities_step, 1) 
    print("avalanche lengths:")
    print(avalanche_lengths)
    
    #get avalanche sizes (# of node activated during each avalanche)
    avalanche_sizes = get_avalanche_sizes(node_activities_step, 1)
    print("avalanche sizes:")
    print(avalanche_sizes)
        
    
    
    
    #log plots for avalanche occurance
    
    #log-log: avalanche lengths vs. occurance 
    length_num = np.histogram(avalanche_lengths, max(avalanche_lengths))[0]
    print(length_num)
    
    #plt.fig()
    plt.loglog(range(len(length_num)), length_num,'-',basex=10,basey=10)
    #plt.show()
    
    #log-log: avalanche sizes vs. occurance 
    size_num = np.histogram(avalanche_sizes, max(avalanche_sizes))[0]    
    print(size_num)
    
    plt.loglog(range(len(size_num)), size_num,'-',basex=10,basey=10)
    plt.show()



