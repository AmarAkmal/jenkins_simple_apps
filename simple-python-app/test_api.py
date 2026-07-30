from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestTaskAPI:
    def setup_method(self):
        from main import tasks, next_id
        tasks.clear()
        # Reset next_id by reassigning the module variable
        import main
        main.next_id = 1

    def test_root(self):
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json() == {"message": "Task API is running"}

    def test_create_task(self):
        resp = client.post("/tasks", json={"title": "Buy milk"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "Buy milk"
        assert data["completed"] is False
        assert data["id"] == 1

    def test_list_tasks(self):
        client.post("/tasks", json={"title": "Task A"})
        client.post("/tasks", json={"title": "Task B"})
        resp = client.get("/tasks")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert data[0]["title"] == "Task A"
        assert data[1]["title"] == "Task B"

    def test_get_task(self):
        client.post("/tasks", json={"title": "My task"})
        resp = client.get("/tasks/1")
        assert resp.status_code == 200
        assert resp.json()["title"] == "My task"

    def test_get_task_not_found(self):
        resp = client.get("/tasks/999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Task not found"

    def test_update_task(self):
        client.post("/tasks", json={"title": "Old title"})
        resp = client.put("/tasks/1", json={"title": "New title", "completed": True})
        assert resp.status_code == 200
        assert resp.json()["title"] == "New title"
        assert resp.json()["completed"] is True

    def test_update_task_not_found(self):
        resp = client.put("/tasks/999", json={"title": "Nope"})
        assert resp.status_code == 404

    def test_delete_task(self):
        client.post("/tasks", json={"title": "Delete me"})
        resp = client.delete("/tasks/1")
        assert resp.status_code == 204
        resp = client.get("/tasks")
        assert len(resp.json()) == 0

    def test_delete_task_not_found(self):
        resp = client.delete("/tasks/999")
        assert resp.status_code == 404
