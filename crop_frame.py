import cv2     # for capturing videos
import math   # for mathematical operations
import matplotlib.pyplot as plt    # for plotting the images
import pandas as pd
import numpy as np    # for mathematical operations
import glob
import os
import dlib
import time


def _shape_to_np(shape):
    xy = []
    for i in range(68):
        xy.append((shape.part(i).x, shape.part(i).y,))
    xy = np.asarray(xy, dtype='float32')
    return xy


def crop_landmarks(path, filename):
  img = cv2.imread(path)
  if img is None:
    print("Could not read image", path)
    return

  try :
    lmarks = []
    dets = detector(img, 1)
    # print("Number of faces detected: {}".format(len(dets)))
    
    if len(dets) != 1:
      print("No of faces mismatch - ", len(dets), path)
      return

    shapes = []
    for k, det in enumerate(dets):
      shape = predictor(img, det)
      shapes.append(shape)
      xy = _shape_to_np(shape)
      lmarks.append(xy)

    lmarks = np.asarray(lmarks, dtype='float32')
    face_1 = lmarks[0]
    min_x, min_y = face_1.min(axis=0)
    max_x, max_y = face_1.max(axis=0)

    min_x = max(0,min_x)
    min_y = max(0,min_y)

    crop_img = img[int(min_y):int(max_y)+1, int(min_x):int(max_x)+1]
    # print((os.path.join(save_path , filename)))
    cv2.imwrite((os.path.join(save_path , filename)),crop_img)
  except Exception as e:
    print("Error, skipping file ", path, e)
    return


start_time = time.time()

save_path = 'D:\\Sarika\\PersonalityPredictionFromAVI\\data\\test\\cropped_frames'
predictor_path = "D:\\Sarika\\PersonalityPredictionFromAVI\\shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)


frame_names = glob.glob('D:\\Sarika\\PersonalityPredictionFromAVI\\data\\test\\frames\\*')
frame_names.sort()

root = 'D:\\Sarika\\PersonalityPredictionFromAVI\\data\\test\\frames\\'
file_names = []
for i in range(len(frame_names)):
  file_names += [frame_names[i].replace(root, '')]

print(file_names[0:10])

# print(file_names[-20:])

print(len(frame_names))

for i in range(len(frame_names)):
  print(i)
  crop_landmarks(frame_names[i], file_names[i])
