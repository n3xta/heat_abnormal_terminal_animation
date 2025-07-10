import src.animator as am
from src.animator_functions import set_multiline_string, debug_info, clear, noise, cluster_noise
from src.engine.classes import Canvas
from src.engine.dat import Vector2
from colorama import Fore, Style
from src.string_defs import data_strings

canvas = Canvas(Vector2(48,32), num_layers=1, merge_rules=())

counter = am.Scene(
    "debug_counter",
    ( am.Generator(
          0, am.Generator.always(), am.Generator.no_create(),
          lambda g, b: debug_info(canvas, g, b, []),
          am.Generator.no_request()
      ), )
)

clear_scene = am.Scene(
    "clear",
    (
        am.Generator(
            0, am.Generator.always(),
            lambda g: clear(canvas, 0),
            am.Generator.no_request(), am.Generator.no_request()
        ),
        # am.Generator(
        #    0, am.Generator.at_beat(0),
        #    lambda g: noise(
        #        canvas, 0, 400 * 240, ("##",), (Style.BRIGHT + Fore.WHITE,)
        #    ),
        #    am.Generator.no_request(), am.Generator.no_request()
        # ),

    )
)


# plaao
wipe = am.Scene(
    "wipe",
    (
        am.Generator(
            0, am.Generator.always(),
            am.Generator.no_create(),
            lambda g, b: noise(
                canvas, 0, int(b ** 1.4), ("##", "@@", "  "),
                (
                    *((Style.BRIGHT + Fore.WHITE,) * b),
                    *((Style.NORMAL + Fore.WHITE,) * (70 - b)),
                    *((Style.BRIGHT + Fore.BLACK,) * 4 * (40 - b)),
                )
            ),
            am.Generator.no_request()
        ),
    )
)

triangle = am.Scene(
    "triangle",
    (
        am.Generator(
            0, am.Generator.always(),
            am.Generator.no_create(),
            lambda g, b: cluster_noise(
                canvas, 0, 1, 1, 1, ("△△", "▲"),
                (
                    *((Style.BRIGHT + Fore.WHITE,) * b),
                    *((Style.NORMAL + Fore.WHITE,) * (70 - b)),
                    *((Style.BRIGHT + Fore.BLACK,) * 4 * (40 - b)),
                )
            ),
            am.Generator.no_request()
        ),
    )
)

###------------------###
### DEBUGGING SCENES ###
###------------------###

def make_lyric_scene(key):
    text = data_strings[key]
    return am.Scene(
        f"lyric_{key}",
        (
            am.Generator(
                0, am.Generator.always(), am.Generator.no_create(),
                # 每帧都把整段 text 画到 (2,5) 位置
                lambda g, b: set_multiline_string(
                    canvas, 0, 2, 5, text, Fore.YELLOW + Style.BRIGHT
                ),
                am.Generator.no_request()
            ),
        )
    )

lyrics_keys = [
    "buildup_1","buildup_2","buildup_3","buildup_4",
    "climax_1","repeat_1",
    "climax_2","climax_3","repeat_2","climax_4"
]

lyric_scenes = [ make_lyric_scene(k) for k in lyrics_keys ]

###--------------------------###
### ALL SCENES FOR INJECTION ###
###--------------------------###

all_scenes = (*lyric_scenes, counter, clear_scene, wipe, triangle)
