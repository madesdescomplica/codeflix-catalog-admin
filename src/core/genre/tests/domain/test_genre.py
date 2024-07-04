from uuid import UUID, uuid4

from faker import Faker
import pytest

from src.core.genre.domain import Genre


class TestGenre:
    faker = Faker()
    genre_id = uuid4()
    name = faker.word()
    is_active = faker.boolean()
    categories = {uuid4(), uuid4()}

    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            Genre()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name can not be longer than 255 caracteres"):
            Genre(name=self.faker.sentence(nb_words=100))

    def test_can_not_create_genre_with_empty_name(self):
        with pytest.raises(ValueError, match="name can not be empty or null"):
            Genre(name="")

    def test_can_not_create_genre_with_null_name(self):
        with pytest.raises(ValueError, match="name can not be empty or null"):
            Genre(name=None)

    def test_genre_must_be_created_with_id_as_uuid4(self):
        genre = Genre(name=self.name)

        assert isinstance(genre.id, UUID)

    def test_created_genre_with_default_values(self):
        genre = Genre(name=self.name)

        assert genre.name == self.name
        assert genre.is_active is True
        assert isinstance(genre.id, UUID)
        assert genre.categories == set()

    def test_genre_is_created_with_provided_values(self):
        genre = Genre(
            id=self.genre_id,
            name=self.name,
            is_active=self.is_active,
            categories=self.categories,
        )

        assert genre.id == self.genre_id
        assert genre.name == self.name
        assert genre.is_active is self.is_active
        assert genre.categories == self.categories

    def test_the_response_of__str__method(self):
        genre = Genre(
            id=self.genre_id,
            name=self.name,
            is_active=self.is_active,
            categories=self.categories
        )

        assert str(genre) == f"id: {self.genre_id}, \
            name: {self.name}, \
            is_active: {self.is_active}, \
            categories: {self.categories}"


    def test_the_response_of__repr__method(self):
        genre = Genre(
            id=self.genre_id,
            name=self.name,
            categories=self.categories,
            is_active=self.is_active
        )

        assert genre.__repr__() == f"id: {self.genre_id}, \
            name: {self.name}, \
            is_active: {self.is_active}, \
            categories: {self.categories}"

class TestActivateGenre:
    faker = Faker()
    name = faker.word()
    categories = {uuid4(), uuid4()}

    def test_activate_inactive_genre(self):
        genre = Genre(
            name=self.name,
            categories=self.categories,
            is_active=False)

        genre.activate()

        assert genre.is_active is True

    def test_activate_active_genre(self):
        genre = Genre(
            name=self.name,
            categories=self.categories,
            is_active=True)

        genre.activate()

        assert genre.is_active is True

    def test_deactivate_inactive_genre(self):
        genre = Genre(
            name=self.name,
            categories=self.categories,
            is_active=False)

        genre.deactivate()

        assert genre.is_active is False

    def test_deactivate_active_genre(self):
        genre = Genre(
            name=self.name,
            categories=self.categories,
            is_active=True)

        genre.deactivate()

        assert genre.is_active is False

class TestEquality:
    faker = Faker()

    def test_when_genres_have_same_id_they_are_equal(self):
        genre_id = uuid4()
        genre1 = Genre(id=genre_id, name="genre1")
        genre2 = Genre(id=genre_id, name="genre1")

        assert genre1 == genre2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid4()
        genre = Genre(id=common_id, name=self.faker.word())
        dummy = Dummy()
        dummy.id = common_id

        assert genre != dummy

class TestChangeName:
    faker = Faker()
    name = faker.word()

    def test_change_name(self):
        updated_genre = self.faker.word()
        genre = Genre(name=self.name)

        genre.change_name(updated_genre)

        assert genre.name == updated_genre

    def test_change_name_with_empty_string(self):
        genre = Genre(name=self.name)

        with pytest.raises(ValueError, match="name can not be empty or null"):
            genre.change_name("")

class TestAddCategory:
    faker = Faker()
    name = faker.word()
    category_id = uuid4()
    categories = {uuid4(), uuid4()}

    def test_add_category_to_genre(self):
        genre = Genre(name=self.name)

        assert self.category_id not in genre.categories
        genre.add_category(self.category_id)
        assert self.category_id in genre.categories

    def test_can_add_multiple_categories(self):
        genre = Genre(name=self.name)
        category_1 = uuid4()
        category_2 = uuid4()

        genre.add_category(category_1)
        genre.add_category(category_2)

        assert category_1 in genre.categories
        assert category_2 in genre.categories
        assert len(genre.categories) == 2
        assert genre.categories == {category_1, category_2}

class TestRemoveCategory:
    faker = Faker()
    name = faker.word()
    category_id = uuid4()
    categories = {uuid4(), category_id}

    def test_remove_category_from_genre(self):
        genre = Genre(name=self.name, categories=self.categories)

        assert self.category_id in genre.categories
        genre.remove_category(self.category_id)
        assert self.category_id not in genre.categories