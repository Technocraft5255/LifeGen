import dearpygui.dearpygui as dpg
from bin import theme

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=200)


class Window:
    def __init__(self):
        theme.set_font("segoeui.ttf", 16, True)

        self.window = dpg.add_window(label="Main Window", tag="main_window")
        self.build_drawlist()
        self.build_menu()
        self.build_controls()
        """
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

            with dpg.drawlist(tag="MainDrawlist",width=1700, height=900, callback=self.test):  # draw-list ()
                dpg.draw_rectangle((0, 0), (), fill=(110, 110, 110), color=(110, 110, 110), thickness=0.0)
                for i in range(40):
                    for j in range(30):
                        dpg.draw_rectangle((2 + 50 * i, 2 + 50 * j), (50 + 50 * i, 50 + 50 * j),
                                           fill=(75, 75, 75), color=(75, 75, 75), thickness=0.0)

                i = 13
                j = 10
                dpg.draw_rectangle((2 + 50 * i, 2 + 50 * j), (50 + 50 * i, 50 + 50 * j), fill=(255, 255, 255),
                                   color=(255, 255, 255), thickness=0.0)
                i = 14
                j = 10
                dpg.draw_rectangle((2 + 50 * i, 2 + 50 * j), (50 + 50 * i, 50 + 50 * j), fill=(255, 255, 255),
                                   color=(255, 255, 255), thickness=0.0)
                i = 14
                j = 9
                dpg.draw_rectangle((2 + 50 * i, 2 + 50 * j), (50 + 50 * i, 50 + 50 * j), fill=(255, 255, 255),
                                   color=(255, 255, 255), thickness=0.0)
                i = 13
                j = 8
                dpg.draw_rectangle((2 + 50 * i, 2 + 50 * j), (50 + 50 * i, 50 + 50 * j), fill=(255, 255, 255),
                                   color=(255, 255, 255), thickness=0.0)

                dpg.draw_rectangle((10, 10), (50, 50), fill=(255, 0, 0), color=(255, 0, 0), thickness=0.0)
                dpg.draw_rectangle((60, 10), (100, 50), fill=(255, 0, 0), color=(255, 0, 0), thickness=0.0)
                dpg.draw_rectangle((10, 60), (50, 100), fill=(255, 0, 0), color=(255, 0, 0), thickness=0.0)
                dpg.draw_rectangle((60, 60), (100, 100), fill=(255, 0, 0), color=(255, 0, 0), thickness=0.0)"""

    def build_drawlist(self):
        dpg.add_drawlist(tag="drawlist", parent=self.window, width=800, height=600, pos=(0, 0))

        dpg.draw_rectangle((0, 0), (800, 600), fill=(110, 110, 110), color=(110, 110, 110),
                           tag="background_rect", parent="drawlist")
        for i in range(40):
            for j in range(30):
                dpg.draw_rectangle((2 + 50 * i, 2 + 50 * j), (50 + 50 * i, 50 + 50 * j),
                                   fill=(75, 75, 75), color=(75, 75, 75), thickness=0.0, parent="drawlist")
        i = 13
        j = 10
        dpg.draw_rectangle((2 + 50 * i, 2 + 50 * j), (50 + 50 * i, 50 + 50 * j), fill=(255, 255, 255),
                           color=(255, 255, 255), thickness=0.0, parent="drawlist")
        i = 14
        j = 10
        dpg.draw_rectangle((2 + 50 * i, 2 + 50 * j), (50 + 50 * i, 50 + 50 * j), fill=(255, 255, 255),
                           color=(255, 255, 255), thickness=0.0, parent="drawlist")
        i = 14
        j = 9
        dpg.draw_rectangle((2 + 50 * i, 2 + 50 * j), (50 + 50 * i, 50 + 50 * j), fill=(255, 255, 255),
                           color=(255, 255, 255), thickness=0.0, parent="drawlist")
        i = 13
        j = 8
        dpg.draw_rectangle((2 + 50 * i, 2 + 50 * j), (50 + 50 * i, 50 + 50 * j), fill=(255, 255, 255),
                           color=(255, 255, 255), thickness=0.0, parent="drawlist")

    def build_menu(self):
        dpg.add_menu_bar(parent="main_window", tag="menu_bar")
        dpg.add_menu(label="File", parent="menu_bar", tag="file_menu")
        dpg.add_menu_item(label="New", callback=lambda: print("New"), parent="file_menu")
        dpg.add_menu_item(label="Open", callback=lambda: print("Open"), parent="file_menu")
        dpg.add_menu_item(label="Save", callback=lambda: print("Save"), parent="file_menu")
        dpg.add_menu_item(label="Save As", callback=lambda: print("Save As"), parent="file_menu")
        dpg.add_menu_item(label="Settings", callback=dpg.stop_dearpygui, parent="file_menu")
        dpg.add_menu_item(label="Exit", callback=dpg.stop_dearpygui, parent="file_menu")

    def build_controls(self):
        self.controls_group = dpg.add_group(horizontal=True, parent="main_window",tag="controls_group")
        dpg.add_text("Hello", parent="controls_group")
        dpg.add_button(label="Run simulation", parent=self.controls_group)
        dpg.add_button(label="Stop simulation", parent="controls_group")
        dpg.add_button(label="Step forward", parent="controls_group")
        dpg.add_drag_double(label="Simulation speed", default_value=1.0, min_value=0.0, max_value=10.0,
                            speed=0.05, width=150, parent="controls_group")

    def update_drawlist_size(self, sender, app_data, user_data):
        viewport_width, viewport_height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()
        dpg.set_item_width("drawlist", viewport_width)
        dpg.set_item_height("drawlist", viewport_height)
        dpg.configure_item("background_rect", pmax=(viewport_width, viewport_height))


window = Window()

theme = theme.theme_load()
dpg.bind_theme(theme)

dpg.set_viewport_resize_callback(window.update_drawlist_size)

dpg.set_frame_callback(0, window.update_drawlist_size)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()
dpg.set_primary_window("main_window", True)

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()
