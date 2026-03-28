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
    ) as response:
        print(f"-- RESPONSE STATUS: {response.status} {response.reason}", flush=True)
        try:
            data = await response.json()
            print("--  RESPONSE BODY (JSON):", flush=True)
            print(json.dumps(data, ensure_ascii=False, indent=2), flush=True)
        except:
            text = await response.text()
            print("-- RESPONSE BODY (TEXT):", flush=True)
            print(text, flush=True)
