from src.xui.xui_service import XUIClient
import os


xui = XUIClient(
    os.environ['PANEL_HOST'],
    os.environ['PANEL_TOKEN'],
    os.environ['INBOUND_REMARK'],
    os.environ['CLIENT_FLOW']
)