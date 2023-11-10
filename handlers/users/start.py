from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import CHANNELS
from keyboards.inline.inline_keyboards import check_button_subs
from loader import dp, db, bot
from utils.misc.check_subs import check


@dp.message_handler(commands=['start'], state='*')
async def show_channels(message: types.Message):
    id = message.from_user.id
    fullname = message.from_user.full_name
    try:
        db.add_user(id=id, name=fullname)
        db.add_active_user(id=id, name=fullname)
    except:
        pass
    if message.text == '/start':
        channels_format = str()
        for channel in CHANNELS:
            chat = await bot.get_chat(channel)
            invite_link = await chat.export_invite_link()
            channels_format += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"

        await message.answer(f"Quyidagi kanallarga obuna bo'ling: \n"
                             f"{channels_format}",
                             reply_markup=check_button_subs,
                             disable_web_page_preview=True)
    try:
        if len(message.text) > 6 and message.text[-11:-1] == "SoftFileBo":
            join = InlineKeyboardMarkup()
            status = False
            result = str()
            for ch in CHANNELS:
                status = await check(user_id=message.from_user.id, channel=ch)
                if status:
                    result += f"<b>{ch.title}</b> kanaliga obuna bo'lgansiz!\n\n"
                else:
                    chinfo = await bot.get_chat(ch)
                    invite_link = await chinfo.export_invite_link()
                    join.add(InlineKeyboardButton(text=chinfo.title, url=invite_link))
                    join.add(InlineKeyboardButton(text="Tekshirish ✅",
                                                  url=f"https://t.me/SoftFileBot?start={message.text[7:-9]}-SoftFileBot"))
                    await message.answer("<b>Davom etish uchun ushbu kanal(larga) kanallarga obuna bo'ling!</b>",
                                         reply_markup=join)
            if status:
                filename = message.text[7:-12]
                print(filename)
                get_file_id = db.select_file_id(file_name=filename)[1]

                get_file_name = db.select_file_id(file_name=filename)[2]
                description = db.select_file_id(file_name=filename)[3]
                try:
                    await message.answer_document(document=get_file_id,
                                                  caption=f"FIle nomi - {get_file_name}\n\n{description}")
                except:
                    try:
                        await message.answer_photo(photo=get_file_id,
                                                   caption=f"FIle nomi - {get_file_name}\n\n{description}")
                    except:
                        await message.answer_audio(audio=get_file_id,
                                                   caption=f"FIle nomi - {get_file_name}\n\n{description}")
            else:
                await message.answer(result, reply_markup=join)
    except:
        await message.answer('Bu file topilmadi.\n Qaytadan urnib ko\'ring !!!')


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = str()
    for channel in CHANNELS:
        status = await check(user_id=call.from_user.id,
                             channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            result += f"<b>{channel.title}</b> kanaliga obuna bo'lgansiz!\n\n"
        else:
            invite_link = await channel.export_invite_link()
            result += (f"<b>{channel.title}</b> kanaliga obuna bo'lmagansiz. "
                       f"<a href='{invite_link}'>Obuna bo'ling</a>\n\n")

    await call.message.answer(result, disable_web_page_preview=True)
