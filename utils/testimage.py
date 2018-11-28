import cv2
import os
import numpy as np

image = cv2.imread('/home/buiduchanh/WorkSpace/Deep_reader/TextRecognitionDataGenerator/out/沖縄県八重山郡竹富町小浜秋葉原ＨＦビル_0.jpg')

im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
print(im_bw.shape)
color_img = cv2.cvtColor(im_bw, cv2.COLOR_GRAY2RGB )
print(color_img.shape)
cv2.imwrite('/home/buiduchanh/WorkSpace/Deep_reader/TextRecognitionDataGenerator/out/result.jpg', color_img)

# img = cv2.imread('/home/buiduchanh/WorkSpace/Deep_reader/TextRecognitionDataGenerator/out/result.jpg')
# cv2.imshow('a', img)
# cv2.waitKey()
# cv2.destroyAllWindows()