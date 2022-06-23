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

from utils import draw_visual, get_audio


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2022.1.4'
expName = 'StartReact Experiment' 
expInfo = {
    'ID': '',
    'Session': '',
    'Blocks': 15, 
    'Trials': 5,
    'Condition': '',
    'Other Notes': ''
}

dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['Date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
fileName = _thisDir + os.sep + u'data/%s.txt' %(expInfo['Session']) 
dataFile = open(fileName, 'w') 
dataFile.write("ID, Experiment Name, Date, Number of Blocks. Number of Trials \n")
dataFile.write("%s, %s, %s, %s, %s" %(expInfo['ID'], expName, expInfo['Date'], expInfo['Blocks'], expInfo['Trials']))

 
logFile = logging.LogFile(fileName+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  

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
# Quiet Audio Constants
QUIET_DB = 80 # db
QUIET_HZ = 500 # Hz
QUIET_TIME = 2/100 # sec
####
quiet_audio = get_audio(amp=QUIET_DB, freq=QUIET_HZ, time=QUIET_TIME)

####
# Startling Audio Constants
LOUD_DB = 115 # db
LOUD_HZ = 500 # Hz
LOUD_TIME = 2/100 # sec
####
startling_audio = get_audio(amp=LOUD_DB, freq=LOUD_HZ, time=LOUD_TIME)

####
# Experiment parameters
NUM_BLOCKS = expInfo['Blocks']
NUM_TRIALS = expInfo['Trials']
####

#### Experiment #####

# Instructions 

click = None
while click == None:
    instruction.draw()
    win.flip()
    c = event.waitKeys(1.0)


# Start experiment

print("Starting session %d", expInfo['Session'])

block = 1
for i in range(NUM_BLOCKS):
    trial = 1
    for j in range(NUM_TRIALS):
        # Fixation
        time_up = randint(5, 10) # Picks pause time between 5 and 10 seconds
        draw_visual(win, fixation, time_up)

        # Stimulus
        sound_picker = randint(0, 2) # Random pick between 0 and 2
        sound_used = { 
            0: None, # no audio
            1: quiet_audio, 
            2: startling_audio 
        }[sound_picker]

        stimulus.draw()

        if sound_used != None:
            sound_used.play()

        win.flip()
        core.wait(2/100) # Wait for 2 ms

        print("Block %d, Trial %d" %(block, trial))
        block += 1
        trial += 1


logging.flush()

# make sure everything is closed down
win.close()
core.quit()