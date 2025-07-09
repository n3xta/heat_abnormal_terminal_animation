# animation_scenes.py
import src.animator as am
from src.animator_functions import set_multiline_string, debug_info, clear
from src.engine.classes import Canvas
from src.engine.dat import Vector2
from colorama import Fore, Style
from src.string_defs import data_strings

canvas = Canvas(Vector2(40,24), num_layers=1, merge_rules=())

# 用来显示 debug info 的 Scene（原样搬过来）
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
        #am.Generator(
        #    0, am.Generator.at_beat(0),
        #    lambda g: noise(
        #        canvas, 0, 40 * 24, ("##",), (Style.BRIGHT + Fore.WHITE,)
        #    ),
        #    am.Generator.no_request(), am.Generator.no_request()
        #),

        am.Generator(
            0, am.Generator.always(),
            lambda g: clear(canvas, 0),
            am.Generator.no_request(), am.Generator.no_request()
        ),
    )
)

# 工厂函数：给一段 text 创建一个 Scene
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

# 你的所有段落 key 列表
lyrics_keys = [
    "buildup_1","buildup_2","buildup_3","buildup_4",
    "climax_1","repeat_1",
    "climax_2","climax_3","repeat_2","climax_4"
]

# 生成所有 Scene 对象
lyric_scenes = [ make_lyric_scene(k) for k in lyrics_keys ]

# 把它们合并到 all_scenes
all_scenes = (*lyric_scenes, counter, clear_scene)
