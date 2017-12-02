#AquesTalkのライブラリをロードしてみた
#coding:utf-8
import wave
import pyaudio
#import StringIO
#from io import StringIO
import io
from ctypes import *

lib = cdll.LoadLibrary("./libAquesTalk2Eva.so.2.3")

str    = c_char_p("なにぬねの、まみむめも、あいうえお、かきくけこ、さしすせそ、たちつてと、はひふへほ、らりるれろ、わおん、きゃきゅきょ、しゃしゅしょ、ちゃちゅちょ、にゃにゅにょ、ひゃひゅひょ、みゃみゅみょ、りゃりゅりょ".encode())
size   = c_int(10)

lib.AquesTalk2_Synthe_Utf8.restype = POINTER(c_char)
wav_p = lib.AquesTalk2_Synthe_Utf8(str,100, byref(size),0)

print("size is %d" % size.value)
#output = StringIO.StringIO(wav_p[:size.value])
output = io.BytesIO(wav_p[:size.value])
wf = wave.open(output, "rb")

# ストリームを開く
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# チャンク単位でストリームに出力し音声を再生
chunk = 1024
data = wf.readframes(chunk)
while data != '':
    stream.write(data)
    data = wf.readframes(chunk)
stream.close()
p.terminate()

lib.AquesTalk2_FreeWave(wav_p)
output.close() 
