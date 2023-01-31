prefs.hardware['audioLib'] = ['PTB']

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2021.2.3'
expName = 'StartReact Experiment' 
expInfo = {
    'ID': '',
    'Blocks': 5, # 5 plus practice 
    'Trials per Block': 30,
    'Block Start (Please only input 1, 2, 3, 4, or 5)': 1, #1-5
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
BLOCK_START = expInfo['Block Start (Please only input 1, 2, 3, 4, or 5)']-1
####
expInfo['Date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
fileName = _thisDir + os.sep + u'data/%s.txt' %(expInfo['ID']) 
dataFile = open(fileName, 'w') 
dataFile.write("ID, Experiment Name, Date, Number of Blocks. Number of Trials \n")
dataFile.write("%s, %s, %s, %s, %s" %(expInfo['ID'], expName, expInfo['Date'], NUM_BLOCKS, NUM_TRIALS))
 
logFile = logging.LogFile(fileName+'.log', level=logging.WARN)
 

endExpNow = False  # flag for 'escape' or other condition => quit the exp

#### Setup ####

# Window
win = visual.Window([800,600], fullscr=True, monitor="testMonitor", units="cm") # Check for escape with full screen

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
        fillColor = 'white',
        lineColor = 'white',
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