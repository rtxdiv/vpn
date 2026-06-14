from src.utils.exceptions import *
import py3xui
import uuid
from src.utils.logger_client import error_log
from datetime import datetime, timedelta


class XUIClient:
    def __init__(self, host, token, remark):
        self._host = host
        self._token = token
        self._remark = remark
        self._api = None
        self._inbound_id = None


    async def login(self):
        self._api = py3xui.AsyncApi(host=self._host, token=self._token, use_tls_verify=False)
        inbound = await self.get_main_inbound()
        self._inbound_id = inbound.id
        working_inbounds = await self.get_working_inbounds()
        print(working_inbounds, flush=True)


    async def get_main_inbound(self) -> py3xui.Inbound:
        try:
            inbounds = await self._api.inbound.get_list()
        except Exception as exc:
            error_log.error(exc)
            raise InboundNotFoundException
        matched_inbounds = [item for item in inbounds if item.remark == self._remark]
        if not matched_inbounds:
            raise InboundNotFoundException
        return matched_inbounds[0]
    

    async def get_working_inbounds(self) -> list[py3xui.Inbound]:
        try:
            inbounds = await self._api.inbound.get_list()
        except Exception as exc:
            error_log.error(exc)
            raise InboundNotFoundException
        matched_inbounds = [item for item in inbounds if item.remark and not item.remark.startswith('dev-')]
        if not matched_inbounds:
            raise InboundNotFoundException
        return matched_inbounds

    
    async def get_by_tgid(self, user_id):
        try:
            return await self._api.client.get_by_email(user_id)
        except Exception as exc:
            if 'not found' in str(exc).lower():
                return None
            raise
        

    # async def enable_client(self, user_id: str, limit_ip: int, days: int):
    #     client = await self.get_by_tgid(user_id)
    #     expiry = self.days_to_expiry(days)
    #     if not client: 
    #         return await self.create_client(
    #             user_id=user_id,
    #             limit_ip=limit_ip,
    #             expiry=expiry,
    #         )
    #     client.enable = True
    #     client.limit_ip = limit_ip
    #     client.expiry_time = expiry
    #     client.reset = 0
    #     await self.update_client(client.uuid, client)


    async def renew_client(self, user_id: str, limit_ip: int, days: int):
        client = await self.get_by_tgid(user_id)
        if not client: 
            expiry = self.days_to_expiry(days)
            return await self.create_client(
                user_id=user_id,
                limit_ip=limit_ip,
                expiry=expiry,
            )
        client.enable = True
        client.limit_ip = limit_ip
        now_ts = int(datetime.now().timestamp() * 1000)
        if client.expiry_time and client.expiry_time > now_ts:
            client.expiry_time = self.days_to_expiry(days, base_ts=client.expiry_time)
        else:
            client.expiry_time = self.days_to_expiry(days)
        await self.update_client(client.uuid, client)


    async def reset_sub_id(self, user_id: str):
        if not user_id: raise GetTgIdException
        client = await self.get_by_tgid(user_id)
        old_uuid = client.uuid
        uuid4 = await self.get_new_uuid()
        client.uuid = uuid4
        client.sub_id = uuid4
        await self.update_client(old_uuid, client)
        return uuid4


    async def get_new_uuid(self) -> str:
        uuid4 = str(uuid.uuid4())
        client = await self.get_by_uuid(uuid4)
        if client: raise GetUuidException
        return uuid4


    async def get_by_uuid(self, uuid: str) -> py3xui.Client:
        if not uuid: raise GetUuidException
        inbound = await self.get_main_inbound()
        client = [item for item in inbound.settings.clients if item.uuid == uuid]
        if not client: return None
        return client[0]
    

    async def create_client(self, user_id: str, limit_ip: int, expiry: int) -> py3xui.Client:
        if not user_id: raise GetTgIdException
        uuid4 = await self.get_new_uuid()
        new_client = py3xui.Client(
            id=uuid4,
            enable=True,
            email=user_id,
            limit_ip=limit_ip,
            expiry_time=expiry,
            sub_id=uuid4,
        )
        working_inbounds = await self.get_working_inbounds()
        added_at_least_once = False
        for inbound in working_inbounds:
            settings_str = str(inbound.stream_settings).lower()
            if inbound.protocol == 'vless' and 'tcp' in settings_str:
                new_client.flow = 'xtls-rprx-vision'
            else:
                new_client.flow = ''
                
            try:
                await self._api.client.add(inbound.id, [new_client])
                added_at_least_once = True
            except Exception as exc:
                error_log.error(f'Ошибка при создании клиента: {exc}')

        if not added_at_least_once:
            raise CreateClientException
    

    async def update_client(self, uuid4: str, new_client: py3xui.Client):
        new_client.id = new_client.uuid
        try: await self._api.client.update(uuid4, new_client)
        except Exception as exc:
            error_log.error(f'Ошибка при обновлении клиента: {exc}')
            raise UpdateClientException


    def days_to_expiry(self, days: int, base_ts: int = None) -> int:
        if base_ts:
            return base_ts + self.days_to_timestamp(days)
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        expiry_date = current_date + timedelta(days=days)
        return int(expiry_date.timestamp() * 1000)

    def days_to_timestamp(self, days: int):
        return days * 24 * 60 * 60 * 1000
    