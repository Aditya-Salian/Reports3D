import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import skimage.io as io
import skimage.color as color
import random as r
import math
from keras.models import Model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import concatenate, Conv2D, MaxPooling2D, Conv2DTranspose
from keras.layers import Input, UpSampling2D,BatchNormalization
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
import keras.backend as K
import glob
import SimpleITK as sitk
import vtk
import os
import sys
import json

    
#https://www.codesofinterest.com/2016/11/keras-image-dim-ordering.html
#(samples, channels, rows, cols)
K.tensorflow_backend.set_image_dim_ordering("th")
img_size = 240      #original img size is 240*240
smooth = 0.005 
num_of_aug = 2
num_epoch = 30
pul_seq = 'Flair'
sharp = False       # sharpen filter
LR = 1e-4
num_of_patch = 4 #must be a square number
label_num = 5

path = r'C:\\Users\\Parin\\transcend1\\transcend1\\'


def create_data_onesubject_val(src):
    
    
    imgs = []
    img = io.imread(src, plugin='simpleitk')
    img = (img-img.mean()) / img.std()      #normalization => zero mean   !!!care for the std=0 problem
    img = img.astype('float32')
    for slice in range(155):     #choose the slice range
        img_t = img[slice,:,:]
        img_t =img_t.reshape((1,)+img_t.shape)
        img_t =img_t.reshape((1,)+img_t.shape)   #become rank 4
        #img_g = augmentation(img_t,num_of_aug)
        for n in range(img_t.shape[0]):
            imgs.append(img_t[n,:,:,:])
    
    
    return np.array(imgs)



def dice_coef(y_true, y_pred):
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


def dice_coef_loss(y_true, y_pred):
    return 1-dice_coef(y_true, y_pred)

def unet_model():
    
    
    inputs = Input((2, img_size, img_size))
    conv1 = Conv2D(64, (3, 3), activation='relu', padding='same') (inputs)
    batch1 = BatchNormalization(axis=1)(conv1)
    conv1 = Conv2D(64, (3, 3), activation='relu', padding='same') (batch1)
    batch1 = BatchNormalization(axis=1)(conv1)
    pool1 = MaxPooling2D((2, 2)) (batch1)
    
    conv2 = Conv2D(128, (3, 3), activation='relu', padding='same') (pool1)
    batch2 = BatchNormalization(axis=1)(conv2)
    conv2 = Conv2D(128, (3, 3), activation='relu', padding='same') (batch2)
    batch2 = BatchNormalization(axis=1)(conv2)
    pool2 = MaxPooling2D((2, 2)) (batch2)
    
    conv3 = Conv2D(256, (3, 3), activation='relu', padding='same') (pool2)
    batch3 = BatchNormalization(axis=1)(conv3)
    conv3 = Conv2D(256, (3, 3), activation='relu', padding='same') (batch3)
    batch3 = BatchNormalization(axis=1)(conv3)
    pool3 = MaxPooling2D((2, 2)) (batch3)
    
    conv4 = Conv2D(512, (3, 3), activation='relu', padding='same') (pool3)
    batch4 = BatchNormalization(axis=1)(conv4)
    conv4 = Conv2D(512, (3, 3), activation='relu', padding='same') (batch4)
    batch4 = BatchNormalization(axis=1)(conv4)
    pool4 = MaxPooling2D(pool_size=(2, 2)) (batch4)
    
    conv5 = Conv2D(1024, (3, 3), activation='relu', padding='same') (pool4)
    batch5 = BatchNormalization(axis=1)(conv5)
    conv5 = Conv2D(1024, (3, 3), activation='relu', padding='same') (batch5)
    batch5 = BatchNormalization(axis=1)(conv5)
    
    up6 = Conv2DTranspose(512, (2, 2), strides=(2, 2), padding='same') (batch5)
    up6 = concatenate([up6, conv4], axis=1)
    conv6 = Conv2D(512, (3, 3), activation='relu', padding='same') (up6)
    batch6 = BatchNormalization(axis=1)(conv6)
    conv6 = Conv2D(512, (3, 3), activation='relu', padding='same') (batch6)
    batch6 = BatchNormalization(axis=1)(conv6)
    
    up7 = Conv2DTranspose(256, (2, 2), strides=(2, 2), padding='same') (batch6)
    up7 = concatenate([up7, conv3], axis=1)
    conv7 = Conv2D(256, (3, 3), activation='relu', padding='same') (up7)
    batch7 = BatchNormalization(axis=1)(conv7)
    conv7 = Conv2D(256, (3, 3), activation='relu', padding='same') (batch7)
    batch7 = BatchNormalization(axis=1)(conv7)
    
    up8 = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same') (batch7)
    up8 = concatenate([up8, conv2], axis=1)
    conv8 = Conv2D(128, (3, 3), activation='relu', padding='same') (up8)
    batch8 = BatchNormalization(axis=1)(conv8)
    conv8 = Conv2D(128, (3, 3), activation='relu', padding='same') (batch8)
    batch8 = BatchNormalization(axis=1)(conv8)
    
    up9 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same') (batch8)
    up9 = concatenate([up9, conv1], axis=1)
    conv9 = Conv2D(64, (3, 3), activation='relu', padding='same') (up9)
    batch9 = BatchNormalization(axis=1)(conv9)
    conv9 = Conv2D(64, (3, 3), activation='relu', padding='same') (batch9)
    batch9 = BatchNormalization(axis=1)(conv9)

    conv10 = Conv2D(1, (1, 1), activation='sigmoid')(batch9)

    model = Model(inputs=[inputs], outputs=[conv10])

    model.compile(optimizer=Adam(lr=LR), loss=dice_coef_loss, metrics=[dice_coef])

    
    return model



def TumourSegmentation(flair, t2):
    
    
    #read one subject to show slices
    pul_seq = 'flair'
    Flair = create_data_onesubject_val(path + flair)
    pul_seq = 't2'
    T2 = create_data_onesubject_val(path + t2)
    
    model = unet_model()
    model.load_weights(path + 'static/weights-full-best.h5')
    
    fl = np.zeros((240, 240, 155))
    #using Flair and T2 as input for full tumor segmentation
    for i in range(0,154):
      x = np.zeros((1,2,240,240),np.float32)
      x[:,:1,:,:] = Flair[i:(i + 1),:,:,:]
      x[:,1:,:,:] = T2[i:(i + 1),:,:,:]
      pred_full = model.predict(x)
      fl[:, :, i] = pred_full[0][0][:, :]
    
    
    return fl



def createSTL(mha, stl):
    
    
    reader = vtk.vtkMetaImageReader()
    reader.SetFileName(mha)
    reader.Update()
    
    threshold = vtk.vtkImageThreshold()
    threshold.SetInputConnection(reader.GetOutputPort())
    threshold.ThresholdByLower(0.1)
    threshold.ReplaceInOn()
    threshold.SetInValue(0)  # set all values below 0.1 to 0
    threshold.ReplaceOutOn()
    threshold.SetOutValue(1)  # set all values above 0.1 to 1
    threshold.Update()

    dmc = vtk.vtkFlyingEdges3D()
    dmc.SetInputConnection(threshold.GetOutputPort())
    dmc.ComputeNormalsOn()
    dmc.GenerateValues(1, 1, 1)
    dmc.Update()
    
    smoother = vtk.vtkWindowedSincPolyDataFilter()
    smoother.SetInputConnection(dmc.GetOutputPort())
    smoother.SetNumberOfIterations(15)
    smoother.BoundarySmoothingOff()
    smoother.Update()

    writer = vtk.vtkSTLWriter()
    writer.SetInputConnection(smoother.GetOutputPort())
    writer.SetFileTypeToBinary()
    writer.SetFileName(stl)
    writer.Write()
    
    
    return 0



def Create3DModel(flair, t2, id):
    
    
    fl = TumourSegmentation(flair, t2)
    
    image = sitk.GetImageFromArray(fl)
    sitk.WriteImage(image, str(path + 'tumour.mha'))
    image2 = sitk.ReadImage(path + flair)
    arr = sitk.GetArrayFromImage(image2)
    image2 = sitk.GetImageFromArray(arr)
    sitk.WriteImage(image2, str(path + 'brain.mha'))
    
    createSTL(path + 'tumour.mha', path + 'tumour.stl')
    createSTL(path + 'brain.mha', path + 'brain.stl')

    os.system(f'blender --background --python blender.py -- {id}')
    
    
    return 0




def TextureEdit(id):
    with open(str(path + 'static/'+id+'modelnew.gltf'), 'r') as myfile:
        data=myfile.read()

    # parse file
    obj = json.loads(data)

    # show values
    temp = obj['materials'][1]
    temp1 = obj['materials'][2]
    temp['alphaMode'] = 'BLEND'
    tempnew = temp['pbrMetallicRoughness']
    tempnew['baseColorFactor'] = [1,1,1,0.1]
    tempnew2 = temp1['pbrMetallicRoughness']
    tempnew2['baseColorFactor'] = [1,0,0,1]
    #print(obj["materials"])

    with open(str(path + 'static/' + id + 'modelnew.gltf'), 'w') as json_file:
        json.dump(obj, json_file)
        
        
    return (str(path + 'static/' + id + 'modelnew.gltf'))

def removefiles(flair,t2):
    os.remove("brain.mha")
    os.remove("brain.stl")
    os.remove("tumour.mha")
    os.remove("tumour.stl")
    os.remove(flair)
    os.remove(t2)






