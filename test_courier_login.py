import os

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


class TestCourierLogin:

    @pytest.mark.parametrize(
        "login_type, password_type, expected_status, expected_message",
        [
            # TODO: добавьте минимум 3 набора данных.
            # Должны быть позитивные и негативные сценарии.
            #
            # Например:
            # ("valid", "valid", 200),
            # ("missing", "valid", 400),
            # ("valid", "missing", 400),
            # ("invalid", "valid", 404),
            ("valid", "valid", 200, None),
            ("missing", "valid", 400, "Недостаточно данных для входа"),
            ("valid", "missing", 400, "Недостаточно данных для входа"),
            ("invalid", "valid", 404, "Учетная запись не найдена"),
        ],
    )
    def test_courier_login(
        self,
        courier,
        login_type,
        password_type,
        expected_status,
        expected_message,
    ):
        # TODO: подготовьте login и password для каждого сценария.
        #
        # Для позитивного сценария используйте данные
        # созданного фикстурой курьера.
        #
        # Для негативных сценариев сформируйте необходимые
        # некорректные или отсутствующие данные.

        logins = {
            "valid": courier["login"],
            "invalid": f"{courier['login']}_wrong",
            "missing": "",
        }
        passwords = {
            "valid": courier["password"],
            "invalid": "wrong_password",
            "missing": "",
        }

        payload = {}
        if logins[login_type] is not None:
            payload["login"] = logins[login_type]
        if passwords[password_type] is not None:
            payload["password"] = passwords[password_type]

        # TODO: отправьте POST /api/v1/courier/login.
        response = requests.post(
            f"{BASE_URL}/api/v1/courier/login",
            json=payload
        )
        # TODO: проверьте ожидаемый статус ответа.
        assert response.status_code == expected_status

        response_data = response.json()
        if expected_status == 200:
            assert "id" in response_data
        else:
            assert response_data["message"] == expected_message