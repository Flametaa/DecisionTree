#!/usr/bin/env python
# coding: utf-8

# In[6]:


#parameters are :
    # data is the input data in the format list[list[int]]
    # dic is the dictionnary linking each attribute to an index
    # tree is the resulting tree from BuildDecisionTree (heap Tree)
    # alpha is float
    # minNum is int 
    # d is the default class (binary)
def prune(data,dic,tree,alpha, minNum, d):
 
    testTree = [ [] for k in range(len(tree))] # same as with error function we built the test tree
    testTree[0] = data
    for i in range(len(tree)): 
        if len(tree[i])==0:
            continue
        node = tree[i]
        if (node[2]!=""): ## node is not leaf
            condition = node[2].split(" ")
            At = condition[0] ## tested attribute
            values = [int(x) for x in condition[1:]]
            for prod in testTree[i]:
                if prod[dic[At]] in values:
                    testTree[i*2+1].append(prod)
                else :
                    testTree[i*2+2].append(prod)
    
    pruned = [tt for tt in tree] # pruned is the result of this function it starts the same as tree
    err = error(data,dic,tree,alpha) # compute the generalization error of the tree 
    
    for i in range(len(tree)-1,-1,-1): # starting from the last node (MaxLvl downto 0)
        if len(pruned[i])==0:
            continue
        node = pruned[i] # node of the pruned tree (starting from last node)
        temp = [xx for xx in pruned] # temp is the temporary tree where we try to prune and see the result
        if len(node)>0 and node[0]==-1: #if node is not leaf
            records = testTree[i] # the records contained in the corresponding node (=num records left child+num records right child)
            if len(records)<minNum: # if number of records <minNum we prune with the default class d
                temp[i] = (d,tree[i][1],"",0) # the node becomes a leaf with class d
                temp[2*i+1]=[] #delete left and right child
                temp[2*i+2]=[]
                tempErr = error(data,dic,temp,alpha) # compute gen error of the temp tree
                if (tempErr<err): # minimizing the err
                    pruned = temp # if tempErr < err then we prune and update err
                    err = tempErr
            else:
                cla1 = 0;cla2 = 0;
                # cla1 number of records having the class 0 and cla2 number of records having the class 1
                for record in records: #counting
                    if record[len(record)-1]==0:
                        cla1+=1
                    else :
                        cla2+=1
                        
                if cla1>cla2: # then the node is a leaf with class 0
                    temp[i] = (0,tree[i][1],"",0)
                    temp[2*i+1]=[]
                    temp[2*i+2]=[]
                    tempErr = error(data,dic,temp,alpha)# compute gen error of the temp tree
                    if (tempErr<err):# if tempErr < err then we prune and update err
                        pruned = temp
                        err = tempErr
                    
                else : # then the node is a leaf with class 1
                    temp[i] = (1,tree[i][1],"",0)
                    temp[2*i+1]=()
                    temp[2*i+2]=()
                    tempErr = error(data,dic,temp,alpha)# compute gen error of the temp tree
                    if (tempErr<err):# if tempErr < err then we prune and update err
                        pruned = temp
                        err = tempErr
    print("the generalization error of the pruned tree is = ",err) # printing the gen error
    
    return pruned 


            
            


# In[5]:


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
            
    return num_errors+alpha*num_leaves  


# In[ ]:


def printTree(tree):
    #print tree BFS
    
    q=[]
    q.append(0)
    while(len(q)>0):
        node = q.pop(0)
        t = tree[node]
        
        if (node==0):
            if (t[0]==-1): # if node is root but not leaf
                print("Root")
                print("Level",t[1])
                print("Feature",t[2] )
                print("Gini",t[3])
                q.append(node*2+1)
                q.append(node*2+2)
            else : # if tree has only one node
                print("Root/leaf")
                print("Level",t[1])
                
                print("Gini",t[3])
                
        else:
            if (t[0]==-1): # if node is not leaf
                print("Intermediate")
                print("Level",t[1])
                print("Feature :",t[2] )
                print("Gini",t[3])
                q.append(node*2+1)
                q.append(node*2+2)
            else: # if node is leaf
                print("Leaf")
                print("Level",t[1])
                print("Gini",t[3])


    

