# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 13:37:54 2019

@author: 77433
"""

import cv2 as cv
import numpy as np
import my_algorithm as my
import math
from matplotlib import pyplot as plt

def get_ROI(path):
    img_temp=cv.imread(path,0)   # read img in gray mode
    img_gray=img_temp.copy()
    img =cv.imread(path,-1)
    rows,cols=img_temp.shape
    img_temp=cv.Canny(img_temp,90,240)  #get the main edges
    img_temp=my.get_edges(img_temp)   # only get the fingger edges
    points=my.get_centerline(img_temp)  #get the center points position for fitline
    line =cv.fitLine(points,cv.DIST_L2,0,0.01,0.01)
    angle = math.atan(line[1]/line[0])*180/math.pi  # get the angle for rotation
    angle= 90-angle if angle>0 else -90-angle
    M = cv.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),angle,1)
    img_rotation = cv.warpAffine(img,M,(cols,rows))   # rotation completed
    img_temp_rotation=cv.warpAffine(img_temp,M,(cols,rows))
    img_gray_rotation=cv.warpAffine(img_gray,M,(cols,rows))
    roi_cols=my.find_peak(img_gray_rotation[round(rows/2),:])
    roi_rows=my.find_bottom_rotation(img_temp_rotation) 
    ROI=img_rotation[roi_rows[0]:roi_rows[1],roi_cols[0]:roi_cols[1]]  #cut
    return ROI



if __name__=="__main__":
    path='clahe_test3.bmp'
    ROI=get_ROI(path)
    original=cv.imread(path,-1)
    cv.imshow("ROI",ROI)
    cv.imshow("original",original)
    
    cv.waitKey(0)
    cv.destroyAllWindows()