import dearpygui.dearpygui as dpg


def set_font(font, size=20, windows_default_font=False):
    font_path = ("C:/Windows/Fonts/" if windows_default_font else "") + font
    with dpg.font_registry():
        default_font = dpg.add_font(font_path, size)
    dpg.bind_font(default_font)


def theme_load():
    with dpg.theme() as main_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (240, 240, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg, (240, 240, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Border, (240, 240, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (240, 240, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_Button, (220, 220, 220), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (210, 210, 210), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 200, 200), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (240, 240, 240), category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (240, 240, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (240, 240, 240), category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (240, 240, 240), category=dpg.mvThemeCat_Core)

            # dpg.add_theme_color(dpg.mvThemeCol_CheckMark, theme_data["color"]["check_mark"], category=dpg.mvThemeCat_Core)

            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,2, category=dpg.mvThemeCat_Core)

    return main_theme
