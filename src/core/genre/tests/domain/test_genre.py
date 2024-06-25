from uuid import UUID, uuid4

from faker import Faker
import pytest

from src.core.genre.domain import Genre


class TestGenre:
    faker = Faker()
    category_id = uuid4()
    name = faker.word()
    description = faker.sentence()
    is_active = faker.boolean()

    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Genre()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name can not be longer than 255 caracteres"):
            Genre(name=self.faker.sentence(nb_words=100))

    def test_created_category_with_default_values(self):
        genre = Genre(name=self.name)

        assert genre.name == self.name
        assert genre.is_active is True
        assert isinstance(genre.id, UUID)
        assert genre.categories == set()

    def test_category_is_created_with_provided_values(self):
        category = Genre(
            id=self.category_id,
            name=self.name,
            description=self.description,
            is_active=self.is_active
        )

        assert category.id == self.category_id
        assert category.name == self.name
        assert category.description == self.description
        assert category.is_active is self.is_active

    def test_can_not_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name can not be empty or null"):
            Genre(name="")

    def test_can_not_create_category_with_null_name(self):
        with pytest.raises(ValueError, match="name can not be empty or null"):
            Genre(name=None)

    def test_the_response_of__str__method(self):
        category = Genre(
            id=self.category_id,
            name=self.name,
            description=self.description,
            is_active=self.is_active
        )

        assert str(category) == f"id: {self.category_id}, \
            name: {self.name}, \
            description: {self.description}, \
            is_active: {self.is_active}"


    def test_the_response_of__repr__method(self):
        category = Genre(
            id=self.category_id,
            name=self.name,
            description=self.description,
            is_active=self.is_active
        )

        assert category.__repr__() == f"id: {self.category_id}, \
            name: {self.name}, \
            description: {self.description}, \
            is_active: {self.is_active}"

class TestUpdateCategory:
    faker = Faker()
    name = faker.word()
    description = faker.sentence()

    def test_update_category_with_name_and_description(self):
        updated_name = self.faker.word()
        updated_description = self.faker.sentence()
        category = Genre(name=self.name, description=self.description)

        category.update_Genre(name=updated_name, description=updated_description)

        assert category.name == updated_name
        assert category.description == updated_description

    def test_update_category_with_invalid_name(self):
        category = Genre(name=self.name, description=self.description)

        with pytest.raises(ValueError, match="name can not be longer than 255 caracteres"):
            category.update_Genre(
                name=self.faker.sentence(nb_words=100),
                description=self.faker.sentence()
            )

    def test_can_not_update_category_with_empty_name(self):
        category = Genre(name=self.name, description=self.description)

        with pytest.raises(ValueError, match="name can not be empty or null"):
            category.update_Genre(
                name="",
                description=self.faker.sentence()
            )

    def test_can_not_update_category_with_null_name(self):
        category = Genre(name=self.name, description=self.description)

        with pytest.raises(ValueError, match="name can not be empty or null"):
            category.update_Genre(
                name=None,
                description=self.faker.sentence()
            )

class TestActivateCategory:
    faker = Faker()
    name = faker.word()
    description = faker.sentence()

    def test_activate_inactive_Genre(self):
        category = Genre(
            name=self.name,
            description=self.description,
            is_active=False)

        category.activate()

        assert category.is_active is True

    def test_activate_active_Genre(self):
        category = Genre(
            name=self.name,
            description=self.description,
            is_active=True)

        category.activate()

        assert category.is_active is True

    def test_deactivate_inactive_Genre(self):
        category = Genre(
            name=self.name,
            description=self.description,
            is_active=False)

        category.deactivate()

        assert category.is_active is False

    def test_deactivate_active_Genre(self):
        category = Genre(
            name=self.name,
            description=self.description,
            is_active=True)

        category.deactivate()

        assert category.is_active is False

class TestEquality:
    faker = Faker()

    def test_when_categories_have_same_id_they_are_equal(self):
        category_id = uuid4()
        category1 = Genre(id=category_id, name="category1")
        category2 = Genre(id=category_id, name="category1")

        assert category1 == category2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid4()
        category = Genre(id=common_id, name=self.faker.word())
        dummy = Dummy()
        dummy.id = common_id

        assert category != dummy
