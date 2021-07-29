import json
import pyaudio
import wave
from playsound import playsound
import os
from ibm_watson import SpeechToTextV1,TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
audio = pyaudio.PyAudio()
print('Start...')
sound = audio.open(format=pyaudio.paInt16,
                   channels=2,
                   rate=44100,
                   frames_per_buffer=1024,
                   input=True)
list_of_frames = []
key = "AMNlvYjLpqloN8XtodmAmDs5PaC8-FlPnD0RmDnOW7ZS"
url = "https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/5bdf7444-c3eb-4305-95b5-75f7760aa78c"
iam = IAMAuthenticator(key)
stt = SpeechToTextV1(authenticator=iam)
stt.set_service_url(url)
for i in range(0, int(100)):
    f = sound.read(1024)
    list_of_frames.append(f)
print("End...")
sound.stop_stream()
sound.close()
audio.terminate()
wav_file = wave.open("temp.wav", 'wb')
wav_file.setnchannels(2)
wav_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
wav_file.setframerate(44100)
writer = b''.join(list_of_frames)
wav_file.writeframes(writer)
wav_file.close()
wave_file_sender = open("temp.wav",'rb')
sender_results = stt.recognize(wave_file_sender,content_type='audio/wav')
sender_results = str(sender_results)
removed_str = 'inline; filename=\"result.json\"'
if removed_str in sender_results :
    sender_results = sender_results.replace(removed_str,"")
sender_results = json.loads(sender_results)
sender_results = sender_results.get("result")
sender_results = sender_results.get("results")[0]
sender_results = sender_results.get('alternatives')[0]
sender_results = sender_results.get("transcript")
print(sender_results)
wave_file_sender.close()
txt_file = open("reader_sound.txt",'w')
txt_file.write(sender_results)
txt_file.close()
sender_txt_from_bot = "My language is arabic"
key = "_juVUjfxSDTNXTE92h8Z72amBuoJmiiyeS4ZD6BQPcGf"
url = "https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/c28b6b86-eeaa-4d86-bb4e-e899cd3fde8e"
iam = IAMAuthenticator(key)
tts = TextToSpeechV1(authenticator=iam)
tts.set_service_url(url)
reader_txt = open("reader_txt.mp3",'wb')
reciever_results = tts.synthesize(sender_txt_from_bot,accept="audio/mp3").get_result()
reciever_results = reciever_results.content
reader_txt.write(reciever_results)
reader_txt.close()
playsound("reader_txt.mp3")     
