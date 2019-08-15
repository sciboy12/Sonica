import sys
import os
# Enables importing snowboydecoder from subdir
sys.path.insert(1, './snowboy')
import snowboydecoder
import pyaudio
import vlc
import datetime
import pyttsx3

# Init pyttsx3
engine = pyttsx3.init()

# Config
# speech volume and rate
engine.setProperty('volume',2)
engine.setProperty('rate', 157)

# Sensitivity for all menu commands
command_sensitivity=0.4

# Hotword1 sensitivity
hotword_sensitivity=0.43

# Normal playback volume
vol = 100

# Playback volume when in menu/speaking time
vol_low = 70

# Station stream URLs
# Any station/file that works with VLC should work here
url1 = "https://listen.moe/opus"
url2 = "https://ice10.securenetsystems.net/WQIO?type=.mp3"
url3 = "https://wosu.streamguys1.com/Classical_128"

# Enables reload command
debug = True
# Config end


#define VLC instance
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

#Define VLC player
player=instance.media_player_new()

# Init VLC with url1 as a placeholder
media=instance.media_new(url1)
player.set_media(media)

# Placeholders
global station_n
station_n = 0
interrupted = False

def interrupt_callback():
    global interrupted
    return interrupted

# Play/pause internet radio stations using VLC
def station(n):

    # Play station 1
    if n == 1:
        station_n = 1
        media = instance.media_new(url1)
        player.set_media(media)
        player.play()

    # Play station 2
    elif n == 2:
        station_n = 2
        media = instance.media_new(url2)
        player.set_media(media)
        player.play()

    # Play station 3
    elif n == 3:
        station_n = 3
        media = instance.media_new(url3)
        player.set_media(media)
        player.play()

    # Stop playback
    elif n == 0:
        player.stop()

    state_sleep()
# Speaks the current time in 12-hour format
def time():
    now = datetime.datetime.now()
    time = datetime.time(now.hour, now.minute)

    # swap these lines for 24-hour time
    time = time.strftime("%I:%M %p")
    #time = time.strftime("%H:%M %p")

    engine.say(time)
    engine.runAndWait()
    state_sleep()

# Restarts the script with any saved changes to sonica.py taking effect
def reload():
    python = sys.executable
    os.execl(python, python, * sys.argv)

if debug == True:
    # Filenames for models
    models = ['Station 1.pmdl','Station 2.pmdl', 'Station 3.pmdl', 'pause_en.pmdl', 'sleep.pmdl', 'Time.pmdl', 'reload.pmdl']
    # Commands to execute
    callbacks = [lambda: station(1),
                     lambda: station(2),
                     lambda: station(3),
                     lambda: station(0),
                     lambda: state_sleep(),
                     lambda: time(),
                     lambda: reload()]
else:
    # Filenames for models
    models = ['Station 1.pmdl','Station 2.pmdl', 'Station 3.pmdl', 'pause_en.pmdl', 'sleep.pmdl', 'Time.pmdl']
    # Commands to execute
    callbacks = [lambda: station(1),
                     lambda: station(2),
                     lambda: station(3),
                     lambda: station(0),
                     lambda: state_sleep(),
                     lambda: time()]

# Model filename
model = 'Hey Sonica.pmdl'

command_detector = snowboydecoder.HotwordDetector(models, sensitivity=command_sensitivity)
detector = snowboydecoder.HotwordDetector(model, sensitivity=hotword_sensitivity)

def state_menu():
    print('MENU')

    # Reduce volume
    player.audio_set_volume(vol_low)

    # Play menu tone
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)

    # Start detection for commands
    command_detector.start(detected_callback=callbacks, interrupt_check=interrupt_callback, sleep_time=0.03)

    # Stop detection
    detector.terminate()

def state_sleep():
    print('SLEEP')

    # Restore volume to normal
    player.audio_set_volume(vol)

    # Play sleep tone
    snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)

    # Start detection for hotword
    detector.start(detected_callback=state_menu, interrupt_check=interrupt_callback, sleep_time=0.03)

    # Stop detection
    detector.terminate()

state_sleep()
