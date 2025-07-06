"""
Heat Abnormal - Terminal Animation Engine
Main application entry point.
"""

import os
import sys
import time
import keyboard
from colorama import init, Fore, Style

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.animator import SceneManager
from src.core.canvas import Canvas, Vector2, enable_ansi
from src.music.audio_player import AudioPlayer, MusicSynchronizer
from src.scenes.heat_abnormal_scenes import create_all_scenes, create_heat_abnormal_events

# Initialize colorama
init()
enable_ansi()


class HeatAbnormalApp:
    """Main application class for the Heat Abnormal animation."""
    
    def __init__(self):
        """Initialize the application."""
        self.canvas = None
        self.scene_manager = None
        self.audio_player = None
        self.music_sync = None
        self.running = False
        self.debug_mode = False
        self.last_beat = -1
        self.frame_times = []
        
        # Configuration
        self.config = {
            'audio_file': 'assets/heat_abnormal.wav',
            'bpm': 183.0,  # Updated BPM
            'animation_subdivisions': 1,  
            'canvas_width': 80,
            'canvas_height': 24,
            'target_fps': 60
        }
        
        self.animation_bpm = self.config['bpm'] * self.config['animation_subdivisions']
        # self.animation_bpm = self.config['bpm']
        self.frame_delay = 1.0 / self.config['target_fps']
        
        self.setup()
    
    def setup(self):
        """Set up the application components."""
        print("🎬 Initializing Heat Abnormal Animation Engine...")
        
        # Create canvas
        self.canvas = Canvas(
            self.config['canvas_width'], 
            self.config['canvas_height'],
            layers=5
        )
        
        # Set global canvas for scenes
        import src.scenes.heat_abnormal_scenes as scenes_module
        scenes_module.canvas = self.canvas
        
        # Create scenes and events
        scenes = create_all_scenes()
        events = create_heat_abnormal_events()
        
        # Create scene manager
        self.scene_manager = SceneManager(scenes, events)
        
        # Create audio player
        self.audio_player = AudioPlayer(
            self.config['audio_file'],
            self.config['bpm'],
            beats_per_measure=4
        )
        
        # Create music synchronizer
        self.music_sync = MusicSynchronizer(self.audio_player, self.animation_bpm)
        
        print("✓ Setup complete")
        self.show_info()
    
    def show_info(self):
        """Show application information."""
        print("\n" + "="*60)
        print("🎵 HEAT ABNORMAL - Terminal Animation Engine")
        print("="*60)
        print(f"Canvas Size: {self.config['canvas_width']}x{self.config['canvas_height']}")
        print(f"Audio File: {self.config['audio_file']}")
        print(f"BPM: {self.config['bpm']}")
        print(f"Animation BPM: {self.animation_bpm}")
        print(f"Target FPS: {self.config['target_fps']}")
        print("\nControls:")
        print("  SPACE    - Play/Pause")
        print("  R        - Restart")
        print("  D        - Toggle Debug")
        print("  S        - Skip ahead 10 seconds")
        print("  ESC/Q    - Quit")
        print("="*60)
        print("Press SPACE to start...")
    
    def handle_keyboard(self):
        """Handle keyboard input."""
        try:
            if keyboard.is_pressed('space'):
                self.toggle_playback()
                time.sleep(0.2)  # Prevent multiple triggers
            
            if keyboard.is_pressed('r'):
                self.restart()
                time.sleep(0.2)
            
            if keyboard.is_pressed('d'):
                self.toggle_debug()
                time.sleep(0.2)
            
            if keyboard.is_pressed('s'):
                self.skip_ahead()
                time.sleep(0.2)
            
            if keyboard.is_pressed('esc') or keyboard.is_pressed('q'):
                self.quit()
                
        except Exception as e:
            # Handle keyboard errors gracefully
            pass
    
    def toggle_playback(self):
        """Toggle audio playback."""
        if self.audio_player.is_playing:
            self.audio_player.pause()
            print("⏸ Paused")
        else:
            self.audio_player.play()
            print("▶ Playing")
    
    def restart(self):
        """Restart the animation."""
        print("🔄 Restarting...")
        self.audio_player.stop()
        self.scene_manager.cur_beat = -1
        self.last_beat = -1
        self.canvas.clear_all()
        self.audio_player.play()
    
    def toggle_debug(self):
        """Toggle debug mode."""
        self.debug_mode = not self.debug_mode
        if self.debug_mode:
            # Add debug scene
            self.scene_manager.add_scene("debug")
            print("🐛 Debug mode ON")
        else:
            # Remove debug scene
            self.scene_manager.remove_scene("debug")
            print("🐛 Debug mode OFF")
    
    def skip_ahead(self, seconds=10):
        """Skip ahead by specified seconds."""
        current_time = self.audio_player.get_current_time()
        new_time = current_time + seconds
        
        # Also advance the scene manager
        beats_to_skip = int(seconds * self.animation_bpm / 60)
        self.scene_manager.cur_beat += beats_to_skip
        
        self.audio_player.seek(new_time)
        print(f"⏭ Skipped to {new_time:.1f}s")
    
    def quit(self):
        """Quit the application."""
        print("\n👋 Goodbye!")
        self.running = False
        self.audio_player.stop()
    
    def update(self):
        """Update the animation."""
        current_time = time.time()
        
        # Update audio player
        self.audio_player.update()
        
        # Get synchronized beat
        current_beat = self.music_sync.get_synchronized_beat()
        
        # Update animation if beat has changed
        if current_beat != self.last_beat:
            self.scene_manager.request_next()
            self.last_beat = current_beat
        
        # Update frame times for FPS calculation 
        self.frame_times.append(current_time)
        if len(self.frame_times) > 10:
            self.frame_times.pop(0)
        
        # Update debug info if debug scene is active
        if self.debug_mode and "debug" in [s.name for s in self.scene_manager.active_scene if s]:
            debug_scene = next((s for s in self.scene_manager.active_scene if s and s.name == "debug"), None)
            if debug_scene and debug_scene.generators:
                debug_scene.generators[0].set_data("frames", self.frame_times)
    
    def render(self):
        """Render the current frame."""
        self.canvas.render()
    
    def run(self):
        """Main application loop."""
        self.running = True
        
        try:
            while self.running:
                frame_start = time.time()
                
                # Handle input
                self.handle_keyboard()
                
                # Update animation
                self.update()
                
                # Render frame
                self.render()
                
                # Check if audio finished
                if self.audio_player.is_finished():
                    print("\n🎵 Audio finished")
                    break
                
                # Frame rate limiting
                frame_time = time.time() - frame_start
                if frame_time < self.frame_delay:
                    time.sleep(self.frame_delay - frame_time)
                
        except KeyboardInterrupt:
            print("\n⚠ Interrupted by user")
        
        except Exception as e:
            print(f"\n💥 Error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        if self.audio_player:
            self.audio_player.stop()
        
        if self.canvas:
            self.canvas.clear_all()
            self.canvas.render()
        
        print("\n🧹 Cleanup complete")


def main():
    """Main entry point."""
    try:
        app = HeatAbnormalApp()
        app.run()
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 