# -*- coding: utf-8 -*-
"""Submission - Machine Learning - Hazmi Cokro.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DXUsVH7GgmLSunKnDWXTpajfZi0nY5Qr

Mochammad Hazmi Cokro Mandiri
> Dataset Rock Paper Scissors

**Library**
"""

# Commented out IPython magic to ensure Python compatibility.
# Library u/ ekstrak dan atur lokasi 
import zipfile
import os

# Library u/ machine learning Tensorflow
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Activation, Dense, Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# Library u/  upload file gcolabs dan plot
from keras.preprocessing import image
from google.colab import files
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# %matplotlib inline

"""**Download Dataset Rock Paper Scissors**"""

# Download dataset menggunakan wget
!wget https://dicodingacademy.blob.core.windows.net/picodiploma/ml_pemula_academy/rockpaperscissors.zip

"""**Unzip / Ekstrak Dataset**"""

# Ekstrak file tipe zip
ekstrak_zip = 'rockpaperscissors.zip'
out_zip = zipfile.ZipFile(ekstrak_zip, 'r')
out_zip.extractall('/dataset')
out_zip.close()

"""**Atur Lokasi Dataset RockPaperScissors**"""

# Mengatur Lokasi dataset yang akan digunakan
dir_dataset = "/dataset/rockpaperscissors/rps-cv-images"
dir_paper = os.path.join("/dataset/rockpaperscissors/rps-cv-images/paper")
dir_rock = os.path.join("/dataset/rockpaperscissors/rps-cv-images/rock")
dir_scissors = os.path.join("/dataset/rockpaperscissors/rps-cv-images/scissors")

# Mengecek jumlah data rock paper scissor
total_paper = len(os.listdir(dir_paper))
total_rock = len(os.listdir(dir_rock))
total_scissors = len(os.listdir(dir_scissors))

# Mencetak jumlah data rock paper scissor
print("Total Data Paper Image      : ",total_paper)
print("Total Data Rock Image       : ",total_rock)
print("Total Data Scissors Image  : ",total_scissors)

"""**Implementasi Image Data Generator Tensorflow untuk pengolahan gambar**"""

# Pembuatan Train dan Validation  data generator 
# Untuk augmentasi gambar

#Ukuran validation 40% dari dataset
val_size = 0.4

Train_datagen = ImageDataGenerator(
    rotation_range = 30,
    brightness_range = [0.2,1.0],
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True,
    fill_mode = "nearest",
    rescale = 1./255,
    validation_split = val_size
)

Validation_datagen = ImageDataGenerator(
    rotation_range = 30,
    brightness_range = [0.2,1.0],
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True,
    fill_mode = "nearest",
    rescale = 1./255,
    validation_split = val_size
)

"""**Split Dataset -> Train dan Validation | Ukuran Validasi 40 %**"""

# Hasil split dataset dengan 
# Train : 1314 | Validation :  874

# Mengatur lebar dan tinggi gambar
img_width = 150
img_height = 150

# Train dan Validation generator  dengan mode categorical
Train_generator = Train_datagen.flow_from_directory(
    dir_dataset,
    target_size = (img_width,img_height),
    color_mode = "rgb",
    class_mode = "categorical",
    batch_size = 16,
    shuffle = True,
    subset = "training"
)

Validation_generator = Validation_datagen.flow_from_directory(
    dir_dataset,
    target_size = (img_width,img_height),
    color_mode = "rgb",
    class_mode = "categorical",
    batch_size = 16,
    shuffle = False,
    subset = "validation"
)

"""**Model Sequential + Dropout Regularization**"""

# Pembuatan Model dengan tipe Sequential

Model = Sequential(
    [
     # Activation menggunakan relu + softmax
     Conv2D(32, (3,3), strides = (1,1), activation = 'relu' , input_shape = (img_width,img_height,3)),
     MaxPooling2D(pool_size = (2,2), padding = 'valid'),
     Conv2D(64, (3,3), strides = (1,1), activation = 'relu' ),
     MaxPooling2D(pool_size = (2,2), padding = 'valid'),
     Conv2D(128, (3,3), strides = (1,1), activation = 'relu' ),
     MaxPooling2D(pool_size = (2,2), padding = 'valid'),
     Flatten(),

     # Droupout
     Dropout(0.2),
     
     Dense(128, activation = 'relu'),
     Dense(3, activation='softmax')
    ]
)

"""**Model Compile menggunakan Optimizer**"""

# Penggunaan Optimizer 'Adam' dengan learning rate 0.00146
Adam(learning_rate=0.00146, name='Adam')
Model.compile(optimizer = 'Adam',loss = 'categorical_crossentropy',metrics = ['accuracy'])

"""**Proses Training Dataset + Penggunaan Callbacks**"""

# Proses Training 
batch_size = 16

# Mengatur Jumlah Validation Steps
Validation_steps = Validation_generator.samples / Validation_generator.batch_size -1

# Penggunaan Callbacks dengan fungsi EarlyStopping dengan memonitoring Val_Loss
callback = EarlyStopping(
    monitor = 'val_loss',
    min_delta = 0.001,
    patience = 3,
    verbose = 1,
    mode = 'auto'
)

Model.fit_generator(
    Train_generator,
    steps_per_epoch = 50,
    epochs = 25,
    verbose = 1,
    validation_data = Validation_generator,
    validation_steps = Validation_steps,
    callbacks=[callback]
)

"""**Prediksi Hasil Model gambar antara Rock Paper Scissors**"""

# Upload File ke google colabs
uploaded = files.upload()

# pengkondisian
for file_upload in uploaded.keys():

  path = file_upload
  img = image.load_img(path, target_size=(150,150))
  imgplot = plt.imshow(img)
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)

  # Membuat numpy vstack array untuk hasil prediksi 
  images = np.vstack([x])
  classes = Model.predict(images, batch_size=16)
  
  print("\n")
  print('Hasil Prediksi : ',classes[0],'\n')

# Pengkondisian 
# Ketika array ke 0 = 1 maka tergolong Paper
# Ketika array ke 1 = 1 maka tergolong Rock
# Ketika array ke 2 = 1 maka tergolong Scissors
  if classes[0][0] == 1:
    print('Kategori Gambar : Paper')
  elif classes[0][1] == 1:
    print('Kategori Gambar : Rock')
  else:
    print('Kategori Gambar : Scissor')