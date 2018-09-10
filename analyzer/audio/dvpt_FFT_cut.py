#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack
import numpy as np
from matplotlib import pyplot as plt

fs_rate, signal = wavfile.read("./audio/f-0222.wav")
print("type signal:"+str(type(signal))) #mytest
print("signal:"+str(signal)) #mytest
print("signal.size:"+str(signal.size)) #mytest
print ("Frequency sampling", fs_rate)
l_audio = len(signal.shape)
print(signal.shape)
print ("Channels", l_audio)
if l_audio == 2:
    signal = signal.sum(axis=1) / 2
N = signal.shape[0]
print ("Complete Samplings N", N)
secs = N / float(fs_rate)
print ("secs", secs)
Ts = 1.0/fs_rate  # sampling interval in time
print ("Timestep between samples Ts", Ts)
# time vector as scipy arange field / numpy.ndarray
t = scipy.arange(0, secs, Ts)
print("type t:"+str(type(t))) #mytest
print("t:"+str(t)) #mytest
FFT = abs(scipy.fft(signal)) 
print("type FFT:"+str(type(FFT))) #mytest
print("FFT:"+str(FFT)) #mytest
FFT_side = FFT[range(N/2)]  # one side FFT range
print("type FFT_side:"+str(type(FFT_side))) #mytest
print("FFT_side:"+str(FFT_side)) #mytest
freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])
print(t[1]-t[0]) #mytest
print(freqs) #mytest
fft_freqs = np.array(freqs)
print(fft_freqs) #mytest
freqs_side = freqs[range(N/2)]  # one side frequency range
fft_freqs_side = np.array(freqs_side)
plt.subplot(311)
p1 = plt.plot(t, signal, "g")  # plotting the signal
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.subplot(312)
p2 = plt.plot(freqs, FFT, "r")  # plotting the complete fft spectrum
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count dbl-sided')
plt.subplot(313)
# plotting the positive fft spectrum
p3 = plt.plot(freqs_side, abs(FFT_side), "b")
plt.xlabel('Frequency (Hz)')
plt.ylabel('Count single-sided')
plt.show()
