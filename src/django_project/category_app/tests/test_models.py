from uuid import UUID

from django.forms import ValidationError
from django.test import TestCase

from django_project.category_app.models import Category

class TestCategoryModel(TestCase):
    def test_create_category(self):
        # Test creating a Category instance
        category = Category.objects.create(
            name="Movies",
            description="A category for movies",
            is_active=True
        )
        self.assertIsInstance(category, Category)
        self.assertEqual(category.name, "Movies")
        self.assertEqual(category.description, "A category for movies")
        self.assertTrue(category.is_active)
        self.assertIsInstance(category.id, UUID)

    def test_category_str(self):
        # Test the __str__ method
        category = Category(name="Books")
        self.assertEqual(str(category), "Books")

    def test_default_is_active(self):
        # Test default value of is_active
        category = Category.objects.create(name="Music")
        self.assertTrue(category.is_active)

    def test_name_max_length(self):
    # Create a Category instance with a name exceeding the max length
        category = Category(name='x' * 256)  # Assuming max_length=255
        # Assert that a ValidationError is raised during full_clean
        with self.assertRaises(ValidationError):
            category.full_clean()