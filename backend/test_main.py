from bson.objectid import ObjectId
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


class TestUserAPI:

    def test_user_create_endpoint(self):
        response = client.post(
            "/api/v1/auth/user/",
            json={
                "id": "688623106f7539d679d2f33a",
                "username": "testuser",
                "email": "test@example.com",
                "first_name": "tester",
                "password": "testpassword",
            },
        )

        result = response.json()
        self.user_id = result["user_id"]
        assert response.status_code == 200
        assert result["message"] == "User created successfully"

    def test_user_detail_endpoint(self):
        response = client.get(
            "/api/v1/auth/user/688623106f7539d679d2f33a",
        )

        result = response.json()

        assert response.status_code == 200
        assert result["_id"] == "688623106f7539d679d2f33a"

    def test_user_update_endoint(self):
        response = client.put(
            "/api/v1/auth/user/688623106f7539d679d2f33a",
            json=(
                {
                    "username": "johndoe",
                    "email": "john.doe@example.com",
                    "first_name": "John",
                }
            ),
        )

        result = response.json()

        assert response.status_code == 200
        assert result["message"] == "User updated successfully"

    def test_user_delete_endpoint(self):
        response = client.delete(
            "/api/v1/auth/user/688623106f7539d679d2f33a",
        )

        result = response.json()
        assert response.status_code == 200
        assert result["message"] == "User deleted successfully"
