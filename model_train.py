# import modules
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

dataset_path    = 'datasets'
plot_image      = 'plot.png'
model_file      = 'model_trained.model'

learning_rate   = 0.0001
epochs          = 20
bs              = 32

imagePaths = list(paths.list_images(dataset_path))
data    = []
labels  = []

for imagePath in imagePaths:
	label = imagePath.split(os.path.sep)[-2]
	image = load_img(imagePath, target_size = (224, 224))
	image = img_to_array(image)
	image = preprocess_input(image)
	data.append(image)
	labels.append(label)

data = np.array(data, dtype="float32")
labels = np.array(labels)

lb = LabelBinarizer()
labels = lb.fit_transform(labels)
labels = to_categorical(labels)

(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size = 0.20, stratify = labels, random_state = 42)

aug = ImageDataGenerator(rotation_range = 20, zoom_range = 0.15, width_shift_range = 0.2, height_shift_range = 0.2, shear_range = 0.15, horizontal_flip = True, fill_mode = "nearest")

baseModel = MobileNetV2(weights="imagenet", include_top=False, input_tensor = Input(shape = (224, 224, 3)))

headModel = baseModel.output
headModel = AveragePooling2D(pool_size = (7, 7))(headModel)
headModel = Flatten(name = "flatten")(headModel)
headModel = Dense(128, activation = "relu")(headModel)
headModel = Dropout(0.5)(headModel)
headModel = Dense(2, activation = "softmax")(headModel)

model = Model(inputs=baseModel.input, outputs = headModel)

for layer in baseModel.layers:
	layer.trainable = False

print("[INFO] Creating model...")
opt = Adam(lr = learning_rate, decay = learning_rate / epochs)
model.compile(loss = "binary_crossentropy", optimizer = opt, metrics = ["accuracy"])

print("[INFO] training head...")
H = model.fit(aug.flow(trainX, trainY, batch_size = bs), steps_per_epoch = len(trainX) // bs, validation_data = (testX, testY), validation_steps = len(testX) // bs, epochs = epochs)

print("[INFO] Testing network...")
predict = model.predict(testX, batch_size = bs)
predict = np.argmax(predict, axis = 1)

print(classification_report(testY.argmax(axis = 1), predict, target_names = lb.classes_))

print("[INFO] Saving trained model...")
model.save(model_file, save_format = "h5")