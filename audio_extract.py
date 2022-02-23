import subprocess
import glob

video_paths = glob.glob('D:\\Sarika\\PersonalityPredictionFromAVI\\data\\test\\test-2e\\*')
video_paths.sort()

print(video_paths[0:10])
print(len(video_paths))

for i in range(len(video_paths)):
# for i in range(5):
	print(i)
	video_path = video_paths[i]
	video_name = video_path[0:-4]
	# print(video)
	command = "ffmpeg -loglevel panic -i \"{}\" -ab 160k -ac 2 -ar 44100 -vn D:\\Sarika\\PersonalityPredictionFromAVI\\data\\test\\audio\\{}.wav".format(video_path, video_path.replace('D:\\Sarika\\PersonalityPredictionFromAVI\\data\\test\\test-2e\\', ''))
	# print(command)
	subprocess.call(command)