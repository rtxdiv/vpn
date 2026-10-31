import aiocron
from src.database.database_service import get_new_periods, use_period
from src.bot.bot_service import send_system_message
from src.database.models import UserPeriods
from src.utils.logger_client import error_log


async def activate_new_periods():
    try:
        periods: list[tuple[UserPeriods, int]] = await get_new_periods()
        errors = []
        for period, devices in periods:
            try:
                await use_period(period=period, devices=devices)
            except Exception as e:
                errors.append(period)
                error_log.error(str(e))
        await send_system_message(f'⌛ <b>Активация новых периодов</b>\nВсего: {len(periods)}\nОшибок: {len(errors)}')

    except Exception as e:
        await send_system_message(f'❗ <b>Активация новых периодов</b>\nОшибка сервера: {e}')


aiocron.crontab('0 0 * * *')(activate_new_periods)
