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
3. [Model Training](#modeltraining)
4. [Model Testing](#modeltesting)
5. [Model Explanation by SHAP](#modelexplanation)

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

![image.png](https://i.loli.net/2021/11/14/XvguCoQJy5qF9dx.png)

---

## Model Training<a name="modeltraining"></a>


---


## Model Testing<a name="modeltesting"></a>


---

## Model Explanation by SHAP<a name="modelexplain"></a>



---





