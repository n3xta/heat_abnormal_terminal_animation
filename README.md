# Heat Abnormal - Terminal Animation Engine

一个用于创建与音乐同步的终端动画的引擎，基于日本歌曲"Heat Abnormal"制作。

## 🎬 特性

- 🎵 **音乐同步**: 与音频文件完美同步的动画
- 🎨 **多层渲染**: 支持多层次的视觉效果
- 🎭 **场景系统**: 灵活的场景管理和切换
- ⚡ **高性能**: 优化的渲染引擎，支持60fps
- 🎮 **交互控制**: 实时播放控制和调试功能
- 🌈 **丰富效果**: 内置多种视觉效果库

## 📦 安装

### 依赖要求

- Python 3.7+
- Windows 10+ / macOS / Linux

### 安装步骤

1. 克隆项目：
```bash
git clone https://github.com/yourusername/heat_abnormal.git
cd heat_abnormal
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 准备音频文件：
将你的音频文件放在 `assets/heat_abnormal.wav`

4. 运行程序：
```bash
python main.py
```

## 🎮 控制说明

| 按键 | 功能 |
|------|------|
| `SPACE` | 播放/暂停 |
| `R` | 重新开始 |
| `D` | 切换调试模式 |
| `S` | 快进10秒 |
| `ESC` / `Q` | 退出程序 |

## 🏗️ 项目结构

```
heat_abnormal/
├── assets/                    # 资产文件
│   ├── heat_abnormal.txt     # 歌词文件
│   └── heat_abnormal.wav     # 音频文件
├── src/                      # 源代码
│   ├── core/                 # 核心动画引擎
│   │   ├── animator.py       # 动画系统核心类
│   │   ├── canvas.py         # 渲染画布
│   │   ├── effects.py        # 视觉效果库
│   │   └── __init__.py
│   ├── music/                # 音乐同步
│   │   ├── audio_player.py   # 音频播放器
│   │   └── __init__.py
│   ├── scenes/               # 场景定义
│   │   ├── heat_abnormal_scenes.py  # 主要场景
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py               # 主应用程序
├── .cursorrules/             # 开发指南
├── main.py                   # 项目入口点
├── requirements.txt          # 依赖项
└── README.md                 # 本文件
```

## 🎨 核心概念

### 动画系统架构

- **SceneManager**: 管理所有场景和事件的总控制器
- **Scene**: 场景，包含多个生成器的容器
- **Generator**: 生成器，创建具体视觉效果的组件
- **Event**: 事件，控制场景切换和状态更新
- **Canvas**: 画布，处理终端渲染

### 时序控制

```python
# 基于音乐BPM的时序控制
bpm = 179.0  # 歌曲的BPM
animation_subdivisions = 8  # 每个音乐拍子的动画细分数
animation_bpm = bpm * animation_subdivisions  # 实际动画BPM
```

## 🎭 场景示例

### 创建简单场景

```python
def create_my_scene():
    def render_text(generator, beat):
        text = generator.get_data("text")
        if text:
            typewriter_effect(canvas, generator, 2, Vector2(10, 10), 
                            Style.BRIGHT + Fore.YELLOW, True)
    
    scene = Scene(
        "my_scene",
        [
            Generator(
                0, Generator.always(),
                lambda g: g.set_data("text", "Hello World!", "offset", 0),
                render_text,
                Generator.no_request()
            )
        ]
    )
    
    return scene
```

### 添加事件

```python
events = [
    Event(0, Event.swap_scene("my_scene")),
    Event(60, lambda c: c.set_generator_data("my_scene", 0, "text", "New Text!")),
]
```

## 🌈 视觉效果

### 内置效果

- **打字机效果**: 文字逐字显示
- **噪点效果**: 随机字符噪点
- **波浪效果**: 波浪动画
- **故障效果**: 画面故障干扰
- **脉冲效果**: 文字闪烁
- **矩阵雨**: Matrix风格数字雨
- **加载条**: 进度条动画

### 使用效果

```python
# 打字机效果
typewriter_effect(canvas, generator, layer, position, color, True)

# 噪点效果
noise_effect(canvas, layer, amount, chars, colors)

# 波浪效果
wave_effect(canvas, layer, y, amplitude, frequency, phase, char, color)
```

## 🎵 音乐同步

### 音频播放器

```python
audio_player = AudioPlayer(
    "assets/heat_abnormal.wav",
    bpm=179.0,
    beats_per_measure=4
)

# 播放控制
audio_player.play()
audio_player.pause()
audio_player.seek(position)
```

### 同步器

```python
music_sync = MusicSynchronizer(audio_player, animation_bpm)

# 获取当前拍子
current_beat = music_sync.get_synchronized_beat()

# 设置偏移
music_sync.set_time_offset(offset_seconds)
```

## 🐛 调试功能

启用调试模式（按 `D` 键）可以显示：

- 当前拍子信息
- 活动场景列表
- 每秒编辑次数
- 帧率信息
- 颜色调色板

## 📊 性能优化

### 渲染优化

- 使用 `Generator.every_n_beats()` 控制更新频率
- 避免不必要的清除操作
- 合理使用多层渲染

### 内存管理

- 定期清理不用的数据
- 避免在生成器中存储大量数据
- 使用 `canvas.clear_layer()` 清理特定层

## 🔧 配置

### 主要配置项

```python
config = {
    'audio_file': 'assets/heat_abnormal.wav',
    'bpm': 179.0,
    'animation_subdivisions': 8,
    'canvas_width': 80,
    'canvas_height': 24,
    'target_fps': 60
}
```

## 🤝 开发指南

查看 [开发指南](.cursorrules/development_guide.md) 获取详细的开发文档。

### 快速开始

1. 创建新场景
2. 添加生成器
3. 实现渲染函数
4. 添加事件
5. 测试和调试

## 📝 许可证

本项目基于 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。

## 🎉 致谢

- 基于 [just-playback](https://github.com/cheofusi/just_playback) 的音频播放
- 使用 [keyboard](https://github.com/boppreh/keyboard) 处理输入
- 使用 [colorama](https://github.com/tartley/colorama) 实现跨平台颜色支持
- 参考了 [credits_public](https://github.com/plaaosert/credits_public) 的动画系统设计

## 📞 联系方式

如有问题或建议，请提交 [Issue](https://github.com/yourusername/heat_abnormal/issues) 或发送邮件至 [your.email@example.com]。

---

**享受创造属于你的终端动画！** 🎬✨ 