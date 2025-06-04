import dearpygui.dearpygui as dpg
from bin import theme
dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=200)


class Window:
    def __init__(self):
        self.window = dpg.window(label="Window", tag="Window")
        theme.set_font("segoeui.ttf", 16, True)

        with self.window:
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="New", callback=lambda: print("New"))
                    dpg.add_menu_item(label="Open", callback=lambda: print("Open"))
                    dpg.add_menu_item(label="Save", callback=lambda: print("Save"))
                    dpg.add_menu_item(label="Save As", callback=lambda: print("Save As"))
                    dpg.add_menu_item(label="Settings", callback=dpg.stop_dearpygui)
                    dpg.add_menu_item(label="Exit", callback=dpg.stop_dearpygui)
                with dpg.menu(label="Edit"):
                    dpg.add_menu_item(label="Undo", callback=lambda: print("Undo"))
                    dpg.add_menu_item(label="Redo", callback=lambda: print("Redo"))
                with dpg.menu(label="Help"):
                    dpg.add_menu_item(label="About", callback=lambda: print("About"))

            with dpg.group(horizontal=True):
                dpg.add_text("Hello")
                dpg.add_button(label="Run simulation")
                dpg.add_button(label="Stop simulation")
                dpg.add_button(label="Step forward")
                dpg.add_drag_double(label="Simulation speed", default_value=1.0, min_value=0.0, max_value=10.0,
                                    speed=0.05, width=150)

            with dpg.drawlist(width=400, height=300,callback=self.test):
                dpg.draw_rectangle((10, 10), (50, 50), fill=(255, 0, 0), color=(255, 0, 0), thickness=0.0)

    def test(self, sender, app_data, user_data):
        print(sender, app_data, user_data)
        print(dpg.get_mouse_pos())


window = Window()

theme = theme.theme_load()
dpg.bind_theme(theme)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()
dpg.set_primary_window("Window", True)

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
    # window.update()

dpg.destroy_context()
