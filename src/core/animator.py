"""
Core animation system classes for the terminal animation engine.
Contains the fundamental building blocks: DataStoringObject, SceneManager, Event, Scene, Generator
"""

class DataStoringObject:
    """Base class for objects that need to store and manage data."""
    
    def __init__(self):
        self.data = {}

    def set_data(self, *ident):
        """Set data using key-value pairs: set_data(key1, value1, key2, value2, ...)"""
        for i in range(0, len(ident), 2):
            self.data[ident[i]] = ident[i + 1]

    def get_data(self, ident):
        """Get data by key, returns None if key doesn't exist."""
        return self.data.get(ident)

    def oper_data(self, ident, oper):
        """Apply an operation to existing data."""
        if ident in self.data:
            self.data[ident] = oper(self.data[ident])


class SceneManager(DataStoringObject):
    """Manages all scenes, events, and the global animation state."""
    
    def __init__(self, scenes, events):
        super().__init__()
        
        # Create scene dictionary for quick lookup
        self.scenes = {scene.name: scene for scene in scenes}
        
        # Group events by beat for efficient processing
        self.events = {}
        for event in events:
            if event.beat not in self.events:
                self.events[event.beat] = []
            self.events[event.beat].append(event)
        
        # Set parent references
        for scene in scenes:
            scene.set_parent(self)
        
        self.active_scene = []
        self.cur_beat = -1

    def start_scene(self, scene_name, at=0):
        """Start a scene as the primary scene."""
        if len(self.active_scene) == 0:
            self.active_scene.append(None)
        
        self.active_scene[0] = self.scenes[scene_name]
        self.active_scene[0].start(at)

    def add_scene(self, scene_name, at=0):
        """Add a scene as a layer on top of existing scenes."""
        self.active_scene.append(self.scenes[scene_name])
        self.active_scene[-1].start(at)

    def remove_scene(self, scene_name):
        """Remove a scene from the active scene list."""
        scene = self.scenes[scene_name]
        if scene in self.active_scene:
            self.active_scene.remove(scene)

    def request_next(self, render=True):
        """Request the next frame from all active scenes."""
        for scene in self.active_scene:
            if scene:
                scene.request_frame(render)
        
        self.next_beat()

    def next_beat(self):
        """Advance to the next beat and process any events."""
        self.cur_beat += 1
        if self.cur_beat in self.events:
            for event in self.events[self.cur_beat]:
                event.do(self)

    def set_scene_data(self, scene_name, *ident):
        """Set data on a specific scene."""
        if scene_name in self.scenes:
            self.scenes[scene_name].set_data(*ident)

    def set_generator_data(self, scene_name, generator_index, *ident):
        """Set data on a specific generator within a scene."""
        if scene_name in self.scenes:
            scene = self.scenes[scene_name]
            if 0 <= generator_index < len(scene.generators):
                scene.generators[generator_index].set_data(*ident)


class Event:
    """Represents a timed event that can modify the animation state."""
    
    def __init__(self, beat, do):
        self.beat = beat
        self.do = do

    @staticmethod
    def swap_scene(scene_name, at=0):
        """Create an event that swaps to a new scene."""
        return lambda sm: sm.start_scene(scene_name, at)

    @staticmethod
    def layer_scene(scene_name, at=0):
        """Create an event that layers a scene on top."""
        return lambda sm: sm.add_scene(scene_name, at)

    @staticmethod
    def remove_scene(scene_name):
        """Create an event that removes a scene."""
        return lambda sm: sm.remove_scene(scene_name)


class Scene(DataStoringObject):
    """A scene contains multiple generators and manages their execution."""
    
    def __init__(self, name, generators):
        super().__init__()
        
        self.parent = None
        self.name = name
        self.generators = generators
        self.start_beat = 0
        self.internal_beat = 0

    def set_parent(self, parent):
        """Set the parent SceneManager."""
        self.parent = parent

    def request_frame(self, render=True):
        """Request a frame from all generators in this scene."""
        beat = self.internal_beat
        
        if render:
            for generator in self.generators:
                if beat >= generator.start_beat and generator.condition(beat):
                    # Clear previous frame if not the first frame
                    if beat != self.start_beat and beat != generator.start_beat:
                        generator.request_clear(generator, beat - 1)
                    
                    # Render current frame
                    generator.request(generator, beat)
        
        self.internal_beat += 1

    def start(self, at):
        """Start the scene at a specific beat."""
        for generator in self.generators:
            generator.set_parent(self.parent)
            generator.set_scene(self)
            generator.on_create(generator)
        
        self.start_beat = at
        self.internal_beat = at
        self.request_frame()


class Generator(DataStoringObject):
    """A generator creates specific visual effects within a scene."""
    
    def __init__(self, start_beat, condition, on_create, request, request_clear):
        super().__init__()
        
        self.parent = None
        self.scene = None
        
        self.start_beat = start_beat
        self.condition = condition
        self.on_create = on_create
        self.request = request
        self.request_clear = request_clear

    def set_parent(self, parent):
        """Set the parent SceneManager."""
        self.parent = parent

    def set_scene(self, scene):
        """Set the parent Scene."""
        self.scene = scene

    # Condition helper methods
    @staticmethod
    def combine_conditions(*conditions):
        """Combine multiple conditions with AND logic."""
        return lambda b: all(c(b) for c in conditions)

    @staticmethod
    def always():
        """Always execute condition."""
        return lambda b: True

    @staticmethod
    def every_n_beats(beat):
        """Execute every N beats."""
        return lambda b: b % beat == 0

    @staticmethod
    def every_on_off(on, off):
        """Execute for 'on' beats, then skip 'off' beats."""
        return lambda b: (b % (on + off)) < on

    @staticmethod
    def every_off_on(off, on):
        """Skip 'off' beats, then execute for 'on' beats."""
        return lambda b: (b % (on + off)) >= off

    @staticmethod
    def before_n(beat):
        """Execute before beat N."""
        return lambda b: b < beat

    @staticmethod
    def after_n(beat):
        """Execute after beat N."""
        return lambda b: b >= beat

    @staticmethod
    def at_beat(beat):
        """Execute only at beat N."""
        return lambda b: b == beat

    @staticmethod
    def between_beats(start, end):
        """Execute between two beats (inclusive)."""
        return lambda b: start <= b <= end

    # Helper methods for common generator patterns
    @staticmethod
    def no_create():
        """No initialization needed."""
        return lambda g: None

    @staticmethod
    def no_request():
        """No rendering needed."""
        return lambda g, b: None 