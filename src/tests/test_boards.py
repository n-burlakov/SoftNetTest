import json

import pytest
from .conftest import test_app
from ..app.api.crud import crud_boards as crud


# CREATE board TEST
def test_create_board(test_app, monkeypatch):
    test_request_payload = {"title": "something"}
    test_response_payload = {'title': 'something'}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/boards/", content=json.dumps(test_request_payload), )

    assert response.status_code == 201
    assert response.json()['title'] == test_response_payload['title']


def test_create_board_invalid_json(test_app):
    response = test_app.post("/boards/", content=json.dumps({"title": "1"}))
    assert response.status_code == 422


# READ board TEST
def test_read_board(test_app, monkeypatch):
    test_data = {"id": 1, "title": "something"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/boards/1")
    assert response.status_code == 200
    assert response.json()['id'] == test_data['id']
    assert response.json()['title'] == test_data['title']


def test_read_board_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/boards/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "board not found"

    response = test_app.get("/boards/0")
    assert response.status_code == 422


# READ ALL boards TEST
def test_read_all_boards(test_app, monkeypatch):
    test_data = [
        {
            "title": "something"
        },
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud, "get_all", mock_get_all)

    response = test_app.get("/boards/")
    assert response.status_code == 200


# PUT boards TEST
def test_update_board(test_app, monkeypatch):
    test_update_data = {"title": "someone else one more", "id": 1}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud, "put", mock_put)

    response = test_app.put("/boards/1/", content=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"title": "bar"}, 404],
        [999, {"title": "foo"}, 404],
        [1, {"title": "foo"}, 404],
        [0, {"title": "foo"}, 422],
    ],
)
def test_update_board_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/boards/{id}/", content=json.dumps(payload), )
    assert response.status_code == status_code


# DELETE boards TEST
def test_remove_board(test_app, monkeypatch):
    test_data = {"title": "something", "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/boards/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_board_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/boards/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "board not found"

    response = test_app.delete("/boards/0/")
    assert response.status_code == 422
