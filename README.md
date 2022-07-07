# StartReact Experiment Design

# Install

Make sure Python3.9 is installed on your computer. Then, run the following:
```

  # setup virtual environment
  python3.9 -m venv ~/envs/psychopy
  source $HOME/envs/psychopy/bin/activate	

  # clone 
  https://github.com/schornb/startreact_experiment.git  

  cd ./startreact_experiment/src
  pip install -r requirements.txt

  # Run trials
  python experiment.py

```

# Data
When starting the experiment, a prompt comes up. You should enter the participants's ID, the number of blocks, 
the number of trials (default to 5 blocks with 15 blocks each respectively), and any other notes.

During the trial, data about each block will be recorded in the data folder for future use. 

