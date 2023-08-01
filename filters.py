from aiogram.filters import BaseFilter
from aiogram.types import Message
from database.db import session, UserIdTable
from datetime import datetime

class FilterInDB(BaseFilter):
    async def __call__(self, message: Message) -> bool:

        all_scores = session.query(UserIdTable).all()
        user_ids = [score.user_id for score in all_scores]

        if message.from_user.id in user_ids:
            return False
        else:
            return True
        
class FilterWithTime(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        now = datetime.now()
        user = session.query(UserIdTable).filter(UserIdTable.user_id == message.from_user.id).first()
        if user:
            user_data = user.data_create
            time_difference = datetime.utcnow() - user_data
            total_seconds = time_difference.total_seconds()
            # minutes = total_seconds // 60
            if total_seconds >= 30:
                return True
            else:
                return False
        else:
            return False
