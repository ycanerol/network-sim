#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 15:14:50 2017

@author: ycanerol


Network simulator in python

Based off of Beggs Plenz 2003 and Beggs Haldemann 2005 papers


"""

import numpy as np
import matplotlib as plt
from random import shuffle

#Initialization
#Enter and change parameters here

node_nr=8
#avg_connection_per_node=node_nr/10  #To be changed, this is a coarse determination
connections=4   #Defined as C in the paper
sigma=1.2

#%% Generating the network
nodes=[[] for i in range(node_nr)]
#Nodes list will contain lists indices of connected nodes to each element

for i in range(node_nr):
    a=list(range(node_nr))
    shuffle(a)
    #We shuffle the index list, the connections of current node will be taken from here
    
    #connections=int(np.floor(np.random.normal(avg_connection_per_node,5)))
    #Number of connections is determined by normal distribution
    
    nodes[i]=a[:connections+1]
    #We take one more than needed, in case one of the indices point to the neuron itself
    
    flag=True
    for j in range(connections):
        if nodes[i][j]==i:
            flag=False
            #print("removed {}\n".format(i))
            nodes[i].remove(i)
            #Remove self-connection
    if flag:
        del nodes[i][-1]
        #If we removed no self-connections, delete the extra index at the end.
        
#We established a recurrent network, we need to establish transmission proabability for each connection

tr_probabilities=[[] for i in range(node_nr)]
for i in range(node_nr):
    for j in range(len(nodes[i])):
        divider=list(np.sort(np.random.random_sample(connections-1)))
        divider.insert(0,0)
        divider.insert(len(divider),1)
        divider=np.multiply(divider,sigma) #Scale the interval to be the size of sigma
        for k in range(1,connections):
            tr_probabilities[i].append(divider[k]-divider[k-1])
        #The constraint is that for each node sigma_i should be equal to sigma
        #Sums of the probabilities for one node should be sigma
        #For this, we divide the sigma into C parts and use the sizes of the parts as probabilities
        
        
