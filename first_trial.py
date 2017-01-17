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

node_nr=200
transmit_prob=0.01
avg_connection_per_node=node_nr/10  #To be changed, this is a coarse determination


nodes=[[] for i in range(node_nr)]
#Nodes list will contain lists indices of connected nodes to each element

for i in range(node_nr):
    a=list(range(node_nr))
    shuffle(a)
    #We shuffle the index list, the connections of current node will be taken from here
    connections=int(np.floor(np.random.normal(avg_connection_per_node,5)))
    #Number of connections is determined by normal distribution
    nodes[i]=a[:connections+1]
    #We take one more than needed, in case one of the indices point to the neuron itself
    flag=True
    for j in range(connections):
        if nodes[i][j]==i:
            flag=False
            print("removed {}\n".format(i))
            nodes[i].remove(i)
            #Remove self-connection
    if flag:
        del nodes[i][-1]
        #If we removed no self-connections, delete the extra index at the end.
        
       
   
