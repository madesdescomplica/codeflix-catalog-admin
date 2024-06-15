from dataclasses import dataclass

from src.core.category.domain import Category, CategoryRepository


@dataclass
class ListCategoryResponse:
    data: list[Category]

@dataclass
class ListCategory:
    repository: CategoryRepository

    def execute(self) -> ListCategoryResponse:
        categories = self.repository.list()

        return ListCategoryResponse(data=[
            Category(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active
            )
            for category in categories
        ])