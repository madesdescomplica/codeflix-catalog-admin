from uuid import UUID, uuid4

from faker import Faker
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.category.domain import Category
from django_project.category_app.repository import DjangoORMCategoryRepository


faker = Faker()

@pytest.fixture
def category():
    return Category(
        name=faker.word(),
        description=faker.sentence(),
        is_active=faker.boolean()
    )

@pytest.fixture
def other_category():
    return Category(
        name=faker.word(),
        description=faker.sentence(),
        is_active=faker.boolean()
    )

@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()

@pytest.mark.django_db
class TestListAPI:

    def test_list_categories(
        self,
        category: Category,
        other_category: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category)
        category_repository.save(other_category)

        url = "/api/categories/"
        response = APIClient().get(url)
        expected_data = {
            "data": [
                {
                    "id": str(category.id),
                    "name": category.name,
                    "description": category.description,
                    "is_active": category.is_active
                },
                {
                    "id": str(other_category.id),
                    "name": other_category.name,
                    "description": other_category.description,
                    "is_active": other_category.is_active
                }
            ]
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

@pytest.mark.django_db
class TestRetrieveAPI:
    def test_return_400_when_id_is_not_valid(self):
        url = "/api/categories/invalid_id/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_category_when_exists(
        self,
        category: Category,
        other_category: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category)
        category_repository.save(other_category)

        url = f"/api/categories/{other_category.id}/"
        response = APIClient().get(url)
        expected_data = {
            "data": {
                "id": str(other_category.id),
                "name": other_category.name,
                "description": other_category.description,
                "is_active": other_category.is_active
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_return_404_when_category_not_exists(self):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestCreateAPI:
    def test_return_400_when_payload_is_invalid(self, category: Category):
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "",
                "description": category.description,
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."]
        }

    def test_when_payload_is_valid_then_create_category_and_return_201(
        self,
        category,
        category_repository: DjangoORMCategoryRepository
    ):
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": category.name,
                "description": category.description
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        created_category_id = UUID(response.data["id"])

        assert category_repository.get_by_id(created_category_id) == Category(
            id=created_category_id,
            name=category.name,
            description=category.description
        )

        assert category_repository.list() == [
            Category(
                id=created_category_id,
                name=category.name,
                description=category.description
            )
        ]

@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self, category: Category):
        url = '/api/categories/invalid_id/'
        response = APIClient().put(
            url,
            data={
                "name": "",
                "description": category.description,
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "id": ["Must be a valid UUID."],
            "is_active": ["This field is required."],
        }

    def test_when_payload_is_valid_then_update_category_and_return_204(
        self,
        category: Category,
        other_category: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category)

        url = f"/api/categories/{category.id}/"
        response = APIClient().put(
            url,
            data={
                "name": other_category.name,
                "description": other_category.description,
                "is_active": other_category.is_active
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(category.id)
        assert updated_category == Category(
            id=category.id,
            name=other_category.name,
            description=other_category.description,
            is_active=other_category.is_active
        )

    def test_when_category_does_not_exist_then_return_404(self, category: Category):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().put(
            url,
            data={
                "name": category.name,
                "description": category.description,
                "is_active": category.is_active
            },
            format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestPartialUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self, category: Category):
        url = '/api/categories/invalid_id/'
        response = APIClient().patch(
            url,
            data={
                "name": "",
                "description": category.description,
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
            "name": ["This field may not be blank."],
        }

    def test_when_payload_is_valid_then_update_name_and_return_204(
        self,
        category: Category,
        other_category: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category)
        updated_name = other_category.name

        url = f"/api/categories/{category.id}/"
        response = APIClient().patch(
            url,
            data={
                "name": updated_name
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(category.id)
        assert updated_category == Category(
            id=category.id,
            name=updated_name,
            description=category.description,
            is_active=category.is_active
        )

    def test_when_payload_is_valid_then_update_description_and_return_204(
        self,
        category: Category,
        other_category: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category)
        updated_description = other_category.description

        url = f"/api/categories/{category.id}/"
        response = APIClient().patch(
            url,
            data={
                "description": updated_description
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(category.id)
        assert updated_category == Category(
            id=category.id,
            name=category.name,
            description=updated_description,
            is_active=category.is_active
        )

    def test_when_payload_is_valid_then_update_is_active_and_return_204(
        self,
        category: Category,
        other_category: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category)
        updated_isactive = other_category.is_active

        url = f"/api/categories/{category.id}/"
        response = APIClient().patch(
            url,
            data={
                "is_active": updated_isactive
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(category.id)
        assert updated_category == Category(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=updated_isactive
        )

    def test_when_category_does_not_exist_then_return_404(self, category: Category):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().patch(
            url,
            data={
                "description": category.description,
                "is_active": category.is_active
            },
            format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestDeleteCategoryAPI:

    def test_when_category_does_not_exist_then_return_400(self):
        url = f"/api/categories/invalid_id/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_category_does_not_exist_then_return_404(self):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_category_exists_then_delete_and_return_204(
        self,
        category: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category)

        url = f"/api/categories/{category.id}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert category_repository.list() == []
