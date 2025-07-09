from colorama import Style

def type_text(canvas, generator, layer, pos, colour):
    """
    打字机：每帧多显示 1 个字符，存储 offset 在 generator.data 里
    """
    text  = generator.get_data("text")  # 目标字符串
    off   = generator.get_data("offset") or 0
    show  = text[:off]
    canvas.set_string(layer, pos, show + ("_" if off < len(text) else " "), colour)
    if off < len(text):
        generator.set_data("offset", off + 1)

def blink(canvas, layer, pos, colour_a, colour_b, beat):
    """
    每拍在 (pos) 位置闪烁 "##"
    """
    col = colour_a if beat % 2 == 0 else colour_b
    canvas.set_string(layer, pos, "##", col + Style.BRIGHT)
