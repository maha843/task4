import json
import pyaudio
import wave
from playsound import playsound
import os
from ibm_watson import SpeechToTextV1,TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
print("Merge speech to text")
key = "AMNlvYjLpqloN8XtodmAmDs5PaC8-FlPnD0RmDnOW7ZS"
url = "https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/5bdf7444-c3eb-4305-95b5-75f7760aa78c"
iam = IAMAuthenticator(key)
stt = SpeechToTextV1(authenticator=iam)
stt.set_service_url(url)
_file_sender = open("speech_to_text.mp3",'rb')
sender_results = stt.recognize(_file_sender,content_type='audio/mp3')
sender_results = str(sender_results)
removed_str = 'inline; filename=\"result.json\"'
if removed_str in sender_results :
    sender_results = sender_results.replace(removed_str,"")
sender_results = json.loads(sender_results)
sender_results = sender_results.get("result")
sender_results = sender_results.get("results")[0]
sender_results = sender_results.get('alternatives')[0]
sender_results = sender_results.get("transcript")
_file_sender.close()
txt_file = open("speech_to_text.txt",'a')
txt_file.write(" " + sender_results)
txt_file.close()
print("Merge Text to Speech")
txt = ""
txt_file = open("text_to_speech.txt",'r')
txt = txt_file.readline()
txt_file.close()
key = "_juVUjfxSDTNXTE92h8Z72amBuoJmiiyeS4ZD6BQPcGf"
url = "https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/c28b6b86-eeaa-4d86-bb4e-e899cd3fde8e"
iam = IAMAuthenticator(key)
tts = TextToSpeechV1(authenticator=iam)
tts.set_service_url(url)
reader_txt = open("text_to_speech.mp3",'ab')
reciever_results = tts.synthesize(txt,accept="audio/mp3").get_result()
reciever_results = reciever_results.content
reader_txt.write(reciever_results)
reader_txt.close()
