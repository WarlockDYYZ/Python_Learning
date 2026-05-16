import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button


# 设置中文字体
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.sans-serif'] = ['SimHei']
# 🔥 加上这一句，强制3D图也用正确字体，100%解决负号报错
plt.rcParams['mathtext.default'] = 'regular'

# 创建图表
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.3)
# 初始参数
a0, b0, c0 = 1, 0.5, 0.2
# 创建数据
x = np.linspace(0, 10, 1000)
# 初始函数
def f(x, a, b, c):
    return a * np.sin(x + b) * np.exp(-c * x)
y = f(x, a0, b0, c0)
# 绘制初始曲线
line, = ax.plot(x, y, 'b-', linewidth=2)
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)
ax.set_title('交互式函数绘图', fontsize=16, fontweight='bold')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.grid(True, alpha=0.3)
# 创建滑块
# 振幅滑块
ax_a = plt.axes([0.1, 0.15, 0.8, 0.03])
slider_a = Slider(ax_a, '振幅', 0.1, 3.0, valinit=a0)
# 相位滑块
ax_b = plt.axes([0.1, 0.1, 0.8, 0.03])
slider_b = Slider(ax_b, '相位', -np.pi, np.pi, valinit=b0)
# 衰减滑块
ax_c = plt.axes([0.1, 0.05, 0.8, 0.03])
slider_c = Slider(ax_c, '衰减', 0.01, 1.0, valinit=c0)
# 定义更新函数
def update(val):
    a = slider_a.val
    b = slider_b.val
    c = slider_c.val
    line.set_ydata(f(x, a, b, c))
    fig.canvas.draw_idle()
# 绑定更新事件
slider_a.on_changed(update)
slider_b.on_changed(update)
slider_c.on_changed(update)
# 创建重置按钮
ax_reset = plt.axes([0.4, 0.01, 0.2, 0.04])
button_reset = Button(ax_reset, '重置', color='lightblue', hovercolor='blue')
def reset(event):
    slider_a.reset()
    slider_b.reset()
    slider_c.reset()
button_reset.on_clicked(reset)
plt.show()
# 创建动画示例
import matplotlib.animation as animation
# 创建动画图表
fig_ani, ax_ani = plt.subplots(figsize=(10, 8))
# 初始数据
x_ani = np.linspace(0, 10, 1000)
y_ani = np.sin(x_ani)
# 绘制初始线
line_ani, = ax_ani.plot(x_ani, y_ani, 'r-', linewidth=3)
ax_ani.set_xlim(0, 10)
ax_ani.set_ylim(-1.5, 1.5)
ax_ani.set_title('动画演示', fontsize=16, fontweight='bold')
ax_ani.set_xlabel('X')
ax_ani.set_ylabel('Y')
ax_ani.grid(True, alpha=0.3)
# 定义动画更新函数
def animate(i):
    # 正弦波向右移动
    y_ani = np.sin(x_ani - i/50)
    line_ani.set_ydata(y_ani)
    return line_ani,
# 创建动画
ani = animation.FuncAnimation(fig_ani, animate, frames=1000,
                              interval=50, blit=True, repeat=True)
# 添加暂停/播放按钮
ax_pause = plt.axes([0.01, 0.01, 0.08, 0.04])
button_pause = Button(ax_pause, '暂停', color='lightcoral', hovercolor='red')
# 控制动画状态
is_paused = False
def pause_play(event):
    global is_paused
    if is_paused:
        ani.resume()
        button_pause.label.set_text('暂停')
    else:
        ani.pause()
        button_pause.label.set_text('播放')
    is_paused = not is_paused
button_pause.on_clicked(pause_play)

# 3D 图不支持自动排版
# plt.tight_layout()
# 换成这行（3D图专用，自动调整间距，不报错）
plt.subplots_adjust(wspace=0.3, hspace=0.3)
plt.show()