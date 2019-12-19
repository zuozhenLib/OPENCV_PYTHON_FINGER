# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 17:03:47 2019

@author: 77433
"""
import numpy as np
import cv2 as cv

def get_edges(img):   # img : single channel img which has been processed by cv.Canny
    rows,cols=img.shape
    center=rows/2
    index=[]
    up_index=[]
    for i in range(cols):
        temp_index=np.argwhere(img[:,i]==255)
        temp_index=temp_index.tolist()
        for j in temp_index:
            if j[0]<center:
                up_index.append(center-j[0])      
        up=len(up_index)-1
        up_index.clear()
        down = up+1
        try:
            index.append([temp_index[up][0],i] )
        except IndexError:
            index.append([index[-2][0],i])
        try:
            index.append([temp_index[down][0],i])
        except IndexError:
            index.append([index[-2][0],i])
    result_img=np.zeros((rows,cols),dtype="uint8")
    #print(index)
    for j in index:
        result_img[j[0],j[1]]=255
    return result_img


def get_centerline(img):   # img : single channel img which has been processed by get_edges
    rows,cols=img.shape
    coord=[]
    for i in range(cols):
        temp_index=np.argwhere(img[:,i]==255)
        temp_index=temp_index.tolist()
        center_position=round((temp_index[0][0]+temp_index[1][0])/2)
        temp_index.clear()
        coord.append([center_position,i])
    #print(coord)
    points=np.array(coord)
    return points
    '''
    result_img=np.zeros((rows,cols),dtype="uint8")
    
    for j in coord:
        result_img[j[0],j[1]]=255
    return result_img
    '''

def my_equalizehist(single):
    hist=cv.calcHist([single],[0],None,[256],[0,256])
    num_of_pixels=single.size
    ratio=np.zeros(256)
    transf_map=np.zeros(256)
    result=single.copy()
    j=0
    for i in hist:
        if j>0:
            ratio[j]=i/num_of_pixels+ratio[j-1]
        else:
             ratio[j]=i/num_of_pixels
        transf_map[j]=round(ratio[j]*255)
        j=j+1
    for i in range(single.shape[0]):
        for j in range(single.shape[1]):
            result[i][j]=transf_map[single[i][j]]
        #result[result==j]=k[j]     
    return result

def find_peak(arr):  #only work for particular series of image
    peaks=[]
    step=1
    pos=1
    while(pos<600):
        if (arr[pos]>=arr[pos+step])and(arr[pos]>arr[pos-step]):
            if ((arr[pos]>arr[pos+20])and(arr[pos]>arr[pos-20])):
                peaks.append(pos)
        pos=pos+step
    peak1=0
    peak2=340
    print(peaks)
    for i in peaks:
        if (i<340):
            if arr[i]>=arr[peak1] :
                peak1=i
        else:
             if arr[i]>=arr[peak2] : 
                peak2=i 
    if(peak2-peak1)<200 :
        print("EOI error in peak")
    return peak1,peak2

def find_bottom(img):  # this img had been processed by my.get_edges
    rows,cols=img.shape
    pos1=0
    pos2=rows
    for i in range(cols):
        temp_index=np.argwhere(img[:,i]==255)
        temp_index=temp_index.tolist()
        if temp_index[0][0]>pos1:
            pos1=temp_index[0][0]
        if temp_index[1][0]<pos2:
            pos2=temp_index[1][0]
    return pos1,pos2

# because after rotation the grayscale will change,and it never equal to 255 any more
# so the find_bottom doesn't work for the img which has been rotated
# and  I make a new func for this
def find_bottom_rotation(img):  
    rows,cols=img.shape
    pos1=0
    pos2=rows
    for i in range(rows):
        if i<rows/2:
            if img[i,:].sum()!=0:
                if i>pos1:
                    pos1=i
        else:
            if img[i,:].sum()!=0:
                if i<pos2:
                    pos2=i
    return pos1,pos2