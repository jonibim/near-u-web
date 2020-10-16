from threading import Thread
import RPi.GPIO as GPIO
import simpleaudio as sa
import pyaudio
import sounddevice as sd
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play as pplay
import wave
import json as js
import time
import os


GPIO.setmode(GPIO.BCM)
GPIO_PIR = 8
GPIO.setup(GPIO_PIR, GPIO.IN)
PATH_FOLDER = './near_u'

# Check if the file exists


global run
run = True


def check_existence():
    if (os.path.isfile(PATH_FOLDER + '/initial')):
        os.remove(PATH_FOLDER + "/initial")
    if not (os.path.isfile(PATH_FOLDER + '/current')):
        f = open(PATH_FOLDER + "/current", "w")
        f.write("")
        f.close()

def pre_start():
    f = open("./near_u/initial", "w")
    f.write("")
    f.close()

def running():
    f = open("./near_u/running", "w")
    f.write("")
    f.close()

def reset():
    f = open(PATH_FOLDER + "/current", "w")
    f.write("")
    f.close()
    
def writeJSONandExecute(json):
    running()
    with open(PATH_FOLDER + '/current', 'w') as outfile:
        json_object = js.dumps(json, indent=4)
        outfile.write(json_object)
    decider(json)


def readJSONandExectute():
    with open(PATH_FOLDER + '/current', 'w') as json_file:
        data = js.load(json_file)


def readJSON():
    with open(PATH_FOLDER + '/current', 'w') as json_file:
        data = js.load(json_file)
    return data


def decider(json):
    message = json['title']
    repeat = json['repeat']
    print("started")
    if json['c_type'] == 1:
        #print('yes')
        run = True
        zero_to_one(message,repeat)
        #zero_to_one(json['title'], json['repeat'])
    elif json['c_type'] == 0:
        #print('no')
        run = True
        one_to_zero(message,repeat)
        # reset()
        #zero_to_one(json['title'], json['repeat'])


def one_to_zero(msg, iterations):
    tolerance = 100
    if iterations > 0:
        while (os.path.isfile(PATH_FOLDER + '/running')) and iterations > 0:
            if GPIO.input(GPIO_PIR) == 0:
                tolerance -= 1
            if tolerance == 0:
                play(msg)
                iterations -= 1
                tolerance = 100
    else:
        while (os.path.isfile(PATH_FOLDER + '/running')):
            if GPIO.input(GPIO_PIR) == 0:
                tolerance -= 1
            if tolerance < 0:
                play(msg)
                print('play')
                tolerance = 100
    reset()
    print('stopped')


def zero_to_one(msg, iterations):
    tolerance = 100
    if iterations > 0:
        while (os.path.isfile(PATH_FOLDER + '/running')) and iterations > 0:
            if GPIO.input(GPIO_PIR) == 1:
                tolerance -= 1
            if tolerance < 0:
                play(msg)
                iterations -= 1
                tolerance = 100
    else:
        while (os.path.isfile(PATH_FOLDER + '/running')):
            #print(GPIO.input(GPIO_PIR))
            if GPIO.input(GPIO_PIR) == 1:
                tolerance -= 1
            if tolerance < 0:
                print('play')
                play(msg)
                tolerance = 100
    reset()
    print('stopped')


def play(msg):
    filename = './recordings/'+msg +'.mp3'
    f = open(PATH_FOLDER + "/playing", "w")
    f.write("")
    f.close()  

    # Extract data and sampling rate from file
    # data, fs = sf.read(filename, dtype='float32')  
    # sd.play(data, fs)
    # status = sd.wait()  # Wait until file is done playing

    sound = AudioSegment.from_mp3(filename)
    pplay(sound)

    # convert wav to mp3                                                            
    # wave_obj = sa.WaveObject.from_wave_file(filename)
    # play_obj = wave_obj.play()
    # play_obj.wait_done()  # Wait until sound has finished playing
    os.remove(PATH_FOLDER + "/playing")
