import py3xui
import uuid

class XUIClient:
    def __init__(self, host: str, login: str, password: str):
        self._host = host
        self._login = login
        self._password = password
        self._api = None
        self._protocol = 'vless'
        self._inbound_id = None


    async def login(self):
        self._api = py3xui.AsyncApi(self._host, self._login, self._password, use_tls_verify=False)
        await self._api.login()

        inbound = await self.get_inbound()
        self._inbound_id = inbound.id


    async def get_inbound(self) -> py3xui.Inbound:
        inbounds = await self._api.inbound.get_list()
        inbound = [item for item in inbounds if item.protocol == self._protocol][0]
        if not inbound: raise Exception('Inbound not fiend')
        return inbound


    async def get_by_tgid(self, id: any) -> py3xui.Client:
        if not id: raise Exception
        try: 
            inbound = await self.get_inbound()
            client = [item for item in inbound.settings.clients if item.email == str(id)]
            if not client: return None
            return client[0]
        
        except:
            return None


    async def create_client(self, id: any, limit_ip: int, expiry: int):
        uid = str(uuid.uuid4())
        new_client = py3xui.Client(id=uid, enable=True, email=str(id), limitIp=limit_ip, expiryTime=expiry, flow='xtls-rprx-vision', subId=uid)
        await self._api.client.add(self._inbound_id, [new_client])

