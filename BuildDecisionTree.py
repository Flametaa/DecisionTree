from math import log2
#the parameters of the buildTree function take as parameters:
    #D which is the input Data (Records)
    #dic which is the dictionnary that correspands each attribute to an index (example dic['A']=0)
    #Attributes contains the values that can be taken by each attribute (exp Attributes[0] contains 
                                                                    #the values that can be taken by the attribute 'A')
    #A is a list of all the attributes
    #node is the position of the node in the tree
    #lvl is the level of the corresponding node
    
def BuildTree(D,dic,Attributes,A,minNum,node,lvl,d,tree):
    
    # tree[node] = [-1 if not leaf and class if leaf , level, Feature , GINI]
    GINI_split = 0 # the GINI of The corresponding node
    ma = 0 #used to maximize information gain
    
    res = '';
    
    splitAtt = 0; #the best attribute we will chose to split the tree
    
    if (len(A)==0): # if we finished splitting the tree then the node will be a leaf
                    # and will take all the records in the same class
        tree[node] = (D[0][len(D[0])-1],lvl,"",0)
        return;
    if len(D)<minNum: # if the number of records <minNum the the node will be a leaf take the class d (default)
            tree[node] = (d,lvl,"",0)
            return
    for a in A: # iterate attributes to find the best split
        Att=dic[a] # the index of the corresponding attribute in the input data
        test = True # to check if all records have the same class
        clas = D[0][len(D[0])-1] # class of the first record
        L = Attributes[Att] # the possible values that the attribute can take
        C1 = [0 for co in range(len(L))] # holds for each possible value the number of records having class 0
        C2 = [0 for co in range(len(L))] # holds for each possible value the number of records having class 1
        for rec in D:
            if rec[len(D[0])-1]==0:
                C1[rec[Att]]+=1
            else:
                C2[rec[Att]]+=1

            if (rec[len(D[0])-1]!=clas):
                test = False
        
        if (test): # if all records have same class the node is a leaf with the same class
            tree[node] = (clas,lvl,"",0)
            return

        
        for spli in range(1,len(L)): # spli is the index of the split
                spl1=L[0:spli] # spl1 values to the left
                spl2=L[spli:]  # spl2 values to the right
                
                c01 = sum(C1) # number of records having class =0 in the node
                c02 = sum(C2) # number of records having class =1 in the node
                c11 = sum(C1[0:spli]) # number of records having class =0 in the left child
                c12 = sum(C2[0:spli]) # number of records having class =1 in the left child
                c21 = sum(C1[spli:]) # number of records having class =0 in the right child
                c22 = sum(C2[spli:]) # number of records having class =1 in the right child
                
                if ((c11+c12)==0 or (c21+c22)==0 or (c01+c02)==0): #no division by zero
                    continue
                EntropyP = 0;Entropy1=0;Entropy2=0; # Entropy1 is the entropy of the left child and Entropy2 of the right child
                                                    # EntropyP is the entropy of the parent
                
                if (c01/(c01+c02))!=0: # for no log2(0)
                    EntropyP-= (c01/(c01+c02)) * log2((c01/(c01+c02))) 
                if (c02/(c01+c02))!=0:
                    EntropyP-= (c02/(c01+c02)) * log2((c02/(c01+c02)))
                if (c11/(c11+c12))!=0:
                    Entropy1 = -1 * (c11/(c11+c12)) * log2((c11/(c11+c12))) 
                if (c12/(c11+c12))!=0:
                    Entropy1-= (c12/(c11+c12)) * log2((c12/(c11+c12)))
                if (c22/(c21+c22))!=0:
                    Entropy2 = -1 * (c22/(c21+c22)) * log2((c22/(c21+c22))) 
                if (c21/(c21+c22))!=0:
                    Entropy2-= (c21/(c21+c22)) * log2((c21/(c21+c22)))
                Entropy_split = EntropyP - (Entropy1 * ((c11+c12)/(c11+c12+c22+c21)) + Entropy2*((c21+c22)/(c11+c12+c22+c21)))
                if (Entropy_split>ma): #maximizing the information gain
                    ma = Entropy_split
                    res = spli
                    splitAtt = a
                    GINI1=1-(c11/(c11+c12))**2-(c12/(c11+c12))**2
                    GINI2=1-(c22/(c21+c22))**2-(c21/(c21+c22))**2
                    GINI_split = GINI1 * ((c11+c12)/(c11+c12+c22+c21)) + GINI2*((c21+c22)/(c11+c12+c22+c21))

    right = [] #records to the right
    left=[]    #records to the left
    
    L=Attributes[dic[splitAtt]] #index of the chosen attribute that maximizes info gain
    
    for i in D:
        if i[dic[splitAtt]] in L[0:res]:
            left.append(i)
        else:
            right.append(i)
    
    st = splitAtt # st is the string of the feature example 'A 0 1'
   
    for ss in L[0:res]:
        st+=" "
        st+=str(ss) 
    tree[node]=(-1,lvl,st,GINI_split) #finally setting the node to the chosen values
    
    A.pop(A.index(splitAtt)) # deleting the used attribute from the set of attributes
    #recursive call for right and left child
    BuildTree(left,dic,Attributes,A,minNum,node*2+1,lvl+1,d,tree) 
    BuildTree(right,dic,Attributes,A,minNum,node*2+2,lvl+1,d,tree)
    
              


# In[1]:


def BuildDecisionTree(D,dic,Attributes,A,minNum,node,lvl,d):
    tree=[() for i in range(2**(len(Attributes)+1))] # the resulting tree passed as global var to BuildTree
    # tree[node] = [-1 if not leaf and class if leaf , level, Feature , GINI]
    BuildTree(D,dic,Attributes,A,minNum,node,lvl,d,tree)
    return tree

    


# In[3]:


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


    





