import time
from just_playback import Playback
from animator_scenes import all_scenes, canvas
import animator as heat
# from string_defs import data_strings
# from animator_functions import debug_info

offset = 0.4
beat = 0
delay = 60.0 / 183.0 / 8.0  # Assuming 183 BPM, 8 beats per measure

filename = "./assets/heat_abnormal.wav"
playback = Playback()
playback.load_file(filename)
playback.play()

time_start = time.time()
last_update = time.time()
prev_pos = 0

last_frames = []

event_16_time = 128
event_12_time = 96
event_4_time = 32

controller = heat.SceneManager(all_scenes, (
    # buildup
    heat.Event(48, heat.Event.swap_scene("triangle")),

    # heat.Event(48, heat.Event.swap_scene("clear")),
    heat.Event(120, heat.Event.swap_scene("lyric_buildup_1")),
    heat.Event(120 + event_16_time * 1 - 1, heat.Event.swap_scene("clear")),
    heat.Event(120 + event_16_time * 1, heat.Event.swap_scene("lyric_buildup_2")),
    heat.Event(120 + event_16_time * 2 - 1, heat.Event.swap_scene("clear")),
    heat.Event(120 + event_16_time * 2, heat.Event.swap_scene("lyric_buildup_3")),
    heat.Event(120 + event_16_time * 3 - 1, heat.Event.swap_scene("clear")),
    heat.Event(120 + event_16_time * 3, heat.Event.swap_scene("lyric_buildup_4")),
    heat.Event(120 + event_16_time * 4 - 1, heat.Event.swap_scene("clear")),
    
    # Climax 1
    heat.Event(120 + event_16_time * 4, heat.Event.swap_scene("lyric_climax_1")),
    heat.Event(120 + event_16_time * 5 - 1, heat.Event.swap_scene("clear")),
    heat.Event(120 + event_16_time * 5, heat.Event.swap_scene("lyric_repeat_1")),
    heat.Event(120 + event_16_time * 5 + event_12_time * 1 - 1, heat.Event.swap_scene("clear")),
    heat.Event(120 + event_16_time * 5 + event_12_time * 1, heat.Event.swap_scene("lyric_climax_2")),
    heat.Event(120 + event_16_time * 5 + event_12_time * 1 + event_4_time * 1 - 1, heat.Event.swap_scene("clear")),

    # Climax 2
    heat.Event(120 + event_16_time * 5 + event_12_time * 1 + event_4_time * 1, heat.Event.swap_scene("lyric_climax_3")),
    heat.Event(120 + event_16_time * 6 + event_12_time * 1 + event_4_time * 1 - 1, heat.Event.swap_scene("clear")),
    heat.Event(120 + event_16_time * 6 + event_12_time * 1 + event_4_time * 1, heat.Event.swap_scene("lyric_repeat_2")),
    heat.Event(120 + event_16_time * 6 + event_12_time * 2 + event_4_time * 1 - 1, heat.Event.swap_scene("clear")),
    heat.Event(120 + event_16_time * 6 + event_12_time * 2 + event_4_time * 1, heat.Event.swap_scene("lyric_climax_4")),
))

while playback.active:
    next_beat = (playback.curr_pos - offset) > ((beat - 0) * delay)
    need_update = time.time() - (1/30) > last_update

    if next_beat:
        controller.request_next()
        canvas.render_all()
        last_frames.append(time.time())
        if len(last_frames) > 10:
            last_frames.pop(0)

        beat += 1
        last_update = time.time()

