from math import floor
import pygame as pg
from pygame import Vector2


class Game:
    def __init__(self):
        # Chunk map stocks : {chunk_pos (Vector2): chunk (list of Vector2)}
        self.chunk_map = {}

    def open(self, file_path):
        # Load saved life simulation file here
        pass

    def save(self, file_path):
        # Save current simulation state in a file
        pass

    def add_cell(self, cell):
        cell_chunk = self.get_chunk(cell)
        cell_chunk.append(cell)

    def get_chunk(self, cell: Vector2) -> Vector2:
        chunk_pos = Vector2(floor(cell[0] / 16), floor(cell[1] / 16))
        if chunk_pos not in self.chunk_map:
            self.chunk_map[chunk_pos] = []
        return self.chunk_map[chunk_pos]


class App:
    def __init__(self, game_instance: Game):
        self.temp = []
        pg.init()
        self.fps = 60
        self.clock = pg.time.Clock()
        self.is_running = True
        self.game = game_instance

        # Window size and creation
        self.size = Vector2(1000, 800)
        self.SSAA_factor = 2

        self.SSAA_surface = pg.Surface(self.size * self.SSAA_factor)
        self.screen = pg.display.set_mode(self.size, pg.RESIZABLE)

        # Viewport creation
        self.viewport = ViewPort(Vector2(0, 50), self.size - Vector2(0, 50))

        self.last_mouse_pos = Vector2(pg.mouse.get_pos())
        self.drag_delta = 0  # To detect if a click is a drag or a simple click

    def run(self):
        """Main application loop."""
        while self.is_running:
            self.SSAA_surface.fill((0, 0, 0))

            # Draw viewport area and test rectangle
            self.viewport.draw(self.SSAA_surface, (50, 50, 50))
            for row in range(int(self.viewport.start_pos.x)-5, int(self.viewport.end_pos.x)+5, 1):
                for col in range(int(self.viewport.start_pos.y)-5, int(self.viewport.end_pos.y)+5, 1):
                    self.viewport.draw_rect(self.SSAA_surface, (0, 0, 0), Vector2(row + 0.05, col + 0.05),
                                            Vector2(row + 1, col + 1))
            for cell in self.temp:
                self.viewport.draw_rect(self.SSAA_surface, (255, 255, 255), cell, cell+Vector2(1, 1))

            # Limit FPS and update screen
            self.clock.tick(self.fps)
            self.screen.blit(pg.transform.smoothscale(
                self.SSAA_surface, self.size*self.SSAA_factor
            ), (0, 0))
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
                self.viewport.dragging = True
                self.last_mouse_pos = Vector2(pg.mouse.get_pos())
                self.drag_delta = 0

            if event.type == pg.MOUSEBUTTONUP:
                self.viewport.dragging = False
                if self.drag_delta < 2 and event.button == 1:
                    val = self.viewport.screen_to_viewport(Vector2(pg.mouse.get_pos()))
                    val.x = floor(val.x)
                    val.y = floor(val.y)
                    self.temp.append(val)
                    print("val", val)

            if event.type == pg.MOUSEMOTION:
                if self.viewport.dragging:
                    self.viewport.handle_drag(Vector2(pg.mouse.get_pos()), self.last_mouse_pos)
                    self.drag_delta += (self.last_mouse_pos - Vector2(pg.mouse.get_pos())).length()
                    self.last_mouse_pos = Vector2(pg.mouse.get_pos())

            # Zoom in/out with mouse wheel
            if event.type == pg.MOUSEWHEEL:
                self.viewport.handle_zoom(Vector2(pg.mouse.get_pos()), event.precise_y)

            if event.type == pg.KEYDOWN:
                pass


class ViewPort:
    def __init__(self, pos, size):
        # Coordinate space visible inside viewport (world coordinates)
        self.start_pos = Vector2(-16, -36 / 3)
        self.end_pos = Vector2(16, 36 / 3)

        # Actual pixel position and size on screen
        self.viewport_pos = pos or Vector2(0, 0)
        self.viewport_size = size or Vector2(1000, 800)

        self.dragging = False

    def viewport_to_screen(self, pos: Vector2) -> Vector2:
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

    def screen_to_viewport(self, pos: Vector2) -> Vector2:
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

    def draw(self, screen, background_color):
        """Draw the viewport boundary (simple white rectangle)."""
        pg.draw.rect(screen, background_color, (self.viewport_pos, self.viewport_size))

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
        # Apply zoom by scaling these vectors if zoom is not too high or too low
        if ((self.end_pos-self.start_pos).length() < 500 and zoom_value >= 0) or ((self.end_pos-self.start_pos).length() > 1 and zoom_value < 0):
            self.start_pos += to_start_pos_vector * zoom_value
            self.end_pos += to_end_pos_vector * zoom_value

        # Cleanup temporary objects
        del to_start_pos_vector, to_end_pos_vector, viewport_mouse_pos

    def handle_drag(self, mouse_pos: Vector2, last_mouse_pos: Vector2):
        """Drag-to-pan (not implemented yet)."""
        world_mouse_pos = self.screen_to_viewport(mouse_pos)
        world_last_mouse_pos = self.screen_to_viewport(last_mouse_pos)

        self.start_pos += world_last_mouse_pos - world_mouse_pos
        self.end_pos += world_last_mouse_pos - world_mouse_pos

    def draw_rect(self, screen, color, pos1, pos2):
        """Draw a red rectangle using world coordinates."""
        screen_pos1 = self.viewport_to_screen(pos1)
        screen_pos2 = self.viewport_to_screen(pos2)
        pg.draw.rect(screen, color,
                     (screen_pos1, screen_pos2 - screen_pos1))


game = Game()
app = App(game)
app.run()
