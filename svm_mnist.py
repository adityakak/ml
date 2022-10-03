from keras.datasets import mnist
from sklearn.svm import SVC, LinearSVC
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

    num_samples = 15000
    random_num_list = set()
    for i in range(num_samples):
        value = np.random.randint(0, 59999)
        while value in random_num_list:
            value = np.random.randint(0, 59999)
        random_num_list.add(value)
    x_train_short = np.zeros(shape=(num_samples, 784))
    y_train_short = np.zeros(shape=(num_samples,))
    for idx, i in enumerate(random_num_list):
        x_train_short[idx] = x_train[idx]
        y_train_short[idx] = y_train[idx]

    svm = LinearSVC(dual=False)
    svm.fit(x_train_short, y_train_short)
    predict = svm.predict(x_test)
    print(accuracy_score(predict, y_test))
    print(time.perf_counter() - start)


if __name__ == "__main__":
    main()

#Aditya Kak Class of 2022