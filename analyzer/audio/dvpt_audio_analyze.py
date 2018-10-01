import os
import sys
__root = os.path.abspath(
    os.path.dirname(os.path.abspath(__file__)) + (os.sep + '..') * (
        len(os.path.dirname(os.path.abspath(__file__)).split(os.sep)) -
        os.path.dirname(os.path.abspath(__file__)).split(os.sep).index(
            'VeXtract'
        ) - 1
    )) + os.sep
sys.path.append(__root)

from helper import logger
log = logger.Logger(__name__)

from matplotlib import pyplot as plt
from scipy import signal
from scipy.io import wavfile
import numpy as np

def analyze_audio_list(file_name, frame_size=44100, noverlap=None):
	"""
	分析音訊頻率與強度
	file_name: 檔案名稱
	frame_size: 音框大小
	noverlap: 音框樣本重疊數
	- >{
		{
		time:時間點
			{
			# 一個頻率值對應一個強度
			frequency:頻率
			frequency strength:頻率強度
			...
			}
		}
		,...
	}
	"""
	AUDIO_FILE = __root + "file\\TESTFILE\\{file_name}"
	sampling_rate,audio_wave_data=wavfile.read(AUDIO_FILE)

	# Average audio wav data method
	audio_wave_data_average = np.average(wav, axis=1)
	frequency, time_segment, each_frequency_strength_corresponds_to_time_segment  = signal.stft(audio_wave_data_average, sampling_rate, nperseg=frame_size, noverlap=noverlap)
	time_segment_length = time_segment.size
	frequency_block_num = frequency.size
	channel_information_list = list()
	for segment in range(0,time_segment_length):
		segment_temp_list = list()
		frequency_corresponds_to_strength_temp_list = list()
		for num in range(0,frequency_block_num):
			temp_list = list()
			temp_list.append(frequency[num,0],each_frequency_strength_corresponds_to_time_segment[num,segment])
			frequency_corresponds_to_strength_temp_list.append(temp_list)	
		segment_temp_list.extend(time_segment[segment],frequency_corresponds_to_strength_temp_list)
		channel_information.append(segment_temp_list)
	return channel_information_list	

	# Analyze the left and right channels method
	channel_number = len(audio_wave_data.shape)
	audio_wave_data_length = audio_wave_data.shape[0]
	if channel_number == 2:
		left_channel = audio_wave_data[:,0]
		right_channel = audio_wave_data[:,1]
		left_frequency, left_time_segment, left_each_frequency_strength_corresponds_to_time_segment = signal.stft(left_channel, sampling_rate, nperseg=frame_size, noverlap=noverlap)
		right_frequency, right_time_segment, right_each_frequency_strength_corresponds_to_time_segment = signal.stft(right_channel, sampling_rate, nperseg=frame_size, noverlap=noverlap)
		left_channel_information_list = list()
		right_channel_information_list = list()
		time_segment_length = left_time_segment.size
		frequency_block_num = left_frequency.size
		for segment in range(0,time_segment_length):
		left_segment_temp_list = list()
		right_segment_temp_list = list()
		left_frequency_corresponds_to_strength_temp_list = list()
		right_frequency_corresponds_to_strength_temp_list = list()
			for num in range(0,frequency_block_num):
				left_temp_list = list()
				right_temp_list = list()
				left_temp_list.append(left_frequency[num,0],left_each_frequency_strength_corresponds_to_time_segment[num,segment])
				right_temp_list.append(right_frequency[num,0],right_each_frequency_strength_corresponds_to_time_segment[num,segment])
				left_frequency_corresponds_to_strength_temp_list.append(left_temp_list)	
				right_frequency_corresponds_to_strength_temp_list.append(right_temp_list)	
			left_segment_temp_list.extend(left_time_segment[segment],left_frequency_corresponds_to_strength_temp_list)
			right_segment_temp_list.extend(right_time_segment[segment],right_frequency_corresponds_to_strength_temp_list)
			left_channel_information_list.append(left_segment_temp_list)
			right_channel_information_list.append(right_segment_temp_list)
		return left_channel_information_list,right_channel_information_list	
	else:
		frequency, time_segment, each_frequency_strength_corresponds_to_time_segment  = signal.stft(audio_wave_data, sampling_rate, nperseg=frame_size, noverlap=noverlap)
		time_segment_length = time_segment.size
		frequency_block_num = frequency.size
		channel_information_list = list()
		for segment in range(0,time_segment_length):
			segment_temp_list = list()
			frequency_corresponds_to_strength_temp_list = list()
			for num in range(0,frequency_block_num):
				temp_list = list()
				temp_list.append(frequency[num,0],each_frequency_strength_corresponds_to_time_segment[num,segment])
				frequency_corresponds_to_strength_temp_list.append(temp_list)	
			segment_temp_list.extend(time_segment[segment],frequency_corresponds_to_strength_temp_list)
			channel_information.append(segment_temp_list)
		return channel_information_list	
	
if __name__ == "__main__":
    analyze_audio_list()


#以下先省略

# for block in range(0,audio_wave_length,frame_size):
# 			left_channel = left_channel[block:block+frame_size]
# 			right_channel = right_channel[block:block+frame_size]
# 			left_frequency, left_time_segment, left_each_frequency_strength_corresponds_to_time_segment = signal.stft(left_channel, sampling_rate, nperseg=frame_size, noverlap=noverlap)
# 			right_frequency, right_time_segment, right_each_frequency_strength_corresponds_to_time_segment = signal.stft(right_channel, sampling_rate, nperseg=frame_size, noverlap=noverlap)
# 			time_segment = left_time_segment.size
# 			for segment in range(0,time_segment):
# 				left_frequency__corresponds_to_strength_temp = list()
# 				right_frequency__corresponds_to_strength_temp = list()
# 				temp_list1 = list()
# 				temp_list2 = list()
# 				temp_list1.append(time_block_number[num])
# 				temp_list2.append(time_block_number[num])
# 			left_channel_information.append(temp_list1)
# 			right_channel_information.append(temp_list2)
# 		return left_channel_information_list,right_channel_information_list
