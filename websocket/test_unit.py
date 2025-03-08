from server import send_notification
from app_types import NotificationBody
from datetime import datetime
from vars import NOTIFICAITON_CAT
import asyncio


if __name__ == '__main__':
    asyncio.run(send_notification(NotificationBody(
        user_id="user_id",
        category='category',
        token='token'
    ), {}))