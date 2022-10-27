#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import locale_setup
from psychopy import prefs
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
    'Blocks': 5, 
    'Trials per Block': 15,
    'Other Notes': ''
}

####
# Experiment parameters
ID = expInfo['ID']
NUM_BLOCKS = expInfo['Blocks']
NUM_TRIALS = expInfo['Trials per Block']
####

dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['Date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
fileName = _thisDir + os.sep + u'data/%s.txt' %(expInfo['ID']) 
dataFile = open(fileName, 'w') 
dataFile.write("ID, Experiment Name, Date, Number of Blocks. Number of Trials \n")
dataFile.write("%s, %s, %s, %s, %s" %(expInfo['ID'], expName, expInfo['Date'], NUM_BLOCKS, NUM_TRIALS))
 
logFile = logging.LogFile(fileName+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  

endExpNow = False  # flag for 'escape' or other condition => quit the exp

#### Setup ####

# Window
win = win = visual.Window([800,600], fullscr=False, monitor="testMonitor", units="cm")

# Instruction

INSTRUCTION_TEXT = "To add instruction later!"

instruction = visual.TextStim(win, 
        text=INSTRUCTION_TEXT
    )

# Fixation cross
fixation = visual.ShapeStim(win, 
    vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),
    lineWidth=5,
    closeShape=False,
    lineColor="white"
)

# Stimulus circle
stimulus = visual.Circle(win, 
        radius=5,
        fillColor = 'red',
        lineColor = 'red'
    )

####
# Stimulus Parameters
STIMULUS_DURATION = 1/10 # seconds
####

####
# Sound Parameters 
NUM_SOUNDS = 3
QUIET_DB = 80 # db
QUIET_HZ = 500 # Hz
QUIET_TIME = 2/100 # sec
LOUD_DB = 115 # db
LOUD_HZ = 500 # Hz
LOUD_TIME = 2/100 # sec
SYNC_DB = 115 # db
SYNC_HZ = 100 # Hz
SYNC_TIME = 100e-3 # sec
####

#### Experiment #####

# Instructions 

wait_for_click(win, instruction)

# Start experiment

print("Starting experiment...")

assert NUM_TRIALS % NUM_SOUNDS == 0, "Number of blocks must be a multiple of number of sounds"

for block in range(NUM_BLOCKS):

    # add stimulus of 3 X 100 Hz tones lasting for 100 ms with 200 ms between them
    sync = get_audio(SYNC_DB, SYNC_HZ, SYNC_TIME)
    now = core.getTime()
    sync.play(when=now)

    sync = get_audio(SYNC_DB, SYNC_HZ, SYNC_TIME)
    snow = core.getTime()
    sync.play(when=now+200e-3)

    sync = get_audio(SYNC_DB, SYNC_HZ, SYNC_TIME)
    now = core.getTime()
    sync.play(when=now+200e-3)

    # Set sound
    sounds = np.tile(np.arange(NUM_SOUNDS), int(NUM_TRIALS/NUM_SOUNDS))
    np.random.shuffle(sounds)

    # Click to start block
    block_text = visual.TextStim(win, 
        text="Block %d\nClick to Start" %(block+1)
    )

    wait_for_click(win, block_text)

    for trial in range(NUM_TRIALS):

        
        # Fixation
        time_up = randint(5, 10) # Picks pause time between 5 and 10 seconds
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
            sound_used.play(when=nextFlip)

        win.flip()
        core.wait(STIMULUS_DURATION) # Wait for 2 ms

        logFile.write("Block %d, Trial %d, Loadness: %d, Pause: %d" %(block+1, trial+1, sound_picker, time_up))
        print("Block %d, Trial %d, Loadness: %d, Pause: %d" %(block+1, trial+1, sound_picker, time_up))




logging.flush()

# make sure everything is closed down
win.close()
core.quit()