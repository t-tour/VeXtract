
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

import numpy as np
from scipy.io import wavfile
from scipy import signal
from matplotlib import pyplot as plt


def analyze_audio_list(file, frame_size=44100, noverlap=None):
    """
    利用STFT分析音訊(.wav)，獲取對應時間點中包含頻率值與其強度

    Parameters:
        file(str): 檔案路徑
        frame_size(int): 音框大小 ※預設 44100
        noverlap(int): 音框樣本重疊數 ※預設 None
    Returns:
        each frequency and strength corresponds to cast point
        Architecture:
            [
                {
                    "time" : (start_time, end_time),  # 單位:秒和小數點
                    "spectrum" : [
                        (
                            頻率值,
                            強度
                        ),...  # 排序:以強度由小至大
                    ]
                },...
            ]
        """
    sampling_rate, audio_wave_data = wavfile.read(file)

    # Average audio wav data method
    audio_wave_data_average = np.average(audio_wave_data, axis=1)
    frequency, time_segment, each_frequency_strength_corresponds_to_time_segment = signal.stft(
        audio_wave_data_average, sampling_rate, nperseg=frame_size, noverlap=noverlap)
    time_segment_length = time_segment.size
    frequency_block_num = frequency.size
    channel_information_list = list()
    for seg in range(1, time_segment_length - 1, 1):
        segment_tuple = (time_segment[seg - 1], time_segment[seg])
        frequency_corresponds_to_strength_temp_list = [
            [frequency[num], each_frequency_strength_corresponds_to_time_segment[num, seg]] for num in range(frequency_block_num)]
        segment_dict = dict(
            {'time': segment_tuple, 'spectrum': frequency_corresponds_to_strength_temp_list})
        channel_information_list.append(segment_dict)
    print(channel_information_list[:5])
    return channel_information_list

    # # Analyze the left and right channels method
    # channel_number = len(audio_wave_data.shape)
    # audio_wave_data_length = audio_wave_data.shape[0]
    # if channel_number == 2:
    # 	left_channel = audio_wave_data[:,0]
    # 	right_channel = audio_wave_data[:,1]
    # 	left_frequency, left_time_segment, left_each_frequency_strength_corresponds_to_time_segment = signal.stft(left_channel, sampling_rate, nperseg=frame_size, noverlap=noverlap)
    # 	right_frequency, right_time_segment, right_each_frequency_strength_corresponds_to_time_segment = signal.stft(right_channel, sampling_rate, nperseg=frame_size, noverlap=noverlap)
    # 	left_channel_information_list = list()
    # 	right_channel_information_list = list()
    # 	time_segment_length = left_time_segment.size
    # 	frequency_block_num = left_frequency.size
    # 	for segment in range(0,time_segment_length):
    # 		left_segment_temp_list = list()
    # 		right_segment_temp_list = list()
    # 		left_frequency_corresponds_to_strength_temp_list = [[[left_frequency[num], left_each_frequency_strength_corresponds_to_time_segment[num,segment]] for num in range(frequency_block_num)]]
    # 		right_frequency_corresponds_to_strength_temp_list = [[[right_frequency[num], right_each_frequency_strength_corresponds_to_time_segment[num,segment]] for num in range(frequency_block_num)]]
    # 		cast_point_temp_list = [left_time_segment[segment]]
    # 		left_segment_temp_list.extend(cast_point_temp_list)
    # 		right_segment_temp_list.extend(cast_point_temp_list)
    # 		left_segment_temp_list.extend(left_frequency_corresponds_to_strength_temp_list)
    # 		right_segment_temp_list.extend(right_frequency_corresponds_to_strength_temp_list)
    # 		left_channel_information_list.append(left_segment_temp_list)
    # 		right_channel_information_list.append(right_segment_temp_list)
    # 	return left_channel_information_list , right_channel_information_list
    # else:
    # 	frequency, time_segment, each_frequency_strength_corresponds_to_time_segment  = signal.stft(audio_wave_data, sampling_rate, nperseg=frame_size, noverlap=noverlap)
    # 	time_segment_length = time_segment.size
    # 	frequency_block_num = frequency.size
    # 	channel_information_list = list()
    # 	for segment in range(0,time_segment_length):
    # 		segment_temp_list = list()
    # 		frequency_corresponds_to_strength_temp_list = [[[frequency[num], each_frequency_strength_corresponds_to_time_segment[num,segment]] for num in range(frequency_block_num)]]
    # 		cast_point_temp_list = [time_segment[segment]]
    # 		segment_temp_list.extend(cast_point_temp_list)
    # 		segment_temp_list.extend(frequency_corresponds_to_strength_temp_list)
    # 		channel_information_list.append(segment_temp_list)
    # 	return channel_information_list


if __name__ == "__main__":
    analyze_audio_list(os.path.join(__root, "file", "tt.wav"))
