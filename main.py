from math import floor
import os
from tkinter import filedialog, messagebox
import pygame as pg
from pygame import Vector2


class Game:
    def __init__(self):
        # Chunk map stocks : {chunk_pos tuple (x_chunk, y_chunk): chunk (list of Vector2)}
        self.chunk_map = {}
        self.computed_chunk_map = {}
        self.save_file_path = ""

    def open(self):
        """
        Docstring for open
        
        :param self: Description
        :param file_path: Description
        """
        file_path = filedialog.askopenfilename(filetypes=[("LifeGen files", "*.life"), ("All files", "*.*")])
        if not file_path:
            return  # No file path selected
        
        self.save_file_path = file_path
        
        # Load life simulation file here
        with open(file_path, 'rb') as f:
                signature = f.read(4)
                if signature != b'LG10':
                    messagebox.showerror("Invalid file", "The selected file is not a valid LifeGen file.")
                    return
                self.chunk_map = {}
                while True:
                    cell_data = f.read(8)
                    if not cell_data:
                        break  # End of file
                    cell_x = int.from_bytes(cell_data[:4], 'little', signed=True)
                    cell_y = int.from_bytes(cell_data[4:], 'little', signed=True)
                    self.add_cell(Vector2(cell_x, cell_y))
        pass

    def save(self, save_as=False):
        """
        Save current simulation state in a file after asking for overwrite if file exists
        
        :param self: Description
        :param file_path: Description
        """
        if not save_as and self.save_file_path != "":
            file_path = self.save_file_path
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".life",
                                                             filetypes=[("LifeGen files", "*.life"),
                                                                        ("All files", "*.*")])
            if not file_path:
               return  # No file path selected
            
            # Check if file does not already exist
            if os.path.exists(file_path):
                if not messagebox.askyesno("Overwrite file?", "The file already exists. Do you want to overwrite it?"):
                  return  # Do not overwrite
            
        # Save life simulation file here
        with open(file_path, 'wb') as f:
            f.write(b'LG10')  # File signature (Life Gen v1.0)
            for chunk_pos, cells in self.chunk_map.items():
                for cell in cells:
                    f.write(int(cell.x).to_bytes(4, 'little', signed=True))
                    f.write(int(cell.y).to_bytes(4, 'little', signed=True))
    
    def update_chunk_map(self):
        """
        Update the chunk map
        """
        self.chunk_map = self.computed_chunk_map
        self.computed_chunk_map = {}
    
    def clear(self):
        """
        Clear the simulation
        """
        self.computed_chunk_map = {}
        self.update_chunk_map()

    def toggle_cell(self, cell: Vector2):
        """
        Toggle a cell in the simulation
        
        :param self: Description
        :param cell: Description
        :type cell: Vector2
        """
        cell_chunk_pos = self.get_chunk(cell)
        if cell in self.chunk_map[cell_chunk_pos]:
            self.chunk_map[cell_chunk_pos].remove(cell)
        else:
            self.chunk_map[cell_chunk_pos].append(cell)

    def add_cell(self, cell: Vector2, computed=False):
        """
        Add a cell to the simulation
        
        :param self: Description
        :param cell: Description
        :type cell: Vector2
        """
        cell_chunk_pos = self.get_chunk(cell)
        if computed:
            if cell_chunk_pos not in self.computed_chunk_map:
                self.computed_chunk_map[cell_chunk_pos] = []
            self.computed_chunk_map[cell_chunk_pos].append(cell)
        else:
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
    
    def get_cell_state(self, cell: Vector2) -> bool:
        """
        Return whether a cell is alive or dead
        
        :param self: Description
        :param cell: Description
        :type cell: Vector2
        :return: True if cell is alive, False otherwise
        :rtype: bool
        """
        cell_chunk_pos = self.get_chunk(cell)
        return cell in self.chunk_map[cell_chunk_pos]
    
    def get_cell_neighbors(self, cell_x: int, cell_y: int) -> list[Vector2]:
        """
        Get the neighbors of a cell
        
        :param self: Description
        :param cell_x: Description
        :param cell_y: Description
        :return: List of neighbor cells
        :rtype: list
        """
        neighbors = []
        
        # Check if any cell neighbors are in another chunk
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip the cell itself
                if self.get_cell_state(Vector2(cell_x + dx, cell_y + dy)):
                    neighbors.append(Vector2(cell_x + dx, cell_y + dy))
        return neighbors

    def compute_next_generation(self):
        """
        Compute the next generation of the simulation
        """
        # Implement the rules of the life simulation here
        chunks_to_compute = set()
        for chunk_pos, cells in self.chunk_map.items():
            # Add neighboring chunks to compute list
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if (chunk_pos[0] + dx, chunk_pos[1] + dy) not in chunks_to_compute:
                        chunks_to_compute.add((chunk_pos[0] + dx, chunk_pos[1] + dy))
        for chunk_pos in chunks_to_compute:
            for x in range(16):
                for y in range(16):
                    neighbors_number = len(self.get_cell_neighbors(chunk_pos[0]*16+x, chunk_pos[1]*16+y))
                    if neighbors_number  in [2, 3] and self.get_cell_state(Vector2(chunk_pos[0]*16+x, chunk_pos[1]*16+y)):
                        self.add_cell(Vector2(chunk_pos[0]*16+x, chunk_pos[1]*16+y), computed=True)
                    elif neighbors_number == 3:
                        self.add_cell(Vector2(chunk_pos[0]*16+x, chunk_pos[1]*16+y), computed=True)


class MenuBar:
    def __init__(self, screen: pg.Surface, size):
        self.screen = screen
        self.size = Vector2(size)
        self.font = pg.font.Font("C:/Windows/Fonts/segoeui.ttf", 12)
        self.menus = list[Menu]()
        self.active = False
        self.active_menu = None
        self.hovered_menu = None

    def draw(self):
        """
        Draw the menu bar and its menus
        
        :param self: Description
        """
        pg.draw.rect(self.screen, "#EEEEEE", (0, 0, self.size.x, 24))

        offset = 5
        for menu in self.menus:
            menu_text = menu.get_text()
            if self.hovered_menu == menu:
                pg.draw.rect(self.screen, "#C8C8C8",
                             (menu_text.get_offset() + Vector2(offset - 5, 0), menu_text.get_size() + Vector2(8, 7)))
            self.screen.blit(menu_text, (offset, 3))
            if self.active_menu == menu and self.active:
                menu.draw(self.screen, Vector2(offset - 5, 24))
            offset += menu.get_rect().width + 8
        del offset

    def add_menu(self, menu):
        """
        Add a menu to the menu bar
        
        :param self: Description
        :param menu: Description
        """
        self.menus.append(menu)

    def get_collision_box(self):
        return pg.Rect(0, 0, self.screen.get_width(), 24)

    def handle_events(self, event: pg.event.Event, keyboard: pg.key, mouse: pg.mouse):
        """
        Handle events for the menu bar like clicksn, hovers and events on sub-menus
        
        :param self: Description
        :param event: Description
        :type event: pg.event.Event
        :param keyboard: Description
        :type keyboard: pg.key
        :param mouse: Description
        :type mouse: pg.mouse
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            # check press on menubar
            if self.get_collision_box().collidepoint(mouse.get_pos()):
                offset = 5
                for menu in self.menus:
                    rect = menu.get_rect()
                    rect.x += offset
                    if rect.collidepoint(mouse.get_pos()):
                        if not self.active:
                            self.active = True
                            self.active_menu = menu
                        else:
                            self.active = False
                    offset += rect.width + 8
                del offset
            # check press on the active menu
            elif self.active:
                if self.active_menu.get_menu_rect().collidepoint(mouse.get_pos()):
                    self.active_menu.handle_event("press", mouse)
                else:
                    self.active = False
                    self.hovered_menu = None
            else:
                self.active = False
                self.hovered_menu = None
        if event.type == pg.MOUSEMOTION:
            offset = 5
            self.hovered_menu = None
            for menu in self.menus:
                rect = menu.get_rect()
                rect.x += offset
                if rect.collidepoint(mouse.get_pos()):
                    if self.active:
                        self.active_menu = menu
                    self.hovered_menu = menu
                offset += rect.width + 8
            del offset
            if self.active:
                self.hovered_menu = self.active_menu
                self.active_menu.handle_event("active", mouse)

    def resize(self, size):
        """
        Handle the menu bar resizing on window resize
        
        :param self: Description
        :param size: Description
        """
        self.size = size


class Menu:
    def __init__(self, name, theme):
        self.name = name
        self.theme = theme
        self.font = pg.font.Font("C:/Windows/Fonts/segoeui.ttf", 12)
        self.text = self.font.render(self.name, 1, "#000000")
        self.commands = {}
        self.menu_rect = pg.Rect(0, 0, 0, 0)
        self.pos = Vector2(0, 0)
        self.width = 0

    def get_rect(self):
        """
        Get the collision box rectangle of the menu text
        
        :param self: Description
        """
        return self.text.get_rect()

    def get_menu_rect(self):
        """
        Get the collision box rectangle of the menu dropdown
        
        :param self: Description
        """
        return self.menu_rect

    def get_text(self):
        """
        Get the rendered text surface of the menu
        
        :param self: Description
        """
        return self.text

    def add_command(self, name: str, command: object):
        """
        Add a command to the menu
        
        :param self: Description
        :param name: Description
        :type name: str
        :param command: Description
        :type command: object
        """
        self.commands[name] = {"command": command,
                               "rendered_text": self.font.render(name, 1, "#000000"),
                               "active": False}

    def draw(self, screen, pos: Vector2):
        """
        Draw the menu dropdown on click at given position
        
        :param self: Description
        :param screen: Description
        :param pos: Description
        :type pos: Vector2
        """
        self.pos = pos
        self.menu_rect = pg.Rect(0, 0, 0, 0)
        texts = list[pg.Surface]()
        self.width = 0
        height_sum = 1
        for name, data in self.commands.items():
            text = data["rendered_text"]
            texts.append(text)
            self.width = max(self.width, text.get_rect().width)
            height_sum += text.get_rect().height + 2
            del text
        self.menu_rect = pg.Rect((self.pos, (self.width + 20, height_sum)))
        pg.draw.rect(screen, "#EEEEEE", self.menu_rect)

        offset = Vector2(5, 1)
        for name, data in self.commands.items():
            text_rect = data["rendered_text"].get_rect()
            if data["active"]:
                pg.draw.rect(screen, "#C8C8C8", (
                    text_rect.x + offset.x + pos.x - 5,
                    text_rect.y + offset.y + pos.y - 1,
                    self.width + 20,
                    text_rect.h + 3))
            screen.blit(data["rendered_text"], self.pos + offset)
            offset.y += data["rendered_text"].get_rect().height + 2
        del offset, text_rect, height_sum

    def handle_event(self, event, mouse):
        offset = Vector2(5, 1)
        for name, data in self.commands.items():
            text_rect = data["rendered_text"].get_rect()
            if pg.Rect(
                    (text_rect.x + offset.x + self.pos.x - 5, text_rect.y + offset.y + self.pos.y - 1, self.width + 20,
                     text_rect.h + 2)).collidepoint(mouse.get_pos()):
                if event == "press":
                    data["command"]()
                elif event == "active":
                    data["active"] = True
            else:
                data["active"] = False

            offset.y += text_rect.height + 2
        del offset


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
        self.draw_grid()
    
    def draw_grid(self):
        """for row in range(int(self.start_pos.x)-5, int(self.end_pos.x)+5, 1):
                for col in range(int(self.start_pos.y)-5, int(self.end_pos.y)+5, 1):
                    self.draw_rect( 
                        (0, 0, 0), 
                        Vector2(row + 0.05, col + 0.05),
                        Vector2(row + 1, col + 1))
        """
        for row in range(int(self.start_pos.x)-5, int(self.end_pos.x)+5, 1):
            if self.viewport_size.x / (self.end_pos.x - self.start_pos.x) > 10:  # Only draw grid if zoomed in enough
                pg.draw.rect(self.screen, (50, 50, 50), (self.viewport_to_screen(Vector2(row + -0.025, self.start_pos.y)), (self.viewport_to_screen(Vector2(row + 0.025, self.end_pos.y))) - self.viewport_to_screen(Vector2(row + -0.025, self.start_pos.y))), 0)
        
        for col in range(int(self.start_pos.y)-5, int(self.end_pos.y)+5, 1):
            """self.draw_rect( 
                (50, 50, 50), 
                Vector2(self.start_pos.x, col + -0.025),
                Vector2(self.end_pos.x, col + 0.025))"""
            pg.draw.rect(self.screen, (50, 50, 50), (self.viewport_to_screen(Vector2(self.start_pos.x, col + -0.025)), (self.viewport_to_screen(Vector2(self.end_pos.x, col + 0.025))) - self.viewport_to_screen(Vector2(self.start_pos.x, col + -0.025))), 0)


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
        screen_pos1.x, screen_pos1.y = floor(screen_pos1.x), floor(screen_pos1.y)
        screen_pos2.x, screen_pos2.y = floor(screen_pos2.x), floor(screen_pos2.y)
        pg.draw.rect(self.screen, color,
                     (screen_pos1, screen_pos2 - screen_pos1))


class Button:
    def __init__(self, screen, width, height, text, background_color, foreground_color):
        self.screen = screen
        self.active = False
        self.state = False

    def draw(self):
        pass

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.on_press()
            self.active  = True
            self.state = True

    
    def get_collision_box(self):
        pass

    def get_state(self):
        pass

    def on_press(self):
        pass

    def on_release(self):
        pass


class Slider:
    def __init__(self):
        pass
    
    def draw(self):
        pass

    def handle_event(self, event):
        pass

    def get_collision_box(self):
        pass

    def get_value(self):
        pass

class Label:
    def __init__(self):
        pass

    def draw(self):
        pass

    def handle_event(self, event):
        pass

    def get_collision_box(self):
        pass


class App:
    def __init__(self, game_instance: Game, window_title="LifeGen", fps=60):
        pg.init()
        self.fps = fps
        self.clock = pg.time.Clock()
        self.tick_event = pg.USEREVENT + 1
        pg.time.set_timer(self.tick_event, 1000//20)  # Set timer to trigger every 1/20th of a second
        self.is_running = True
        self.game = game_instance

        """for i in range(-50, 50):
            for j in range(-50, 50):
                if random.random() < 0.5:
                    self.game.add_cell(Vector2(i, j))"""

        self.last_mouse_pos = Vector2(pg.mouse.get_pos())
        self.drag_delta = 0  # To detect if a click is a drag or a simple click

        # Window size and creation
        self.size = Vector2(1000, 800)
        self.screen = pg.display.set_mode(self.size, pg.RESIZABLE)

        # Set window title
        pg.display.set_caption(window_title)

        # Viewport creation
        self.viewport = ViewPort(pos = Vector2(0, 50), size = self.size - Vector2(0, 50), screen = self.screen)

        # Menu bar creation
        self.menubar = MenuBar(self.screen, Vector2(self.size.x, 24))
        file_menu = Menu("File", theme={})
        file_menu.add_command("New", lambda: print("New file"))
        file_menu.add_command("Save", self.game.save)
        file_menu.add_command("Save As", lambda :self.game.save(save_as=True))
        file_menu.add_command("Open", self.game.open)
        file_menu.add_command("Examples", lambda: print("Open examples"))
        file_menu.add_command("Preferences", lambda: print("Open settings"))
        file_menu.add_command("Exit", lambda: (pg.quit(), exit(0)))
        self.menubar.add_menu(file_menu)
        edit_menu = Menu("Edit", theme={})
        edit_menu.add_command("Undo", lambda: print("Undo action"))
        edit_menu.add_command("Redo", lambda: print("Redo action"))
        edit_menu.add_command("Clear world", lambda: self.game.clear())
        edit_menu.add_command("Randomize chunk", lambda: print("Randomize chunk"))
        self.menubar.add_menu(edit_menu)
        sim_menu = Menu("Simulation", theme={})
        sim_menu.add_command("Next Generation", lambda: (self.game.compute_next_generation(), self.game.update_chunk_map()))
        sim_menu.add_command("Start simulation", lambda: print("Start simulation"))
        sim_menu.add_command("Pause simulation", lambda: print("Pause simulation"))
        self.menubar.add_menu(sim_menu)
        about_menu = Menu("About", theme={})
        about_menu.add_command("About LifeGen", lambda: messagebox.showinfo("About LifeGen", "LifeGen v1.0\nA simple life simulation application."))
        about_menu.add_command("Help", lambda: messagebox.showinfo("Help", "Use mouse to pan and zoom.\nClick to toggle cells.\nSpace to advance one generation.\nCtrl+S to save."))
        about_menu.add_command("Check for updates", lambda: print("Check for updates"))
        about_menu.add_command("Report a bug", lambda: print("Report a bug"))
        self.menubar.add_menu(about_menu)
        


    def run(self):
        """Main application loop."""
        while self.is_running:
            self.screen.fill((0, 0, 0))

            # Draw viewport area and rectangles
            self.viewport.draw((0, 0, 0))
            
            
            
            # Draw all cells  TODO: Optimize drawing by only drawing visible chunks
            for chunk_pos, cells in self.game.chunk_map.items():
                for cell in cells:
                    self.viewport.draw_rect((255, 255, 255), cell, cell+Vector2(1.005, 1.005))

            # Draw menu bar
            self.menubar.draw()


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
                self.viewport.dragging = True
                self.last_mouse_pos = Vector2(pg.mouse.get_pos())
                self.drag_delta = 0

            elif event.type == pg.MOUSEBUTTONUP:
                self.viewport.dragging = False
                if self.drag_delta < 2 and event.button == 1:
                    cell_pos = self.viewport.screen_to_viewport(Vector2(pg.mouse.get_pos()))
                    cell_pos.x = floor(cell_pos.x)
                    cell_pos.y = floor(cell_pos.y)
                    self.game.toggle_cell(cell_pos)

            elif event.type == pg.MOUSEMOTION:
                if self.viewport.dragging:
                    self.viewport.handle_drag(Vector2(pg.mouse.get_pos()), self.last_mouse_pos)
                    self.drag_delta += (self.last_mouse_pos - Vector2(pg.mouse.get_pos())).length()
                    self.last_mouse_pos = Vector2(pg.mouse.get_pos())

            # Zoom in/out with mouse wheel
            elif event.type == pg.MOUSEWHEEL:
                self.viewport.handle_zoom(Vector2(pg.mouse.get_pos()), event.precise_y)

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.game.compute_next_generation() # Advance simulation by one generation
                    self.game.update_chunk_map()
                if event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_CTRL:
                    # Save file dialog
                    self.game.save()

            if event.type == pg.MOUSEBUTTONDOWN or self.menubar.active or self.menubar.get_collision_box().collidepoint(pg.mouse.get_pos()):
                self.menubar.handle_events(event, pg.key, pg.mouse)
            
            if event.type == self.tick_event:
                if pg.key.get_pressed()[pg.K_END]:  # If space is held down, keep advancing generations
                    self.game.compute_next_generation()
                    self.game.update_chunk_map()


game = Game()
app = App(game)
app.run()
