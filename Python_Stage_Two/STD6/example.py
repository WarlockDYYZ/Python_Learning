import threading
import time


def print_star():
    print(100 * "*")


# 基础线程创建
# crawl  v.爬 n.缓慢的速度
def crawl(link, delay=3):
    print(f"crawl started for {link}")
    time.sleep(delay)  # 模拟阻塞I/O操作
    print(f"crawl ended for {link}")


# 定义要处理的链接
links = (
    "https://python.org",
    "https://docs.python.org",
    "https://peps.python.org"
)

# 创建并启动线程
threads = []
for link in links:
    # 使用args传递位置参数，kwargs传递关键字参数
    # 创建线程
    t = threading.Thread(target=crawl, args=(link,), kwargs={"delay": 2})
    # 将创建的线程添加到列表中
    threads.append(t)
    # 前面仅是创建和添加，线程不会自己启动，需显示启动线程
    # 一旦启动，线程会立即开始运行 crawl 函数
    t.start()

# 等待所有线程完成
for t in threads:
    # 依次等待 threads 中的线程执行结束
    t.join()
print_star()


# 继承threading.Thread类
class MyThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print(f"线程 {self.name} 正在运行")


# 创建并启动线程
thread1 = MyThread("线程1")
thread2 = MyThread("线程2")
thread1.start()
thread2.start()
print_star()


# Lock
# 定义计数器类
class Counter:
    def __init__(self):
        self.count = 0
        # lock：线程锁，保证同一时间只有一个线程修改 count
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:  # 使用with语句自动管理锁，自动加锁、自动解锁
            self.count += 1


counter = Counter()


# 每个线程循环 10 万次 调用累加
def worker():
    for _ in range(100_000):
        # 调用带锁的累加
        counter.increment()


# 创建并启动多个线程
# 空列表，用于储存之后创建的进程
threads = []
# 循环创建 5 个线程
for _ in range(5):
    # 创建一个线程对象
    # target=worker：表示线程启动后，去执行 worker 函数
    # 5 次循环 → 创建 5 个独立线程
    t = threading.Thread(target=worker)
    # 把创建好的线程 放进列表里保存
    # 后面要用 join() 等待线程结束
    threads.append(t)
    # 真正启动线程！
    # 线程开始执行 worker() 函数
    # 5 个线程 同时、并发运行
    t.start()

# 等待所有线程完成，所有 5 个线程全部跑完，主线程再继续
for t in threads:
    t.join()
print(f"最终计数: {counter.count}")  # 预期输出: 500000
print_star()


# RLock 可重入锁, Reentrant Lock
# 同一个线程可以多次加锁，不会死锁
lock = threading.RLock()


def recursive_function(n):
    with lock:
        if n > 0:
            print(f"递归深度: {n}")
            recursive_function(n - 1)


# 调用递归函数
recursive_function(5)
print_star()


# Condition 条件变量
# 缓冲区和条件变量
buffer = []
buffer_size = 5
condition = threading.Condition()


# 生产者线程
def producer():
    for i in range(10):
        item = f"产品-{i}"
        with condition:
            # 等待缓冲区有空间
            while len(buffer) >= buffer_size:
                condition.wait()
            buffer.append(item)
            print(f"生产者生产了 {item} (队列大小: {len(buffer)})")
            condition.notify()  # 通知消费者有新数据


# 消费者线程
def consumer():
    while True:
        with condition:
            # 等待缓冲区有数据
            while not buffer:
                condition.wait()
            item = buffer.pop(0)
            print(f"消费者消费了 {item} (队列大小: {len(buffer)})")
            condition.notify()  # 通知生产者有空间


# 创建线程
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer, daemon=True)
# 启动线程
producer_thread.start()
consumer_thread.start()
# 等待生产者完成
producer_thread.join()






