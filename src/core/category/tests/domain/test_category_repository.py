from inspect import isabstract
from unittest.mock import patch

from faker import Faker
import pytest

from src.core.category.domain import Category, CategoryRepository


class TestCategoryRepository:
    faker = Faker()

    def test_should_CategoryRepository_is_an_abstract_class(self):
        assert isabstract(CategoryRepository)

    @patch.multiple(CategoryRepository, __abstractmethods__=set())
    def test_should_CategoryRepository_raise_a_NotImplementedError_if_not_implemented(self):
        category = Category(name=self.faker.word(), description=self.faker.sentence())
        category_repository = CategoryRepository()

        with pytest.raises(NotImplementedError, match='Should implement method: save'):
            category_repository.save(category)
