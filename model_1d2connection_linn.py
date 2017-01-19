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
import matplotlib as plt
import random
from random import randint


node_num = 10   # a square number is preferred --> easier for visualizatio in 2D matrix later
connection_num = 2
initializing_node_num = 3

if (node_num <= connection_num):
    print ('more nodes than connections, pls check ur network! Default: 2 outgoing connections from each node')
    

old_node_states = np.zeros (node_num) # records original statuss of nodes on = 1; off = 0
new_node_states = np.zeros (node_num) # records statuss of nodes after info transmission on = 1; off = 0
node_connections = np.zeros([node_num,connection_num]) #indeces of connections made from each node
p_connections = np.zeros([node_num,connection_num]) # probabilities of each connection

#print (node_connections)


#setting connections bewteen nodes, exlcuding duplicates and self-connections 
for i in range(0,node_num):
    random_list = random.sample(range(0, node_num), connection_num + 1) #generate a list of non-duplicated random connections for node i
    
    for j in range (0, connection_num): #put in the connections
            node_connections[i][j] = random_list[j]
            
            while (node_connections[i][j] == i):
                node_connections[i][j] = random_list[connection_num] # re-connect to exclude self-connections


print (node_connections)
            
# setting probabilities for each connection, to make sigma = 1, sum p_connections from i should = 1!
for i in range(0,node_num):
    for j in range (0, connection_num):
            p_connections[i][j] = random.random()          

print (p_connections)

#%%
# initializing the network with active nodes

active_nodes = random.sample(range(0, node_num), initializing_node_num) #array of 3 non-duplicate integers

print (active_nodes)

for i in active_nodes:
            old_node_states[i] = 1  #activate the network
            
#new_node_states = old_node_states # get the new states ready
print (old_node_states)


#%%
# network in action

t = 30 # number of runs
connection_transmission = np.zeros([node_num,connection_num]) # transmission form node i to node_connections[i][j] = 1, no transmission = 0


#determine whether connections transmit. input_value (0,1)
def if_connect(input_value, probability): 
    if (input_value <= probability):
        return 1
    else:
        return 0

# setting transmission status to each connection
#for k in range (0, t):
for j in range (0,connection_num):
    for i in range(0,node_num):
        connection_transmission[i][j] = if_connect(random.random(), p_connections[i][j])
        
print (connection_transmission)        


#assign values to nodes after one round
node_activated = np.zeros (node_num) #record whether node has changed from 0 to 1 in the current round: Yes --> 1; No --> 0
for j in range (0,connection_num):
    for i in range(0,node_num):
        
        if (old_node_states[i] == 1 and connection_transmission[i][j] == 1): #if ancester state ==1 and transmission == 1 --> descendent = 1
            new_node_states[node_connections[i][j]] = 1
            node_activated[node_connections[i][j]] = 1
        elif (node_activated [node_connections[i][j]] == 1):
            #a node has been changed from 0 to one by previous connections in this round --> it ramains 1
            new_node_states[node_connections[i][j]] == 1
        else:
            new_node_states[node_connections[i][j]] = 0
        #print (new_node_states)

print (new_node_states)
        
"""
for i in range(0,node_num): #setting new values for each node according to threshold

    if (sum_input[i] >= threshold):
        network1[network1[i][int(node_info / 2) + 1]][0] = 1
    else:
        network1[network1[i][int(node_info / 2) + 1]][0] = 0
        
print (network1)
"""

#%%
# let's visualize our network in a 2D matrix!

# split the 1D array into square 2D and plot the states






