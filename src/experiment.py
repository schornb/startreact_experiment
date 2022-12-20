#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pickle import TRUE
from psychopy import locale_setup
from psychopy import prefs

prefs.hardware['audioLib'] = ['PTB']
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy.random import randint
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

from utils import draw_visual, get_audio, wait_for_click


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2022.1.4'
expName = 'StartReact Experiment' 
expInfo = {
    'ID': '',
    'Blocks': 5, # 5 plus practice 
    'Trials per Block': 30,
    'Block Start': 0, #0-4
    # ^ pick what trial you want to start at if you need to restart the experiment
    # check 
    'Other Notes': '',
}

# https://psychopy.org/api/gui.html
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel

####
# Experiment parameters
ID = expInfo['ID']
NUM_BLOCKS = expInfo['Blocks']
NUM_TRIALS = expInfo['Trials per Block']
PRACTICE_TRIALS = 3
TOTAL_TRIALS = NUM_TRIALS + PRACTICE_TRIALS
DELAY_MIN = 7 # seconds
DELAY_MAX = 12 # seconds
BLOCK_START = expInfo['Block Start']
####
expInfo['Date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
fileName = _thisDir + os.sep + u'data/%s.txt' %(expInfo['ID']) 
dataFile = open(fileName, 'w') 
dataFile.write("ID, Experiment Name, Date, Number of Blocks. Number of Trials \n")
dataFile.write("%s, %s, %s, %s, %s" %(expInfo['ID'], expName, expInfo['Date'], NUM_BLOCKS, NUM_TRIALS))
 
logFile = logging.LogFile(fileName+'.log', level=0)
 

endExpNow = False  # flag for 'escape' or other condition => quit the exp

#### Setup ####

# Window
win = visual.Window([800,600], fullscr=False, monitor="testMonitor", units="cm") # Check for escape with full screen

# Instruction

TEST_RUN_TEXT = "TEST RUN"

BLOCK_TEXTS = np.array(["Raise your arm to the side", "Bend your elbow", "Extend your elbow", "Lift your wrist", "Move your index finger towards your thumb"])

# Have different instructions per block
# Prepare to raise your arm to the side as fast as you can

# Fixation cross
fixation = visual.ShapeStim(win, 
    vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),
    lineWidth=5,
    closeShape=False,
    lineColor="white",
    autoLog=True
)

# Stimulus circle
stimulus = visual.Circle(win, 
        radius=7,
        fillColor = 'red',
        lineColor = 'red',
        autoLog=True
    )

####
# Stimulus Parameters
STIMULUS_DURATION = 1/20 # seconds
####

####
# Sound Parameters 
NUM_SOUNDS = 3
QUIET_DB = 80 # db
QUIET_HZ = 500 # Hz
QUIET_TIME = 1/20 # sec
LOUD_DB = 120 # db
LOUD_HZ = 500 # Hz
LOUD_TIME = 1/20 # sec
SYNC_DB = 80 # db
SYNC_HZ = 500 # Hz
SYNC_TIME = 100e-3 # sec
####

#### Experiment #####

# Start experiment

print("Starting experiment...")

assert NUM_TRIALS % NUM_SOUNDS == 0, "Number of blocks must be a multiple of number of sounds"

for block in range(BLOCK_START, NUM_BLOCKS):

    # image = visual.ImageStim(win, image='images/blank.png')

    # draw_visual(win, image, STIMULUS_DURATION)



    # add stimulus of 3 X 100 Hz tones lasting for 100 ms with 200 ms between them
   
    sync = get_audio(SYNC_DB, SYNC_HZ, SYNC_TIME)
    sync.autoLog = True
    now = core.getTime()
    sync.play(when=now, log=True)
    
    sync = get_audio(SYNC_DB, SYNC_HZ, SYNC_TIME)
    sync.autoLog = TRUE
    snow = core.getTime()
    sync.play(when=now+200e-3, log=True)

    sync = get_audio(SYNC_DB, SYNC_HZ, SYNC_TIME)
    sync.autoLog = TRUE
    now = core.getTime()
    sync.play(when=now+200e-3, log=True)

    # Set sound

    # First trial is practice, so order is set

    test_run_instruction = visual.TextStim(win,
        text=TEST_RUN_TEXT
    )

    sounds = np.zeros(NUM_TRIALS+PRACTICE_TRIALS, dtype=int)
    sounds_random = np.tile(np.arange(NUM_SOUNDS), int(NUM_TRIALS/NUM_SOUNDS))
    np.random.shuffle(sounds_random)
    sounds[0:PRACTICE_TRIALS] = [0, 1, 2]
    sounds[PRACTICE_TRIALS:] = sounds_random

    # Click to start block

    # Add practice trial (one of each sound)

    block_instruction = visual.TextStim(win,
        text=f"Block {block+1}\n{BLOCK_TEXTS[block]}\nClick to Start"
    )

    wait_for_click(win, block_instruction)

    total_time = 0
    current_time = core.getTime()

    for trial in range(TOTAL_TRIALS):

        PRACTICE = (trial < PRACTICE_TRIALS) # [0, 1, 2]
        
        if trial == 0:
            wait_for_click(win, test_run_instruction)
        if trial == PRACTICE_TRIALS:
            wait_for_click(win, block_instruction)


        # Fixation
        time_up = randint(DELAY_MIN, DELAY_MAX) # Picks pause time between 5 and 10 seconds
        draw_visual(win, fixation, time_up)

        # Stimulus
        sound_picker = sounds[trial]
        sound_used = { 
            0: None, # no audio
            1: get_audio(amp=QUIET_DB, freq=QUIET_HZ, time=QUIET_TIME), # quiet audio
            2: get_audio(amp=LOUD_DB, freq=LOUD_HZ, time=LOUD_TIME) # startling_audio 
        }[sound_picker]

        stimulus.draw()

        if sound_used != None:
            nextFlip = win.getFutureFlipTime(clock='ptb')
            sound_used.play(when=nextFlip, log=True)

        win.logOnFlip("stimPresented",10)
        win.flip()
        core.wait(STIMULUS_DURATION) # Wait for 2 ms

        total_time += (core.getTime() - current_time)
        current_time = core.getTime()

        if PRACTICE:
            logFile.write("Block %d, Practice Trial %d, Loadness: %d, Pause: %d, Trial Time: %d \n" %(block+1, trial+1, sound_picker, time_up, total_time))
            print("Block %d, Practice Trial %d, Loadness: %d, Pause: %d \n" %(block+1, trial+1, sound_picker, time_up))
        else:
            logFile.write("Block %d, Trial %d, Loadness: %d, Pause: %d, Trial Time: %d \n" %(block+1, trial+1-PRACTICE_TRIALS, sound_picker, time_up, total_time))
            print("Block %d, Trial %d, Loadness: %d, Pause: %d \n" %(block+1, trial+1-PRACTICE_TRIALS, sound_picker, time_up))
        logging.flush()



# make sure everything is closed down
win.close()
core.quit()