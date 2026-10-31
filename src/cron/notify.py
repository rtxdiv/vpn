import aiocron
from src.database.database_service import get_not_extended
from src.bot.bot_service import send_system_message, send_not_extended
from src.database.models import UserPeriods
from src.utils.logger_client import error_log


async def notify_not_extended():
    try:
        periods: list[UserPeriods] = await get_not_extended()
        errors = []
        for period in periods:
            try:
                await send_not_extended(user_id=period.user_id, ends=period.ends)
            except Exception as e:
                errors.append(period)
                error_log.error(str(e))
        await send_system_message(f'🔔 <b>Уведомления о продлении</b>\nВсего: {len(periods)}\nОшибок: {len(errors)}')

    except Exception as e:
        await send_system_message(f'❗ <b>Уведомления о продлении</b>\nОшибка сервера: {e}')


aiocron.crontab('10 0 * * *')(notify_not_extended)
