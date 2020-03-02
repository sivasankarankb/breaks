
# app.py - What ties it all together.

from ui import AppUI_tkinter
from logic import AppLogic

ui = AppUI_tkinter()
logic = AppLogic(ui)

ui.start()
