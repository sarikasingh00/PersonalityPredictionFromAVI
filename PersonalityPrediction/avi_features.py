import subprocess
import glob
import os
import cv2     # for capturing videos
import math   # for mathematical operations
import matplotlib.pyplot as plt    # for plotting the images
import pandas as pd
import numpy as np    # for mathematical operations
import glob
import os
import dlib
import time
import math
# from celery import task


# @task
def feature_pipeline(path):
	print(path)
	# path of form - uploads/username/avi/videoname
	audio_extract(path)
	audio_path = audio_feature(path)
	
	frame_extract(path)
	video_path = loop_frame_crop(path)

	return audio_path, video_path

def audio_extract(path):
	print('audio extract')
	
	folder, username, subfolder, name = path.split('/')
	
	path = os.path.join(os.getcwd(), 'media' ,path).replace('/', '\\')
	print(path)  
	
	output_folder = 'media/' + folder + '/' + username + '/audio/'
	output_folder = os.path.join(os.getcwd(), output_folder).replace('/', '\\')
	print(output_folder)

	if not os.path.isdir(output_folder):
		print('making directory' + output_folder)
		os.mkdir(output_folder)
	
	output_path = output_folder + name + '.wav'
	print(output_path)

	command = "ffmpeg -i \"{}\" -ab 160k -ac 2 -ar 44100 -vn {}".format(path, output_path)
	# print(command)
	subprocess.call(command)
	# return output_path


def audio_feature(path):
	print('audio feature')
	folder, username, audio, name = path.split('/')

	audio_path = os.path.join(os.getcwd(), 'media' , folder, username, 'audio', name + '.wav').replace('/', '\\')
	print(audio_path)  

	# audio_path = './media/' + folder + '/' + username + '/audio/' + name + '.wav'
	# output_path = './media/' + folder + '/' + username + '/audio_features/' + name

	output_folder = 'media/' + folder + '/' + username + '/audio_features/'
	output_folder = os.path.join(os.getcwd(), output_folder).replace('/', '\\')
	print(output_folder)

	if not os.path.isdir(output_folder):
		print('making directory' + output_folder)
		os.mkdir(output_folder)

	output_path = output_folder + name

	command =  f'python D:/pyAudioAnalysis/pyAudioAnalysis/audioAnalysis.py featureExtractionFile -i {audio_path} -mw 1.0 -ms 1.0 -sw 1.0 -ss 1.0 -o {output_path}'
	subprocess.call(command, shell = True)
	return output_path + '_st.csv'


def frame_extract(path):
	# path of form - uploads/username/avi/videoname
	folder, username, subfolder, name = path.split('/')
	
	path = os.path.join(os.getcwd(), 'media' ,path).replace('/', '\\')
	print(path)  

	output_folder = 'media/' + folder + '/' + username + '/frames/'
	output_folder = os.path.join(os.getcwd(), output_folder).replace('/', '\\')
	print("frame output folder - ", output_folder)

	if not os.path.isdir(output_folder):
		print('making directory' + output_folder)
		os.mkdir(output_folder)
	

	cap = cv2.VideoCapture(path)   # capturing the video from the given path
	frameRate = cap.get(cv2.CAP_PROP_FPS) #frame rate - fps
	count = 0
	while(cap.isOpened()):
		frameId = cap.get(1) #current frame number
		ret, frame = cap.read()
		
		if (ret != True):
			break

		video_name_temp = name[0:-4]
		filename = video_name_temp + "_" + str(count) + ".jpg"
		
		if (frameId % math.floor(frameRate) == 0):
			count += 1
			cv2.imwrite((os.path.join(output_folder , filename)),frame)

	cap.release()


def loop_frame_crop(path):
	print('in crop loop')
	predictor_path = "D:\\Sarika\\PersonalityPredictionFromAVI\\shape_predictor_68_face_landmarks.dat"
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(predictor_path)
	print('got predictor and detector')

	folder, username, subfolder, name = path.split('/')
	
	path = 'media/' + folder + '/' + username + '/frames/'
	path = os.path.join(os.getcwd(), path).replace('/', '\\')
	print(path)

	output_folder = 'media/' + folder + '/' + username + '/cropped_frames/'
	output_folder = os.path.join(os.getcwd(), output_folder).replace('/', '\\')
	print(output_folder)

	if not os.path.isdir(output_folder):
		print('making directory' + output_folder)
		os.mkdir(output_folder)

	frame_names = glob.glob(path + '*')
	frame_names.sort()

	# root = 'D:\\Sarika\\PersonalityPredictionFromAVI\\data\\test\\frames\\'
	file_names = []
	for i in range(len(frame_names)):
		file_names += [frame_names[i].replace(path, '')]

	# print(file_names[0:10])

	# print(file_names[-20:])

	print(len(frame_names))

	for i in range(len(frame_names)):
		print(i)
		crop_landmarks(frame_names[i], file_names[i], detector, predictor, output_folder)

	return output_folder


def crop_landmarks(path, filename, detector, predictor, save_path):
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


def _shape_to_np(shape):
	xy = []
	for i in range(68):
		xy.append((shape.part(i).x, shape.part(i).y,))
	xy = np.asarray(xy, dtype='float32')
	return xy