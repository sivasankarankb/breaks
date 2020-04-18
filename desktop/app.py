#!/usr/bin/env python3

# app.py - What ties it all together.

from ui import AppUI
from logic import AppLogic

ui = AppUI()
logic = AppLogic(ui)

ui.start()
logic.cleanup()
