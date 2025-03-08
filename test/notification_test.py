import datetime
import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from websocket.app_types import NotificationBody
from websocket.server import send_notification

NOTIFICAITON_CAT='category'

SERVER_ADDRESS='0.0.0.0' # broadcat no need to worry about it!

NOTIFICATION_SERVICE_PORT=5050
NOTIFICATION_SERVICE_ADDRESS='localhost'
SEND_NOTIFICATION_KEY='send_notification'

print(sys.path)
if __name__ == '__main__':
    requestBody = NotificationBody("alert_mental", 'user', 'userid')
    asyncio.run(
        send_notification(requestBody, {SEND_NOTIFICATION_KEY: datetime.datetime.now() - datetime.timedelta(seconds=10)})
    )