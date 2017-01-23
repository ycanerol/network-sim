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

node_nr=64
connections=4   #Defined as C in the paper
sigma=1.2

#For time iterations
time_steps=50 #How many times we transmit
spont_prob=0.001 #Proabability of  spontaneous activation of connections

#%%
def set_array(node_nr):     #Function to set an array of empty arrays
    a=[[]for a in range(node_nr)]
    return a

#%% Generating the network
nodes=set_array(node_nr)
#Nodes list will contain lists indices of connected nodes to each element

for i in range(node_nr):
    a=list(range(node_nr))
    shuffle(a)
    #We shuffle the index list, the connections of current node will be taken from here
    
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
flag=True
prob_iteration_count=0
while flag:
    tr_probabilities=set_array(node_nr)
    for i in range(node_nr):
        divider=list(np.sort(np.random.random_sample(connections-1)))
        divider.insert(0,0)
        divider.append(1)
        divider=list(np.multiply(divider,sigma)) #Scale the interval to be the size of sigma
        for k in range(1,len(divider)):
            tr_probabilities[i].append(divider[k]-divider[k-1])
            #The constraint is that for each node sigma_i should be equal to sigma
            #Sums of the probabilities for one node should be sigma
            #For this, we divide the sigma into C parts and use the sizes of the parts as probabilities
    all_less_than1=True
    for i in range(node_nr):
        for k in range(connections):
            if tr_probabilities[i][k]>1:
                all_less_than1=False
    if all_less_than1:
        flag=False
    if prob_iteration_count>10000: #Deals with the case that C and sigma are inappropriate, prevents infinite loop
        raise ValueError('More than 10.000 iterations when setting up probabilities, terminating. There are >1 probabilities.')
        break
    prob_iteration_count+=1
del j,k,a,divider,flag
#The network is set up with required properties at this point

#%% Incorporating time and inputs

outputs=list(np.zeros(node_nr)) #Holds the state of each node.

for t in range(time_steps):
    
    inputs=outputs #The outputs of the previous iteration are inputs of current.
    outputs=list(np.zeros(node_nr)) 
    
    for i in range(node_nr):
        for k in range(connections):
            if np.random.random()<spont_prob:              
                outputs[nodes[i][k]]=1
            elif inputs[i] and np.random.random()<tr_probabilities[i][k]:
                outputs[nodes[i][k]]=1  #No else statement so if the same node was activated 
                                        #by another connection, it will not be changed.
        if outputs[i]:
            print('t={:3.0f},i={:2.0f}'.format(t,i))
            
            
        
        
        
        
        
        
        
        
        
