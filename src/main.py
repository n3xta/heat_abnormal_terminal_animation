from src.string_defs import data_strings

lyrics = [
    data_strings["testing_1"],
    data_strings["testing_2"],
    data_strings["testing_3"],
    data_strings["testing_4"],
    data_strings["testing_5"],
    data_strings["testing_7"],
    data_strings["testing_8"],
    data_strings["testing_9"],
    data_strings["testing_10"],
    data_strings["testing_11"],
    data_strings["testing_12"],
    data_strings["testing_13"],
    data_strings["testing_14"],
]

from colorama import Fore, Style
from src.engine.classes import Canvas
from src.engine.dat import Vector2
import src.animator as am
from src.animator_functions import typewrite_by_word, write_history

# 1) 建画布
canvas = Canvas(Vector2(40, 24), num_layers=1, merge_rules=())

# 2) 定义 Scene
lyrics_scene = am.Scene(
    "lyrics",
    (
        # G0: 打字机——每帧跑一次
        am.Generator(
            0, am.Generator.always(),
            lambda g: g.set_data(
                "text",  lyrics,      # 歌词模板
                "offset", 0,          # 当前单词索引
                "lineno", 0,          # 当前行索引
                "type_col", Fore.YELLOW + Style.BRIGHT
            ),
            lambda g, b: typewrite_by_word(
                canvas, g,
                layer = 0,
                x = 2, y = 20,         # 打字机起始坐标（行数倒着往上滚）
                col = g.get_data("type_col")
            ),
            am.Generator.no_request()
        ),

        # G1: history ——把已经打完的行推到屏幕上方
        am.Generator(
            0, am.Generator.always(),
            am.Generator.no_create(),
            lambda g, b: write_history(
                canvas, g,
                layer = 0,
                x = 2, y = 18,         # history 最底部行
                col = g.get_data("type_col"),
                stop = 2               # history 顶端行
            ),
            am.Generator.no_request()
        ),
    )
)

# src/main.py (继续往下写)

import time, sys
from colorama import init

init(autoreset=False)

# -------------------- 场景管理 --------------------
controller = am.SceneManager((lyrics_scene,), ())
controller.start_scene("lyrics")

# -------------------- 清屏 & 隐光标 ----------------
print("\033[?1049h\033[?25l\033[2J\033[1;1H", end="")

# -------------------- 主循环 ----------------------
try:
    fps = 15
    delay = 1 / fps
    while True:
        controller.request_next(render=True)
        canvas.render_all()
        time.sleep(delay)
except KeyboardInterrupt:
    pass
finally:
    print("\033[?1049l\033[?25h", end="")   # 恢复屏幕 & 光标
    sys.stdout.flush()
