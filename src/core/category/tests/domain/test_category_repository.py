from inspect import isabstract
from unittest.mock import patch

from faker import Faker
import pytest

from src.core.category.domain import Category, CategoryRepository


class TestCategoryRepository:
    faker = Faker()
    name=faker.word(),
    description=faker.sentence()

    def test_should_CategoryRepository_is_an_abstract_class(self):
        assert isabstract(CategoryRepository)

    @patch.multiple(CategoryRepository, __abstractmethods__=set())
    def test_should_CategoryRepository_raise_a_NotImplementedError_if_save_method_is_not_implemented(self):
        category = Category(name=self.name, description=self.description)
        category_repository = CategoryRepository()

        with pytest.raises(NotImplementedError, match='Should implement method: save'):
            category_repository.save(category)

    @patch.multiple(CategoryRepository, __abstractmethods__=set())
    def test_should_CategoryRepository_raise_a_NotImplementedError_if_get_by_id_method_is_not_implemented(self):
        category = Category(name=self.name, description=self.description)
        category_repository = CategoryRepository()

        with pytest.raises(NotImplementedError, match='Should implement method: get_by_id'):
            category_repository.get_by_id(category.id)

    @patch.multiple(CategoryRepository, __abstractmethods__=set())
    def test_should_CategoryRepository_raise_a_NotImplementedError_if_update_method_is_not_implemented(self):
        category = Category(name=self.name, description=self.description)
        category_repository = CategoryRepository()

        with pytest.raises(NotImplementedError, match='Should implement method: update'):
            category_repository.update(category)
