from unittest.mock import MagicMock, create_autospec
from uuid import uuid4

from faker import Faker
import pytest

from src.core.category.application import (
    CategoryNotFound,
    GetCategory,
    GetCategoryRequest
)
from src.core.category.domain import Category, CategoryRepository


class TestGetCategory:
    faker = Faker()
    id = uuid4()
    name = faker.word()
    description = faker.sentence()

    def test_get_category_call_repository(self):
        mock_category = Category(
            id=self.id,
            name=self.name,
            description=self.description,
            is_active=True
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = mock_category
        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=mock_category.id)

        use_case.execute(request)

        assert mock_repository.get_by_id.called is True

    def test_when_category_does_not_exist_then_raise_exception(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None
        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=self.id)

        with pytest.raises(CategoryNotFound) as exc_info:
            use_case.execute(request)

        assert str(exc_info.value) == f"Category with id {request.id} not found"

    def test_when_category_exists_then_return_response_dto(self):
        mock_category = Category(
            id=self.id,
            name=self.name,
            description=self.description,
            is_active=True
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = mock_category
        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=mock_category.id)

        response = use_case.execute(request)

        assert response.id == mock_category.id
        assert response.name == mock_category.name
        assert response.description == mock_category.description
        assert response.is_active == mock_category.is_active