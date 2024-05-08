# Library
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout # type: ignore
from tensorflow.keras.models import Model # type: ignore
import os
import warnings
warnings.filterwarnings("ignore")

# Define class
num_classes = 2

# Init path
current_dir = os.path.dirname(__file__)
dataset_dir = os.path.join(current_dir, '..', 'Dataset', 'Gender')

train_dir = os.path.join(dataset_dir, 'train')
test_dir = os.path.join(dataset_dir, 'test')

# Init model
input_image = Input(shape=(100, 100, 3), name='Input')

x = Conv2D(filters=64, kernel_size=(3, 3), padding='same', activation='relu', name='conv1_1')(input_image)
x = Conv2D(filters=64, kernel_size=(3, 3), padding='valid', activation='relu', name='conv1_2')(x)
x = MaxPooling2D(pool_size=(2, 2), name='pool1')(x)
x = Dropout(rate=0.15, name='conv_dropout1')(x)

x = Conv2D(filters=128, kernel_size=(3, 3), padding='same', activation='relu', name='conv2_1')(x)
x = Conv2D(filters=128, kernel_size=(3, 3), padding='valid', activation='relu', name='conv2_2')(x)
x = Conv2D(filters=128, kernel_size=(3, 3), padding='same', activation='relu', name='conv2_3')(x)
x = Conv2D(filters=128, kernel_size=(3, 3), padding='valid', activation='relu', name='conv2_4')(x)
x = MaxPooling2D(pool_size=(2, 2), name='pool2')(x)
x = Dropout(rate=0.15, name='conv_dropout2')(x)

x = Flatten(name='flatten')(x)

x = Dense(units=1024, activation='relu', name='fc1')(x)
x = Dropout(rate=0.25, name='fc_dropout1')(x)

output_label = Dense(units=num_classes, activation='softmax', name='fc3_7ways_softmax')(x)

model = Model(inputs=input_image, outputs=output_label, name='gen_cnn')

# Model Params
batch_sz = 32
epo = 51
img_size = 100

# Create data from path
train_ds = tf.keras.utils.image_dataset_from_directory(train_dir, batch_size=batch_sz, image_size=(img_size, img_size))
test_ds = tf.keras.utils.image_dataset_from_directory(test_dir, batch_size=batch_sz, image_size=(img_size, img_size))

# Compile model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Training model
history = model.fit(train_ds, epochs=epo)

# Save model
model.save("trained_gender.h5")