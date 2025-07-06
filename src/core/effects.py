"""
Visual effects library for terminal animations.
Contains common effects like typewriter, noise, waves, etc.
"""

import random
import time
from typing import List, Tuple, Optional
from colorama import Fore, Style

from .canvas import Canvas, Vector2


def typewriter_effect(canvas: Canvas, generator, layer: int, position: Vector2, 
                     color: str = Style.RESET_ALL, render: bool = True, 
                     speed: int = 3):
    """
    Create a typewriter effect with text appearing character by character.
    
    Expected generator data:
    - 'text': The text to type
    - 'offset': Current character offset (managed automatically)
    
    Args:
        speed: Characters per beat (default: 3)
    """
    text = generator.get_data('text')
    offset = generator.get_data('offset') or 0
    
    if not text:
        return
    
    # Handle special clear command
    if text.startswith('[##CLEAR|'):
        clear_bounds = text.split('|')[1].split(';')
        width, height = int(clear_bounds[0]), int(clear_bounds[1])
        
        if render:
            for y in range(height):
                clear_pos = Vector2(position.x, position.y + y)
                canvas.set_string(layer, clear_pos, ' ' * width, color)
        return
    
    # Process multiline text
    lines = text.split('\n')
    total_chars = 0
    
    for line_num, line in enumerate(lines):
        line_offset = offset - total_chars
        
        if 0 <= line_offset <= len(line):
            # Show characters up to offset
            visible_text = line[:line_offset]
            
            # Add cursor if not at end
            if line_offset < len(line):
                visible_text += '_'
            
            # Clean up special characters
            visible_text = visible_text.replace('~', '').replace('@', '')
            
            if render:
                line_pos = Vector2(position.x, position.y + line_num)
                canvas.set_string(layer, line_pos, visible_text, color)
        
        total_chars += len(line) + 1  # +1 for newline
    
    # Advance offset by speed (characters per beat)
    generator.set_data('offset', offset + speed)


def noise_effect(canvas: Canvas, layer: int, amount: int, 
                chars: str = "!@#$%^&*()_+-=[]{}|;':,.<>?/~`", 
                colors: Optional[List[str]] = None):
    """
    Create random noise effect by placing random characters at random positions.
    
    Args:
        canvas: Canvas to draw on
        layer: Layer to draw on
        amount: Number of noise characters to place
        chars: Characters to use for noise
        colors: List of colors to use (uses white if None)
    """
    if colors is None:
        colors = [Fore.WHITE]
    
    for _ in range(amount):
        pos = Vector2(
            random.randint(0, canvas.dimensions.x - 1),
            random.randint(0, canvas.dimensions.y - 1)
        )
        char = random.choice(chars)
        color = random.choice(colors)
        canvas.set_char(layer, pos, char, color)


def wave_effect(canvas: Canvas, layer: int, y: int, amplitude: int, 
               frequency: float, phase: float, char: str = '~', 
               color: str = Fore.BLUE):
    """
    Create a wave effect across the screen.
    
    Args:
        canvas: Canvas to draw on
        layer: Layer to draw on
        y: Base y position for the wave
        amplitude: Height of the wave
        frequency: Frequency of the wave
        phase: Phase offset for animation
        char: Character to use for the wave
        color: Color of the wave
    """
    import math
    
    for x in range(canvas.dimensions.x):
        wave_y = int(y + amplitude * math.sin(frequency * x + phase))
        if 0 <= wave_y < canvas.dimensions.y:
            canvas.set_char(layer, Vector2(x, wave_y), char, color)


def glitch_effect(canvas: Canvas, layer: int, intensity: int, 
                 glitch_chars: str = "!@#$%^&*()_+-=[]{}|;':,.<>?/~`"):
    """
    Create a glitch effect by randomly corrupting characters on screen.
    
    Args:
        canvas: Canvas to draw on
        layer: Layer to draw on
        intensity: Number of glitch characters to place
        glitch_chars: Characters to use for glitching
    """
    for _ in range(intensity):
        pos = Vector2(
            random.randint(0, canvas.dimensions.x - 1),
            random.randint(0, canvas.dimensions.y - 1)
        )
        char = random.choice(glitch_chars)
        color = random.choice([Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.MAGENTA])
        canvas.set_char(layer, pos, char, color)


def fade_effect(canvas: Canvas, layer: int, region: Tuple[Vector2, Vector2], 
               fade_char: str = ' ', steps: int = 10):
    """
    Create a fade effect in a specific region.
    
    Args:
        canvas: Canvas to draw on
        layer: Layer to draw on
        region: Tuple of (top_left, bottom_right) positions
        fade_char: Character to fade to
        steps: Number of fade steps
    """
    top_left, bottom_right = region
    
    for step in range(steps):
        fade_chance = int((step + 1) * 100 / steps)
        
        for y in range(top_left.y, bottom_right.y + 1):
            for x in range(top_left.x, bottom_right.x + 1):
                if random.randint(0, 100) < fade_chance:
                    canvas.set_char(layer, Vector2(x, y), fade_char, Style.RESET_ALL)
        
        time.sleep(0.1)  # Small delay between steps


def matrix_rain_effect(canvas: Canvas, layer: int, columns: List[int], 
                      chars: str = "ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ", 
                      color: str = Fore.GREEN):
    """
    Create a Matrix-style digital rain effect.
    
    Args:
        canvas: Canvas to draw on
        layer: Layer to draw on
        columns: List of column positions for rain
        chars: Characters to use for the rain
        color: Color of the rain
    """
    for col in columns:
        if 0 <= col < canvas.dimensions.x:
            for y in range(canvas.dimensions.y):
                if random.randint(0, 100) < 15:  # 15% chance for each position
                    char = random.choice(chars)
                    canvas.set_char(layer, Vector2(col, y), char, color)


def loading_bar_effect(canvas: Canvas, layer: int, position: Vector2, 
                      width: int, progress: float, 
                      fill_char: str = '█', empty_char: str = '░',
                      color: str = Fore.CYAN):
    """
    Create a loading bar effect.
    
    Args:
        canvas: Canvas to draw on
        layer: Layer to draw on
        position: Position of the loading bar
        width: Width of the loading bar
        progress: Progress as a float between 0.0 and 1.0
        fill_char: Character for filled portion
        empty_char: Character for empty portion
        color: Color of the loading bar
    """
    filled_width = int(width * progress)
    
    # Draw filled portion
    for x in range(filled_width):
        canvas.set_char(layer, Vector2(position.x + x, position.y), fill_char, color)
    
    # Draw empty portion
    for x in range(filled_width, width):
        canvas.set_char(layer, Vector2(position.x + x, position.y), empty_char, color)


def pulse_effect(canvas: Canvas, layer: int, position: Vector2, 
                text: str, beat: int, color: str = Fore.WHITE):
    """
    Create a pulsing text effect that changes brightness.
    
    Args:
        canvas: Canvas to draw on
        layer: Layer to draw on
        position: Position of the text
        text: Text to pulse
        beat: Current beat for timing
        color: Base color of the text
    """
    # Alternate between normal and bright
    style = Style.BRIGHT if beat % 2 == 0 else Style.NORMAL
    canvas.set_string(layer, position, text, color + style)


def scramble_text_effect(canvas: Canvas, layer: int, position: Vector2, 
                        original_text: str, scramble_chars: str, 
                        reveal_progress: float, color: str = Fore.WHITE):
    """
    Create a text scrambling effect that gradually reveals the original text.
    
    Args:
        canvas: Canvas to draw on
        layer: Layer to draw on
        position: Position of the text
        original_text: The final text to reveal
        scramble_chars: Characters to use for scrambling
        reveal_progress: Progress of reveal (0.0 to 1.0)
        color: Color of the text
    """
    revealed_chars = int(len(original_text) * reveal_progress)
    display_text = ""
    
    for i, char in enumerate(original_text):
        if i < revealed_chars:
            display_text += char
        else:
            display_text += random.choice(scramble_chars)
    
    canvas.set_string(layer, position, display_text, color)


def debug_info(canvas: Canvas, generator, beat: int, last_frames: List[float]):
    """
    Display debug information on screen.
    
    Args:
        canvas: Canvas to draw on
        generator: Generator object for accessing parent data
        beat: Current beat
        last_frames: List of recent frame times for FPS calculation
    """
    # Display beat information
    global_beat = generator.parent.cur_beat
    local_beat = generator.scene.internal_beat if generator.scene else 0
    
    canvas.set_string(0, Vector2(32, 1), 
                     f"{global_beat:4} g | {local_beat:4} l", 
                     Style.BRIGHT + Fore.YELLOW)
    
    # Display active scenes
    scene_count = 0
    for index, scene in enumerate(generator.parent.active_scene):
        if scene and scene.name != "debug_counter":
            active_generators = len([g for g in scene.generators if g.start_beat <= beat])
            scene_info = f"{scene.name} ({active_generators})"
            canvas.set_string(0, Vector2(32, index + 2), 
                             f"{scene_info:^17}", 
                             Style.NORMAL + Fore.GREEN)
            scene_count += 1
    
    # Clear unused debug lines
    for i in range(scene_count, 6):
        canvas.set_string(0, Vector2(32, i + 2), 
                         " " * 17, Style.NORMAL + Fore.GREEN)
    
    # Display edits per second
    canvas.set_string(0, Vector2(32, 8), 
                     f"  {canvas.edits_this_frame:4} e/s", 
                     Style.BRIGHT + Fore.YELLOW)
    
    # Calculate and display FPS
    if len(last_frames) > 1:
        avg_frame_time = sum(last_frames[i] - last_frames[i-1] 
                           for i in range(1, len(last_frames))) / (len(last_frames) - 1)
        fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
    else:
        fps = 0
    
    canvas.set_string(0, Vector2(32, 9), 
                     f" {fps:6.1f} fps", 
                     Style.BRIGHT + Fore.YELLOW)
    
    # Display color palette
    colors = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, 
              Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
    styles = [Style.NORMAL, Style.BRIGHT]
    
    for index in range(16):
        color = colors[index % 8]
        style = styles[index // 8]
        canvas.set_char(0, Vector2(32 + (index % 8), 11 + (index // 8)), 
                       "##", color + style) 