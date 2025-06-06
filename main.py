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



            with dpg.drawlist(width=700, height=700,callback=self.test):  # drawlist ()
                for i in range(10):
                    for j in range(10):
                        dpg.draw_rectangle((10 + 50 * i, 10 + 50 * j), (50 + 50 * i, 50 + 50 * j),
                                           fill=(0, 0, 255), color=(0, 0, 255), thickness=0.0)
                dpg.draw_rectangle((10, 10), (50, 50), fill=(255, 0, 0), color=(255, 0, 0), thickness=0.0)
                dpg.draw_rectangle((60, 10), (100, 50), fill=(255, 0, 0), color=(255, 0, 0), thickness=0.0)
                dpg.draw_rectangle((10, 60), (50, 100), fill=(255, 0, 0), color=(255, 0, 0), thickness=0.0)
                dpg.draw_rectangle((60, 60), (100, 100), fill=(255, 0, 0), color=(255, 0, 0), thickness=0.0)


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
