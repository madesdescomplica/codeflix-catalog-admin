from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain import Category, CategoryRepository
from .models import Category as CategoryModel


@dataclass
class DjangoORMCategoryRepository(CategoryRepository):
    category_model: type[CategoryModel] = CategoryModel

    def save(self, category: Category) -> None:
        self.category_model.objects.create(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category = self.category_model.objects.get(id=id)
            return Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active
            )
        except self.category_model.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        self.category_model.objects.filter(id=id).delete()

    def update(self, category: Category) -> None:
        self.category_model.objects.filter(id=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )

    def list(self) -> list[Category]:
        categories = self.category_model.objects.all()
        return [
            Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active
            ) for category in categories
        ]