"""
Heat Abnormal animation scenes.
Contains all the scene definitions and lyrics data for the animation.
"""

import random
import math
from colorama import Fore, Style

from ..core.animator import Scene, Generator, Event
from ..core.canvas import Canvas, Vector2
from ..core.effects import (
    typewriter_effect, noise_effect, wave_effect, glitch_effect,
    debug_info, pulse_effect, scramble_text_effect
)


# Global canvas instance (will be initialized in main)
canvas: Canvas = None


def get_lyrics_data():
    """Get the lyrics data for the animation."""
    return {
        "intro": """泣いた細胞が海に戻る
世迷言がへばりつく
燕が描いた軌跡を
なぞるように灰色の雲が来ている""",
        
        "verse1": """編んだ名誉で明日を乞う
希望で手が汚れてる
あなたの澄んだ瞳の
色をした星に問いかけている""",
        
        "chorus": """手を取り合い 愛し合えたら
ついに叶わなかった夢を殺す
思考の成れ果て
その中枢には熱異常が起こっている""",
        
        "breakdown": """現実じゃない こんなの
現実じゃない こんなの
現実じゃない こんなの
現実じゃない こんなの""",

        "break": """耐えられないの""",
        
        "bridge": """とうに潰れていた喉
叫んだ音は既に列を成さないで
安楽椅子の上
腐りきった三日月が笑っている もう""",
        
        "breakdown2": """
すぐそこまで
すぐそこまで
すぐそこまで
すぐそこまで
すぐそこまで
すぐそこまで
すぐそこまで
すぐそこまで
""",

        "outro": """
なにかが来ている"""
    }


def create_ocean_scene():
    """Create the ocean background scene."""
    def create_ocean_wave():
        """Create the ocean wave pattern."""
        return "~" * (canvas.dimensions.x - 1)
    
    def render_ocean(generator, beat):
        """Render the ocean background."""
        ocean_pattern = generator.get_data("ocean") or create_ocean_wave()
        ocean_color = generator.get_data("ocean_col") or (Style.NORMAL + Fore.BLUE)
        ocean_glitch = generator.get_data("ocean_glitch") or 0
        
        # Draw ocean waves
        for y in range(canvas.dimensions.y // 2, canvas.dimensions.y - 1):
            wave_offset = int(math.sin(beat * 0.1 + y * 0.1) * 3)
            wave_pos = Vector2(wave_offset, y)
            canvas.set_string(1, wave_pos, ocean_pattern, ocean_color)
        
        # Add glitch effect
        if ocean_glitch > 0:
            glitch_effect(canvas, 1, ocean_glitch)
    
    def clear_ocean(generator, beat):
        """Clear the ocean layer."""
        canvas.clear_layer(1)
    
    def render_text(generator, beat):
        """Render text on the ocean scene."""
        text = generator.get_data("text")
        if text:
            typewriter_effect(canvas, generator, 2, Vector2(5, 5), 
                            Style.BRIGHT + Fore.WHITE, True, speed=4)
    
    def clear_text(generator, beat):
        """Clear the text layer."""
        canvas.clear_layer(2)
    
    ocean_scene = Scene(
        "ocean",
        [
            # Ocean background generator
            Generator(
                0, Generator.every_n_beats(2),
                lambda g: g.set_data("ocean", create_ocean_wave()),
                render_ocean,
                clear_ocean
            ),
            
            # Text overlay generator
            Generator(
                0, Generator.always(),
                lambda g: g.set_data("text", "", "offset", 0),
                render_text,
                clear_text
            )
        ]
    )
    
    return ocean_scene


def create_text_scene():
    """Create a text-focused scene."""
    def render_main_text(generator, beat):
        """Render the main text."""
        text = generator.get_data("text")
        if text:
            typewriter_effect(canvas, generator, 3, Vector2(10, 10), 
                            Style.BRIGHT + Fore.YELLOW, True, speed=5)
    
    def clear_main_text(generator, beat):
        """Clear the main text layer."""
        canvas.clear_layer(3)
    
    def render_background_effects(generator, beat):
        """Render background effects."""
        effect_type = generator.get_data("effect_type") or "none"
        intensity = generator.get_data("intensity") or 5
        
        if effect_type == "noise":
            noise_effect(canvas, 1, intensity)
        elif effect_type == "glitch":
            glitch_effect(canvas, 1, intensity)
        elif effect_type == "wave":
            phase = beat * 0.2
            wave_effect(canvas, 1, canvas.dimensions.y // 2, 5, 0.1, phase)
    
    def clear_background_effects(generator, beat):
        """Clear the background effects layer."""
        canvas.clear_layer(1)
    
    text_scene = Scene(
        "text",
        [
            # Background effects generator
            Generator(
                0, Generator.every_n_beats(1),
                lambda g: g.set_data("effect_type", "none", "intensity", 5),
                render_background_effects,
                clear_background_effects
            ),
            
            # Main text generator
            Generator(
                0, Generator.always(),
                lambda g: g.set_data("text", "", "offset", 0),
                render_main_text,
                clear_main_text
            )
        ]
    )
    
    return text_scene


def create_breakdown_scene():
    """Create the breakdown scene with intense effects."""
    def render_chaotic_text(generator, beat):
        """Render chaotic, repeating text."""
        text = generator.get_data("text") or "現実じゃない"
        base_color = generator.get_data("color") or (Style.BRIGHT + Fore.RED)
        
        # Display text at multiple positions with different effects
        positions = [
            Vector2(10, 8), Vector2(30, 12), Vector2(15, 16), 
            Vector2(40, 6), Vector2(25, 20)
        ]
        
        for i, pos in enumerate(positions):
            if (beat + i) % 4 == 0:  # Stagger the text appearance
                # Add some randomness to the color
                colors = [Fore.RED, Fore.YELLOW, Fore.MAGENTA, Fore.WHITE]
                color = random.choice(colors) + Style.BRIGHT
                canvas.set_string(3, pos, text, color)
    
    def clear_chaotic_text(generator, beat):
        """Clear the chaotic text layer."""
        canvas.clear_layer(3)
    
    def render_intense_effects(generator, beat):
        """Render intense visual effects."""
        intensity = generator.get_data("intensity") or 20
        
        # Heavy glitch effect
        glitch_effect(canvas, 1, intensity)
        
        # Noise effect
        noise_effect(canvas, 2, intensity // 2, 
                    "!@#$%^&*()_+-=[]{}|;':,.<>?/~`", 
                    [Fore.RED, Fore.YELLOW, Fore.MAGENTA])
        
        # Random screen corruption
        for _ in range(intensity):
            pos = Vector2(
                random.randint(0, canvas.dimensions.x - 1),
                random.randint(0, canvas.dimensions.y - 1)
            )
            canvas.set_char(1, pos, '█', Style.BRIGHT + Fore.RED)
    
    def clear_intense_effects(generator, beat):
        """Clear the intense effects layers."""
        canvas.clear_layer(1)
        canvas.clear_layer(2)
    
    breakdown_scene = Scene(
        "breakdown",
        [
            # Intense effects generator
            Generator(
                0, Generator.always(),
                lambda g: g.set_data("intensity", 20),
                render_intense_effects,
                clear_intense_effects
            ),
            
            # Chaotic text generator
            Generator(
                0, Generator.every_n_beats(1),
                lambda g: g.set_data("text", "現実じゃない", "color", Style.BRIGHT + Fore.RED),
                render_chaotic_text,
                clear_chaotic_text
            )
        ]
    )
    
    return breakdown_scene


def create_outro_scene():
    """Create the outro scene with repeating text."""
    def render_climbing_text(generator, beat):
        """Render the climbing 'すぐそこまで' text."""
        text = generator.get_data("text") or "すぐそこまで"
        count = generator.get_data("count") or 0
        
        # Display text in a climbing pattern
        for i in range(min(count, 8)):
            y_pos = canvas.dimensions.y - 2 - i * 2
            x_pos = 10 + (i % 2) * 20
            
            if y_pos >= 0:
                # Fade effect - older text gets dimmer
                if i < count - 2:
                    color = Style.DIM + Fore.CYAN
                else:
                    color = Style.BRIGHT + Fore.CYAN
                
                canvas.set_string(3, Vector2(x_pos, y_pos), text, color)
        
        # Increment count every few beats
        if beat % 8 == 0:
            generator.set_data("count", min(count + 1, 8))
    
    def clear_climbing_text(generator, beat):
        """Clear the climbing text layer."""
        canvas.clear_layer(3)
    
    def render_final_text(generator, beat):
        """Render the final text."""
        text = generator.get_data("text")
        if text:
            # Center the text
            x_pos = (canvas.dimensions.x - len(text)) // 2
            y_pos = canvas.dimensions.y // 2
            
            # Pulsing effect
            color = Style.BRIGHT + Fore.WHITE if beat % 2 == 0 else Style.NORMAL + Fore.WHITE
            canvas.set_string(4, Vector2(x_pos, y_pos), text, color)
    
    def clear_final_text(generator, beat):
        """Clear the final text layer."""
        canvas.clear_layer(4)
    
    outro_scene = Scene(
        "outro",
        [
            # Climbing text generator
            Generator(
                0, Generator.always(),
                lambda g: g.set_data("text", "すぐそこまで", "count", 0),
                render_climbing_text,
                clear_climbing_text
            ),
            
            # Final text generator
            Generator(
                100, Generator.always(),  # Start after 100 beats
                lambda g: g.set_data("text", ""),
                render_final_text,
                clear_final_text
            )
        ]
    )
    
    return outro_scene


def create_clear_scene():
    """Create a scene that clears the screen."""
    def clear_screen(generator, beat):
        """Clear all layers."""
        canvas.clear_all()
    
    clear_scene = Scene(
        "clear",
        [
            Generator(
                0, Generator.at_beat(0),
                Generator.no_create(),
                clear_screen,
                lambda g, b: None  # No need to clear the clear scene
            )
        ]
    )
    
    return clear_scene


def create_debug_scene():
    """Create the debug information scene."""
    def render_debug(generator, beat):
        """Render debug information."""
        debug_info(canvas, generator, beat, generator.get_data("frames") or [])
    
    def clear_debug(generator, beat):
        """Clear the debug layer."""
        canvas.clear_layer(4)
    
    debug_scene = Scene(
        "debug",
        [
            Generator(
                0, Generator.always(),
                lambda g: g.set_data("frames", []),
                render_debug,
                clear_debug
            )
        ]
    )
    
    return debug_scene


def create_all_scenes():
    """Create all scenes for the Heat Abnormal animation."""
    scenes = [
        create_clear_scene(),
        create_ocean_scene(),
        create_text_scene(),
        create_breakdown_scene(),
        create_outro_scene(),
        create_debug_scene()
    ]
    
    return scenes


def create_heat_abnormal_events():
    """Create all events for the Heat Abnormal animation."""
    lyrics = get_lyrics_data()
    
    # Calculate beat positions for each section
    intro_start = 0
    intro_length = 32
    
    verse_start = intro_start + intro_length  # +8 for transition
    verse_length = 32
    
    # chorus: 4拍/句 × 4句 = 16拍
    chorus_start = verse_start + verse_length
    chorus_length = 16 
    
    # breakdown: 2拍/句 × 4句 = 8拍
    breakdown_start = chorus_start + chorus_length
    breakdown_length = 12
    
    # break: 4拍/句 × 1句 = 4拍
    break_start = breakdown_start + breakdown_length
    break_length = 4
    
    # bridge: 4拍/句 × 4句 = 16拍
    bridge_start = break_start + break_length
    bridge_length = 16
    
    # breakdown2: 1拍/句 × 8句 = 8拍
    breakdown2_start = bridge_start + bridge_length
    breakdown2_length = 12
    
    # outro: 4拍/句 × 1句 = 4拍
    outro_start = breakdown2_start + breakdown2_length
    outro_length = 4
    
    events = [
        # Start with clear screen
        Event(0, Event.swap_scene("clear")),
        
        # Intro section - ocean scene
        Event(intro_start, Event.swap_scene("ocean")),
        Event(intro_start, lambda c: c.set_generator_data("ocean", 1, "text", lyrics["intro"], "offset", 0)),
        
        # Verse 1 - text scene
        Event(verse_start, Event.swap_scene("text")),
        Event(verse_start, lambda c: c.set_generator_data("text", 1, "text", lyrics["verse1"], "offset", 0)),
        Event(verse_start, lambda c: c.set_generator_data("text", 0, "effect_type", "wave", "intensity", 8)),
        
        # Chorus - enhanced text scene
        Event(chorus_start, lambda c: c.set_generator_data("text", 1, "text", lyrics["chorus"], "offset", 0)),
        Event(chorus_start, lambda c: c.set_generator_data("text", 0, "effect_type", "noise", "intensity", 10)),
        
        # Breakdown - intense scene
        Event(breakdown_start, Event.swap_scene("breakdown")),
        Event(breakdown_start, lambda c: c.set_generator_data("breakdown", 1, "text", lyrics["breakdown"])),
        Event(breakdown_start, lambda c: c.set_generator_data("breakdown", 0, "intensity", 30)),
        
        # Break - special effect
        Event(break_start, Event.swap_scene("text")),
        Event(break_start, lambda c: c.set_generator_data("text", 1, "text", lyrics["break"], "offset", 0)),
        Event(break_start, lambda c: c.set_generator_data("text", 0, "effect_type", "glitch", "intensity", 15)),
        
        # Bridge - back to ocean
        Event(bridge_start, Event.swap_scene("ocean")),
        Event(bridge_start, lambda c: c.set_generator_data("ocean", 1, "text", lyrics["bridge"], "offset", 0)),
        Event(bridge_start, lambda c: c.set_generator_data("ocean", 0, "ocean_col", Style.DIM + Fore.CYAN)),
        
        # Breakdown 2 - rapid text
        Event(breakdown2_start, Event.swap_scene("breakdown")),
        Event(breakdown2_start, lambda c: c.set_generator_data("breakdown", 1, "text", lyrics["breakdown2"])),
        Event(breakdown2_start, lambda c: c.set_generator_data("breakdown", 0, "intensity", 40)),
        
        # Outro - climbing text
        Event(outro_start, Event.swap_scene("outro")),
        Event(outro_start, lambda c: c.set_generator_data("outro", 1, "text", lyrics["outro"])),
        
        # End
        Event(outro_start + outro_length + 4, Event.swap_scene("clear"))
    ]
    
    return events 