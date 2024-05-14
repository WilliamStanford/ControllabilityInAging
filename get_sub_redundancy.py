import numpy as np
import networkx as nx

def get_binarized_adj(A, frac):
    
    # All matrices were automatically thresholded at 0.001 max streamlines
    initial_min = .001 * max(A)
    threshold = (max(A) + initial_min)*frac
    
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            for k in range(A.shape[2]):
                
                if A[i,j,k] > threshold:
                    A[i,j,k] = 1
                else:
                    A[i,j,k] = 0
     
    return A


def get_redundancy(sub_mat, red_filename):
    
    # need to pass a matrix in the form of a numpy array

    G = nx.from_numpy_matrix(sub_mat)
    red_mat = np.zeros_like(sub_mat)
        
    for i in range(sub_mat.shape[0]):
        for j in range(sub_mat.shape[1]):
            
            if i <= j:
                paths = nx.all_simple_paths(G, source=i, target=j, cutoff=4)            
                red_mat[i, j] = len(list(paths)) 
                red_mat[j, i] = len(list(paths))

 
    np.save(red_filename, red_mat)
    
    return red_mat
        

        
