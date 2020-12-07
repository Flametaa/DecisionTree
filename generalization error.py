#!/usr/bin/env python
# coding: utf-8

# In[7]:


#parameters are :
    # data is the input data in the format list[list[int]]
    # dic is the dictionnary linking each attribute to an index
    # tree is the resulting tree from BuildDecisionTree (heap Tree)
    # alpha is float
def error(data,dic,tree,alpha):
    num_leaves = 0 # number of leaves in tree
    num_errors=0   # number of wrong predictions for the data set
    for i in range(len(tree)): # counting the leaves
        if len(tree[i])==0:
            continue
        if  tree[i][0]!=-1:
            num_leaves+=1
            
    testTree = [[] for k in range(len(tree))] # testTree is the tree containing the records at each node
    
    testTree[0] = data # the root has all the records 
    
    for i in range(len(tree)):
        if len(tree[i])==0:
            continue
        node = tree[i]
        if (node[0]==-1): ## node is not leaf
            condition = node[2].split(" ") # node 2 is like "A 0 1 2"
            At = condition[0] ## tested attribute
            values = [int(x) for x in condition[1:]] 
            # if the value of the tested data of the corresponding attribute is in values then we go left else we go right
            for prod in testTree[i]:
                if prod[dic[At]] in values:
                    testTree[i*2+1].append(prod)
                else :
                    testTree[i*2+2].append(prod)
        
        else : # if node is a leaf
            
            for prod in testTree[i]: 
                # for each record in the node of testTree we check if its class is equal to the predicted class
                if prod[len(prod)-1]!=node[0]:
                    num_errors+=1 # if class[prod] is not equal to the predicted class then we add 1 to error
    genErr = num_errors+alpha*num_leaves
    return  genErr 


# In[ ]:




