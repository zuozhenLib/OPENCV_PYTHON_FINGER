# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 15:48:03 2019

@author: 77433
"""
from skimage import feature
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def LBP_hist(path='0',ROI_img=None):  #path : a path of roi  img : a  ROI img  
    if path!='0':
        img1=cv.imread(path,0)
    else:
        img1=cv.cvtColor(ROI_img,cv.COLOR_BGR2GRAY)
    img=feature.local_binary_pattern(img1,8,3,'default')
    img=img.astype('uint8')
    tile_cols=4
    tile_rows=2
    n=1
    rows,cols=img.shape
    step_rows=round(rows/tile_rows)-1
    step_cols=round(cols/tile_cols)-1
    feature1=[]
    for i in range(tile_rows):
        for j in range(tile_cols):
            tile=img[i*step_rows:(i+1)*step_rows-1,j*step_cols:(j+1)*step_cols-1]
            hist=cv.calcHist([tile],[0],None,[255],[0,255])
            hist=normalization(hist)
            feature1.append(hist) 
            plt.subplot(240+n)
            plt.plot(hist)
            n+=1
    plt.show()
    feature1=np.array(feature1)
    feature1=feature1.ravel()
    return feature1

def normalization(array) : #array 为nparry
    array=array.ravel()
    result =[]
    array_sum=array.sum()
    for i in array:
        result.append(i/array_sum)
    return np.array(result)

if __name__=="__main__":
    path='ROI_clahe_test1.bmp'
    img=cv.imread(path,-1)
    features=LBP_hist('0',img)
    plt.plot(features)
