import os
import time
import zipfile

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, ContentTypes
from aiogram.utils.exceptions import BotBlocked, UserDeactivated, ChatNotFound

from data.config import ADMINS, CHANNELS
from keyboards.default.keyboards import adminpanelbtn, agree, cencelbtn
from keyboards.inline.inline_keyboards import typepost, keyboard_admin_obuna
from loader import dp, bot, db
from states.states import Reklam_State, Matn_state, FeedbackTo, Qoshish, KanalQoshish, KanalOlish

sendfeedback = []
ADMINS = [int(x) for x in ADMINS]


@dp.message_handler(commands='admin')
async def adminpanel(message: types.Message):
    if message.chat.id in ADMINS:
        await message.answer("<b>Admin panel</b>", reply_markup=adminpanelbtn, parse_mode="HTML")


@dp.message_handler(commands=["admins"])
async def adminlar(message: types.Message):
    if message.chat.id == ADMINS[0]:
        await message.answer(f"{ADMINS}")


@dp.message_handler(commands="addadmin")
async def adminadd(message: types.Message):
    if message.chat.id in ADMINS:
        newadmin = message.get_args()
        ADMINS.append(int(newadmin))
        await message.answer("Admin qo'shildi!")


@dp.message_handler(commands="removeadmin")
async def adminadd(message: types.Message):
    if message.chat.id in ADMINS:
        radmin = message.get_args()
        try:
            ADMINS.remove(int(radmin))
            await message.answer("Admin olib tashlandi!")
        except:
            await message.answer(f"{radmin} adminlar ro'yxatida yo'q!")


@dp.message_handler(text="📊 Statistika")
async def adminpanel(message: types.Message):
    count = db.count_users()[0]
    if message.chat.id in ADMINS:
        await message.answer(f"👥 <b>Bot obunachilari:</b> {count}", parse_mode="HTML")


@dp.message_handler(text="📤 Tarqatish")
async def totarqatish(message: types.Message):
    if message.chat.id in ADMINS:
        await message.answer("Tanlang:", reply_markup=typepost)


@dp.callback_query_handler(text="photo")
async def bot_photo_reklama(call: CallbackQuery):
    await call.message.answer('rasmni yuboring')
    await call.answer(cache_time=60)
    await Reklam_State.photo.set()


@dp.message_handler(content_types='photo', state=Reklam_State.photo)
async def get_bot_photo_reklama(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        if message.photo:
            photo_file_id = message.photo[-1].file_id
            await state.update_data({
                'photo': photo_file_id
            })
        await message.answer('textni kiriting')
        await Reklam_State.next()
    else:
        await message.answer('xato malumot yuborildi! ')


@dp.message_handler(content_types=None, state=Reklam_State.caption)
async def get_bot_text_reklama(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await state.update_data(caption=message.text)
        data = await state.get_data()
        photo = data.get('photo')
        caption = data.get('caption')
        await message.answer_photo(photo, caption)
        await message.answer('malumotlar to\'g\'riligini tekshiring', reply_markup=agree, parse_mode='HTML')
        await Reklam_State.next()
    else:
        await message.answer('xato malumot yuborildi! ')


@dp.message_handler(content_types=None, state=Reklam_State.finish)
async def set_reklama_finish(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        soni = 0
        text = msg.text
        if text == 'Ha':
            data = await state.get_data()
            photo = data.get('photo')
            caption = data.get('caption')
            await state.finish()
            await msg.answer('Xabar yuborilmoqda', reply_markup=ReplyKeyboardRemove())
            for id in db.select_all_users():
                user_id = id[0]
                try:
                    soni += 1
                    time.sleep(0.04)
                    print(f"shuncha odamga xabar yuborilmoqda {soni}")
                    await bot.send_photo(chat_id=user_id, photo=photo, caption=caption, parse_mode='HTML')
                except BotBlocked:
                    try:
                        db.delete_active_user(id=user_id)
                    except:
                        continue

                    continue
                except UserDeactivated:
                    try:
                        db.delete_active_user(id=user_id)
                    except:
                        continue

                    continue
                except ChatNotFound:
                    try:
                        db.delete_active_user(id=user_id)
                    except:
                        continue
                    continue
            await msg.answer('reklama yuborildi')
            await msg.answer(f'{soni} yuborildi')
        else:
            await state.finish()
            await msg.answer('reklama qabul qilinmadi', reply_markup=ReplyKeyboardRemove())
            await msg.answer('Tanlang', reply_markup=typepost)
    else:
        await msg.answer('xato malumot yuborildi! ')


@dp.callback_query_handler(text="text")
async def bot_photo_reklama(call: CallbackQuery):
    await call.message.answer('Reklama matnini kiriting')
    await call.answer(cache_time=60)
    await Matn_state.matn.set()


@dp.message_handler(content_types='text', state=Matn_state.matn)
async def get_bot_photo_reklama(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        if message.text:
            reklama_matn = message.text
            await state.update_data({
                'reklama_matn': reklama_matn
            })

            data = await state.get_data()
            reklama_matn = data.get('reklama_matn')
            await message.answer(reklama_matn)
            await message.answer('malumotlar to\'g\'riligini tekshiring', reply_markup=agree, parse_mode='HTML')
            await Matn_state.next()

    else:
        await message.answer('xato malumot yuborildi! ')


@dp.message_handler(content_types=None, state=Matn_state.finish)
async def set_reklama_finish(msg: types.Message, state: FSMContext):
    if msg.from_user.id in ADMINS:
        soni = 0
        text = msg.text
        if text == 'Ha':
            data = await state.get_data()
            reklama_matn = data.get('reklama_matn')
            await state.finish()
            await msg.answer('Xabar yuborilmoqda', reply_markup=ReplyKeyboardRemove())
            for id in db.select_all_users():
                user_id = id[0]
                try:
                    soni += 1
                    time.sleep(0.04)

                    print(f"shuncha odamga xabar yuborilmoqda {soni}")
                    await bot.send_message(chat_id=user_id, text=reklama_matn, parse_mode='HTML')
                except BotBlocked:
                    try:
                        db.delete_active_user(id=user_id)
                    except:
                        continue

                    continue
                except UserDeactivated:
                    try:
                        db.delete_active_user(id=user_id)
                    except:
                        continue

                    continue
                except ChatNotFound:
                    try:
                        db.delete_active_user(id=user_id)
                    except:
                        continue
                    continue
            await msg.answer('reklama yuborildi')
            await msg.answer(f'{soni} yuborildi')
        else:
            await state.finish()
            await msg.answer('reklama qabul qilinmadi', reply_markup=ReplyKeyboardRemove())
            await msg.answer('Tanlang', reply_markup=typepost)
    else:
        await msg.answer('xato malumot yuborildi! ')


@dp.message_handler(text="Xabar yuborish")
async def totarqatish(message: types.Message):
    if message.chat.id in ADMINS:
        await message.answer("Kimga xabar yubormoqchisiz? IDsini yuboring:", reply_markup=cencelbtn)
        await FeedbackTo.getid.set()


@dp.message_handler(state=FeedbackTo.getid)
async def totarqatish(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS:
        idto = message.text
        if idto == "Bekor qilish.":
            await message.answer("Bekor qilindi!", reply_markup=adminpanelbtn)
            await state.finish()
        else:
            sendfeedback.append(idto)
            await message.answer("Endi javob yozmoqchi bo'lgan xabar IDsini yuboring: ", reply_markup=cencelbtn)
            await FeedbackTo.getmsgid.set()


@dp.message_handler(state=FeedbackTo.getmsgid)
async def totarqatish(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS:
        msgid = message.text
        if msgid == "Bekor qilish.":
            await message.answer("Bekor qilindi!", reply_markup=adminpanelbtn)
            await state.finish()
        else:
            sendfeedback.append(msgid)
            await message.answer("Endi Yubormoqchi bo'lgan matnni kiriting: ", reply_markup=cencelbtn)
            await FeedbackTo.sendto.set()


@dp.message_handler(state=FeedbackTo.sendto)
async def totarqatish(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS:
        xabar = message.text
        if xabar == "Bekor qilish.":
            await message.answer("Bekor qilindi!", reply_markup=adminpanelbtn)
        else:
            try:
                await bot.send_message(chat_id=sendfeedback[-2],
                                       text=f"{xabar}\n\n<code>(Murojaatingizga adminimiz tomonidan javob)</code>",
                                       reply_to_message_id=sendfeedback[-1])
                await message.answer("<b>Xabaringiz yuborildi!</b>", reply_markup=adminpanelbtn)
                sendfeedback.remove(sendfeedback[-1])
                sendfeedback.remove(sendfeedback[-1])
            except:
                await message.answer("Xatolik yuz berdi!", reply_markup=adminpanelbtn)
        await state.finish()


@dp.message_handler(text="➕ Ilova qo'shish")
async def qoshishto(message: types.Message):
    if message.chat.id in ADMINS:
        await message.answer("Ilova nomini yuboring!", reply_markup=cencelbtn)
        await Qoshish.nameApp.set()


@dp.message_handler(state=Qoshish.nameApp)
async def totarqatish(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS:
        appname = message.text
        if appname == "Bekor qilish.":
            await message.answer("Bekor qilindi!", reply_markup=adminpanelbtn)
            await state.finish()
        else:

            # db.add_file_id(file_name=appname)
            await state.update_data({
                'appname': appname
            })
            await message.answer("Endi fileni descriptionini yuboring !", reply_markup=cencelbtn)
            await Qoshish.description.set()


@dp.message_handler(state=Qoshish.description)
async def totarqatish(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS:
        description = message.text
        if description == "Bekor qilish.":
            await message.answer("Bekor qilindi!", reply_markup=adminpanelbtn)
            await state.finish()
        else:
            await state.update_data({
                'description': description
            })
            await message.answer("Endi fileni  yuboring !", reply_markup=cencelbtn)
            await Qoshish.fileApp.set()


@dp.message_handler(state=Qoshish.fileApp, content_types=ContentTypes.ANY)
async def totarqatish(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS:
        if message.text == "Bekor qilish.":
            await message.answer("Bekor qilindi!", reply_markup=adminpanelbtn)
            await state.finish()
        else:
            if message.photo:
                await state.update_data({
                    'file_id': message.photo[-1].file_id
                })
            elif message.document:
                await state.update_data({
                    'file_id': message.document.file_id
                })
            elif message.video:
                await state.update_data({
                    'file_id': message.video.file_id
                })
            elif message.audio:
                await state.update_data({
                    'file_id': message.audio.file_id
                })
            elif message.forward_from_message_id:
                await state.update_data({
                    'file_id': message.forward_from_message_id
                })
            else:
                await message.answer('Bu tipdagi file qabul qilinmaydi!!')

            datas = await state.get_data()
            name = datas.get('appname')
            desciption = datas.get('description')
            file_ids = datas.get('file_id')
            print(file_ids)
            try:
                db.add_file_id(file_id=file_ids, file_name=name, description=desciption)
            except Exception as e:
                print(e)
                await message.answer(str(e))
            await bot.send_message(chat_id="-1002085945484",
                                   text=f"<b>Yangi ilova! (№{len(name)})</b>\n\n<b>Ilova nomi:</b> {name}\n<b>Ilova IDsi:</b> <code>{file_ids}</code>\n<b>File linki: </b>https://t.me/SoftFileBot?start={name}-SoftFileBot")
            await message.answer(
                f"<b>File qo'shildi!</b>\n\nLink: https://t.me/SoftFileBot?start={name}-SoftFileBot",
                reply_markup=adminpanelbtn)
            await state.finish()


@dp.message_handler(text="✅ Majburiy obuna")
async def majburiy_obuna_admin(message: types.Message):
    if message.chat.id in ADMINS:
        txt = "<b>Majburiy obuna.\n\nKanallar:</b>\n"
        for ch in CHANNELS:
            chinfo = await bot.get_chat(ch)
            txt += f"<b>Nomi:</b> {chinfo.title}\n"
            txt += f"<b>Username:</b> {chinfo.username}\n"
            txt += f"<b>ID:</b> {ch}\n\n"

        await message.answer(txt, reply_markup=keyboard_admin_obuna)


@dp.callback_query_handler(text="kanal_qoshish")
async def kanal_qoshish(call: CallbackQuery):
    if call.from_user.id in ADMINS:
        await call.message.delete()
        await call.message.answer(f"Qo'shmoqchi bo'lgan kanalingizni IDsini yuboring:", reply_markup=cencelbtn)
        await KanalQoshish.kanal_id.set()


@dp.message_handler(state=KanalQoshish.kanal_id)
async def kanal_qoshildi(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS:
        new_kanal = message.text
        if new_kanal[0] == "-":
            CHANNELS.append(new_kanal)
            await message.answer(f"Endi kanal linkini yuboring!", reply_markup=cencelbtn)
            await KanalQoshish.kanal_url.set()
        elif new_kanal == "🚫 Bekor qilish":
            await message.answer(f"Kanal qo'shish bekor qilindi.", reply_markup=adminpanelbtn)
            await state.finish()
        else:
            await message.answer(f"Iltimos faqat ID yuboring!")


@dp.message_handler(state=KanalQoshish.kanal_url)
async def kanal_qoshildi(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS:
        new_url = message.text
        if new_url[0:12] == "https://t.me":
            await message.answer(f"{new_url} qo'shildi.", reply_markup=adminpanelbtn)
            await state.finish()
        elif new_url == "🚫 Bekor qilish":
            CHANNELS.remove(CHANNELS[-1])
            await message.answer(f"Kanal qo'shish bekor qilindi.", reply_markup=adminpanelbtn)
            await state.finish()
        else:
            await message.answer(f"Iltimos faqat kanal linkini yuboring!")


@dp.callback_query_handler(text="kanal_olib_tashlash")
async def olib_tashlash(call: CallbackQuery):
    if call.from_user.id in ADMINS:
        await call.message.answer(f"Olib tashlamoqchi bo'lgan kanalingizni IDsini kiriting:", reply_markup=cencelbtn)
        await KanalOlish.kanal_olish.set()


@dp.message_handler(state=KanalOlish.kanal_olish)
async def kanal_qoshildi(message: types.Message, state: FSMContext):
    if message.chat.id in ADMINS:
        olinadigan_kanal = message.text
        if olinadigan_kanal in CHANNELS:
            CHANNELS.remove(olinadigan_kanal)
            await message.answer(f"{olinadigan_kanal} olib tashlandi.", reply_markup=adminpanelbtn)
            await state.finish()
        elif olinadigan_kanal[0] == "-":
            await message.answer(f"{olinadigan_kanal} kanallar ro'yxatida yo'q!")
        elif olinadigan_kanal == "🚫 Bekor qilish":
            await message.answer(f"Kanal olish bekor qilindi.", reply_markup=adminpanelbtn)
            await state.finish()
        else:
            await message.answer(f"Iltimos faqat ID yuboring!")


@dp.message_handler(text="Active")
async def adminpanel(message: types.Message):
    if message.chat.id in ADMINS:
        count = db.count_users()[0]
        active_count = db.count_active_users()[0]
        await message.answer(
            f"👥 <b>Bot obunachilari:</b> {count}\n<b>Aktiv obunachilar: {active_count}</b> ",
            parse_mode="HTML")


