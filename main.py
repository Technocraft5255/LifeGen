import pygame as pg
from pygame import Vector2


class Game:
    def __init__(self):
        pass

    def open(self, file_path):
        # Load saved life simulation file here
        pass

    def save(self, file_path):
        # Save current simulation state in a file
        pass


class App:
    def __init__(self, game: Game):
        pg.init()
        self.fps = 60
        self.clock = pg.time.Clock()
        self.is_running = True
        self.game = game

        # Window size and creation
        self.size = Vector2(1000, 800)
        self.screen = pg.display.set_mode(self.size, pg.RESIZABLE)

        # Viewport creation
        self.viewport = ViewPort(Vector2(0, 50), self.size - Vector2(0, 50))

    def run(self):
        """Main application loop."""
        while self.is_running:
            self.screen.fill((0, 0, 0))

            # Draw viewport area and test rectangle
            self.viewport.draw(self.screen)
            self.viewport.draw_rect(self.screen, Vector2(2, 2), Vector2(3, 3))

            # Limit FPS and update screen
            self.clock.tick(self.fps)
            pg.display.flip()

            # Process incoming events
            self.handle_events(pg.event.get())

    def handle_events(self, events):
        """Handle all pygame events."""
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                self.is_running = False
                exit(0)

            if event.type == pg.MOUSEBUTTONDOWN:
                pass

            if event.type == pg.KEYDOWN:
                pass

            # Zoom in/out with mouse wheel
            if event.type == pg.MOUSEWHEEL:
                self.viewport.handle_zoom(Vector2(pg.mouse.get_pos()), event.precise_y)


        for i in range(40):
            for j in range(30):
                dpg.draw_rectangle((2 + 50 * i, 2 + 50 * j), (50 + 50 * i, 50 + 50 * j),
                                   fill=(75, 75, 75), color=(75, 75, 75), thickness=0.0, parent="drawlist")

        for cell in self.game.cells:
            dpg.draw_rectangle((2 + 50 * cell[0], 2 + 50 * cell[1]), (50 + 50 * cell[0], 50 + 50 * cell[1]),
                               fill=(255, 255, 255),
                               color=(255, 255, 255), thickness=0.0, parent="drawlist")

    def test(self, sender, app_data, user_data):
        print(sender, app_data, user_data)
        x,y =dpg.get_mouse_pos()
        cell = (x//50,(y-25)//50)
        if cell in self.game.cells:
            self.game.cells.remove(cell)
        else:
            self.game.cells.append(cell)
        self.update_drawlist()



class Game:
    def __init__(self):
        self.cells = [
            (0,0),
            (1,1),
            (2,2),
            (3,3),
            (4,4),
            (5,5),
            (6,6),
            (7,7),
            (8,8)
        ]

    def open(self, file_path):
        pass

    def save(self, file_path):
        pass


game = Game()
app = App(game)

theme = theme.theme_load()
dpg.bind_theme(theme)

dpg.set_viewport_resize_callback(app.update_drawlist_size)

dpg.set_frame_callback(0, app.update_drawlist_size)




dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()
dpg.set_primary_window(app.window, True)

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()
