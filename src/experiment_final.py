#!/usr/bin/env python
# -*- coding: utf-8 -*-

# %% Import libraries
import psychopy.iohub as io
import numpy as np  # whole numpy lib is available, prepend 'np.'
import os  # handy system and path functions
import sys  # to get file system encoding

#os.add_dll_directory(os.path.join(os.environ['Conda_prefix'],"Lib/site-packages/PyQt5/Qt5/bin"))

from psychopy import prefs, locale_setup, sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.hardware import keyboard
from utils import draw_visual, get_audio, wait_for_click, get_keypress
from cerebus import cbpy

# %% Setup connection to blackrock amplifier
blackrock_ConnectionParameters = cbpy.defaultConParams()
blackrock_ConnectionParameters['client-addr']='192.168.137.3'
cbpy.open(parameter=blackrock_ConnectionParameters)
print("Sending timestamps.....")

# %% Experiment parameters


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

experiment_parameters()

#### Experiment #####

# Start experiment

print("Starting experiment...")

assert NUM_TRIALS % NUM_SOUNDS == 0, "Number of blocks must be a multiple of number of sounds"

for block in range(BLOCK_START, NUM_BLOCKS):

    # image = visual.ImageStim(win, image='images/blank.png')

    # draw_visual(win, image, STIMULUS_DURATION)



    # add stimulus of 3 X 100 Hz tones lasting for 100 ms with 200 ms between them

    # add stimulus of 3 X 100 Hz tones lasting for 100 ms with 200 ms between them
    sync = get_audio(SYNC_DB, SYNC_HZ, SYNC_TIME)
    sync.autoLog = True
    now = core.getTime()
    sync.play(when=now, log=True)
    
    cbpy.set_comment("B" + str(block) + ": sound1")


    sync = get_audio(SYNC_DB, SYNC_HZ, SYNC_TIME)
    sync.autoLog = True
    snow = core.getTime()
    sync.play(when=now+200e-3, log=True)

    sync = get_audio(SYNC_DB, SYNC_HZ, SYNC_TIME)
    sync.autoLog = True
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

    escape = get_keypress(win)
    if not escape:

        block_instruction = visual.TextStim(win,
            text=f"Block {block+1}\n{BLOCK_TEXTS[block]}\nClick to Start"
        )

        wait_for_click(win, block_instruction)

        cbpy.set_comment("B" + str(block) + ": start")
        res, ts = cbpy.time()
        print(int(ts))

        total_time = 0
        current_time = core.getTime()

        for trial in range(TOTAL_TRIALS):

            escape = get_keypress(win)


            PRACTICE = (trial < PRACTICE_TRIALS) # [0, 1, 2]

            if trial == 0:
                wait_for_click(win, test_run_instruction)
            if trial == PRACTICE_TRIALS:
                wait_for_click(win, block_instruction)


            # Fixation
            time_up = np.randint(DELAY_MIN, DELAY_MAX) # Picks pause time between 5 and 10 seconds
            escape = get_keypress(win)
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
            cbpy.set_comment("B" + str(block) + " T " + str(trial) + " P")
            res, ts = cbpy.time()
            print(int(ts))
            core.wait(STIMULUS_DURATION) # Wait for 2 ms

            escape = get_keypress(win)

            total_time += (core.getTime() - current_time)
            current_time = core.getTime()

            if PRACTICE:
                logFile.write("Block %d, Practice Trial %d, Loadness: %d, Pause: %d, Trial Time: %d \n" %(block+1, trial+1, sound_picker, time_up, total_time))
                print("Block %d, Practice Trial %d, Loadness: %d, Pause: %d \n" %(block+1, trial+1, sound_picker, time_up))
            else:
                logFile.write("Block %d, Trial %d, Loadness: %d, Pause: %d, Trial Time: %d \n" %(block+1, trial+1-PRACTICE_TRIALS, sound_picker, time_up, total_time))
                print("Block %d, Trial %d, Loadness: %d, Pause: %d \n" %(block+1, trial+1-PRACTICE_TRIALS, sound_picker, time_up))
            logging.flush()
            escape = get_keypress(win)



    # make sure everything is closed down
    cbpy.close()
    win.close()
    core.quit()