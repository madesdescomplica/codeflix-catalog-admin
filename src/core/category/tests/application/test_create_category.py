from unittest.mock import MagicMock
from uuid import UUID

from faker import Faker
import pytest

from src.core.category.application.exceptions import InvalidCategory
from src.core.category.application.usecases import (
    CreateCategory,
    CreateCategoryRequest,
)
from src.core.category.domain import CategoryRepository


class TestCreateCategory:
    faker = Faker()
    name=faker.word()
    description=faker.sentence()

    @pytest.fixture
    def mock_repository(self) -> CategoryRepository:
        return MagicMock(CategoryRepository)

    def test_create_category_with_valid_data(self, mock_repository: CategoryRepository):
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(
            name=self.name,
            description=self.description,
            is_active=True  # default
        )

        category_id = use_case.execute(request)

        assert category_id is not None
        assert isinstance(category_id, UUID)

    def test_create_category_with_invalid_data(self, mock_repository: CategoryRepository):
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(name="")

        with pytest.raises(InvalidCategory, match="name can not be empty or null") as exc_info:
            use_case.execute(request)

        assert exc_info.type is InvalidCategory
        assert str(exc_info.value) == "name can not be empty or null"

    def test_create_category_call_repository(self, mock_repository: CategoryRepository):
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(
            name=self.name,
            description=self.description,
            is_active=True  # default
        )

        use_case.execute(request)

        assert mock_repository.save.called is True

    def test_create_category_do_not_call_repository_with_invalid_data(
        self,
        mock_repository: CategoryRepository
    ):
        use_case = CreateCategory(repository=mock_repository)
        request = CreateCategoryRequest(name="")

        with pytest.raises(InvalidCategory, match="name can not be empty or null") as exc_info:
            use_case.execute(request)

        assert exc_info.type is InvalidCategory
        assert str(exc_info.value) == "name can not be empty or null"
        assert mock_repository.save.called is False