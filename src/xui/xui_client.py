from src.xui.xui_service import XUIClient
import os


xui = XUIClient(
    host=os.environ['PANEL_HOST'],
    token=os.environ['PANEL_TOKEN'],
    remark=os.environ['MAIN_INBOUND_REMARK']
)