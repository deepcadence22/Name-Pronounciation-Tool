#Author: Karthik

import sys
import os
import google.cloud.texttospeech as tts

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="involuted-ratio-349909-1bd15b3693bf.json"

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

#Given a voice from list_voices() and a text string to convert to speech this function stores the audio into a .wav file with text name as file name
def text_to_wav(voice_name: str, text: str):
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

    filename = f"{text}.wav"
    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Generated speech saved to "{filename}"')