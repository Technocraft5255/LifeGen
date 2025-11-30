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


class ViewPort:
    def __init__(self, pos, size):
        # Coordinate space visible inside viewport (world coordinates)
        self.start_pos = Vector2(-16, -36 / 3)
        self.end_pos = Vector2(16, 36 / 3)

        # Actual pixel position and size on screen
        self.viewport_pos = pos or Vector2(0, 0)
        self.viewport_size = size or Vector2(1000, 800)

    def viewport_to_screen(self, pos: Vector2):
        """
        Convert a coordinate in world-space to a pixel coordinate on screen.
        Performs linear interpolation from world-space to screen-space.
        """
        return Vector2(
            (pos.x - self.start_pos.x) /
            (self.end_pos.x - self.start_pos.x) * self.viewport_size.x + self.viewport_pos.x,
            (pos.y - self.start_pos.y) /
            (self.end_pos.y - self.start_pos.y) * self.viewport_size.y + self.viewport_pos.y
        )

    def screen_to_viewport(self, pos: Vector2):
        """
        Convert a pixel coordinate on screen to world-space coordinates.
        """
        relative_pos = Vector2(
            (pos.x - self.viewport_pos.x) / self.viewport_size.x,
            (pos.y - self.viewport_pos.y) / self.viewport_size.y
        )

        return Vector2(
            (self.end_pos.x - self.start_pos.x) * relative_pos.x + self.start_pos.x,
            (self.end_pos.y - self.start_pos.y) * relative_pos.y + self.start_pos.y,
        )

    def draw(self, screen):
        """Draw the viewport boundary (simple white rectangle)."""
        pg.draw.rect(screen, (255, 255, 255), (self.viewport_pos, self.viewport_size))

    def handle_zoom(self, mouse_pos: Vector2, zoom_value: int | float):
        """
        Zoom in/out around the mouse cursor.
        Positive = zoom in, Negative = zoom out.
        Zooming scales the world-space rectangle (start_pos → end_pos)
        relative to cursor position to give intuitive zoom behavior.
        """
        # Adjust zoom speed differently depending on direction
        if zoom_value >= 0:
            zoom_value *= 0.5
        else:
            zoom_value *= 1 / 3

        # Convert mouse into world coordinates
        viewport_mouse_pos = self.screen_to_viewport(mouse_pos)

        # Vectors from mouse to viewport boundaries
        to_start_pos_vector = self.start_pos - viewport_mouse_pos
        to_end_pos_vector = self.end_pos - viewport_mouse_pos

        # Apply zoom by scaling these vectors
        self.start_pos += to_start_pos_vector * zoom_value
        self.end_pos += to_end_pos_vector * zoom_value

        # Cleanup temporary objects
        del to_start_pos_vector, to_end_pos_vector, viewport_mouse_pos

    def handle_drag(self):
        """Drag-to-pan (not implemented yet)."""
        pass

    def draw_rect(self, screen, pos1, pos2):
        """Draw a red rectangle using world coordinates."""
        screen_pos1 = self.viewport_to_screen(pos1)
        screen_pos2 = self.viewport_to_screen(pos2)
        pg.draw.rect(screen, (255, 0, 0),
                     (screen_pos1, screen_pos2 - screen_pos1))


game = Game()
app = App(game)
app.run()
