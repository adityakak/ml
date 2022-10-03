from keras.datasets import mnist
from sklearn.neighbors import KNeighborsClassifier
import time
from sklearn.metrics import accuracy_score
import numpy as np


def main():
    start = time.perf_counter()
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train_mean = x_train.mean().astype('float32')
    x_test_mean = x_test.mean().astype('float32')

    x_train = (x_train - x_train_mean) / 255.0
    x_test = (x_test - x_test_mean) / 255.0

    x_train = x_train.reshape(len(x_train), -1)
    x_test = x_test.reshape(len(x_test), -1)

    y_train = y_train.reshape(len(y_train), -1).ravel()
    y_test = y_test.reshape(len(y_test), -1).ravel()

    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(x_train, y_train)
    print("Training Time: %s" % (time.perf_counter() - start))

    start = time.perf_counter()
    predict = knn.predict(x_test)
    print("Testing Time: %s" % (time.perf_counter() - start))
    print(accuracy_score(predict, y_test))


if __name__ == "__main__":
    main()

# Aditya Kak Period 3 Class of 2022
