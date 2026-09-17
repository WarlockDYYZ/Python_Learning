from locust import HttpUser, task, between, events
import random
import string

class ShortUrlUser(HttpUser):
    wait_time = between(0.1, 0.5)  # 每次请求间隔 0.1~0.5 秒

    def on_start(self):
        """每个虚拟用户启动时创建一个短链接"""
        self.created_codes = []

    @task(3)  # 权重 3：读多写少
    def redirect(self):
        """模拟访问短链接（重定向）"""
        if self.created_codes:
            code = random.choice(self.created_codes)
            with self.client.get(f"/{code}", catch_response=True) as resp:
                if resp.status_code == 302:
                    resp.success()
                else:
                    resp.failure(f"Unexpected status: {resp.status_code}")

    @task(1)  # 权重 1
    def create_short_url(self):
        """模拟创建短链接"""
        random_path = "".join(random.choices(string.ascii_lowercase, k=20))
        url = f"https://example.com/{random_path}"
        with self.client.post("/shorten", json={"url": url}, catch_response=True) as resp:
            if resp.status_code == 201:
                data = resp.json()
                self.created_codes.append(data["short_code"])
                resp.success()
            else:
                resp.failure(f"Create failed: {resp.status_code}")