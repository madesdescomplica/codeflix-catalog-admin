from unittest.mock import create_autospec
from uuid import uuid4

from faker import Faker
import pytest

from src.core.category.application.usecases import (
    ListCategory,
    ListCategoryResponse
)
from src.core.category.domain import Category, CategoryRepository


class TestListCategory:
    faker = Faker()

    @pytest.fixture
    def category(self) -> Category:
        return Category(
            name=self.faker.word(),
            description=self.faker.sentence(),
            is_active=self.faker.boolean()
        )

    @pytest.fixture
    def mock_repository(self) -> CategoryRepository:
        return create_autospec(CategoryRepository, instance=True)


    def test_should_ListCategory_call_repository_with_list_method(
        self,
        mock_repository: CategoryRepository
    ):
        use_case = ListCategory(repository=mock_repository)

        use_case.execute()

        assert mock_repository.list.called is True

    def test_should_ListCategory_return_an_empty_list(
        self,
        mock_repository: CategoryRepository
    ):
        mock_repository.list.return_value = []
        use_case = ListCategory(repository=mock_repository)

        response = use_case.execute()

        assert response.data == []

    def test_should_ListCategory_return_list_of_Category(
        self,
        mock_repository: CategoryRepository,
        category: Category
    ):
        list_categories = [category]
        mock_repository.list.return_value = list_categories
        use_case = ListCategory(repository=mock_repository)

        response = use_case.execute()

        assert response.data == list_categories

    def test_should_ListCategory_return_list_of_many_categories(
        self,
        mock_repository: CategoryRepository,
        category: Category,
    ):
        other_category = Category(
            id=uuid4(),
            name=self.faker.word(),
            description=self.faker.sentence(),
            is_active=self.faker.boolean()
        )
        list_categories =[category, other_category]
        mock_repository.list.return_value = list_categories
        use_case = ListCategory(repository=mock_repository)

        response = use_case.execute()

        assert response.data == list_categories
