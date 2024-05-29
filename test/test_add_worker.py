from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from main import app
from routers.workers import add_worker
from schemas import WorkerInput, User, Worker

client = TestClient(app)


def test_add_worker():
    response = client.post("/api/workers/",
                           json={
                               "name": "Alex",
                               "age": 26,
                               "profession": "IT support"
                           }, headers={'Authorization': 'Bearer Alex'}
                           )
    assert response.status_code == 200
    worker = response.json()
    assert worker['age'] == 26
    assert worker['profession'] == 'IT support'
    assert worker['name'] == "Alex"


@pytest.mark.asyncio
async def test_add_worker_with_mock_session():
    mock_session = Mock()
    input = WorkerInput(name="Jim", age=26, profession="IT support")
    user = User(username="Alex")
    result = await add_worker(worker_input=input, session=mock_session, user=user)  # Await the async function

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert isinstance(result, Worker)
    assert result.age == 26
    assert result.profession == "IT support"
    assert result.name == "Jim"