---
title: "BIOS 823 Homework 5: Dive into Deep Learning"
layout: post
date: 2021-11-13 22:48
image: https://i.loli.net/2021/11/14/ndIyoTkuEjvzHg6.png
headerImage: true
tag:
- python
- BIOS823
category: blog
author: Caihan Wang
description: 823 HW5
---

# Dive into Deep Learning

## Table of Contents
1. [Introduction](#introduction)
2. [Data Preparation](#datapreparation)
3. [Model Training and Testing](#modeltraining)
4. [Model Evaluation](#modelevaluate)
5. [Model Explanation by SHAP](#modelexplain)

---

## Introduction<a name="introduction"></a>

In this blog, I trained a deep learning model to classify beetles, cockroaches and dragonflies using these [images](https://www.dropbox.com/s/fn73sj2e6c9rhf6/insects.zip?dl=0). You can also download the origin images from the [link](https://people.duke.edu/~ccc14/insects.zip). After model training, I evaluated the model by the accuracy and explained the model by [SHAP](https://github.com/slundberg/shap).

---

## Data Preparation<a name="datapreparation"></a>

```python
# Import Packages
import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import glob

import pathlib
# Read in dataset
data_dir_train = pathlib.Path('insects/train')
data_dir_test = pathlib.Path('insects/test')

batch_size = 32
img_height = 180
img_width = 180

# Create Train dataset
train_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir_train,
  image_size=(img_height, img_width),
  batch_size=batch_size)

# Create Test dataset
test_ds = tf.keras.utils.image_dataset_from_directory(
  data_dir_test,
  image_size=(img_height, img_width),
  batch_size=batch_size)
  
# Check the class names
class_names = train_ds.class_names

# Show some sample pictures
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
  for i in range(9):
    ax = plt.subplot(3, 3, i + 1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_names[labels[i]])
    plt.axis("off")
```

After read in the data, we can see some sample pictures here following:  

![image.png](https://i.loli.net/2021/11/14/CDXrTAles519xB8.png)

---

## Model Training and Testing<a name="modeltraining"></a>

```python
AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

normalization_layer = layers.Rescaling(1./255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
# Notice the pixel values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image))

num_classes = 3

model = Sequential([
  layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_classes)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
              
# Fit the model
epochs=10
history = model.fit(
  train_ds,
  validation_data=test_ds,
  epochs=epochs
)
```
![image.png](https://i.loli.net/2021/11/16/NB2lpwysX1Oerfo.png)  
I set the epoch = 10 and fit the model, the model fitting progress is as following. As we can see, the model can reach about 100% test accuracy in the end.   
![image.png](https://i.loli.net/2021/11/14/B467PvhoN1znrGC.png)


---


## Model Evaluation<a name="modelevaluate"></a>

In this part, I evaluated the model by polt the accuarcy and the loss. The plot is as below:  
![image.png](https://i.loli.net/2021/11/14/2RgtkGKCbvu4dTH.png)

According to the figure above, the overall trend for the plot is that with the epoch increasing, the accuracy will increase and the loss will decrease.  
<br>  
Also, I tried to test a model by a random picture of dragonfly which I downloaded from Google.  

![Random_Dragonfly.jpg](https://i.loli.net/2021/11/14/F9JxYD3wUauVO2y.jpg)  

The code of testing part is as below:  
```python
# Check the model by a random picture of dragonfly from Google
pic = "Random_Dragonfly.jpg"

img = tf.keras.utils.load_img(
    pic, target_size=(img_height, img_width)
)
img_array = tf.keras.utils.img_to_array(img)
img_array = tf.expand_dims(img_array, 0) # Create a batch

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)
```
And the output is "This image most likely belongs to dragonflies with a 83.99 percent confidence.", which is a correct classification.  


---

## Model Explanation by SHAP<a name="modelexplain"></a>

In this part, I converted the train and test dataset to matrix first, and then used GradientExplainer and shap_values function from SHAP to calculate the shap values. At last, produce the figure by the image_plot.  


```python
# SHAP
import shap

# Convert to matrix
x_train = np.concatenate([x for x , y in train_ds], axis = 0)
y_train = np.concatenate([y for x , y in train_ds], axis = 0)

x_test = np.concatenate([x for x , y in test_ds], axis = 0)
y_test = np.concatenate([y for x , y in test_ds], axis = 0)

explainer = shap.GradientExplainer(model, x_train)

# Calculate shap values
sv = explainer.shap_values(x_test[:20])

print("     Reference            Beetles            Cockroach            Dragonflies")
shap.image_plot([sv[i] for i in range(3)], x_test[0:5])
```
The output is:  
![image.png](https://i.loli.net/2021/11/14/kfQxHog9SOiw7CF.png)  

In the figure above, red represents the positive SHAP value and blue represents the negative one. The true values of these five figures is cockroach, cockroach, dragonfly, dragonfly and dragonfly respectively. For the first two rows, we can see that in the cockroach column, they have the more red color than in other two columns, which means the predicted value of these first two figures are cockroach and they are correct predictions. for the last three rows, we can see that in the dragonflies column, they have the more red color than in other two columns, which means the predicted value of these first three figures are dragonflies and they are alao correct predictions.  

---





