import dearpygui.dearpygui as dpg


def molette_callback(sender, app_data):
    direction = app_data  # float: >0 = haut, <0 = bas
    if direction > 0:
        print("Molette vers le haut")
    elif direction < 0:
        print("Molette vers le bas")


def clic_gauche_callback():
    if dpg.is_mouse_button_down(dpg.mvMouseButton_Left):
        print("Clic gauche enfoncé")


def frame_update_callback():
    # vérifie clic gauche à chaque frame
    clic_gauche_callback()


dpg.create_context()
dpg.create_viewport(title='Détection souris', width=600, height=400)

with dpg.handler_registry(tag="drawlist_handler", label="drawlist_handler"):
    dpg.add_mouse_wheel_handler(parent="drawlist_handler", callback=molette_callback)



dpg.setup_dearpygui()
dpg.show_viewport()
while dpg.is_dearpygui_running():
    frame_update_callback()
    dpg.render_dearpygui_frame()
dpg.destroy_context()
