from math import floor
import os
from tkinter import filedialog, messagebox
import pygame as pg
from pygame import Vector2


class Game:
    def __init__(self):
        # Chunk map stocks : {chunk_pos tuple (x_chunk, y_chunk): chunk (list of Vector2)}
        self.chunk_map = {}

    def open(self, file_path):
        # Load saved life simulation file here
        pass

    def save(self, file_path):
        """
        Save current simulation state in a file
        
        :param self: Description
        :param file_path: Description
        """
        # Check if file does not already exist
        
        if os.path.exists(file_path):
            if not messagebox.askyesno("Overwrite file?", "The file already exists. Do you want to overwrite it?"):
                return  # Do not overwrite
            
        # Save life simulation file here
        with open(file_path, 'wb') as f:
            pass

    def add_cell(self, cell: Vector2):
        """
        Add a cell to the simulation
        
        :param self: Description
        :param cell: Description
        :type cell: Vector2
        """
        cell_chunk_pos = self.get_chunk(cell)
        self.chunk_map[cell_chunk_pos].append(cell)

    def get_chunk(self, cell: Vector2) -> tuple:
        """
        Return the chunk position
        :param cell:
        :return:
        """
        chunk_pos = tuple(Vector2(floor(cell.x / 16), floor(cell.y / 16)))
        if chunk_pos not in self.chunk_map:
            self.chunk_map[chunk_pos] = []
        return chunk_pos


class App:
    def __init__(self, game_instance: Game, window_title="LifeGen", fps=60):
        self.temp = []
        pg.init()
        self.fps = fps
        self.clock = pg.time.Clock()
        self.is_running = True
        self.game = game_instance

        self.last_mouse_pos = Vector2(pg.mouse.get_pos())
        self.drag_delta = 0  # To detect if a click is a drag or a simple click

        # Window size and creation
        self.size = Vector2(1000, 800)
        self.screen = pg.display.set_mode(self.size, pg.RESIZABLE)

        # Viewport creation
        self.viewport = ViewPort(pos = Vector2(0, 50), size = self.size - Vector2(0, 50), screen = self.screen)

    def run(self):
        """Main application loop."""
        while self.is_running:
            self.screen.fill((0, 0, 0))

            # Draw viewport area and rectangles
            self.viewport.draw((50, 50, 50))
            self.viewport.draw_grid()
            
            for cell in self.temp:
                self.viewport.draw_rect((255, 255, 255), cell, cell+Vector2(1, 1))

            # Limit FPS and update screen
            self.clock.tick(self.fps)
            pg.display.flip()

            # Process incoming events
            self.handle_events(pg.event.get())

    def handle_events(self, events):
        """Handle all pygame events."""
        for event in events:
            if event.type == pg.QUIT:
                print(self.game.chunk_map)
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
                    self.game.add_cell(val)
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
    def __init__(self, pos, size, screen):
        # Coordinate space visible inside viewport (world coordinates)
        self.start_pos = Vector2(-16, -36 / 3)
        self.end_pos = Vector2(16, 36 / 3)

        # Actual pixel position and size on screen
        self.viewport_pos = pos or Vector2(0, 0)
        self.viewport_size = size or Vector2(1000, 800)
        self.screen = screen

        self.dragging = False

    def viewport_to_screen(self, pos: Vector2) -> Vector2:
        """
        Convert a coordinate in world-space to a pixel coordinate on screen.
        Performs linear interpolation from world-space to screen-space.

        :param pos: World-space position
        :return: Screen-space position
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

        :param pos: Screen-space position
        :return: World-space position
        """
        relative_pos = Vector2(
            (pos.x - self.viewport_pos.x) / self.viewport_size.x,
            (pos.y - self.viewport_pos.y) / self.viewport_size.y
        )

        return Vector2(
            (self.end_pos.x - self.start_pos.x) * relative_pos.x + self.start_pos.x,
            (self.end_pos.y - self.start_pos.y) * relative_pos.y + self.start_pos.y,
        )

    def draw(self, background_color):
        """Draw the viewport boundary (simple rectangle).
        
        :param screen: Pygame surface to draw on
        :param background_color: Background color of the viewport
        """
        pg.draw.rect(self.screen, background_color, (self.viewport_pos, self.viewport_size))
    
    def draw_grid(self):
        for row in range(int(self.start_pos.x)-5, int(self.end_pos.x)+5, 1):
                for col in range(int(self.start_pos.y)-5, int(self.end_pos.y)+5, 1):
                    self.draw_rect( 
                        (0, 0, 0), 
                        Vector2(row + 0.05, col + 0.05),
                        Vector2(row + 1, col + 1))

    def handle_zoom(self, mouse_pos: Vector2, zoom_value: int | float):
        """
        Zoom in/out around the mouse cursor.
        Positive = zoom in, Negative = zoom out.
        Zooming scales the world-space rectangle (start_pos → end_pos)
        relative to cursor position to give intuitive zoom behavior.

        :param mouse_pos: Mouse position in screen coordinates
        :param zoom_value: Zoom amount (positive or negative)
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
        """Drag-to-pan.
        
        :param mouse_pos: Current mouse position in screen coordinates
        :param last_mouse_pos: Last mouse position in screen coordinates"""
        world_mouse_pos = self.screen_to_viewport(mouse_pos)
        world_last_mouse_pos = self.screen_to_viewport(last_mouse_pos)

        self.start_pos += world_last_mouse_pos - world_mouse_pos
        self.end_pos += world_last_mouse_pos - world_mouse_pos

    def draw_rect(self, color, pos1, pos2):
        """Draw a red rectangle using world coordinates."""
        screen_pos1 = self.viewport_to_screen(pos1)
        screen_pos2 = self.viewport_to_screen(pos2)
        pg.draw.rect(self.screen, color,
                     (screen_pos1, screen_pos2 - screen_pos1))


game = Game()
app = App(game)
app.run()
