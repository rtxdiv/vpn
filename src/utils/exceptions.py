from enum import Enum


class ForeseenException(Exception):
    pass

class TelegramAuthError(Exception):
    pass


class Msg(Enum):
    NOT_FORSEEN = 'Произошла непредвиденная ошибка'
    TG_ID_GET = 'Ошибка получения Telegram ID'
    UUID_GET = 'Ошибка получения UUID'
    CLIENT_NOT_FOUND = 'Клиент не найден'
    INBOUND_NOT_FOUND = 'Ошибка поиска VPN-туннеля'
    UUID_GENERATION = 'Ошибка генерации UUID'
    SUB_ID_RESET = 'Ошибка сброса ID подписки'
    CLIENT_CREATE = 'Ошибка создание клиента'
    CLIENT_ENABLE = 'Ошибка обновления клиента'
