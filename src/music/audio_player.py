"""
Audio player module for music synchronization in animations.
Uses just-playback for audio playback control.
"""

import os
import time
from typing import Optional, Callable
from just_playback import Playback


class AudioPlayer:
    """Manages audio playback for synchronized animations."""
    
    def __init__(self, audio_file: str, bpm: float = 120.0, beats_per_measure: int = 4):
        """
        Initialize the audio player.
        
        Args:
            audio_file: Path to the audio file
            bpm: Beats per minute for synchronization
            beats_per_measure: Number of beats per measure
        """
        self.audio_file = audio_file
        self.bpm = bpm
        self.beats_per_measure = beats_per_measure
        
        # Calculate timing
        self.beat_duration = 60.0 / bpm  # Duration of one beat in seconds
        self.measure_duration = self.beat_duration * beats_per_measure
        
        # Playback object
        self.playback: Optional[Playback] = None
        
        # Timing and state
        self.start_time: Optional[float] = None
        self.current_beat = 0
        self.is_playing = False
        
        # Callbacks
        self.on_beat_callback: Optional[Callable[[int], None]] = None
        self.on_measure_callback: Optional[Callable[[int], None]] = None
        
        # Initialize playback
        self._init_playback()
    
    def _init_playback(self):
        """Initialize the playback object."""
        if os.path.exists(self.audio_file):
            try:
                self.playback = Playback()
                self.playback.load_file(self.audio_file)
                print(f"✓ Loaded audio file: {self.audio_file}")
            except Exception as e:
                print(f"✗ Failed to load audio file: {e}")
                self.playback = None
        else:
            print(f"✗ Audio file not found: {self.audio_file}")
            self.playback = None
    
    def play(self, start_offset: float = 0.0):
        """
        Start playing the audio.
        
        Args:
            start_offset: Start playback at this offset in seconds
        """
        if self.playback is None:
            print("⚠ No audio loaded, running without sound")
            self.start_time = time.time() - start_offset
            self.is_playing = True
            return
        
        try:
            if start_offset > 0:
                self.playback.seek(start_offset)
            
            self.playback.play()
            self.start_time = time.time() - start_offset
            self.is_playing = True
            print(f"▶ Started playback at {start_offset:.2f}s")
        except Exception as e:
            print(f"✗ Failed to start playback: {e}")
            self.start_time = time.time() - start_offset
            self.is_playing = True
    
    def pause(self):
        """Pause the audio playback."""
        if self.playback:
            try:
                self.playback.pause()
                self.is_playing = False
                print("⏸ Paused playback")
            except Exception as e:
                print(f"✗ Failed to pause playback: {e}")
    
    def stop(self):
        """Stop the audio playback."""
        if self.playback:
            try:
                self.playback.stop()
                self.is_playing = False
                self.start_time = None
                self.current_beat = 0
                print("⏹ Stopped playback")
            except Exception as e:
                print(f"✗ Failed to stop playback: {e}")
    
    def seek(self, position: float):
        """
        Seek to a specific position in the audio.
        
        Args:
            position: Position in seconds
        """
        if self.playback:
            try:
                self.playback.seek(position)
                self.start_time = time.time() - position
                print(f"⏭ Seeked to {position:.2f}s")
            except Exception as e:
                print(f"✗ Failed to seek: {e}")
    
    def get_current_time(self) -> float:
        """Get the current playback time in seconds."""
        if self.start_time is None:
            return 0.0
        return time.time() - self.start_time
    
    def get_current_beat(self) -> int:
        """Get the current beat number."""
        if self.start_time is None:
            return 0
        
        current_time = self.get_current_time()
        return int(current_time / self.beat_duration)
    
    def get_current_measure(self) -> int:
        """Get the current measure number."""
        return self.get_current_beat() // self.beats_per_measure
    
    def get_beat_progress(self) -> float:
        """Get the progress within the current beat (0.0 to 1.0)."""
        if self.start_time is None:
            return 0.0
        
        current_time = self.get_current_time()
        beat_time = current_time % self.beat_duration
        return beat_time / self.beat_duration
    
    def get_measure_progress(self) -> float:
        """Get the progress within the current measure (0.0 to 1.0)."""
        if self.start_time is None:
            return 0.0
        
        current_time = self.get_current_time()
        measure_time = current_time % self.measure_duration
        return measure_time / self.measure_duration
    
    def set_beat_callback(self, callback: Callable[[int], None]):
        """Set a callback function to be called on each beat."""
        self.on_beat_callback = callback
    
    def set_measure_callback(self, callback: Callable[[int], None]):
        """Set a callback function to be called on each measure."""
        self.on_measure_callback = callback
    
    def update(self):
        """Update the audio player and call callbacks if needed."""
        if not self.is_playing:
            return
        
        current_beat = self.get_current_beat()
        current_measure = self.get_current_measure()
        
        # Check if we've moved to a new beat
        if current_beat != self.current_beat:
            self.current_beat = current_beat
            
            # Call beat callback
            if self.on_beat_callback:
                self.on_beat_callback(current_beat)
            
            # Call measure callback if we're at the start of a measure
            if current_beat % self.beats_per_measure == 0:
                if self.on_measure_callback:
                    self.on_measure_callback(current_measure)
    
    def is_finished(self) -> bool:
        """Check if the audio playback has finished."""
        if self.playback is None:
            return False
        
        # Only consider finished if we were playing and now we're not
        if not self.is_playing:
            return False
        
        try:
            # Check if the playback is still active
            return not self.playback.active
        except:
            return False
    
    def get_duration(self) -> float:
        """Get the total duration of the audio file."""
        if self.playback is None:
            return 0.0
        
        try:
            # This is a placeholder - just-playback might not have this method
            # You may need to calculate this differently
            return 300.0  # Default 5 minutes
        except:
            return 0.0
    
    def get_info(self) -> dict:
        """Get information about the current audio state."""
        return {
            'file': self.audio_file,
            'bpm': self.bpm,
            'beats_per_measure': self.beats_per_measure,
            'beat_duration': self.beat_duration,
            'measure_duration': self.measure_duration,
            'is_playing': self.is_playing,
            'current_time': self.get_current_time(),
            'current_beat': self.get_current_beat(),
            'current_measure': self.get_current_measure(),
            'beat_progress': self.get_beat_progress(),
            'measure_progress': self.get_measure_progress()
        }


class MusicSynchronizer:
    """Synchronizes animation beats with music beats."""
    
    def __init__(self, audio_player: AudioPlayer, animation_bpm: float = None):
        """
        Initialize the synchronizer.
        
        Args:
            audio_player: AudioPlayer instance
            animation_bpm: Override BPM for animation timing (uses audio BPM if None)
        """
        self.audio_player = audio_player
        self.animation_bpm = animation_bpm or audio_player.bpm
        
        # Calculate animation timing
        self.animation_beat_duration = 60.0 / self.animation_bpm
        
        # Offset for fine-tuning synchronization
        self.beat_offset = 0
        self.time_offset = 0.0
    
    def set_beat_offset(self, offset: int):
        """Set an offset for beat synchronization."""
        self.beat_offset = offset
    
    def set_time_offset(self, offset: float):
        """Set a time offset for synchronization."""
        self.time_offset = offset
    
    def get_synchronized_beat(self) -> int:
        """Get the current beat synchronized with the audio."""
        if self.audio_player.start_time is None:
            return 0
        
        # Use audio time with offsets
        current_time = self.audio_player.get_current_time() + self.time_offset
        beat = int(current_time / self.animation_beat_duration) + self.beat_offset
        
        return max(0, beat)
    
    def should_update_animation(self, last_beat: int) -> bool:
        """Check if the animation should be updated."""
        current_beat = self.get_synchronized_beat()
        return current_beat != last_beat
    
    def get_beat_progress(self) -> float:
        """Get the progress within the current animation beat."""
        if self.audio_player.start_time is None:
            return 0.0
        
        current_time = self.audio_player.get_current_time() + self.time_offset
        beat_time = current_time % self.animation_beat_duration
        return beat_time / self.animation_beat_duration 