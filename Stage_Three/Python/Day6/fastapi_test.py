from fastapi.testclient import TestClient
from route_define import app

client = TestClient(app)

def test_get_user():
    response = client.get("/users/123")
    assert response.status_code == 200
    assert response.json()["user_id"] == 123
    assert response.json()["username"] == "user_123"

def test_create_user():
    # 对于普通参数，TestClient 同样使用 params 传递
    response = client.post("/users", params={"username": "zhangsan", "email": "zhangsan@test.com"})
    assert response.status_code == 200
    assert response.json()["username"] == "zhangsan"

def test_update_user():
    response = client.put("/users/123", params={"username": "new_name"})
    assert response.status_code == 200

def test_delete_user():
    response = client.delete("/users/123")
    assert response.status_code == 200
