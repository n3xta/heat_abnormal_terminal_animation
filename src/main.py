
import time, sys
from colorama import init, Fore, Style
from engine.classes import Canvas
from engine.dat import Vector2
import animator as am           # 你的完整版 animator.py
from animator_functions import type_text, blink
from string_defs import text_hello

init()                           # colorama 初始化 (Win 也能彩色)

# 1. 创建 Canvas (40×12 逻辑像素)
canvas = Canvas(Vector2(40, 12), 1, ())

# 2. 定义一个 Scene，里面放两个 Generator
hello_scene = am.Scene(
    "hello",
    (
        # G0: 打字机 (每帧执行，直到写完)
        am.Generator(
            start_beat = 0,
            condition  = am.Generator.always(),
            on_create  = lambda g: g.set_data("text", text_hello, "offset", 0),
            request    = lambda g, b: type_text(canvas, g, 0, Vector2(2, 2), Fore.CYAN+Style.BRIGHT),
            request_clear = am.Generator.no_request()
        ),
        # G1: 左上角闪烁
        am.Generator(
            start_beat = 0,
            condition  = am.Generator.always(),
            on_create  = am.Generator.no_create(),
            request    = lambda g, b: blink(canvas, 0, Vector2(0,0), Fore.YELLOW, Fore.RED, b),
            request_clear = am.Generator.no_request()
        ),
    )
)

# 3. 场景管理器：只有这一幕
controller = am.SceneManager((hello_scene,), ())
controller.start_scene("hello")

# 4. 主循环：每 0.1 秒推进一拍
delay = 0.1         # 10 FPS / 0.1s per beat
beat  = 0
try:
    while True:
        controller.request_next(render=True)
        canvas.render_all()

        beat += 1
        time.sleep(delay)
except KeyboardInterrupt:
    print(Style.RESET_ALL)
    sys.exit()
