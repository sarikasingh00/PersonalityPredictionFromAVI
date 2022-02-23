# # from python_speech_features import mfcc
# from python_speech_features import logfbank
# import scipy.io.wavfile as wav
# import glob
# import numpy as np
# import math


# audio_paths = glob.glob('D:\\Sarika\\PersonalityPredictionFromAVI\\data\\audio\\*')
# audio_paths.sort()

# print(audio_paths[0:10])
# print(len(audio_paths))

# # sig_array = []
# # max_sig = None
# # min_sig = None

# for i in range(len(audio_paths)):
# 	if i%200==0:
# 		print(i)
# 	(rate,sig) = wav.read(audio_paths[i])

# 	# sig_array += [sig]
	
# 	# winstep = int((len(sig) - rate)/(rate*14)) + 1
# 	# winstep = len(sig) / (15*rate)

# 	# low = len(sig)/(15*rate)
# 	# high = len(sig)/(14*rate)

# 	# winstep = (low+high)/2

# 	# winlen = winstep

# 	# n_frame = 1 + math.ceil((len(sig)-rate*winlen)/(rate*winstep))
# 	# if n_frame!=15:
# 	# 	print(audio_paths[i], rate, len(sig), n_frame)
	
# 	fbank_feat = logfbank(sig,rate, winlen=1, winstep=2.2)
# 	if fbank_feat.shape[0]!=15:
# 		print(audio_paths[i], fbank_feat.shape)

# 	name = audio_paths[i].replace('D:\\Sarika\\PersonalityPredictionFromAVI\\data\\audio\\','')[0:-4]
# 	np.save('D:\\Sarika\\PersonalityPredictionFromAVI\\data\\logfbank_15\\{}'.format(name), fbank_feat)


#  # feat,energy = fbank(signal,samplerate,winlen,winstep,nfilt,nfft,lowfreq,highfreq,preemph,winfunc)
#  # frames = sigproc.framesig(signal, winlen*samplerate, winstep*samplerate, winfunc)
#  # numframes = 1 + int(math.ceil((1.0 * slen - frame_len) / frame_step))

#  # 275456 - 1*44100 / 44100


#  # 674816 91136


import os
import subprocess

count = 0
files = os.listdir('D:/Sarika/PersonalityPredictionFromAVI/data/test/audio/')
files.sort()
print(type(files[0:4]))
for i in files:
	# if count%5 ==0:
	print('audio number: ',count)
	file_path = 'D:/Sarika/PersonalityPredictionFromAVI/data/test/audio/' + i
	output_path =  'D:/Sarika/PersonalityPredictionFromAVI/data/test/audio_features/' + i
	command =  f'python D:/pyAudioAnalysis/pyAudioAnalysis/audioAnalysis.py featureExtractionFile -i {file_path} -mw 1.0 -ms 1.0 -sw 1.0 -ss 1.0 -o {output_path}'
	subprocess.call(command, shell = True)
	count +=1