# StartReact Experiment Design

# Install

Make sure latest version of anaconda is installed on your computer (have been unable to get cerebus library reliably installed without it)
``

conda create -n startreact python=3.8
conda activate startreact
conda install cython pyqt
conda numpy scipy matplotlib
conda install numpy scipy matplotlib
pip install https://github.com/CerebusOSS/CereLink/releases/download/v7.0.5/cerebus-0.0.4-cp38-cp38-win_amd64.whl
pip install psychopy

Run from visual studio code using startreact environment


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

