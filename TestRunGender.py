from tensorflow.keras.models import load_model #type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
import matplotlib.pyplot as plt
import numpy as np
import os

model_path = os.path.join(os.path.dirname(__file__), 'TrainedModel', 'trained_gender.h5')

model = load_model(model_path)

batch_size = 32
img_size = 224
class_names = ['man', 'woman']

test_dir = os.path.join(os.path.dirname(__file__), 'Dataset', 'Testing')

for filename in os.listdir(test_dir):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(test_dir, filename)

        img = image.load_img(image_path, target_size=(img_size, img_size))  

        img_array = image.img_to_array(img) / 255.0 

        img_array = np.expand_dims(img_array, axis=0)

        pred_label = model.predict(img_array)
        pred_label = np.argmax(pred_label)

        plt.imshow(img)
        plt.title('Predicted emotion: %s' % class_names[pred_label])
        plt.show()