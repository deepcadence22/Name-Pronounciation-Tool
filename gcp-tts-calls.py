#Author: Karthik

import sys
import os
import google.cloud.texttospeech as tts
from flask import Flask, request, Response
from flask_restful import Api

app=Flask(__name__)
api=Api(app)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="involuted-ratio-349909-1bd15b3693bf.json"

#Returns all list of unique languages given a voice
def unique_languages_from_voices(voices):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set

#Returns language_codes/locales that GCP supports
def list_languages():
    client = tts.TextToSpeechClient()
    response = client.list_voices()
    languages = unique_languages_from_voices(response.voices)
    return sorted(list(languages))

#Returns the genders of voices supported for the language_code given
def list_genders(language_code):
    client = tts.TextToSpeechClient()
    response = client.list_voices()
    voices = sorted(response.voices, key=lambda voice: voice.name)
    return sorted(list(set("MALE" if voice.ssml_gender==1 else "FEMALE" for voice in voices if voice.language_codes==[language_code])))
    
#Returns available voices - language_code must be one of list_languages() , ssml_gender must be one of list_languages(language_code)
def list_voices(language_code,ssml_gender):
    client = tts.TextToSpeechClient()
    response = client.list_voices()
    voices = sorted(response.voices, key=lambda voice: voice.name)
    return [voice.name for voice in voices if voice.ssml_gender==(1 if ssml_gender=="MALE" else 2) and "Wavenet" in voice.name and voice.language_codes==[language_code]]

#The following is a rest endpoint which takes the name and voice as inputs in GET method /pronounce?name="Karthik Peddi"&voice="en-IN-Wavenet-B"
@app.route("/pronounce",methods=["GET"])
def text_to_wav(voice_name=None,text=None):
    voice_name=request.args.get("voice").replace("\"","")
    text=request.args.get("name").replace("\"","")

    if voice_name is None:
        #This is where Akshay's method will be called to get the locale and appropriately select a voice
        pass #Will be replaced with call to Akshay's method like locale=some_method(text) and based on locale random_voice will be selected

    language_code = "-".join(voice_name.split("-")[:2])
    text_input = tts.SynthesisInput(text=text)
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )
    return Response(response.audio_content, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="localhost",port=8080,debug=True)