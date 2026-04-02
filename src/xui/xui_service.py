from src.utils.exceptions import *
import py3xui
import uuid
from src.utils.logger_client import error_log


class XUIClient:
    def __init__(self, host, login, password, protocol, flow):
        self._host = host
        self._login = login
        self._password = password
        self._protocol = protocol
        self._api = None
        self._inbound_id = None
        self._flow = flow


    async def login(self):
        self._api = py3xui.AsyncApi(self._host, self._login, self._password, use_tls_verify=False)
        await self._api.login()

        inbound = await self.get_inbound()
        self._inbound_id = inbound.id


    async def get_inbound(self) -> py3xui.Inbound:
        inbound = None
        try:
            inbounds = await self._api.inbound.get_list()
        except Exception as exc:
            error_log.error(exc)
            raise InboundNotFoundException
        inbound = [item for item in inbounds if item.protocol == self._protocol][0]
        if not inbound: raise InboundNotFoundException
        return inbound


    async def get_by_tgid(self, user_id: str) -> py3xui.Client:
        if not user_id: raise GetTgIdException
        inbound = await self.get_inbound()
        client = [item for item in inbound.settings.clients if item.email == user_id]
        if not client: return None
        return client[0]
        

    async def enable_client(self, user_id: str, expiry: int):
        client = await self._api.client.get_by_email(user_id)
        client.expiry_time = expiry
        client.enable = True
        await self.update_client(client.uuid, client)


    async def reset_sub_id(self, user_id: str):
        if not user_id: raise GetTgIdException
        client = await self._api.client.get_by_email(user_id)
        uuid4 = await self.get_new_uuid()
        client.id = uuid4
        client.sub_id = uuid4
        await self.update_client(client.uuid, client)


    async def get_new_uuid(self) -> str:
        attempts = 3
        while attempts > 0:
            attempts -= 1
            uuid4 = str(uuid.uuid4())
            client = await self.get_by_uuid(uuid4)
            if (client): continue
            return uuid4
        raise GenerateUuidException


    async def get_by_uuid(self, uuid: str) -> py3xui.Client:
        if not uuid: raise GetUuidException
        inbound = await self.get_inbound()
        client = [item for item in inbound.settings.clients if item.uuid == uuid]
        if not client: return None
        return client[0]
    

    async def create_client(self, user_id: str, limit_ip: int, expiry: int, comment: str) -> py3xui.Client:
        if not user_id: raise GetTgIdException
        uuid4 = await self.get_new_uuid()
        new_client = py3xui.Client(
            id=uuid4,
            enable=True,
            email=user_id,
            limitIp=limit_ip,
            expiryTime=expiry,
            flow=self._flow,
            subId=uuid4,
            comment=comment
        )
        try: await self._api.client.add(self._inbound_id, [new_client])
        except Exception as exc:
            error_log.error(exc)
            raise CreateClientException
        return new_client
    

    async def update_client(self, uuid4: str, new_client: py3xui.Client):
        try: await self._api.client.update(uuid4, new_client)
        except Exception as exc:
            error_log.error(exc)
            raise UpdateClientException
