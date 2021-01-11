import numpy

class Network:
    def __init__(self, sizes):
        self.numberOfLayers = len(sizes)
        self.sizes = sizes
        self.biases = []
        self.weights = []

        for i in range(self.numberOfLayers - 1):
            self.biases.append(numpy.random.randn(sizes[i + 1], 1))

        for i in range(self.numberOfLayers - 1):
            self.weights.append(numpy.random.randn(sizes[i+1], sizes[i]))


    def feedforward(self, input):
        for i in range(self.numberOfLayers - 1):
            input = sigmoid(numpy.add(numpy.dot(self.weights[i], input), self.biases[i]))
        return input


    def load(self, w, b):
        self.weights = list(w)
        self.biases = list(b)


def sigmoid(z):
    for i in range(len(z)):
        z[i] = 1.0/(1.0 + numpy.exp(-z[i]))
    return z


