from src.utils.exceptions import ForeseenException, Msg
import py3xui
import uuid


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
        inbounds = await self._api.inbound.get_list()
        inbound = [item for item in inbounds if item.protocol == self._protocol][0]
        if not inbound: raise ForeseenException(Msg.INBOUND_NOT_FOUND)
        return inbound


    async def get_by_tgid(self, id: any) -> py3xui.Client:
        if not id: raise ForeseenException(Msg.TG_ID_GET)
        inbound = await self.get_inbound()
        client = [item for item in inbound.settings.clients if item.email == str(id)]
        if not client: raise ForeseenException(Msg.CLIENT_NOT_FOUND)
        return client[0]


    async def create_client(self, id: any, limit_ip: int, expiry: int, comment: str) -> py3xui.Client:
        if not id: raise ForeseenException(Msg.TG_ID_GET)
        uuid4 = await self.get_new_uuid()
        new_client = py3xui.Client(
            id=uuid4,
            enable=True,
            email=str(id),
            limitIp=limit_ip,
            expiryTime=expiry,
            flow=self._flow,
            subId=uuid4,
            comment=comment
        )
        try: await self._api.client.add(self._inbound_id, [new_client])
        except: raise ForeseenException(Msg.CLIENT_CREATE)
        return new_client
    

    async def enable_client(self, id: any, expiry: int):
        client = await self._api.client.get_by_email(str(id))
        client.expiry_time = expiry
        client.enable = True
        await self.update_client(client.uuid, client, )


    async def reset_sub_id(self, id: any):
        if not id: raise ForeseenException(Msg.TG_ID_GET)
        client = await self._api.client.get_by_email(str(id))
        uuid4 = await self.get_new_uuid()
        client.id = uuid4
        client.sub_id = uuid4
        await self.update_client(client.uuid, client, Msg.SUB_ID_RESET)


    async def get_new_uuid(self) -> str:
        attempts = 3
        while attempts > 0:
            attempts -= 1
            uuid4 = str(uuid.uuid4())
            client = await self.get_by_uuid(uuid4)
            if (client): continue
            return uuid4
        raise ForeseenException(Msg.UUID_GENERATION)


    async def get_by_uuid(self, uuid: str) -> py3xui.Client:
        if not uuid: raise ForeseenException(Msg.UUID_GET)
        inbound = await self.get_inbound()
        client = [item for item in inbound.settings.clients if item.uuid == uuid]
        if not client: return None
        return client[0]
    

    async def update_client(self, uuid4: str, new_client: py3xui.Client, message = Msg.NOT_FORSEEN):
        try: await self._api.client.update(uuid4, new_client)
        except: raise ForeseenException(message)
