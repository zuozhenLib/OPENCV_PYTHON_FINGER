# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 11:51:32 2019

@author: 77433
"""
import cv2 as cv 
import numpy as np
from matplotlib import pyplot as plt
import ROI_completed as RC

kernel=np.ones((7,7),dtype="uint8")

kernel1=np.array([[0,1,0],
                  [1,1,1],
                  [0,1,0]],dtype='uint8')
kernel2=np.ones((3,5),dtype="uint8")
kernel3=np.ones((5,3),dtype="uint8")
#cv.imwrite("./device1_clahe/clahe_test1.bmp",clahe_test1)
#cv.imwrite("clahe_test1.bmp",clahe_test1)


def open_operation(img,kernel,kernel1):

    img=cv.erode(img,kernel1)
    img=cv.dilate(img,kernel)
    return img

def close_operation(img,kernel,kernel1):  # kernel for dilation,kernel1 for erosion
    
    img=cv.dilate(img,kernel)
    img=cv.erode(img,kernel1)
    return img

def feature_binary(path='0',img=None):  #img 是经过get_ROI处理过的ROI图片
    kern = cv.getGaborKernel((17,17),4,0,10,0.5,0,ktype=cv.CV_64F)
    kern2 = cv.getGaborKernel((17,17),4,np.pi/2,10,0.5,0,ktype=cv.CV_64F)
    if path!='0':
        img=cv.imread(path,0)
    ROI=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    fimg = cv.filter2D(ROI,cv.CV_8UC3,kern)
    fimg2=cv.filter2D(ROI,cv.CV_8UC3,kern2)
    ret,fimg_b=cv.threshold(fimg,230,255,cv.THRESH_BINARY_INV)
    ret,fimg2_b=cv.threshold(fimg2,245,255,cv.THRESH_BINARY_INV)
    orimg=cv.bitwise_or(fimg_b,fimg2_b)
    result=close_operation(orimg,kernel,kernel)
    result=cv.erode(result,kernel1)
    return result
    
        
if __name__ =="__main__":
    path1="clahe_test2.bmp"
    ROI=RC.get_ROI(path1)
    dst=feature_binary(img=ROI)
    cv.imshow("ROI",ROI)
    cv.imshow("feature",dst)
    k=cv.waitKey(0)
    if k == 27:         # wait for ESC key to exit
        cv.destroyAllWindows()
    elif k == ord('s'): # wait for 's' key to save and exit
        outpath="feature_"+path1
        cv.imwrite(outpath,dst)
        cv.destroyAllWindows()
