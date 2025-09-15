# lib/tests/test_tasks.py
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Item

pytestmark = pytest.mark.django_db

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_item():
    def _create_item(name="Test Item", description="Test Description"):
        return Item.objects.create(name=name, description=description)
    return _create_item


class TestItemAPI:
    def test_get_items_list(self, api_client, create_item):
        create_item()
        response = api_client.get("/items/")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)
        assert "name" in response.json()[0]

    def test_create_item_success(self, api_client):
        data = {"name": "New Item", "description": "New Description"}
        response = api_client.post("/items/create/", data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == "New Item"

    def test_create_item_invalid(self, api_client):
        data = {"description": "Missing name"}
        response = api_client.post("/items/create/", data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_item_success(self, api_client, create_item):
        item = create_item()
        data = {"name": "Updated Item", "description": "Updated"}
        response = api_client.put(f"/items/{item.id}/", data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == "Updated Item"

    def test_update_item_not_found(self, api_client):
        data = {"name": "Does Not Exist"}
        response = api_client.put("/items/999/", data, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_partial_update_item(self, api_client, create_item):
        item = create_item()
        data = {"description": "Partially Updated"}
        response = api_client.patch(f"/items/{item.id}/patch/", data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["description"] == "Partially Updated"

    def test_partial_update_item_not_found(self, api_client):
        response = api_client.patch("/items/999/patch/", {"name": "Nope"}, format="json")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_item_success(self, api_client, create_item):
        item = create_item()
        response = api_client.delete(f"/items/{item.id}/delete/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Item.objects.count() == 0

    def test_delete_item_not_found(self, api_client):
        response = api_client.delete("/items/999/delete/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
