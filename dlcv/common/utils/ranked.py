import numpy as np

def rank5_accuracy(preds, labels):
    # Initialize the rank-1 and rank-5 accuracies
    rank1 = 0
    rank5 = 0
    
    # Loop overthe predictions and ground truth labels
    for(p, gt) in zip(preds, labels):
        # Sort the probabilities by their index in descending order
        # so that the more confident guesses are at the front of the list
        p = np.argsort(p)[::-1]
        
        # Check if the ground truth label is in the top-5 predictions
        if(gt in p[:5]):
            rank5 += 1
            
        # Check to see if the ground truth is the #1 predictions
        if(gt == p[0]):
            rank1 += 1
            
    # Compute the final rank-1 and rank-5 accuracies
    rank1 /= float(len(preds))
    rank5 /= float(len(preds))
    
    # Return a tuple of the rank-1 and rank-5 accuracies
    return(rank1, rank5)