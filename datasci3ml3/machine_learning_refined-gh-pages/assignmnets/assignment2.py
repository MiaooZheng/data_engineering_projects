import autograd.numpy as np
from autograd import grad
import numpy as np 
import matplotlib.pyplot as plt


# g(w1, w2) = tanh(4w1 + 4w2) + max(1, 0.4w1^2) + 1

def g(w):
    return np.tanh(4 * w[0] + 4 * w[1]) + max(1, 0.4 * w[0] ** 2) + 1

def gradient_descent(g,alpha,max_its,w):
    gradient = grad(g)
    weight_history = [w] # container for weight history
    cost_history = [g(w)] # container for corresponding cost function history
    for k in range(max_its):
        # evaluate the gradient, store current weights and cost function value
        grad_eval = gradient(w)
        # take gradient descent step
        w = w - alpha*grad_eval
        # record weight and cost
        weight_history.append(w)
        cost_history.append(g(w))
    return weight_history,cost_histor