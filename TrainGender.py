import tensorflow as tf
from tensorflow.keras import regularizers, initializers, Sequential # type: ignore
from tensorflow.keras.layers import Conv2D, Dropout, MaxPooling2D, Flatten, Dense # type: ignore
import os

import warnings
warnings.filterwarnings("ignore")

train_dir = os.path.join(os.path.dirname(__file__), 'Dataset', 'Gender', 'train')
test_dir = os.path.join(os.path.dirname(__file__), 'Dataset', 'Gender', 'test')

batch_size = 32
img_size = 224

train_ds = tf.keras.utils.image_dataset_from_directory(train_dir, batch_size=batch_size, image_size=(img_size, img_size))

test_ds = tf.keras.utils.image_dataset_from_directory(test_dir, batch_size=batch_size, image_size=(img_size, img_size))

class_names = ['man', 'woman']

train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
test_ds = test_ds.prefetch(tf.data.AUTOTUNE)

data_augmentation = Sequential([
    tf.keras.layers.Resizing(180, 180),
])

regularizer = regularizers.l1(0.001)
initializer = initializers.HeNormal(seed=20)

model = Sequential([
    data_augmentation,
    Conv2D(64, 3, activation="relu", kernel_initializer=initializer, kernel_regularizer=regularizer),
    MaxPooling2D((2, 2)),
    Conv2D(32, 3, activation="relu", kernel_initializer=initializer, kernel_regularizer=regularizer),
    MaxPooling2D((2, 2)),
    Dropout(0.2),
    Flatten(),
    Dense(10, activation="softmax")
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

history = model.fit(train_ds, epochs=50)

model.save("trained_gender.h5")