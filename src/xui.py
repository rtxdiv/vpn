from exceptions import ForeseenException
import py3xui
import uuid

class XUIClient:
    def __init__(self, host, login, password, protocol):
        self._host = host
        self._login = login
        self._password = password
        self._protocol = protocol
        self._api = None
        self._inbound_id = None


    async def login(self):
        self._api = py3xui.AsyncApi(self._host, self._login, self._password, use_tls_verify=False)
        await self._api.login()

        inbound = await self.get_inbound()
        self._inbound_id = inbound.id


    async def get_inbound(self) -> py3xui.Inbound:
        inbounds = await self._api.inbound.get_list()
        inbound = [item for item in inbounds if item.protocol == self._protocol][0]
        if not inbound: raise ForeseenException('Не найден туннель сервера')
        return inbound


    async def get_by_tgid(self, id: any) -> py3xui.Client:
        if not id: raise ForeseenException('Не передан Tg-ID')
        inbound = await self.get_inbound()
        client = [item for item in inbound.settings.clients if item.email == str(id)]
        if not client: return None
        return client[0]


    async def create_client(self, id: any, limit_ip: int, expiry: int, comment: str) -> py3xui.Client:
        if not id: raise ForeseenException('Не передан Tg-ID')
        uuid4 = str(uuid.uuid4())
        new_client = py3xui.Client(
            id=uuid4,
            enable=True,
            email=str(id),
            limitIp=limit_ip,
            expiryTime=expiry,
            flow='xtls-rprx-vision',
            subId=uuid4,
            comment=comment
        )
        await self._api.client.add(self._inbound_id, [new_client])
        return new_client


    async def reset_sub_id(self, id: any):
        if not id: raise ForeseenException('Не передан Tg-ID')
        try:
            client = await self._api.client.get_by_email(str(id))
        except:
            raise ForeseenException('Клиент не найден')
        original_uuid = client.uuid
        uuid4 = str(uuid.uuid4())
        client.id = uuid4
        client.sub_id = uuid4
        await self._api.client.update(original_uuid, client)
