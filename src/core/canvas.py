"""
Canvas rendering system for terminal output.
Provides the core rendering functionality for the animation engine.
Based on the reference implementation with optimized rendering.
"""

import os
import sys
from bisect import insort_right, bisect_right
from platform import system as system_type
from typing import List, Optional, Tuple
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform color support
init()


class Vector2:
    """2D vector for position coordinates."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x + other, self.y + other)
        else:
            raise ValueError("Accepted data types are float, int and Vector2.")
    
    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x - other, self.y - other)
        else:
            raise ValueError("Accepted data types are float, int and Vector2.")
    
    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        else:
            raise ValueError("Accepted data types are float, int and Vector2.")
    
    def __truediv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x / other, self.y / other)
        else:
            raise ValueError("Accepted data types are float, int and Vector2.")
    
    def __floordiv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)
        elif isinstance(other, (int, float)):
            return Vector2(self.x // other, self.y // other)
        else:
            raise ValueError("Accepted data types are float, int and Vector2.")
    
    def __pos__(self):
        return Vector2(abs(self.x), abs(self.y))
    
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def magnitude(self):
        return ((self.x ** 2) + (self.y ** 2)) ** 0.5


class RenderSection:
    """A section of text to be rendered with specific styling."""
    
    id_inc = 0
    
    def __init__(self, string, start, code):
        self.id = RenderSection.id_inc
        RenderSection.id_inc += 1
        
        self.string = string
        self.start = start
        self.length = len(self.string)
        self.end = self.start + self.length
        self.code = code
    
    def __lt__(self, other):
        return self.start < other
    
    def __gt__(self, other):
        return self.start > other
    
    def add_char(self, char):
        self.string += char
        self.end += 2
        self.length += 2
    
    def mod_char(self, char, loc):
        if loc == self.end:
            self.add_char(char)
        else:
            self.string = self.string[:loc] + char + self.string[loc + 2:]
    
    def add_section(self, other):
        diff = other.start - self.start
        self.string = self.string[:diff] + other.string + self.string[diff + other.length:]
        self.length = len(self.string)
        self.start = min(other.start, self.start)
        self.end = self.start + self.length
    
    def add_section_below(self, other):
        diff = self.start - other.start
        self.string = other.string[:diff] + self.string + other.string[diff + self.length:]
        self.length = len(self.string)
        self.start = min(other.start, self.start)
        self.end = self.start + self.length
    
    def subtract_char(self, loc):
        first = None
        last = None
        if loc > self.start:
            diff = loc - self.start
            first = RenderSection(self.string[:diff], self.start, self.code)
        
        if loc < self.end:
            diff = self.end - loc
            last = RenderSection(self.string[diff:], loc + 2, self.code)
        
        return first, last
    
    def subtract_section(self, other):
        first = None
        last = None
        if other.start > self.start:
            diff = other.start - self.start
            first = RenderSection(self.string[:diff], self.start, self.code)
        
        if other.end < self.end:
            diff = self.end - other.end
            last = RenderSection(self.string[self.length - diff:], other.end, self.code)
        
        return first, last


class Layer:
    """A single rendering layer."""
    
    def __init__(self, layer_id, dimensions):
        self.dimensions = Vector2(dimensions.x * 2, dimensions.y)
        self.max_loc = self.dimensions.x * self.dimensions.y
        
        self.id = layer_id
        self.new_groups = []
        self.full_str = ["" for i in range(self.dimensions.x * self.dimensions.y)]
    
    def set_char(self, loc, char, code):
        """Set a single character in the layer."""
        if loc >= self.max_loc or loc < 0:
            return
        
        # Find the rightmost value less than or equal to loc
        i = bisect_right(self.new_groups, loc) - 1
        if i >= len(self.new_groups) or i < 0:
            i = None
        else:
            # Check backwards for same start location
            while i >= 1 and self.new_groups[i - 1].start == loc:
                i -= 1
        
        if i is not None:
            insert_group = self.new_groups[i]
            
            if insert_group.end >= loc:
                if insert_group.code != code:
                    sub_groups = insert_group.subtract_char(loc)
                    self.new_groups.pop(i)
                    
                    if sub_groups[0]:
                        insort_right(self.new_groups, sub_groups[0])
                    if sub_groups[1]:
                        insort_right(self.new_groups, sub_groups[1])
                    
                    i = None
                else:
                    insert_group.mod_char(char, loc)
            else:
                i = None
        
        if i is None:
            insort_right(self.new_groups, RenderSection(char, loc, code))
        
        self.full_str[loc] = code + char
    
    def set_string(self, loc, string, code):
        """Set a string in the layer."""
        if loc >= self.max_loc or loc < 0:
            return
        
        start_i = bisect_right(self.new_groups, loc) - 1
        if start_i < 0:
            start_i = 0
        
        while start_i >= 1 and self.new_groups[start_i - 1].start == loc:
            start_i -= 1
        
        cut_string = string[:self.max_loc - loc]
        add_group = RenderSection(cut_string, loc, code)
        add_groups = [None, add_group, None]
        remove = []
        
        for mid_i in range(start_i, len(self.new_groups)):
            mid_group = self.new_groups[mid_i]
            
            if mid_group.start >= add_group.end:
                break
            
            if mid_group.end > add_group.start:
                if mid_group.start >= add_group.start and mid_group.end <= add_group.end:
                    remove.append(mid_i)
                else:
                    if mid_group.code == add_group.code:
                        add_group.add_section_below(mid_group)
                        remove.append(mid_i)
                    else:
                        sub_groups = mid_group.subtract_section(add_group)
                        if sub_groups[0]:
                            add_groups[0] = sub_groups[0]
                        if sub_groups[1]:
                            add_groups[2] = sub_groups[1]
                        remove.append(mid_i)
        
        remove.reverse()
        for index in remove:
            self.new_groups.pop(index)
        
        add_index = bisect_right(self.new_groups, loc)
        for group in add_groups:
            if group:
                self.new_groups.insert(start_i + add_index, group)
                add_index += 1
        
        for index, char in enumerate(string):
            if loc + index < len(self.full_str):
                self.full_str[loc + index] = code + char


class Canvas:
    """Main canvas for rendering terminal animations."""
    
    def __init__(self, width: int, height: int, layers: int = 5, merge_rules=None):
        self.dimensions = Vector2(width, height)
        self.num_layers = layers
        self.layers = [Layer(i, self.dimensions) for i in range(layers)]
        self.merge_rules = merge_rules or []
        self.edits_this_frame = 0
    
    def set_char(self, layer: int, location: Vector2, char: str, code: str = ""):
        """Set a character at a specific position and layer."""
        if 0 <= layer < self.num_layers:
            loc = int(location.x * 2) + (location.y * self.dimensions.x * 2)
            self.layers[layer].set_char(loc, char, code)
            self.edits_this_frame += 1
    
    def set_string(self, layer: int, location: Vector2, string: str, code: str = ""):
        """Set a string starting at a specific position."""
        if 0 <= layer < self.num_layers:
            loc = int(location.x * 2) + (location.y * self.dimensions.x * 2)
            self.layers[layer].set_string(loc, string, code)
            self.edits_this_frame += 1
    
    def set_multiline_string(self, layer: int, position: Vector2, text: str, color: str = ""):
        """Set a multiline string starting at a specific position."""
        lines = text.split('\n')
        for line_offset, line in enumerate(lines):
            line_pos = Vector2(position.x, position.y + line_offset)
            if line_pos.y >= self.dimensions.y:
                break
            self.set_string(layer, line_pos, line, color)
    
    def get_char(self, layer: int, position: Vector2) -> str:
        """Get a character from a specific position and layer."""
        if (0 <= layer < self.num_layers and 
            0 <= position.x < self.dimensions.x and 
            0 <= position.y < self.dimensions.y):
            loc = int(position.x * 2) + (position.y * self.dimensions.x * 2)
            if 0 <= loc < len(self.layers[layer].full_str):
                return self.layers[layer].full_str[loc]
        return ' '
    
    def fill_rectangle(self, layer: int, position: Vector2, size: Vector2, char: str, color: str = ""):
        """Fill a rectangle with a character."""
        for y in range(size.y):
            for x in range(size.x):
                fill_pos = Vector2(position.x + x, position.y + y)
                if (fill_pos.x >= self.dimensions.x or fill_pos.y >= self.dimensions.y):
                    break
                self.set_char(layer, fill_pos, char, color)
    
    def draw_border(self, layer: int, position: Vector2, size: Vector2, 
                   border_chars: str = "+-+||+-+", color: str = ""):
        """Draw a border around a rectangle."""
        # Parse border characters: top-left, top, top-right, left, right, bottom-left, bottom, bottom-right
        if len(border_chars) == 8:
            tl, t, tr, l, r, bl, b, br = border_chars
        else:
            tl = t = tr = l = r = bl = b = br = border_chars[0] if border_chars else '#'
        
        # Top and bottom borders
        for x in range(size.x):
            self.set_char(layer, Vector2(position.x + x, position.y), 
                         tl if x == 0 else (tr if x == size.x - 1 else t), color)
            self.set_char(layer, Vector2(position.x + x, position.y + size.y - 1), 
                         bl if x == 0 else (br if x == size.x - 1 else b), color)
        
        # Left and right borders
        for y in range(1, size.y - 1):
            self.set_char(layer, Vector2(position.x, position.y + y), l, color)
            self.set_char(layer, Vector2(position.x + size.x - 1, position.y + y), r, color)
    
    def clear_layer(self, layer: int):
        """Clear a specific layer."""
        if 0 <= layer < self.num_layers:
            self.layers[layer].set_string(0, " " * self.dimensions.x * self.dimensions.y, "")
    
    def clear_all(self):
        """Clear all layers."""
        for layer in range(self.num_layers):
            self.clear_layer(layer)
    
    def render_blank(self):
        """Render a blank screen."""
        print("\033[1;1H\033[1;37;40m" + (("  " * self.dimensions.x + "\n") * self.dimensions.y))
    
    def render_all(self):
        """Render all layers to the terminal."""
        # Merge layers from bottom to top then render the resulting group list
        total_string = "\033[1;1H\033[1;39m"
        
        # Process all layers, starting from the bottom
        for layer in self.layers:
            for group in layer.new_groups:
                lineno = group.start // (self.dimensions.x * 2)
                add_string = ""
                add_string += "\033[{};{}H".format(
                    lineno + 1, group.start % (self.dimensions.x * 2) + 1
                )
                
                add_string += group.code
                
                offset = group.start % (self.dimensions.x * 2)
                # If overrun is greater than x, then it breaks a line boundary
                split = 0
                stop = 0
                while stop <= group.length:
                    if lineno >= self.dimensions.y:
                        break
                    
                    stop = (self.dimensions.x * 2) - offset + split
                    add_string += group.string[split:stop] + ("\n" if stop <= group.length else "")
                    offset = 0
                    lineno += 1
                    split += stop - split
                
                total_string += add_string
            
            # Clear the layer's groups after rendering
            layer.new_groups.clear()
        
        self.edits_this_frame = 0
        print(total_string + "\033[27;0H", end="\n")
    
    def render(self, clear_screen: bool = True):
        """Render the canvas to the terminal."""
        self.render_all()
    
    def get_terminal_size(self) -> Vector2:
        """Get the terminal size."""
        try:
            import shutil
            size = shutil.get_terminal_size()
            return Vector2(size.columns, size.lines)
        except:
            return Vector2(80, 24)  # Default fallback


def enable_ansi():
    """
    Uses a hack to enable ANSI mode in the Windows console. Does nothing on Linux.
    """
    if system_type() == "Windows":
        # Enable ANSI escape sequence support
        os.system("") 