import asyncio # модуль для асин. программирования
from aiogram import Router, types, Bot, Dispatcher, F # первый это вместо диспетчера, второй для типа я не знаю как он работает но он помогает обращаться к айди пользователя и тд, бот это обращение к апи, диспетчер щас не знаю как работает
from aiogram.filters import Command # команды
from config import TOKEN # токен
from buttons import lesson_button # кнопки
import logging # логер изменений ошибок и тд
from database import session, UserIdTable, UserState
from filters import FilterInDB, FilterWithTime
from aiogram.fsm.context import FSMContext
from text_task import *
from datetime import datetime

router = Router()


@router.message(FilterWithTime())
async def other(message: types.Message):
    await message.answer("Ты истратил время донать")

@router.message(
    FilterInDB(),
    Command('start'),
)
async def start_bot(message: types.Message, state: FSMContext):
    await state.set_state(UserState.TaskFirst)
    await message.answer(text="какой нибудь стартовый текст", reply_markup=lesson_button)
    new_user_id = UserIdTable(user_id=message.from_user.id)
    session.add(new_user_id)
    session.commit()

@router.callback_query(UserState.TaskFirst, F.data == "introductory_lesson")  
async def text_lesson_1(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Текст для урока 1")
    await state.set_state(UserState.TaskFirstLesson)

@router.callback_query(UserState.TaskFirstLesson, F.data == "task_lesson")  
async def task_lesson_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.TaskFirstAnswer)
    await callback.message.answer("Вы должны будете скопировать текст ниже и вставить в начало ответа, иначе ответ не будет принят. У вас 24 часа чтобы решить его")
    await callback.message.answer("какой то сложный текст который кто то должен копировать")
    

@router.message(UserState.TaskFirstAnswer)
async def answer_task_1(message: types.Message, state: FSMContext):
    text = message.text    
    if text.find(text_for_task_1) != -1:
        user = session.query(UserIdTable).filter(UserIdTable.user_id == message.from_user.id).first()
        user.date_create = datetime.utcnow
        await message.answer("ответ принят")
        state.update_data(TaskFirstAnswer=text)
    else:
        await message.answer("неправильная форма ответа")

async def main():

    dp = Dispatcher()
    dp.include_router(router)
    bot = Bot(TOKEN, parse_mode="HTML")

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    asyncio.run(main())