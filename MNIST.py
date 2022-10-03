import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras import layers
import time


def print_weights(weight_list):
    f = open("output.txt", "w")
    for wb in weight_list:
        for individual in wb:
            output = individual.flatten().tolist()
            for item in output:
                f.write(str(item) + " ")
            f.write("\n")
        f.write("\n")


def main():
    start = time.perf_counter()
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    image_size = x_test.shape[1] * x_test.shape[2]

    x_train = x_train.reshape(x_train.shape[0], image_size)
    x_test = x_test.reshape(x_test.shape[0], image_size)

    x_train_mean = x_train.mean().astype('float32')
    x_test_mean = x_test.mean().astype('float32')

    x_train_std = x_train.std().astype('float32')
    x_test_std = x_test.std().astype('float32')

    x_train = (x_train - x_train_mean) / x_train_std
    x_test = (x_test - x_test_mean) / x_test_std

    y_train = keras.utils.to_categorical(y_train, 10)
    y_test = keras.utils.to_categorical(y_test, 10)

    network = Sequential()

    network.add(keras.Input(shape=(784,)))
    network.add(layers.Dense(512, activation='relu'))
    network.add(layers.Dropout(.2))
    network.add(layers.Dense(512, activation='relu'))
    network.add(layers.Dropout(.2))
    network.add(layers.Dense(10, activation='softmax'))

    network.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    network.fit(x_train, y_train, batch_size=64, epochs=1, verbose=True)
    network.evaluate(x_test, y_test, verbose=True)

    print(time.perf_counter() - start)
    print(network.summary())

    print_weights([network.layers[0].get_weights(), network.layers[2].get_weights(), network.layers[4].get_weights()])


if __name__ == "__main__":
    main()
