from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import matplotlib.cbook 
import matplotlib.pyplot as plt
import wave, sys, pyaudio
import sounddevice as sd
import scipy.signal
from sklearn.decomposition import FastICA
import numpy as np

def play(sound):
	sd.play(sound, blocking=True)

def play_two(file_new):
	chunk_size = 1024
    # Instantiate PyAudio.
	p = pyaudio.PyAudio()
	print(file_new)
	wf = wave.open(file_new,'rb')
	print(wf)
	# Open stream.
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
	    channels=wf.getnchannels(),
	    rate=wf.getframerate(),
	                output=True)

	data = wf.readframes(chunk_size)
	while len(data) > 0:
	    stream.write(data)
	    data = wf.readframes(chunk_size)

	# Stop stream.
	stream.stop_stream()
	stream.close()

	# Close PyAudio.
	p.terminate()


def ICA_analysis(X):
	ica = FastICA(n_components=3)
	print(X)
	S = ica.fit_transform(X)  # Reconstruct signals
	print(S.T[0])
	scipy.io.wavfile.write("three-new.wav",)



def plot(fs, data):
	a = data.T[0] # this is a two channel soundtrack, I get the first track
	b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
	c = fft(b) # calculate fourier transform (complex numbers list)
	print("furier transform")
	print(c)
	d = len(c)//2  # you only need half of the fft list (real signal symmetry)
	plt.plot(abs(c[:(d-1)]),'r') 
	plt.show()

def frequencyFilter(signal):
   for i in range(20000, len(signal)-20000):
      signal[i] = 0

def processWithNumpy(signal):
   transformedSignal = np.fft.fft(signal)
   frequencyFilter(transformedSignal)

   cleanedSignal = np.fft.ifft(transformedSignal)
   return np.array(cleanedSignal, dtype=np.float64)
fs, data = wavfile.read('three-sounds.wav') # load the data
data = data*0.001
data= ICA_analysis(data)
wavfile.write("output_comp.wav", fs,  data)
play_two("output_comp.wav")

WHERE ILEFT OFF: 
THERES OSME SORT OF BUG WITH ICA AND HOW IT WAS NOT WORKING
https://github.com/scikit-learn/scikit-learn/pull/2738