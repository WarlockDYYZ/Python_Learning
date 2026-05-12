import queue
import threading

q = queue.Queue()

# 生产者：放5个任务，不放None结束符
def producer():
    for i in range(5):
        item = f"消息-{i}"
        q.put(item)
        print(f"生产者放入: {item}")

# 消费者：死循环，没有任何退出条件
def consumer():
    while True:
        # 任务取完后，这里永久阻塞卡着
        item = q.get()
        print(f"消费者取出: {item}")
        q.task_done()

if __name__ == "__main__":
    t_prod = threading.Thread(target=producer)
    t_cons = threading.Thread(target=consumer)

    # 重点：不设置 daemon=True
    t_prod.start()
    t_cons.start()

    # 等生产者放完任务
    t_prod.join()

    # 等队列所有任务处理完成
    q.join()

    print("=== 主线程代码全部执行完毕 ===")
    # 走到这里：主线程结束，但消费者线程还活着卡在 get()
    # 程序【卡死不退出】