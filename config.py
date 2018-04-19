import os

# BASE PATH /
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
# BASE PATH/DATA
DATA_PATH = os.path.join(BASE_PATH, 'Data')
# BASE PATH/LOGS
LOGS_PATH = os.path.join(BASE_PATH, 'Logs')

if not os.path.exists(os.path.join(BASE_PATH, 'Logs')):
    os.mkdir(os.path.join(BASE_PATH, 'Logs'))

if not os.path.exists(os.path.join(BASE_PATH, 'Data')):
    os.mkdir(os.path.join(BASE_PATH, 'Data'))

FILE_LIST = os.listdir(DATA_PATH)


