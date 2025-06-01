import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=200)


class Window:
    def __init__(self):
        self.window = dpg.window(label="Window", tag="Window")

        with self.window:
            dpg.add_text("Conway's Game of Life")



window = Window()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()
dpg.set_primary_window("Window", True)

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
    # window.update()

dpg.destroy_context()
