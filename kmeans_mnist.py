from keras.datasets import mnist
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import accuracy_score
import numpy as np
import time


def assign_values(model, actual):
    labels = {}
    for i in range(len(np.unique(model.labels_))):
        index = np.where(model.labels_ == i)
        num = np.bincount(actual[index]).argmax()
        labels[i] = num
    return labels


def main():
    start = time.perf_counter()
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train_mean = x_train.mean().astype('float32')
    x_test_mean = x_test.mean().astype('float32')

    x_train_std = x_train.std().astype('float32')
    x_test_std = x_test.std().astype('float32')

    x_train = (x_train - x_train_mean) / x_train_std
    x_test = (x_test - x_test_mean) / x_test_std

    x_train = x_train.reshape(len(x_train), -1)
    x_test = x_test.reshape(len(x_test), -1)

    k_means = MiniBatchKMeans(n_clusters=256)
    k_means.fit(x_train)

    r_val = assign_values(k_means, y_train)
    n_labels = np.zeros(len(k_means.labels_))
    for i in range(len(k_means.labels_)):
        n_labels[i] = r_val[k_means.labels_[i]]

    predictions = k_means.predict(x_test)
    answers = np.vectorize(r_val.get)(predictions)
    print(accuracy_score(answers, y_test))
    print(time.perf_counter() - start)


if __name__ == "__main__":
    main()

#Aditya Kak Class of 2022