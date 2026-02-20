import py3xui
import uuid

class XUIClient:
    def __init__(self, host, login, password):
        self._host = host
        self._login = login
        self._password = password
        self._api = None
        self._vless_id = None

    async def login(self):
        self._api = py3xui.AsyncApi(self._host, self._login, self._password, use_tls_verify=False)
        await self._api.login()

        inbounds = await self._api.inbound.get_list()
        vless = [item for item in inbounds if item.remark == 'vless'][0]
        self._vless_id = vless.id


    async def get_by_tgid(self, id):
        try:
            if not id: raise Exception

            client = await self._api.client.get_by_email(id)
            if not client: raise Exception
            return client

        except Exception as err:
            print(err)
            return None
        

    async def create_client(self, id, limit_ip, expiry):
        uid = str(uuid.uuid4())
        new_client = py3xui.Client(id=uid, enable=True, email=str(id), limitIp=limit_ip, expiryTime=expiry, flow='xtls-rprx-vision', subId=uid)
        await self._api.client.add(self._vless_id, [new_client])

