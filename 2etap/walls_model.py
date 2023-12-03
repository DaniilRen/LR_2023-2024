import keras
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from keras.src.saving.saving_api import zipfile
from keras.utils import to_categorical
from keras import backend as K
import numpy as np
import cv2 as cv
import os

zip_file = '../assets/train.zip'
z = zipfile.ZipFile(zip_file, 'r')
z.extractall()


def get_recal(y_true, y_pred):
    positive_true = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    positive = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = positive_true / (positive + K.epsilon())
    return recall


def get_precision(y_true, y_pred):
    positive_true = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    positive_pred = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = positive_true / (positive_pred + K.epsilon())
    return precision


def f_score(y_true, y_pred):
    recall = get_recal(y_true, y_pred)
    precision = get_precision(y_true, y_pred)
    score = 2*((precision*recall)/(precision+recall+K.epsilon()))
    return score


def data_preparation(image, dir):
    image = cv.imread(f'train/{dir}/{image}')
    image = np.asarray(image)
    image = image / 255
    image = image.reshape(227, 227, 3)
    return image


x1 = np.asarray(list(map(lambda x: data_preparation(x, 1),
                         os.listdir('train/1'))))
x0 = np.asarray(list(map(lambda x: data_preparation(x, 0),
                         os.listdir('train/0')[:989])))
x = np.concatenate([x0, x1])

y1 = np.ones(len(x1), dtype=np.uint8)
y0 = np.zeros(len(x1), dtype=np.uint8)
y = np.concatenate([y0, y1])


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25,
                                                    shuffle= True)
y_train = to_categorical(y_train, num_classes=2)
y_test = to_categorical(y_test, num_classes=2)
print(y_train.shape)

model = keras.Sequential([
    # Flatten(input_shape=(227, 227, 3)),
    # Dense(128, activation='relu'),
    # Dense(2, activation='softmax')
    Conv2D(32, (3, 3), padding='same', activation='relu',
           input_shape=(227, 227, 3)),
    MaxPooling2D(pool_size=(2, 2), padding='valid'),
    Conv2D(32, (3, 3), padding='same', activation='relu'),
    MaxPooling2D(pool_size=(2, 2), padding='valid'),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(2, activation='relu')
])

model.compile(optimizer='adam', loss=keras.losses.SparseCategoricalCrossentropy(),
              metrics=[f_score])
history = model.fit(x, y, batch_size=16, epochs=15, validation_split=0.2)


def interpretate_prediction(pred):
    return np.array(list(map(lambda x: np.argmax(x), pred)))


prediction = model.predict(x_test)
print(y_test.shape, prediction.shape)
print(y_test[:20])
prediction = interpretate_prediction(prediction)
prediction = to_categorical(prediction, num_classes=2)
print(prediction[:20])
print(classification_report(y_test, prediction))