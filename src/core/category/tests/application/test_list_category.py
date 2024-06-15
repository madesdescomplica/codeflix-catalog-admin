from unittest.mock import create_autospec
from uuid import uuid4

from faker import Faker
import pytest

from src.core.category.application.usecases import ListCategory
from src.core.category.domain import Category, CategoryRepository


class TestListCategory:
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

    def test_should_ListCategory_call_repository_with_list_method(
        self,
        mock_repository: CategoryRepository
    ):
        use_case = ListCategory(repository=mock_repository)

        use_case.execute()

        assert mock_repository.list.called is True