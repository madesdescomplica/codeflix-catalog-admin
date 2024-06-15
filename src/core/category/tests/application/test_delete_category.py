from unittest.mock import create_autospec
from uuid import uuid4

from faker import Faker
import pytest

from src.core.category.application.exceptions import (
    CategoryNotFound,
    InvalidCategory
)
from src.core.category.application.usecases import (
    DeleteCategory,
    DeleteCategoryRequest
)
from src.core.category.domain import Category, CategoryRepository


class TestDeleteCategory:
    faker = Faker()
    name = faker.word()
    description = faker.sentence()
    is_active = faker.boolean()

    @pytest.fixture
    def category(self) -> Category:
        return Category(
            name=self.name,
            description=self.description,
            is_active=self.is_active
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

    def test_when_category_does_not_exist_then_raise_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None
        use_case = DeleteCategory(repository=mock_repository)
        request = DeleteCategoryRequest(id=uuid4())

        with pytest.raises(CategoryNotFound) as exc_info:
            use_case.execute(request)

        assert str(exc_info.value) == f"Category with id {request.id} not found"

    def test_delete_category_from_repository_with_delete_method(
        self,
        mock_repository: CategoryRepository,
        category: Category
    ):
        use_case = DeleteCategory(mock_repository)
        use_case.execute(DeleteCategoryRequest(id=category.id))

        mock_repository.delete.assert_called_once_with(category.id)

    def test_should_DeleteCategory_not_call_repository_with_delete_method_if_raise_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None
        use_case = DeleteCategory(repository=mock_repository)
        request = DeleteCategoryRequest(id=uuid4())

        with pytest.raises(CategoryNotFound):
            use_case.execute(request)

        mock_repository.delete.assert_not_called()