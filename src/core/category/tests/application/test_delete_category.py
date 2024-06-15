from unittest.mock import create_autospec
from uuid import uuid4

from faker import Faker
import pytest

from src.core.category.application import DeleteCategory, DeleteCategoryRequest
from src.core.category.domain import Category, CategoryRepository


class TestDeleteCategory:
    faker = Faker()
    id = uuid4()
    name = faker.word()
    description = faker.sentence()

    @pytest.fixture
    def category(self) -> Category:
        return Category(
            id=self.id,
            name=self.name,
            description=self.description,
            is_active=True
        )

    @pytest.fixture
    def mock_repository(self, category: Category) -> CategoryRepository:
        repository = create_autospec(CategoryRepository, instance=True)
        repository.get_by_id.return_value = category
        return repository

    def test_should_DeleteCategory_call_repository_with_get_by_id_method(
        self,
        mock_repository: CategoryRepository,
        category: Category
    ):
        use_case = DeleteCategory(repository=mock_repository)
        request = DeleteCategoryRequest(id=category.id)

        use_case.execute(request)

        assert mock_repository.get_by_id.called is True