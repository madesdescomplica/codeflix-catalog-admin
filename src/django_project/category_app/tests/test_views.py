from uuid import UUID, uuid4

from django.urls import reverse
from faker import Faker
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.category.domain import Category
from django_project.category_app.repository import DjangoORMCategoryRepository


faker = Faker()

@pytest.fixture
def category_movie():
    return Category(
        name="Movie",
        description="Movie description"
    )

@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary description"
    )

@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()

@pytest.mark.django_db
class TestListAPI:

    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = "/api/categories/"
        response = APIClient().get(url)
        expected_data = {
            "data": [
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active
                },
                {
                    "id": str(category_documentary.id),
                    "name": category_documentary.name,
                    "description": category_documentary.description,
                    "is_active": category_documentary.is_active
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
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = f"/api/categories/{category_documentary.id}/"
        response = APIClient().get(url)
        expected_data = {
            "data": {
                "id": str(category_documentary.id),
                "name": category_documentary.name,
                "description": category_documentary.description,
                "is_active": category_documentary.is_active
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
    def test_return_400_when_payload_is_invalid(self):
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "",
                "description": "Movie description",
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."]
        }

    def test_when_payload_is_valid_then_create_category_and_return_201(
        self,
        category_repository: DjangoORMCategoryRepository
    ):
        url = "/api/categories/"
        response = APIClient().post(
            url,
            data={
                "name": "Movie",
                "description": "Movie description",
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        created_category_id = UUID(response.data["id"])

        assert category_repository.get_by_id(created_category_id) == Category(
            id=created_category_id,
            name="Movie",
            description="Movie description"
        )

        assert category_repository.list() == [
            Category(
                id=created_category_id,
                name="Movie",
                description="Movie description"
            )
        ]

@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_payload_is_invalid_then_return_400(self):
        url = '/api/categories/invalid_id/'
        response = APIClient().put(
            url,
            data={
                "name": "",
                "description": "Movie description",
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
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository
    ):
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().put(
            url,
            data={
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True
            }
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        updated_category = category_repository.get_by_id(category_movie.id)
        assert updated_category == Category(
            id=category_movie.id,
            name="Documentary",
            description="Documentary description",
            is_active=True
        )

    def test_when_category_does_not_exist_then_return_404(self):
        url = f"/api/categories/{uuid4()}/"
        response = APIClient().put(
            url,
            data={
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True
            },
            format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND