from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain import CategoryRepository
from .exceptions import CategoryNotFound


@dataclass
class GetCategoryRequest:
    id: UUID

@dataclass
class GetCategoryResponse:
    id: UUID
    name: str
    description: str
    is_active: bool

@dataclass
class GetCategory:
    repository: CategoryRepository

    def execute(self, request: GetCategoryRequest) -> GetCategoryResponse:
        category = self.repository.get_by_id(request.id)

        if category is None:
            raise CategoryNotFound(f"Category with id {request.id} not found")

        return GetCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )