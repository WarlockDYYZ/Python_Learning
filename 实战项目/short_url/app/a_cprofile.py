import cProfile
import pstats
from io import StringIO


def run_benchmark():
    """模拟一次短链接创建 + 重定向的完整流程"""
    from app.main import create_short_url, redirect_short_url
    create_short_url(url="https://example.com/benchmark")
    redirect_short_url(short_code="abc123")

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    # 执行 100 次以放大热点
    for _ in range(100):
        run_benchmark()

    profiler.disable()

    # 按累计耗时排序输出 Top 20
    stream = StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats("cumulative")
    stats.print_stats(20)

    print(stream.getvalue())