from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain import Category, CategoryRepository
from ..exceptions import InvalidCategory


@dataclass
class CreateCategoryRequest:
    name: str
    description: str = ""
    is_active: bool = True

@dataclass
class CreateCategoryResponse:
    id: UUID

@dataclass
class CreateCategory:
    repository: CategoryRepository

    def execute(self, request: CreateCategoryRequest) -> CreateCategoryResponse:
        try:
            category = Category(
                name=request.name,
                description=request.description,
                is_active=request.is_active
            )
        except ValueError as e:
            raise InvalidCategory(e)

        self.repository.save(category)
        return CreateCategoryResponse(category.id)
