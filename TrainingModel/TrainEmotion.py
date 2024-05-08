# Library
import tensorflow as tf
import os
import pandas as pd
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout # type: ignore
from tensorflow.keras.models import Model # type: ignore
import warnings
warnings.filterwarnings("ignore")

# Define class
num_classes = 7   # angry, disgust, fear, happy, neutral, sad, and surprise

# Init path
current_dir = os.path.dirname(__file__)
dataset_dir = os.path.join(current_dir, '..', 'Dataset', 'Emotion')

train_df = pd.read_csv(os.path.join(dataset_dir, 'train_labels.csv'), dtype={'label': str})
test_df = pd.read_csv(os.path.join(dataset_dir, 'test_labels.csv'), dtype={'label': str})

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

model = Model(inputs=input_image, outputs=output_label, name='emo_cnn')

# Model Params
batch_sz = 32
epo = 101
img_size = 100

# Create data from path
train_df['image'] = train_df.apply(lambda row: os.path.join(dataset_dir, 'DATASET', 'train', row['label'], row['image']), axis=1)
test_df['image'] = test_df.apply(lambda row: os.path.join(dataset_dir, 'DATASET', 'test', row['label'], row['image']), axis=1)

train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=15,
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)
test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_dataframe(
    dataframe=train_df,
    x_col='image',
    y_col='label',
    target_size=(100, 100),
    batch_size=batch_sz,
    class_mode='categorical',
    shuffle=True
)

test_generator = test_datagen.flow_from_dataframe(
    dataframe=test_df,
    x_col='image',
    y_col='label',
    target_size=(100, 100),
    batch_size=batch_sz,
    class_mode='categorical',
    shuffle=False
)

# Compile model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Training model
history = model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    epochs=epo,
    validation_data=test_generator,
    validation_steps=len(test_generator)
)

# Save model
model.save('trained_emotion.h5')