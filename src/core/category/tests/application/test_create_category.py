from uuid import UUID

from faker import Faker
import pytest

from src.core.category.application import create_category, InvalidCategoryData


class TestCreateCategory:
    faker = Faker()

    def test_create_category_with_valid_data(self):
        category_id = create_category(
            name=self.faker.word(),
            description=self.faker.sentence(),
            is_active=True  # default
        )

        assert category_id is not None
        assert isinstance(category_id, UUID)

    def test_create_category_with_invalid_data(self):
        with pytest.raises(InvalidCategoryData, match="name can not be empty or null") as exc_info:
            create_category(name="")

        assert exc_info.type is InvalidCategoryData
        assert str(exc_info.value) == "name can not be empty or null"
