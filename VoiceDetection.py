import streamlit as st

import speech_recognition as sr
import os
from deepgram import DeepgramClient,PrerecordedOptions,FileSource

import wave

directory = r'D:\\majed\\Data Science\\deployment\\checkpoint\\VoiceCheckpoint\\Speech_recognition'

os.chdir(directory)

DEEPGRAM_API_KEY='68be8412d0aa265e6b0a02da9a415c0e8f38e355'



def transcribe_speech(Language) :

    # Initialisation de la classe de reconnaissance
    r = sr.Recognizer()
    # Lecture du microphone comme source

    with sr.Microphone() as source :

        st.info("Parlez maintenant..." )

        # écoute la parole et la stocke dans la variable audio_text

        audio_text = r.listen(source)

        st.info("Transcription..." )

        try :

            # utiliser la reconnaissance vocale de Google

            text = r.recognize_google(audio_text,language=Language)

            return text

        except Exception as e:
            print(f"Exception: {e}")  

            return "Désolé, je n'ai pas compris." 


def deepgram(Language):
    
    r = sr.Recognizer()
    dg= DeepgramClient(DEEPGRAM_API_KEY)
    
    if Language=='en-US':
        Language=='en'
    elif Language=='fr-FR':
        Language=='fr'
    
    try:  
        with sr.Microphone() as source :

            st.info("Parlez maintenant..." )

            # écoute la parole et la stocke dans la variable audio_text

            audio_text = r.listen(source)

            st.info("Transcription..." )

            with open("output.wav", "wb") as f: 
                f.write(audio_text.get_wav_data())

            with open("output.wav", "rb") as file:
                buffer_data = file.read()

            payload: FileSource = {
                "buffer": buffer_data,
            }
        
            #STEP 2: Configure Deepgram options for audio analysis
            options = PrerecordedOptions(
            model="nova-2",
            language=Language,
            smart_format=True,
            )

            # STEP 3: Call the transcribe_file method with the text payload and options
            response = deepgram.listen.rest.v("1").transcribe_file(payload, options)

            return response.to_json(indent=4)
        
    except Exception as e:
        print(f"Exception: {e}")    
        return "Désolé, je n'ai pas compris."
    









def main() :

    st.title("Speech Recognition App" )

    api_to_use=1
    Language='en-US'
    
    
    API = st.radio(
        'Choisir l''API a utiliser:',
        ('Speech Recognizer','Deepgram'))
    if API:
        if API=='Deepgram':
            api_to_use=2

    
    lang = st.radio(
        'Choisir la langue:',
        ('English','French','Arabic'))
    if lang:
        if lang=='French':
            Language='fr-FR'
        else:
            Language='ar'


    st.write("Cliquez sur le microphone pour commencer à parler:" )



    # ajouter un bouton pour déclencher la reconnaissance vocale

    if st.button("Start Recording"):

        if api_to_use==1:
            text = transcribe_speech(Language)
        elif api_to_use==2:
            text = deepgram(Language)
        else:
            text= ''

        st.write("Transcription : " , text)

if __name__ == "__main__" :

    main()
