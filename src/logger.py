import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# combines the current working directory (os.getcwd()), the "logs" folder name, and the LOG_FILE variable. This will give you the complete path to the log file, including the folder structure.
logs_path = os.path.join(os.getcwd(),"logs",LOG_FILE)

# This line creates the directory structure specified by the logs_path . exist_ok=True argument ensures that the directory is created only if it doesn't already exist. If the directory already exists, it will not raise an error.
os.makedirs(logs_path,exist_ok=True)

# to create the complete path to the log file, including the filename.
LOG_FILE_PATH = os.path.join(logs_path,LOG_FILE)


logging.basicConfig(
    filename=LOG_FILE_PATH,
    ## The format in which the Logging information would be printed and log files would be Created:
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# if __name__ == "__main__":
#     logging.info("This is a test message")