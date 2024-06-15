from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain import CategoryRepository


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


@dataclass
class UpdateCategory:
    repository: CategoryRepository

    def execute(self, request: UpdateCategoryRequest) -> None:
        self.repository.get_by_id(request.id)
