from inspect import isabstract
from unittest.mock import patch
from uuid import uuid4

from faker import Faker
import pytest

from src.core.category.domain import Category, CategoryRepository


class TestCategoryRepository:
    faker = Faker()

    @pytest.fixture
    def category(self) -> Category:
        return Category(
            id=uuid4(),
            name=self.faker.word(),
            description=self.faker.sentence(),
            is_active=True
        )

    @pytest.fixture
    @patch.multiple(CategoryRepository, __abstractmethods__=set())
    def category_repository(self) -> CategoryRepository:
        return CategoryRepository()


    def test_should_CategoryRepository_is_an_abstract_class(self):
        assert isabstract(CategoryRepository)

    def test_should_CategoryRepository_raise_a_NotImplementedError_if_save_method_is_not_implemented(
        self,
        category_repository: CategoryRepository,
        category: Category
    ):
        with pytest.raises(NotImplementedError, match='Should implement method: save'):
            category_repository.save(category)

    def test_should_CategoryRepository_raise_a_NotImplementedError_if_get_by_id_method_is_not_implemented(
        self,
        category_repository: CategoryRepository,
        category: Category
    ):
        with pytest.raises(NotImplementedError, match='Should implement method: get_by_id'):
            category_repository.get_by_id(category.id)

    def test_should_CategoryRepository_raise_a_NotImplementedError_if_update_method_is_not_implemented(
        self,
        category_repository: CategoryRepository,
        category: Category
    ):
        with pytest.raises(NotImplementedError, match='Should implement method: update'):
            category_repository.update(category)

    def test_should_CategoryRepository_raise_a_NotImplementedError_if_delete_method_is_not_implemented(
        self,
        category_repository: CategoryRepository,
        category: Category
    ):
        with pytest.raises(NotImplementedError, match='Should implement method: delete'):
            category_repository.delete(category.id)

    def test_should_CategoryRepository_raise_a_NotImplementedError_if_list_method_is_not_implemented(
        self,
        category_repository: CategoryRepository
    ):
        with pytest.raises(NotImplementedError, match='Should implement method: list'):
            category_repository.list()
