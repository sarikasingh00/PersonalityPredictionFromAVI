import librosa
import numpy as np
import os

count = 0
files = os.listdir('D:/Sarika/PersonalityPredictionFromAVI/data/train/train audio/')
files.sort()
print(files[0:4])

for i in files:
	# if count%5 ==0:
	print('audio number: ',count)
	file_path = 'D:/Sarika/PersonalityPredictionFromAVI/data/train/train audio/' + i
	output_path =  'D:/Sarika/PersonalityPredictionFromAVI/data/train/train mfcc/' + i
	y, sr = librosa.load(file_path)
	mfcc = librosa.feature.mfcc(y=y, sr=sr)
	np.save(output_path, mfcc)
	# command =  f'python D:/pyAudioAnalysis/pyAudioAnalysis/audioAnalysis.py featureExtractionFile -i {file_path} -mw 1.0 -ms 1.0 -sw 1.0 -ss 1.0 -o {output_path}'
	# subprocess.call(command, shell = True)
	count +=1