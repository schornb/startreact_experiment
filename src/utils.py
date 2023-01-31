
from psychopy import prefs
prefs.hardware['audioLib'] = ['PTB']
prefs.hardware['audioLatencyMode'] = 3

from psychopy import visual, core, sound, event, logging


import numpy as np
from cerebus import cbpy

def wait_for_click(win, visual):
    """
    Waits for a keypress to be pressed

    :param win: window projected on monitor
    :param visual: visual to be displayed
    :returns: key pressed
    """
    click = None
    while click == None:
        visual.draw()
        win.flip()
        click = event.waitKeys()
    if click[0] == 'Esc':
        win.close()
        core.quit()
    return click

def draw_visual(window, visual, time):
    """
    Draws a visual image onto the window

    :param window: window projected on monitor
    :param visual: visual to be displayed
    :param time: time visual is displayed (s)
    :returns: shows visual on window
    """
    
    visual.draw()
    window.flip()
    core.wait(time)

def convert_db_to_vol(this_vol):
    """
    Returns the volume value of a dB

    :param this_vol: the volume value (in dB)
    :returns: the volume value as a float between 0 and 1
    """
    return ((0.34/0.1)/(10**(111.8/20)))*(10**(this_vol/20))

def get_audio(amp, freq, time):
    """
    Returns a sound object given the amplitude, frequency, and time
    
    :param amp: Amplitude value (in dB)
    :param freq: Frequency value (in Hz)
    :param time: Time value (in s)
    :returns: sound object in Psychopy
    """
    return sound.Sound(value=freq, secs=time, hamming=False, volume=convert_db_to_vol(amp), preBuffer=-1, syncToWin=True, autoLog=True)

def get_keypress(win):
    keys = event.getKeys()
    if keys and keys[0] == 'Esc':
        win.close()
        core.quit()
    else: 
        return False

def presentBlock(win, blockText, blockLog):
    escape = get_keypress(win)
    if not escape:

        block_instruction = visual.TextStim(win,blockText)

        #text=f"Block {block+1}\n{expInfo['BLOCK_TEXTS'][block]}\nPress any key to Start"
        
        wait_for_click(win, block_instruction)

        cbpy.set_comment(blockLog + ": start")


def presentTrials(win, expInfo, stimParams, blockText, logFile, numTrials, soundStrengths, fixation, stimulus):

        total_time = 0
        current_time = core.getTime()
        for trial in range(numTrials):
            # Fixation
            time_up = np.random.uniform(expInfo['DELAY_MIN'], expInfo['DELAY_MAX'] ) # Picks pause time between delay_min and delay_max seconds
            draw_visual(win, fixation, time_up)
 
            # Stimulus
            sound_picker = soundStrengths[trial]            
            sound_used = stimParams['sound_used'][sound_picker]              
            if sound_used != None:
                nextFlip = win.getFutureFlipTime(clock='now')
                print(str(nextFlip))
                sound_used.play(when=0, log=True)

            stimulus.draw()
            
           

            win.logOnFlip("stimPresented",10)
            win.flip()
            
            cbpy.set_comment(blockText + " T " + str(trial) + " P" + str(soundStrengths[trial]))
            core.wait(stimParams['STIMULUS_DURATION'])

            logFile.write(blockText + " Trial %d, Loudness: %d, Pause: %.3f, Trial Time: %.3f \n" %(trial+1, sound_picker, time_up, core.getTime()))
            print(blockText +         " Trial %d, Loudness: %d, Pause: %.3f, Trial Time: %.3f \n" %(trial+1, sound_picker, time_up, core.getTime()))
            
            logging.flush()

