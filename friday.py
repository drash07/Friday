import speech_recognition as sr
import pyttsx3
import os

speech = sr.Recognizer()

try:
    engine = pyttsx3.init()
except ImportError:
    print('Requested driver is not found')
except RuntimeError:
    print('Driver fails to initialize')

voices = engine.getProperty('voices')

engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')
rate = engine.getProperty('rate')
engine.setProperty('rate', rate)


# AI Friday
def speak_text_cmd(cmd):
    engine.say(cmd)
    engine.runAndWait()


# user voice command
def read_voice_cmd():
    voice_text = ''
    print('Listening...')
    with sr.Microphone() as source:
        audio = speech.listen(source)
    try:
        voice_text = speech.recognize_google(audio)
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print('Network error')
    return voice_text


if __name__ == '__main__':
    speak_text_cmd('Hello Mrs. Patel Shah. ')

    while True:

        voice_note = read_voice_cmd()
        print('{}'.format(voice_note))

        if 'Hello' in voice_note:
            speak_text_cmd('How can I help you today?')
            continue
        elif 'open' in voice_note:
            speak_text_cmd('Here it is...')
            os.system('open /Applications/"{}".app'.format(voice_note.replace('open ', '')))
            continue
        elif 'Bye' in voice_note:
            speak_text_cmd('Bye Mrs. Shah')
            exit()
