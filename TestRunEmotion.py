# Library 
import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image # type: ignore
from tensorflow.keras.models import load_model # type: ignore

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'TrainedModel', 'trained_emotion.h5')

model = load_model(model_path)

# Model Params
img_size = 100

# Path
image_dir = os.path.join(os.path.dirname(__file__), 'Dataset', 'Testing')

# Testing
emotion_mapping = {
    0: 'surprise',
    1: 'fear',
    2: 'disgust',
    3: 'happy',
    4: 'sad',
    5: 'angry',
    6: 'neutral'
}

for filename in os.listdir(image_dir):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(image_dir, filename)

        img = image.load_img(image_path, target_size=(img_size, img_size))  

        img_array = image.img_to_array(img) / 255.0 

        img_array = np.expand_dims(img_array, axis=0)

        pred_label = model.predict(img_array)
        pred_label = np.argmax(pred_label)

        plt.imshow(img)
        plt.title('Predicted emotion: %s' % emotion_mapping[pred_label])
        plt.show()
