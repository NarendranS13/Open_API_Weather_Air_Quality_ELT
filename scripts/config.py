import os

### Extract the current directory
Scripts_folder = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(Scripts_folder)

### Setup the project logs directory
LOG_DIR = os.path.join(parent_dir, "logs","project_logs")


### Create the Data Dir to save extracted Data.
DATA_DIR = os.path.join(parent_dir,"Data")