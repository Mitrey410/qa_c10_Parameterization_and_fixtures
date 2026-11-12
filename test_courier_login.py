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
        url = BASE_URL or os.getenv("BASE_URL")

        logins = {
            "valid": courier["login"],
            "invalid": f"{courier['login']}_wrong",
            "missing": None,
        }
        passwords = {
            "valid": courier["password"],
            "invalid": "wrong_password",
            "missing": None,
        }

        payload = {
            "login": logins[login_type],
            "password": passwords[password_type],
        }

        response = requests.post(
            f"{url}/api/v1/courier/login",
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
