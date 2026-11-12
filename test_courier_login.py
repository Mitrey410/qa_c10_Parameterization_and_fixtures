import os

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


class TestCourierLogin:

    @pytest.mark.parametrize(
        "login_type, password_type, expected_status",
        [
            ("valid", "valid", 200),
            ("missing", "valid", 400),
            ("valid", "missing", 400),
            ("invalid", "valid", 404),
        ],
    )
    def test_courier_login(
        self,
        courier,
        login_type,
        password_type,
        expected_status,
    ):
        payload = {}

        if login_type == "valid":
            payload["login"] = courier["login"]
        elif login_type == "invalid":
            payload["login"] = f"{courier['login']}_wrong"

        if password_type == "valid":
            payload["password"] = courier["password"]
        elif password_type == "invalid":
            payload["password"] = "wrong_password"

        response = requests.post(
            f"{BASE_URL}/api/v1/courier/login",
            json=payload,
        )

        assert response.status_code == expected_status

        response_data = response.json()
        if expected_status == 200:
            assert "id" in response_data
        elif expected_status == 400:
            assert response_data["message"] == "Недостаточно данных для входа"
        elif expected_status == 404:
            assert response_data["message"] == "Учетная запись не найдена"
