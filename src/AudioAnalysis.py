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
plt.show()

# [30000:31000]
pd.Series(data[10000:11000]).plot(figsize=(10, 5), lw=1, title='Raw Audio Zoomed-in', color = color_pal[1])
plt.show()


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

##### PLOT MELODY BANDS
mel_spec_db = librosa.amplitude_to_db(melody_spec, ref=np.max)

#define frequency in 6 bands
num_bands = 6
n_mels=256

#define frequency ranges in Hz
freq_ranges = {
    "Sub-bass (20–60 Hz)": (20, 60),
    "Bass (60–250 Hz)": (60, 250),
    "Low Midrange (250–500 Hz)": (250, 500),
    "Midrange (500–2k Hz)": (500, 2000),
    "Upper Midrange (2k–4k Hz)": (2000, 4000),
    "Treble (4k–20k Hz)": (4000, 20000)
}

#convert Hz to Mel scale
mel_frequencies = librosa.mel_frequencies(n_mels=n_mels, fmin=0, fmax=samplerate/2)

#find the closest Mel bin for a given Hz range
def get_mel_bin_range(fmin, fmax):
    min_bin = np.searchsorted(mel_frequencies, fmin)
    max_bin = np.searchsorted(mel_frequencies, fmax)
    return min_bin, max_bin

#function to plot a frequency band
def plot_mel_band(mel_band, title):
    fig, ax = plt.subplots(figsize=(10, 4))
    img = librosa.display.specshow(mel_band, x_axis='time', y_axis='mel', sr=samplerate, ax=ax)
    ax.set_title(title, fontsize=14)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    plt.show()

#extract and visualize each frequency band
for band_name, (fmin, fmax) in freq_ranges.items():
    min_bin, max_bin = get_mel_bin_range(fmin, fmax)
    band = mel_spec_db[min_bin:max_bin, :]
    plot_mel_band(band, band_name)


   #### DIFF VISUALS
plt.figure(figsize=(12, 6))

#extract and plot energy for each frequency band
for band_name, (fmin, fmax) in freq_ranges.items():
    min_bin, max_bin = get_mel_bin_range(fmin, fmax)

# Compute mean energy (dB) over time for the given frequency band
band_energy = np.mean(mel_spec_db[min_bin:max_bin, :], axis=0)

#plot the energy over time
plt.plot(band_energy, label=band_name, linewidth=2)

#frequency bands plot
plt.xlabel("Time Frames", fontsize=14)
plt.ylabel("Energy (dB)", fontsize=14)
plt.title("Frequency Band Energy Over Time", fontsize=16)
plt.legend(title="Frequency Bands")
plt.grid(True)
plt.show()