import glob
import pandas as pd
import numpy as np

video_names = glob.glob('D:\\Sarika\\PersonalityPredictionFromAVI\\data\\audio_features\\*.wav_st.csv')
video_names.sort()
print(video_names[0:10])


time_steps = 15 # Frames extracted from the video 
aud_ft = 68 # Number of Audio features extracted from each non overlapping frame 
aud_2 = np.empty((0,time_steps,aud_ft))  # numpy array to contain the audio features 


audio_features = []
for video in video_names:
    aud = pd.read_csv(video,header=None)
    aud = np.array(aud)
    if aud.shape[0]!=15:
    	rows = 15 - aud.shape[0]
    	zeros = np.zeros((rows, 68))
    	aud = np.vstack((aud,zeros))
    # print(aud.shape)
    aud_2 = np.vstack((aud_2,aud[np.newaxis,...]))

print(aud_2.shape)