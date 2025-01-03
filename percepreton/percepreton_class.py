'''
A basic percepreton class multiple inputs calculates a weighted sum of these inputs, 
applies an activation function to determine its output, 
and adjusts its weights during training to minimize prediction errors.

A percepreton is the basic block of machine learning in which it is the equavilent of a human brain's neuron. It preforms basic binary classificaiton based on
different input weights and then makes a decision. When connected with many other precepretons it creates a network of decisions which can make intelligent decisions
ultimately mimicking neural pathways. This connection network is a neural network.
'''


class Perceptron:
  def __init__(self, num_inputs=3, weights=[1,1,1]):
    self.num_inputs = num_inputs
    self.weights = weights
    
  def weighted_sum(self, inputs):
    weighted_sum = 0
    for i in range(self.num_inputs):
      weighted_sum += self.weights[i]*inputs[i]
    return weighted_sum
  
  def activation(self, weighted_sum):
    if weighted_sum >= 0:
      return 1
    if weighted_sum < 0:
      return -1
    
  def training(self, training_set):
    foundLine = False
    while not foundLine:
      total_error = 0
      for inputs in training_set:
        prediction = self.activation(self.weighted_sum(inputs))
        actual = training_set[inputs]
        error = actual - prediction
        total_error += abs(error)
        for i in range(self.num_inputs):
          self.weights[i] += error*inputs[i]
      if total_error == 0:
        foundLine = True
      
cool_perceptron = Perceptron()

