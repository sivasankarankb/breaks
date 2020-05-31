#!/usr/bin/env python3

# app.py - What ties it all together.

import ui
import logic
import persistance

if __name__ == '__main__':
    app_ui = ui.App()
    work_timer_ui = ui.WorkTimer(master=app_ui.get_top_level_window())
    work_timer_logic = logic.WorkTimer(work_timer_ui)

    graph_data = []
    work_data = persistance.WorkData()
    data = work_data.load()

    if data != None:
        data = data[-1][1]
        colors = ['#ffcc00', '#0033cc']
        icolor = 0
        for event in data:
            graph_data.append((event[2], colors[icolor]))
            icolor = (icolor + 1) % 2

    time_graph = ui.TimeGraph(master=app_ui.get_top_level_window())

    time_graph.set_graph_data(graph_data)

    time_graph.draw_graph()

    app_ui.start()
    work_timer_logic.cleanup()
