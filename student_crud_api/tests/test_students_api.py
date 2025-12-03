import json

def test_get_all_students(client):
    response = client.get("/students")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_add_student(client):
    response = client.post(
        "/students",
        data=json.dumps({
            "name": "Dheekshith",
            "age": 22,
            "course": "Artificial Intelligence"}),
        content_type="application/json"
    )
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["name"] == "Dheekshith"


def test_add_student_without_required_field(client):
    response = client.post(
        "/students",
        data=json.dumps({"age": 20, "course": "Physics"}),
        content_type="application/json"
    )
    assert response.status_code == 400


def test_get_student_not_found(client):
    response = client.get("/students/999999")
    assert response.status_code == 404


def test_update_student(client):
    post = client.post(
        "/students",
        data=json.dumps({
            "name": "Ninad",
            "age": 21,
            "course": "Compiler Design"
        }),
        content_type="application/json"
    )
    student_id = post.json["id"]

    updated_data = {
        "name": "Ninad",
        "age": 22,
        "course": "Compiler Design" 
    }
    response = client.put(
        f"/students/{student_id}",
        data=json.dumps(updated_data),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert response.json["age"] == 22
    assert response.json["name"] == "Ninad"


def test_delete_student(client):
    post = client.post(
        "/students",
        data=json.dumps({"name": "To Delete", "age": 25, "course": "Math"}),
        content_type="application/json"
    )
    student_id = post.json["id"]

    response = client.delete(f"/students/{student_id}")
    assert response.status_code == 204

    check_deleted = client.get(f"/students/{student_id}")
    assert check_deleted.status_code == 404


def test_get_student_by_id(client):
    test_student_name = "Student for Retrieval"
    post_response = client.post(
        "/students",
        data=json.dumps({
            "name": test_student_name, 
            "age": 21, 
            "course": "History"
        }),
        content_type="application/json"
    )
    assert post_response.status_code == 201
    student_id = post_response.json["id"]
    
    get_response = client.get(f"/students/{student_id}")
    
    assert get_response.status_code == 200
    assert get_response.json["id"] == student_id
    assert get_response.json["name"] == test_student_name