# -*- coding:utf-8 -*-
from pydub import AudioSegment
from pydub.utils import make_chunks
import speech_recognition as sr
import wave
import contextlib


def audio_cut_and_recognize(file_name, chunk_length_ms, file_format='wav', start_time=0.0, out_route='./cut'):
    r = sr.Recognizer()
    myaudio = AudioSegment.from_file(file_name, file_format)
    chunk_length_ms = chunk_length_ms
    chunks = make_chunks(myaudio, chunk_length_ms)
    start_time = start_time
    for i, chunk in enumerate(chunks):
        chunk_name = "{route}/chunk{index}.wav".format(
            route=out_route, index=i)
        print("exporting", chunk_name)
        chunk.export(chunk_name, format="wav")
        with sr.AudioFile(chunk_name)as source:
            audio = r.record(source)
        vocie_recognize = r.recognize_google(audio, language='zh-TW')
        print(vocie_recognize)
        with contextlib.closing(wave.open(chunk_name, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            end_time = start_time+duration
            print("start time:"+str(start_time)+"  "+"end time:"+str(end_time))
        start_time = start_time+end_time


if __name__ == "__main__":
    audio_cut_and_recognize('./audio/a-0101.wav', 10000)
    #tests
