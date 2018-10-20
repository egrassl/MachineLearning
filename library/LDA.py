import numpy as np
import matplotlib.pyplot as plt



class LDA(object):
    def __init__(self, samples, classes):
        # Initial checks
        if len(samples) == 0 or len(classes) == 0:
            raise ValueError("Cannot initialize with empty inputs!")

        # Initialize properties
        self.samples = samples
        self.classes = classes
        self.dimensions = len(samples)
        self.n = len(classes)

        # Sets groups amount
        self.unique_classes = []
        for i in range(0, self.n):
            if not self.classes[i] in self.unique_classes:
                self.unique_classes.append(self.classes[i])

        # Gets central point
        self.mean = []
        for i in range(0, self.dimensions):
            self.mean.append(np.mean(samples[i]))

        self.scatter_between = self.scatter_b()
        self.scatter_within = self.scatter_w()

    # Creates 0.0 filled matrix
    @staticmethod
    def empty_mx(rows, columns):
        res = np.empty((rows, columns), np.float64)
        for i in range(0, res.shape[0]):
            for j in range(0, res.shape[1]):
                res.itemset((i, j), 0.0)
        return res

    def scatter_b(self):
        sb = self.empty_mx(self.dimensions, self.dimensions)

        t_samples = np.matrix(self.samples).transpose().tolist()

        # Applies scatter between matrix formula
        for c in self.unique_classes:
            elements = []
            for i in range(0, self.n):
                if self.classes[i] == c:
                    elements.append(t_samples[i])

            samples = np.matrix(elements).transpose().tolist()
            # Gets the mean for the class c
            class_mean = []
            for i in range(0, self.dimensions):
                class_mean.append(np.mean(samples[i]))

            # Applies formula
            diff = np.matrix(np.subtract(class_mean, self.mean))
            diff_transposed = diff.transpose()
            mul = np.matmul(diff_transposed, diff)
            value = np.multiply(len(elements), mul)
            sb = np.add(sb, value)

        return sb.tolist()

    def scatter_w(self):
        sw = self.empty_mx(self.dimensions, self.dimensions)

        t_samples = np.matrix(self.samples).transpose().tolist()

        # Applies scatter withing formula
        for c in self.unique_classes:
            elements = []
            for i in range(0, self.n):
                if self.classes[i] == c:
                    elements.append(t_samples[i])

            samples = np.matrix(elements).transpose().tolist()
            # Gets the mean for the class c
            class_mean = []
            for i in range(0, self.dimensions):
                class_mean.append(np.mean(samples[i]))

            # Applies formula
            for i in range(0, len(elements)):
                diff = np.matrix(np.subtract(elements[i], class_mean))
                diff_transposed = diff.transpose()
                mul = np.matmul(diff_transposed, diff)
                sw = np.add(sw, mul)

        return sw.tolist()