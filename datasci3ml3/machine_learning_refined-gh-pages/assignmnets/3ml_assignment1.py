import numpy as np 
import matplotlib.pyplot as plt

def random_search(g,alpha_choice,max_its,w,num_samples):
    # run random search
    weight_history = []         # container for weight history
    cost_history = []           # container for corresponding cost function history
    alpha = 0
    for k in range(1,max_its+1):        
        # check if diminishing steplength rule used
        if alpha_choice == 'diminishing':
            alpha = 1/float(k)
        else:
            alpha = alpha_choice
            
        # record weights and cost evaluation
        weight_history.append(w)
        cost_history.append(g(w))
        
        # construct set of random unit directions
        directions = np.random.randn(num_samples,np.size(w))
        norms = np.sqrt(np.sum(directions*directions,axis = 1))[:,np.newaxis]
        directions = directions/norms   
        
        ### pick best descent direction
        # compute all new candidate points
        w_candidates = w + alpha*directions
        
        # evaluate all candidates
        evals = np.array([g(w_val) for w_val in w_candidates])

        # if we find a real descent direction take the step in its direction
        ind = np.argmin(evals)
        if g(w_candidates[ind]) < g(w):
            # pluck out best descent direction
            d = directions[ind,:]
        
            # take step
            w = w + alpha*d
        
    # record weights and cost evaluation
    weight_history.append(w)
    cost_history.append(g(w))
    return weight_history,cost_history

'''
# define function
g = lambda w: np.dot(w.T,w) + 2

# run random search algorithm 
alpha_choice = 0.3; w = np.array([3,4]); num_samples = 1000; max_its = 5
weight_history,cost_history = random_search(g,alpha_choice,max_its,w,num_samples)

plt.plot(weight_history)
plt.title("Weight History")
plt.xlabel("Iterations")
plt.ylabel("W")
plt.show()

# Plot the cost_history
plt.plot(cost_history)
plt.title("Cost History")
plt.xlabel("Iterations")
plt.ylabel("Cost")
plt.show()



P = [10, 100, 1000, 10000]

# Plot the results
for p in P:
    fractions = []
    for N in range(1, 26):
        w0 = np.array([1] + [0]*(N-1))
        # Generate P random directions
        directions = np.random.randn(p,np.size(w0))
        norms = np.sqrt(np.sum(directions*directions,axis = 1))[:,np.newaxis]
        directions = directions/norms   
        # Evaluate the partial derivative in each direction at the point w0
        derivatives = np.array([np.dot(direction, w0) for direction in directions])
        # Count the number of descent directions
        descent_directions = np.count_nonzero(derivatives < 0)
        # Calculate the fraction of descent directions
        fraction = descent_directions / p
        fractions.append(fraction)
    plt.plot(fractions,label = str(p))
    plt.xlabel("Number of dimensions (N)")
    plt.ylabel("Fraction of descent directions")
    plt.legend()
plt.show()

'''