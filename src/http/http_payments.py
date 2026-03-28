from .http_client import get_session
import json


base_url = 'https://1plat.cash'

async def create_payment():
    session = get_session()
    payload = {
        'merchant_order_id': 'order1',
        'user_id': 12345678,
        'amount': 100,
        'method': 'sbp',
    }
    async with session.post(
        url=f'{base_url}/api/merchant/order/create/by-api',
        json=payload
    ) as resp:
        print(f"RESPONSE STATUS: {resp.status} {resp.reason}", flush=True)
        try:
            data = await resp.json()
            print(f'RESPONSE (josn):\n{json.dumps(data, ensure_ascii=False, indent=2)}', flush=True)
        except:
            text = await resp.text()
            print(f'RESPONSE (text):\n{text}', flush=True)


async def get_shop_info():
    session = get_session()
    async with session.get(
        url=f'{base_url}/api/shop/info/by-api',
    ) as resp:
        try:
            data = await resp.json()
            print(f'RESPONSE (josn):\n{json.dumps(data, ensure_ascii=False, indent=2)}', flush=True)
        except:
            text = await resp.text()
            print(f'RESPONSE (text):\n{text}', flush=True)
