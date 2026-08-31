from inspect import cleandoc


def test_should_creat_task(client):

    response = client.post("/tasks",
                           json={"title": "integration test"})

    assert response.status_code == 201

    body = response.json()

    assert body["title"] == "integration test"
    assert body["id"] == 1
    assert body["completed"] is False

def test_should_list_created_task(client):

    created_task = client.post("/tasks",json={"title": "integration test"})

    assert created_task.status_code == 201

    list_of_tasks = client.get("/tasks")

    assert list_of_tasks.status_code == 200

    tasks = list_of_tasks.json()

    assert tasks[0]["title"] == "integration test"
    assert tasks[0]["id"] == 1

def test_should_trim_task_title(client):

    response = client.post("/tasks",json={"title": "    integration test  "})

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "integration test"

def test_should_reject_trim_blank_task_title(client):

    response = client.post("/tasks",json={"title": "   "})
    assert response.status_code == 400
    assert response.json() == {"detail": "Task title cannot be blank"}

def test_should_reject_blank_task_title(client):
    response = client.post("/tasks",json={"title": ""})
    assert response.status_code == 422

def test_should_complete_task(client):
    response = client.post("/tasks",json={"title": "integration test"})

    task_id = response.json()["id"]

    complete_response = client.patch(f"/tasks/{task_id}/complete")

    assert complete_response.status_code == 200

    assert complete_response.json()["completed"] is True

def test_should_return_404_when_completing_unknown_task(client):
    response = client.patch(f"/tasks/{666}/complete")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_should_delete_task(client):
    response = client.post("/tasks",json={"title": "integration test"})

    task_id = response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    list_of_tasks = client.get("/tasks")

    assert list_of_tasks.json() == []

def test_should_return_404_when_delete_unknown_task(client):
    response = client.delete(f"/tasks/{666}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}