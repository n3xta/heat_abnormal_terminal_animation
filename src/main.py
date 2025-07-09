import time
from just_playback import Playback

offset = 0
beat = -60
delay = 60.0 / 183.0 / 8.0

filename = "./assets/heat_abnormal.wav"

playback = Playback()
playback.load_file(filename)

playback.play()

time_start = time.time()
last_update = time.time()
prev_pos = 0

while playback.active:

    next_beat = (playback.curr_pos - offset) > ((beat - 0) * delay)
    need_update = time.time() - (1/30) > last_update

    if next_beat:
        # controller.request_next()
        # canvas.render_all()
        # last_frames.append(time.time())
        # if len(last_frames) > 10:
        #     last_frames.pop(0)

        beat += 1

    # if need_update:
    #     if keyboard.is_pressed("p"):
    #         if not paused_this_frame:
    #             if playback.paused:
    #                 playback.resume()
    #             else:
    #                 playback.pause()

    #             paused_this_frame = True
    #     else:
    #         paused_this_frame = False

    #     if keyboard.is_pressed(","):
    #         if not ff_this_frame:
    #             ff_this_frame = True
    #         else:
    #             playback.seek(playback.curr_pos + delay * 3)

    #     if keyboard.is_pressed("."):
    #         if not ff_this_frame:
    #             ff_this_frame = True
    #         else:
    #             playback.seek(playback.curr_pos + delay * 7)

    #     if keyboard.is_pressed("/"):
    #         if not ff_this_frame:
    #             ff_this_frame = True
    #         else:
    #             playback.seek(playback.curr_pos + delay * 15)
        # else:
        #     # print("n", ff_this_frame, pygame.mixer.music.get_pos() + prev_pos, prev_pos)
        #     if ff_this_frame:
        #         # print("unpausing now")
        #         ff_this_frame = False
        #         ffwing.toggle_music()

        last_update = time.time()
