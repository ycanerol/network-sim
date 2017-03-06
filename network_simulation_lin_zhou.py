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


# network sizes
row = 12
node_num = row * row   # a square number is preferred --> easier for visualizatio in 2D matrix later
connection_num = 4

if (node_num <= connection_num):
    print ('more nodes than connections, pls check ur network! Default: 9 nodes, 2 outgoing connections from each node')
    node_num = 9
    connection_num = 2

    
# networko in action
experiment_num = 5000 # number of experimetns with t steps
t = 100 # number of steps
sigma = 1.0   # average number of nodes activated by one anscester 
activity_mode = True #True for "driven mode", False for "spontaneous mode"
initializing_node_num = 1 # for 'driven' mode: number of initializing nodes, here we don't put in spontaneous activation at each step
p_spontaneous = 0 # for 'spontaneous' mode: probability of node being spontaneously active

print_img = False
save_img = False

analyze_avalanches = True
subsample = True # sample& analyze only first num of nodes 
subsample_num = 10



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
    




# get avalanche sizes. i.e. # of active nodes during each avalanche
# step_size: define "continous", here >= 1 to include duplicates --> calculate size
def get_avalanche_sizes(data, step_size = 1):
    break_indeces = np.array((np.where(np.diff(data) > step_size)))#array of index where steps stop being continous 
   
    avalanche_steps = np.array_split(data, break_indeces[0]+1) # list steps in all avalanches, including duplicates
    
    size_list = []
    for i in range(len(avalanche_steps)):
        size_list.append(len(avalanche_steps[i])) #add up #of active nodes in each step
        
    return size_list
    
    
#get first subsample_num of node activities from full-length recordings, 
# return subsampled recordings of node activity steps in ascending order
def subsample(node_activities_num, node_activities_step, subsample_num):
    node_activities_num_sort = np.array([np.argsort(node_activities_num)]) #sort by ascending node number
    print(node_activities_num_sort) 
    #node_activities_num_sort = [int(x) for x in node_activities_num_sort]
    
#    
#    new = []
#    for i in node_activities_num_sort:
#        new.append(int(i))
#    node_activities_num_sort = new
#    
#    
    
    node_activities_step_sort = node_activities_step[np.array([node_activities_num_sort])] # sort steps to match node numbers 
    
    sample_trim_index = node_activities_num_sort.index(subsample_num + 1) #cut out first subsample_num nodes: subsample
    node_activities_step_sort = node_activities_step_sort[:sample_trim_index]
    
    return np.sort(node_activities_step_sort) 
        
    
        
#%%
# for experiments with t steps:
exp_count = 0
# to record counts in one experiment

avalanche_lengths = []
avalanche_sizes = []
    

    
#%% setting up the network: new networks for each experiment
while exp_count < experiment_num:
    
    old_node_states = np.zeros(node_num) # records original statuss of nodes on = 1; off = 0
    new_node_states = np.zeros(node_num) # records statuss of nodes after info transmission on = 1; off = 0
    node_activities = []
    node_connections = np.zeros([node_num,connection_num]) #indeces of connections made from each node
    p_connections = np.zeros([node_num,connection_num]) # probabilities of each connection
    connection_transmission = np.zeros([node_num,connection_num]) # record transmission form node i to node_connections[i][j] = 1, no transmission = 0
                             
    #print ("connections: \n", node_connections)
    
    
    #setting connections bewteen nodes, exlcuding duplicates and self-connections 
    for i in range(0,node_num):
        random_list = random.sample(range(0, node_num), connection_num + 1) #generate a list of non-duplicated random connections for node i
        
        for j in range (0, connection_num): #put in the connections
                node_connections[i][j] = random_list[j]
                
                while (node_connections[i][j] == i):
                    node_connections[i][j] = random_list[connection_num] # re-connect to exclude self-connections
    
    
    #print ("connection matrix: \n", node_connections)
    
    
    
    #%%
    # setting RANDOM probabilities for each connection, to make sigma = 1, sum p_connections from i should = 1!
    #count = 0
    #flag = True
    #while flag and count <= 1000:
    #
    #    for i in range(node_num):
    #        #generate a list of probabilities with sum = sigma
    #        divider_list = list(np.sort(np.random.random_sample((connection_num - 1)) ))
    #        divider_list.insert(0,0)
    #        divider_list.append(1)
    #        divider_list = [i * sigma for i in divider_list]
    #        #divider_list = list(np.multiply(divider,sigma))
    #        #divider_list = divider_list.sort()
    #        
    #        for j in range (connection_num):
    #            p_connections[i][j] = divider_list[j+1] - divider_list[j]       
    #
    #    #check if all probabilities are less than 1, if not: repeat & generate new probabilities
    #    all_less_than_one = True
    #    for i in range(node_num):
    #        for j in range (connection_num):
    #            if p_connections[i][j] > 1: 
    #                all_less_than_one = False
    #    
    #    if  all_less_than_one:
    #        flag = False
    #    count += 1
    
    
    #print probability matrix generation results     
    #if not all_less_than_one:
    #    print ("failed to generate all probabilities after 1001 attempts, conside a smaller sigma/connection_num ratio.")   
    #else:         
    #    print ("<1 probabilities generated after " + str(count) + " rounds. \n")            
    #print ("transmission probability matrix: \n", p_connections)
    #
    
    #%%
    #generate EVEN connection probabilities
    p_connections = np.full(([node_num,connection_num]), (sigma/connection_num))



#%%
    # to initialize the network:
    # 'driven' mode: initializing the network with active nodes
    
    if activity_mode: 
    
        active_nodes = random.sample(range(0, node_num), initializing_node_num) #array of 3 non-duplicate integers
        
        #print (active_nodes)
        
        for i in active_nodes:
            old_node_states[i] = 1  #activate the network

        
    else:    
        
        #'spontaneous' mode: initializing each node with spontaneous active probability p_spontaneous
        
        for i in range(0,node_num):
            old_node_states[i] = if_activate(random.random(), p_spontaneous)
        
        #print ("original network: \n", old_node_states)
    
    
#%%
    count_t = 0
    
    
    # This is one experiment with t steps of network activity
    node_activities_num = []
    node_activities_step = []
    
    while count_t < t: # iterate through t steps of activity
    
        #assign connection transmission
        for j in range (0,connection_num):
            for i in range(0,node_num):
                connection_transmission[i][j] = if_activate(random.random(), p_connections[i][j])
                

        #assign values to nodes after one round
    #    node_activated = np.zeros (node_num) #record whether node has changed from 0 to 1 in the current round: Yes --> 1; No --> 0
        for j in range (0,connection_num):
            for i in range(0,node_num):
                
                if ((old_node_states[i] == 1 and connection_transmission[i][j] == 1) or if_activate(random.random(), p_spontaneous) == 1): 
                    # if ancester state ==1 and transmission == 1 --> descendent = 1
                    new_node_states[int(node_connections[i][j])] = 1

                    if subsample and 0 <= node_connections[i][j] < subsample_num:
    
                        node_activities_step.append(count_t) #record node activation events
                        node_activities_num.append(node_connections[i][j])

                    else:
                        node_activities_step.append(count_t) #record node activation events
                        node_activities_num.append(node_connections[i][j])
                        
    
#                elif (if_activate(random.random(), p_spontaneous) == 1): 
#                    #print ('node ' + str(node_connections[i][j]) + 'is spontaneously activated.')
#                    # if a neuron is sontaneously activated 
#                    new_node_states[int(node_connections[i][j])] = int(1)
#                    node_activities_step.append(count_t) #record node activation events
#                    node_activities_num.append(node_connections[i][j])


        old_node_states = new_node_states    
        new_node_states = np.zeros(node_num)
        count_t += 1
        #print("node activites in experiment " + str(exp_count),node_activities_step)
        
#    if subsample: 
#        node_activities_step = subsample(node_activities_num, node_activities_step, subsample_num)
        
        
#record images from each step:
               
        if print_img:
            
            # get 2d network
            network = split(new_node_states, row)
            #print(network)
            
            #make a color map of fixed colors: 0 --> black; 1 --> white
            cmap = colors.ListedColormap(['black', 'white'])
            bounds=[0,0.5,1]
            norm = colors.BoundaryNorm(bounds, cmap.N)
            
            #plot & save img for this round 
            img = plt.matshow(network, cmap=cmap, norm=norm)
            # make a color bar
            plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=[0, 1])
            
        
        if print_img and save_img:    
            
            plt.savefig('/Users/zhoulinn/python/network-sim-pics/network'+'{0:0>3}'.format(str(count_t))+'.jpg')
            plt.show()
            #time.sleep(0.05) # delays for 0.5 seconds    
            #then find pics in directory & generate videos with imageJ
            #print(node_activities)
            
#%%
    if analyze_avalanches:
        #collect avalanches
        
        #active_steps = [] #record steps when there's activity
    
        
        #get avalache lengths (# of steps in each avalanche)
        avalanche_lengths.extend(get_avalanche_lengths(node_activities_step, 1)) 

        
        #get avalanche sizes (# of node activated during each avalanche)
        avalanche_sizes.extend(get_avalanche_sizes(node_activities_step, 1))
        
            
    
    exp_count += 1   
    print('finished experiment ' + str(exp_count))
    

#%%

#print("avalanche lengths: \n", avalanche_lengths)
#print("avalanche sizes: \n", avalanche_sizes)
#print("length num: ", length_num)
#print("size num: ", size_num)

 
#log plots for avalanche occurance

length_num_powerbin = np.histogram(avalanche_lengths, bins=np.logspace(0, np.log10(max(avalanche_lengths)), base=10.0), density=False)[0]
length_num_powerbin_edges = np.histogram(avalanche_lengths, bins=np.logspace(0, np.log10(max(avalanche_lengths)), base=10.0), density=False)[1]
plt.loglog(length_num_powerbin_edges[1:], length_num_powerbin,'o',basex=10,basey=10)
plt.xlim(-1, max(avalanche_lengths)+100) 
plt.axvline(x=t,linestyle='--',color="r") # node_nr should be the end of power law relationship
#plt.title('avalanche lengths, nodes:'+ str(node_num) + '\n exp:'+ str(experiment_num) + '\n steps:' + str(t) + '\n sigma:' + str(sigma) + '\n p_spont:' + str(p_spontaneous))
#plt.title('avalanche lengths')
plt.xlabel('avalanche length')
plt.ylabel('P(legth)')
#plt.show()
#print("length_num_powerbin: \n", length_num_powerbin)

plt.savefig('/Users/zhoulinn/python/network-sim-pics/avalanche_lengths111', dpi=900)

#%%

size_num_powerbin = np.histogram(avalanche_sizes, bins=np.logspace(0, np.log10(max(avalanche_sizes)), base=10.0), density=False)[0]
size_num_powerbin_edges = np.histogram(avalanche_sizes, bins=np.logspace(0, np.log10(max(avalanche_sizes)), base=10.0), density=False)[1]
plt.loglog(size_num_powerbin_edges[1:], size_num_powerbin,'o',basex=10,basey=10)
plt.axvline(x=node_num,linestyle='--',color="r") # node_nr should be the end of power law relationship
#plt.title('avalanche sizes, nodes:'+ str(node_num) + '\n exp:'+ str(experiment_num) + '\n steps:' + str(t) + '\n sigma:' + str(sigma) + '\n p_spont:' + str(p_spontaneous))
#plt.title('avalanche sizes')
plt.xlabel('avalanche size')
plt.ylabel('P(size)')
#plt.show()
#print("size_num_powerbin: \n", length_num_powerbin)
plt.savefig('/Users/zhoulinn/python/network-sim-pics/avalanche_sizess111', dpi=900)



# try Yunus' code to see what the plot looks like:
#%% Generating log-log plot, Avalanche frame lengths histogram
log_plot_base = 10
log_max_frames=np.log(max(avalanche_lengths))/np.log(log_plot_base)
# Define the upper border for x axis bins                
plt.hist(avalanche_lengths,bins=np.logspace(0,log_max_frames,base=log_plot_base))
plt.xscale('log',basex=log_plot_base)
plt.yscale('log',basey=log_plot_base)
plt.axvline(x=node_num,linestyle='--',color="r") # node_nr should be the end of power law relationship
plt.title('avalanche lengths, nodes:'+ str(node_num) + '\n exp:'+ str(experiment_num) + '\n steps:' + str(t) + '\n sigma:' + str(sigma) + '\n p_spont:' + str(p_spontaneous))
plt.show()






