class ForeseenException(Exception):
    def __init__(self, message='Произошла ошибка'):
        super().__init__(message)

class GetTgIdException(ForeseenException):
    def __init__(self, message='Ошибка получения Telegram ID'):
        super().__init__(message)

class GetUuidException(ForeseenException):
    def __init__(self, message='Ошибка получения UUID'):
        super().__init__(message)

class ClientNotFoundException(ForeseenException):
    def __init__(self, message='Клиент не найден'):
        super().__init__(message)

class InboundNotFoundException(ForeseenException):
    def __init__(self, message='Ошибка поиска VPN-туннеля'):
        super().__init__(message)

class GenerateUuidException(ForeseenException):
    def __init__(self, message='Ошибка генерации UUID'):
        super().__init__(message)

class ResetSubIdException(ForeseenException):
    def __init__(self, message='Ошибка сброса ID подписки'):
        super().__init__(message)

class CreateClientException(ForeseenException):
    def __init__(self, message='Ошибка создания клиента'):
        super().__init__(message)

class UpdateClientException(ForeseenException):
    def __init__(self, message='Ошибка обновления клиента'):
        super().__init__(message)


class TelegramAuthError(Exception):
    pass
