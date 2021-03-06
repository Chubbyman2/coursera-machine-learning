import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt


def get_hyperplane_value(x, w, b, offset):
    return (-w[0] * x + b + offset) / w[1]


class SVM:

    def __init__(self, lr=0.01, lambda_param=0.01, n_iters=1000):
        self.lr = lr
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape

        # y_ has -1 where less than 0 and 1 otherwise
        y_ = np.where(y <= 0, -1, 1)

        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                condition = y_[idx] * \
                    (np.dot(x_i, self.weights) - self.bias) >= 1
                if condition:
                    self.weights -= self.lr * \
                        (2 * self.lambda_param * self.weights)
                else:
                    self.weights -= self.lr * \
                        (2 * self.lambda_param *
                         self.weights - np.dot(x_i, y_[idx]))
                    self.bias -= self.lr * y_[idx]

    def predict(self, X):
        approx = np.dot(X, self.weights) - self.bias
        return np.sign(approx)


if __name__ == "__main__":
    X, y = datasets.make_blobs(
        n_samples=50, n_features=2, centers=2, cluster_std=1.05, random_state=1234)
    y = np.where(y == 0, -1, 1)

    clf = SVM()
    clf.fit(X, y)
    print(clf.weights, clf.bias)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.scatter(X[:, 0], X[:, 1], marker='o', c=y)

    x0_1 = np.amin(X[:, 0])
    x0_2 = np.amax(X[:, 0])

    x1_1 = get_hyperplane_value(x0_1, clf.weights, clf.bias, 0)
    x1_2 = get_hyperplane_value(x0_2, clf.weights, clf.bias, 0)

    x1_1_m = get_hyperplane_value(x0_1, clf.weights, clf.bias, -1)
    x1_2_m = get_hyperplane_value(x0_2, clf.weights, clf.bias, -1)

    x1_1_p = get_hyperplane_value(x0_1, clf.weights, clf.bias, 1)
    x1_2_p = get_hyperplane_value(x0_2, clf.weights, clf.bias, 1)

    ax.plot([x0_1, x0_2], [x1_1, x1_2], 'y--', label="Decision Boundary")
    ax.plot([x0_1, x0_2], [x1_1_m, x1_2_m], 'k', label="Margin Line")
    ax.plot([x0_1, x0_2], [x1_1_p, x1_2_p], 'k')

    x1_min = np.amin(X[:, 1])
    x1_max = np.amax(X[:, 1])
    ax.set_ylim([x1_min-3, x1_max+3])

    plt.title("SVM")
    plt.xlabel("x_1")
    plt.ylabel("x_2")
    plt.legend(loc="upper right")

    plt.show()
