import dearpygui.dearpygui as dpg

# Transformation globale
offset = [0, 0]
zoom = [1.0]

def update_view():
    width = dpg.get_item_width("drawlist")
    height = dpg.get_item_height("drawlist")
    dpg.configure_item("background_rect", pmin=(0, 0), pmax=(width, height))

def apply_transform(pos):
    # Applique le zoom et le décalage
    return [(pos[0] - offset[0]) / zoom[0], (pos[1] - offset[1]) / zoom[0]]

def mouse_events():
    mouse_pos = dpg.get_mouse_pos()
    mouse_delta = dpg.get_mouse_drag_delta()

    is_dragging = dpg.is_mouse_button_down(0)
    is_hovered = dpg.is_item_hovered("drawlist")

    if is_dragging and is_hovered:
        offset[0] += mouse_delta[0]
        offset[1] += mouse_delta[1]

    # Zoom avec molette
    wheel = dpg.add_mouse_wheel_handler()
    if wheel != 0 and is_hovered:
        zoom_factor = 1.1 if wheel > 0 else 1 / 1.1
        old_zoom = zoom[0]
        zoom[0] *= zoom_factor

        # Centre le zoom sur la souris
        mouse_x, mouse_y = mouse_pos
        offset[0] = mouse_x - ((mouse_x - offset[0]) / old_zoom) * zoom[0]
        offset[1] = mouse_y - ((mouse_y - offset[1]) / old_zoom) * zoom[0]

def render_loop():
    mouse_events()

    # Clear et redraw
    dpg.delete_item("drawlist", children_only=True)

    # Redessine le fond (doit toujours être là)
    width = dpg.get_item_width("drawlist")
    height = dpg.get_item_height("drawlist")
    dpg.draw_rectangle((0, 0), (width, height), fill=(255, 255, 255, 255), color=(255, 255, 255, 255),
                       tag="background_rect", parent="drawlist")

    # Exemple d'objet transformé
    start = apply_transform((100, 100))
    end = apply_transform((400, 400))
    dpg.draw_line(start, end, color=(255, 0, 0, 255), thickness=3, parent="drawlist")

dpg.create_context()
dpg.create_viewport(title="Zoom & Drag", width=800, height=600)

# Supprimer le padding et la bordure
theme = dpg.add_theme()
comp = dpg.add_theme_component(dpg.mvAll, parent=theme)
dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 0, 0, parent=comp)
dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0, parent=comp)
dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 0, 0, parent=comp)
dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 0, parent=comp)
dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 255, 255, 255), parent=comp)
dpg.bind_theme(theme)

# Fenêtre sans déco
dpg.add_window(tag="main_window", no_title_bar=True, no_move=True, no_resize=True,
               no_close=True, no_scrollbar=True, no_scroll_with_mouse=True,
               no_bring_to_front_on_focus=True, pos=(0, 0))

# Drawlist plein écran
dpg.add_drawlist(tag="drawlist", parent="main_window", width=800, height=600, pos=(0, 0))

# Resize auto
def resize(sender, app_data, user_data):
    width = dpg.get_viewport_client_width()
    height = dpg.get_viewport_client_height()
    dpg.set_item_width("drawlist", width)
    dpg.set_item_height("drawlist", height)
    update_view()

dpg.set_viewport_resize_callback(resize)
dpg.set_frame_callback(0, resize)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()
dpg.set_primary_window("main_window", True)

# Boucle manuelle avec mise à jour du rendu
while dpg.is_dearpygui_running():
    render_loop()
    dpg.render_dearpygui_frame()

dpg.destroy_context()
