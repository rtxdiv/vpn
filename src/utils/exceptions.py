class ForeseenException(Exception):
    pass

class GetTgIdException(ForeseenException):
    def __init__(self, message='Ошибка получения Telegram ID'):
        self.message = message
        super().__init__(self.message)

class GetUuidException(ForeseenException):
    def __init__(self, message='Ошибка получения UUID'):
        self.message = message
        super().__init__(self.message)

class ClientNotFoundException(ForeseenException):
    def __init__(self, message='Клиент не найден'):
        self.message = message
        super().__init__(self.message)

class InboundNotFoundException(ForeseenException):
    def __init__(self, message='Ошибка поиска VPN-туннеля'):
        self.message = message
        super().__init__(self.message)

class GenerateUuidException(ForeseenException):
    def __init__(self, message='Ошибка генерации UUID'):
        self.message = message
        super().__init__(self.message)

class ResetSubIdException(ForeseenException):
    def __init__(self, message='Ошибка сброса ID подписки'):
        self.message = message
        super().__init__(self.message)

class CreateClientException(ForeseenException):
    def __init__(self, message='Ошибка создания клиента'):
        self.message = message
        super().__init__(self.message)

class UpdateClientException(ForeseenException):
    def __init__(self, message='Ошибка обновления клиента'):
        self.message = message
        super().__init__(self.message)


class TelegramAuthError(Exception):
    pass
