from aiogram.dispatcher.filters.state import StatesGroup, State




class Contact(StatesGroup):
    contact = State()

class FeedbackTo(StatesGroup):
    getid = State()
    getmsgid = State()
    sendto = State()

class Qoshish(StatesGroup):
    nameApp = State()
    description = State()
    fileApp = State()

class KanalQoshish(StatesGroup):
    kanal_id = State()
    kanal_url = State()

class KanalOlish(StatesGroup):
    kanal_olish = State()



class Reklam_State(StatesGroup):
    photo = State()
    caption = State()
    finish = State()

class Matn_state(StatesGroup):
    matn = State()
    finish = State()

