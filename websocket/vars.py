from datetime import timedelta

SERVER_PORT=8083
SERVER_ADDRESS='0.0.0.0'

DATE_TIME_KEY = 'last_t_s'

# Client Globals
SLEEP_TIME_TH_SECONDS = timedelta(seconds=4)
SLEEP_MESSAGE_ALERT = b'SLEEP THREASHHOLD REACHED\n'