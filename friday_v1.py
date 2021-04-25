import speech_recognition as sr
import os
from playsound import playsound
import webbrowser
import random

speech = sr.Recognizer()
greeting_dict = {'hello': 'hello', 'hi': 'hi'}
open_launch_dict = {'open': 'open', 'launch': 'launch'}
google_search_dict = {'what': 'what', 'why': 'why', 'who': 'who', 'which': 'which'}
social_media_dict = {'facebook': 'http://www.facebook.com', 'youtube': 'https://www.youtube.com/'}

mp3_greeting_list = ['mp3/friday/greeting_1.mp3', 'mp3/friday/greeting_1.mp3']
mp3_open_launch_list = ['mp3/friday/open_launch2.mp3', 'mp3/friday/open_launch1.mp3']
mp3_google_search_list = []
mp3_listening_issues_list = ['mp3/friday/difficutly_hearing1.mp3']
mp3_struggling_list = ['mp3/friday/difficulty_hearing2.mp3']

error_occurrence = 0


def is_valid_google_search(phrase):
    if google_search_dict.get(phrase.split(' ')[0]) == phrase.split(' ')[0]:
        return True


def play_sound(mp3_list):
    mp3 = random.choice(mp3_list)
    playsound(mp3)


def read_voice_cmd():
    voice_text = ''
    print('Listening...')

    global error_occurrence

    try:
        with sr.Microphone() as source:
            audio = speech.listen(source=source, timeout=10, phrase_time_limit=5)
        voice_text = speech.recognize_google(audio)

    except sr.UnknownValueError:
        if error_occurrence == 0:
            play_sound(mp3_listening_issues_list)
            error_occurrence+=1
        elif error_occurrence == 1:
            play_sound(mp3_struggling_list)
            error_occurrence+=1
        pass
    except sr.RequestError as e:
        print('Network error')
    except sr.WaitTimeoutError:
        if error_occurrence == 0:
            play_sound(mp3_listening_issues_list)
            error_occurrence += 1
        elif error_occurrence == 1:
            play_sound(mp3_struggling_list)
            error_occurrence += 1
        pass
    return voice_text


def is_valid_greeting(greet_dict, voice_note):
    for key, value in greet_dict.iteritems():
        try:
            if value == voice_note.split(' ')[0]:
                return True
                break
            elif key == voice_note.split(' ')[1]:
                return True
                break
        except IndexError:
            pass

    return False


def is_valid_open_launch(open_launch_dict1, voice_note1):
    for key, value in open_launch_dict1.iteritems():
        if value == voice_note.split(' ')[0]:
            return True
            break

    return False


if __name__ == '__main__':

    playsound('mp3/friday/greetings.mp3')

    while True:

        voice_note = read_voice_cmd().lower()
        print('{}'.format(voice_note))

        if is_valid_greeting(greeting_dict, voice_note):
            print('greeting...')
            play_sound(mp3_greeting_list)
            continue
        elif is_valid_open_launch(open_launch_dict, voice_note):
            print('Opening...')
            play_sound(mp3_open_launch_list)
            # Launch social media here
            if is_valid_greeting(social_media_dict, voice_note):
                key = voice_note.split(' ')[1]
                webbrowser.open(social_media_dict.get(key))
            else:
                os.system('open /Applications/"{}".app'.format(voice_note.replace('open ', '').replace('launch ', '')))
            continue
        elif is_valid_google_search(voice_note):
            print('Searching....')
            play_sound(mp3_google_search_list)
            webbrowser.open('https://www.google.com/search?q={}'.format(voice_note))
            continue
        elif 'thank you friday' in voice_note:
            playsound('mp3/friday/thankyou1.mp3')
            continue
        elif 'bye' in voice_note:
            playsound('mp3/friday/goodbye1.mp3')
            exit()
