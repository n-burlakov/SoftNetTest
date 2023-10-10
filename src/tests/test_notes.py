import json

import pytest
from .conftest import test_app
from ..app.api.crud import crud_notes as crud


# CREATE NOTE TEST
def test_create_note(test_app, monkeypatch):
    test_request_payload = {"text": "something", "board_id": 1}
    test_response_payload = {"id": 1, "text": "something"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/notes/", content=json.dumps(test_request_payload), )

    assert response.status_code == 201
    assert response.json()['id'] == test_response_payload['id']
    assert response.json()['text'] == test_response_payload['text']


def test_create_note_invalid_json(test_app):
    response = test_app.post("/notes/", content=json.dumps({"text": "1"}))
    assert response.status_code == 422


# READ NOTE TEST
def test_read_note(test_app, monkeypatch):
    test_data = {"id": 1, "text": "something"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notes/1")
    assert response.status_code == 200
    print(response.json())
    # assert response.json() == test_data


def test_read_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.get("/notes/0")
    assert response.status_code == 422


# READ ALL NOTES TEST
def test_read_all_notes(test_app, monkeypatch):
    test_data = [
        {"text": "something", "id": 1},
        {"text": "someone", "id": 2},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/notes/")
    assert response.status_code == 200
    # assert response.json() == test_data


# PUT NOTES TEST
def test_update_note(test_app, monkeypatch):
    test_update_data = {"text": "someone else one more", "id": 1}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/notes/1/", content=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"text": "bar"}, 404],
        [999, {"text": "foo"}, 404],
        [1, {"text": "foo"}, 404],
        [0, {"text": "foo"}, 422],
    ],
)
def test_update_note_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/notes/{id}/", content=json.dumps(payload), )
    assert response.status_code == status_code


# DELETE NOTES TEST
def test_remove_note(test_app, monkeypatch):
    test_data = {"text": "something", "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/notes/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/notes/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.delete("/notes/0/")
    assert response.status_code == 422
