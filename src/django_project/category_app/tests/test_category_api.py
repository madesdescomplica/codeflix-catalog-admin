from faker import Faker
import pytest
from rest_framework.test import APIClient

from src.core.category.domain import Category
from django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.mark.django_db
class TestCategoryAPI:
    faker = Faker()

    @pytest.fixture
    def category_movie(self):
        return Category(
            name=self.faker.word(),
            description=self.faker.sentence(),
        )

    @pytest.fixture
    def category_documentary(self):
        return Category(
            name=self.faker.word(),
            description=self.faker.sentence(),
        )

    @pytest.fixture
    def category_repository(self) -> DjangoORMCategoryRepository:
        return DjangoORMCategoryRepository()

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
        expected_data = [
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

        assert response.status_code == 200
        assert response.data == expected_data