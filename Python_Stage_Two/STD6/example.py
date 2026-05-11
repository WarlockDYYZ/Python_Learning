import threading
import time
import concurrent.futures
import queue


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
        with condition:  # 自动加锁
            # 等待缓冲区有空间
            while len(buffer) >= buffer_size:
                condition.wait()  # 阻塞，释放锁
            buffer.append(item)
            print(f"生产者生产了 {item} (队列大小: {len(buffer)})")
            condition.notify()  # 通知消费者有新数据

    # 一些注释代码的优化，发结束标记
    with condition:
        buffer.append(None)  # None 作为结束标志
        condition.notify()


# 消费者线程
def consumer():
    while True:  # 一直消费
        with condition:
            # 等待缓冲区有数据
            while not buffer:
                condition.wait()
            # 从列表缓冲区的【最前面】拿走一个元素，FIFO
            item = buffer.pop(0)

            # 优化
            if item is None:
                break  # 收到结束信号，自己退出，不继续循环

            print(f"消费者消费了 {item} (队列大小: {len(buffer)})")
            condition.notify()  # 通知生产者有空间


# 创建线程
producer_thread = threading.Thread(target=producer)
# daemon=True：消费者是守护线程，主线程结束它自动结束
# 优化
# consumer_thread = threading.Thread(target=consumer, daemon=True)
consumer_thread = threading.Thread(target=consumer)
# 启动线程
producer_thread.start()
consumer_thread.start()
# 等待生产者完成，10 次循环结束
producer_thread.join()
# 为使输出更清晰，等待消费者线程结束
consumer_thread.join()
print_star()


# 创建信号量，限制最多3个线程同时访问
semaphore = threading.Semaphore(3)


def worker(task_id):
    with semaphore:  # 获取信号量
        print(f"线程{task_id} 开始执行")
        time.sleep(2)  # 模拟任务执行
        print(f"线程{task_id} 执行完成")


# 创建多个线程
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
# 等待所有线程完成
for t in threads:
    t.join()
print_star()


# 创建事件对象
# 刚创建时：内部标志 = False（关闭）
event = threading.Event()


# 等待事件的线程
def waiter():
    print("等待事件...")
    event.wait()  # 阻塞直到事件被设置，一直等到别的线程调用 event.set() 才会继续
    print("事件已收到，继续执行")


# 设置事件的线程
def signaler():
    time.sleep(3)
    print("设置事件信号")
    event.set()  # 事件标志变成 True，所有 wait () 的线程都会被唤醒！


# 创建并启动线程
waiter_thread = threading.Thread(target=waiter)
signaler_thread = threading.Thread(target=signaler)
waiter_thread.start()
signaler_thread.start()
# 等待线程完成
waiter_thread.join()
signaler_thread.join()


# ThreadPoolExecutor 线程池
def delayed_task(seconds):
    time.sleep(seconds)
    return f"任务完成于 {seconds} 秒后"


# 使用with语句自动管理线程池
with concurrent.futures.ThreadPoolExecutor() as executor:
    # 提交多个任务
    delays = [2, 1, 3]
    futures = [executor.submit(delayed_task, delay) for delay in delays]
    # 按完成顺序获取结果
    print("任务结果（按完成顺序）：")
    for future in concurrent.futures.as_completed(futures):
        print(future.result())

# 使用map方法简化任务提交
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(delayed_task, delays))
    print("n任务结果（按提交顺序）：")
    for result in results:
        print(result)
print_star()


# 自定义线程池
class ThreadPool:
    def __init__(self, max_workers):
        self.max_workers = max_workers  # 最多几个线程
        self.tasks = queue.Queue()      # 任务队列（所有任务放这里），一个线程安全的任务队列
        self.workers = []               # 保存线程对象

        # 创建工作线程，固定数量
        for i in range(max_workers):
            # target 指定：线程启动后，要去执行的函数；name 给线程起个名字，方便看日志，造一个工人线程
            worker = threading.Thread(target=self.worker_loop, name=f"Worker-{i}")
            # 设置为守护线程，随主线程结束而结束
            worker.daemon = True
            worker.start()
            self.workers.append(worker)

    def worker_loop(self):
        while True:  # ？。。。
            # 从队列拿任务（.get() 没有任务就阻塞等待）
            # .get() 取出来的是：
            # ( process_data, ("数据-1",), {} )
            # task = process_data  函数本身
            # args = ("数据-1",)    位置参数元组
            # kwargs = {}          关键字参数字典
            task, args, kwargs = self.tasks.get()
            try:
                # task 是你传进来的函数：process_data
                # *args 展开位置参数
                # **kwargs 展开关键字参数
                task(*args, **kwargs)  # 执行任务函数
            except Exception as e:
                # 获取当前线程的名字(在构造时定义的名字)
                print(f"线程 {threading.current_thread().name} 执行任务时出错: {e}")
            finally:
                self.tasks.task_done()  # 标记任务完成

    def submit(self, task, *args, **kwargs):
        # 也就是把 (函数, 位置参数元组, 关键字参数字典) 放进队列，线程会自动取
        self.tasks.put((task, args, kwargs))

    def join(self):
        # 主线程阻塞在这里，直到队列里所有任务都被执行完
        self.tasks.join()


# 使用线程池
pool = ThreadPool(max_workers=3)


# 定义任务函数
def process_data(data):
    print(f"处理数据: {data} (线程: {threading.current_thread().name})")
    time.sleep(1)


# 提交多个任务
for i in range(10):
    pool.submit(process_data, f"数据-{i}")
# 等待所有任务完成
pool.join()
print("所有任务已完成")
print_star()


# Queue 队列通信
# 创建线程安全队列
q = queue.Queue()


# 生产者线程
def producer():
    for i in range(5):
        item = f"消息-{i}"
        q.put(item)
        print(f"生产者放入: {item}")
    q.put(None)  # 放入结束标志


# 消费者线程
def consumer():
    while True:
        item = q.get()
        if item is None:  # 遇到结束标志
            q.put(None)  # 重新放入，让其他消费者也能收到
            break
        print(f"消费者取出: {item}")
        q.task_done()  # 标记任务完成


# 创建线程
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)
# 启动线程
producer_thread.start()
consumer_thread.start()
# 等待生产者完成
producer_thread.join()
# 等待队列中的所有任务完成
q.join()
print("所有消息处理完成")
print_star()


# 使用 Event 进行同步
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
