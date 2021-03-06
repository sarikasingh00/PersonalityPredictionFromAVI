import cv2     # for capturing videos
import glob
import os
import math

video_files_root = "D:\\Sarika\\PersonalityPredictionFromAVI\\data\\test\\test-2e\\"

# get all video file names
video_names = glob.glob(video_files_root + "*.mp4")
print(video_names[0:10])

for i in range(len(video_names)):
  video_names[i] = video_names[i].replace(video_files_root, '')

print(video_names[0:10])

#extracts 1 frame per second

path = 'D:\\Sarika\\PersonalityPredictionFromAVI\\data\\test\\frames'

for i in range(len(video_names)):
	print(i)

	video_name = video_names[i]
	videoFile = video_files_root + video_name
	# print(video_name)

	cap = cv2.VideoCapture(videoFile)   # capturing the video from the given path
	# print(cap)
	frameRate = cap.get(cv2.CAP_PROP_FPS) #frame rate - fps
	# print(frameRate)
	count = 0
	# print(cap.isOpened())
	while(cap.isOpened()):
		# print("in if")
		frameId = cap.get(1) #current frame number
		ret, frame = cap.read()
		# print(ret)
		if (ret != True):
			break
		if (frameId % math.floor(frameRate) == 0):
	  		# video_name_temp = video_name[0:-4].replace('.','#')
			video_name_temp = video_name[0:-4]
			filename = video_name_temp + "_" + str(count) + ".jpg"
			count += 1
			# print((os.path.join(path , filename)))
			cv2.imwrite((os.path.join(path , filename)),frame)
	  		# cv2.imwrite(filename, frame)
	cap.release()

print ("Done!")


"""
duration - 7s
fps -50
framecount - 350

step - framecount/15 - ceil(350/15) - 24

frameid - 0,349

frameId % step == 0:
 0 23 46 ... 230 345

"""