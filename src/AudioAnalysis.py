import itertools

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

from glob import glob

import librosa
import librosa.feature
import librosa.display
import IPython.display as ipd

#CHANGES TO SUPPORT .PY:
# call plt.show()  after each plot to display (matplotlib)
import sounddevice as sd
import soundfile as sf


sns.set_theme(style="white", palette=None)
color_pal=plt.rcParams["axes.prop_cycle"].by_key()["color"]
color_cycle = itertools.cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"]) #itertools

audio_files = glob('../data/songs/*.mp3')

#2d data shape (cant be used with Series)
#data, samplerate = sf.read(audio_files[0])

# 1d data shape: (mono True makes it 1d)
data, samplerate = librosa.load(audio_files[0], mono=True)

# Play the audio
#sd.play(data, samplerate)
#sd.wait()

print("Audio data: ", data)
print("Data shape: ", {data.shape})
print("Audio samplerate: ", samplerate)


pd.Series(data).plot(figsize=(10, 5), lw=1, title='Raw Audio', color = color_pal[0])
#plt.show()

# [30000:31000]
pd.Series(data[10000:11000]).plot(figsize=(10, 5), lw=1, title='Raw Audio Zoomed-in', color = color_pal[1])
#plt.show()


# will trim the silent spots in the audio
#librosa.effects.trim(data, top_db=20) # 12min YT (can change the threshold of trim)


# soft Fourier Transform
D = librosa.stft(data) #transform data w FT
sound_db = librosa.amplitude_to_db(np.abs(D), ref=np.max) # S_db sound in decibel form
print("Sound_db shape: ", sound_db.shape)


fig, ax = plt.subplots(figsize=(10, 5))
img = librosa.display.specshow(sound_db, x_axis='time', y_axis='log', ax=ax)
ax.set_title('Sound Spectrogram', fontsize=20)
fig.colorbar(img, ax=ax, format='%+2.0f')
plt.show()

#MEL spectrogram (melodic spectrogram (frequencies))
melody_spec = librosa.feature.melspectrogram(y=data, sr=samplerate, n_mels=256) # n_mels is the # of mels we ask it to provide
sound_db_melody = librosa.amplitude_to_db(np.abs(D), ref=np.max)

fig, ax = plt.subplots(figsize=(15, 5))
img = librosa.display.specshow(sound_db_melody, x_axis='time', y_axis='log', ax=ax)
ax.set_title('Melody Spectrogram', fontsize=20)
fig.colorbar(img, ax=ax, format='%+2.0f')
plt.show()