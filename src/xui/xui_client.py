from src.xui.xui_service import XUIClient
import os


xui = XUIClient(
    os.environ['PANEL_HOST'] + '/' + os.environ['PANEL_PATH'],
    os.environ['PANEL_LOGIN'],
    os.environ['PANEL_PASSWORD'],
    os.environ['INBOUND_PROTOCOL'],
    os.environ['CLIENT_FLOW']
)