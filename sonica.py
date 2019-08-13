from functools import wraps
import errno
import sys
import importlib
import os
sys.path.insert(1, './snowboy')
import snowboydecoder
import pyaudio
import signal
import vlc
import numpy
import datetime
import pyttsx3
from contextlib import contextmanager
pause_on_time = True
interrupted = False
engine = pyttsx3.init()

engine.setProperty('volume',1.55)
engine.setProperty('rate', 155)

command_sensitivity=0.5
hotword_sensitivity=0.6

station1 = vlc.MediaPlayer("https://wosu.streamguys1.com/Classical_128")
#station1.audio_set_volume(80)

#station1 = vlc.MediaPlayer("https://listen.moe/stream")
#station1.audio_set_volume(121)

station2 = vlc.MediaPlayer("https://ice10.securenetsystems.net/WQIO?type=.mp3")
#station2.audio_set_volume(121)

global s_one_playing
global s_two_playing

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

class TimeoutError(Exception):
    pass

def timeout(seconds):
    def decorator(func):
        def _handle_timeout(signum, frame):
            state_sleep()

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

def station(n):
    
    #global station

    if n == 1:
        s_two_playing = False
        station2.stop()

        s_one_playing = True
        station1.play()
        

    elif n == 2:
        s_one_playing = False
        station1.stop()
        

        s_two_playing = True
        station2.play()
        
    elif n == 0:
        station1.stop()
        station2.stop()
        s_one_playing = False
        s_two_playing = False

    elif n == None:
        stop_station(n)

    state_sleep()

def time():
    if 's_one_playing' in globals():
        if s_one_playing == True:
            print('Stopping station 2')
            s_one_playing = False
            station1.stop()
    if 's_two_playing' in globals():
        if s_two_playing == False:
            print('Stopping station 2')
            s_two_playing = False
            station2.stop()

    now = datetime.datetime.now()
    #d = datetime.strptime("10:30", "%H:%M")
    time = datetime.time(now.hour, now.minute)
    time = time.strftime("%I:%M %p")
    #print(time)
    engine.say(time)
    engine.runAndWait() 

    if 's_one_playing' in globals():
        if s_one_playing == False:
            print('Playing station 1')
            s_one_playing = True
            station1.play()
    if 's_two_playing' in globals():
        if s_two_playing == False:
            print('Playing station 2')
            s_two_playing = True
            station2.play()

    state_sleep()

def reload():
    python = sys.executable
    os.execl(python, python, * sys.argv)

callbacks = [lambda: station(1),
                 lambda: station(2),
                 lambda: station(0),
                 lambda: state_sleep(),
                 lambda: time(),
                 lambda: reload()]
models = ['Station 1.pmdl','Station 2.pmdl', 'pause_en.pmdl', 'sleep.pmdl', 'Time.pmdl', 'reload.pmdl']
command_detector = snowboydecoder.HotwordDetector(models, sensitivity=command_sensitivity)

#@timeout(5)
def state_menu():
    print('MENU')
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
    menu = True
    
    #models = ['Station 1.pmdl','Station 2.pmdl', 'pause_en.pmdl', 'sleep.pmdl', 'Time.pmdl']

    #command_detector = snowboydecoder.HotwordDetector(models, sensitivity=command_sensitivity)
    #snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
    command_detector.start(detected_callback=callbacks, interrupt_check=interrupt_callback, sleep_time=0.03)
    #time = time.time()
    



def state_sleep():
    print('')
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)
    
    model = 'Hey Sonica.pmdl'
    signal.signal(signal.SIGINT, signal_handler)

    detector = snowboydecoder.HotwordDetector(model, sensitivity=hotword_sensitivity)
    detector.start(detected_callback=state_menu, interrupt_check=interrupt_callback, sleep_time=0.03)
    detector.terminate()
menu = False
state_sleep()
