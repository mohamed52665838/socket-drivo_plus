from datetime import timedelta
from dotenv import load_dotenv
import os
load_dotenv()

SERVER_PORT=os.getenv("WS_PORT")
OUR_KEY=os.getenv("OUR_KEY")

sleep_time_alert = os.getenv('SLEEP_TIME_ALERT') 
no_face_time_alert = os.getenv('NF_TIME_ALERT')
application_port = os.getenv('APP_PORT')
notification_service_port = os.getenv('NOTIFICATION_SERVICE_PORT')
variable_confidential = os.getenv('CONF_VAR')

SLEEP_THREASHOLD= int(sleep_time_alert) if sleep_time_alert is not None else 3
NO_FACE_THREASHOLD= int(no_face_time_alert) if no_face_time_alert is not None else 10
APP_PORT=int(application_port) if application_port is not None else 5643
NOTIFICATION_SERVICE_PORT=int(notification_service_port) if notification_service_port is not None else 80
VAR_CONF= float(variable_confidential) if variable_confidential is not None else 0.25 # var must be between 0.2 and 0.35


NO_FACE_ALERT='NO_FACE_LONG_TIME'
SEND_NOTIFICATION_KEY='send_notification'

NOTIFICAITON_CAT='category'
SERVER_ADDRESS='0.0.0.0' # broadcat no need to worry about it!
NOTIFICATION_SERVICE_ADDRESS='web' # name of service

DATE_TIME_KEY = 'last_t_s'
NO_FACE_KEY = 'no_face_key'

# Client Globals
SLEEP_TIME_TH_SECONDS = timedelta(seconds=4)
SLEEP_MESSAGE_ALERT = b'SLEEP THREASHHOLD REACHED\n'