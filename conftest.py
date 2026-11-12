import os
import uuid

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def courier():
    # TODO: сгенерируйте уникальный логин курьера.
    # Например, используйте uuid.
    base_url = os.getenv("BASE_URL")
    login = f"courier_{uuid.uuid4().hex[:8]}"

    courier_data = {
        "login": login,
        "password": "1234",
        "firstName": "Test",
    }

    # TODO: создайте курьера через POST /api/v1/courier.
    # Сохраните ответ, чтобы убедиться, что создание прошло успешно.
    response = requests.post(
        f"{base_url}/api/v1/courier",
        json=courier_data,
    )
    assert response.status_code == 201

    # TODO: получите id созданного курьера.
    # Для этого используйте POST /api/v1/courier/login
    # с login и password из courier_data.
    #
    # login_response = requests.post(...)
    # courier_id = login_response.json()["id"]
    login_response = requests.post(
        f"{base_url}/api/v1/courier/login",
        json={
            "login": courier_data["login"],
            "password": courier_data["password"],
        },
    )
    assert login_response.status_code == 200
    courier_id = login_response.json()["id"]

    # TODO: передайте в тест данные, необходимые для авторизации.
    yield {
        "login": courier_data["login"],
        "password": courier_data["password"],
        "id": courier_id,
    }

    # TODO: после завершения теста удалите созданного курьера.
    # DELETE /api/v1/courier/{id}
    requests.delete(f"{base_url}/api/v1/courier/{courier_id}")