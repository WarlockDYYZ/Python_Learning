import threading
import time

# 创建事件对象
event = threading.Event()
# 工作线程
def worker():
   print("工作线程等待开始信号...")
   event.wait()  # 等待事件
   print("工作线程开始执行任务")
# 主线程
print("主线程准备中...")
time.sleep(2)
print("主线程发送开始信号")
event.set()  # 设置事件
# 创建并启动工作线程
thread = threading.Thread(target=worker)
thread.start()
# 等待工作线程完成
thread.join()