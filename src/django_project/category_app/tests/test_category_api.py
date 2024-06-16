from faker import Faker
from rest_framework.test import APITestCase

from src.core.category.domain import Category
from django_project.category_app.repository import DjangoORMCategoryRepository


class TestCategoryAPI(APITestCase):
    faker = Faker()

    def test_list_categories(self):
        category = Category(
            name=self.faker.word(),
            description=self.faker.sentence(),
        )
        other_category = Category(
            name=self.faker.word(),
            description=self.faker.sentence(),
        )
        repository = DjangoORMCategoryRepository()
        repository.save(category)
        repository.save(other_category)

        url = "/api/categories/"
        response = self.client.get(url)
        expected_data = [
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

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)