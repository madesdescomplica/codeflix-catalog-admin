from unittest.mock import MagicMock, create_autospec
from uuid import uuid4

from faker import Faker
import pytest

from src.core.category.application.exceptions import CategoryNotFound
from src.core.category.application.usecases import GetCategory, GetCategoryRequest
from src.core.category.domain import Category, CategoryRepository


class TestGetCategory:
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

    def test_get_category_call_repository(
        self,
        mock_repository: CategoryRepository,
        category: Category
    ):
        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=category.id)

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

    def test_when_category_exists_then_return_response_dto(
        self,
        mock_repository: CategoryRepository,
        category: Category
    ):
        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryRequest(id=category.id)

        response = use_case.execute(request)

        assert response.id == category.id
        assert response.name == category.name
        assert response.description == category.description
        assert response.is_active == category.is_active
