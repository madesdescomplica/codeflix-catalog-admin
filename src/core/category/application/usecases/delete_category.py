from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain import CategoryRepository
from ..exceptions import CategoryNotFound

@dataclass
class DeleteCategoryRequest:
    id: UUID

@dataclass
class DeleteCategory:
    repository: CategoryRepository

    def execute(self, request: DeleteCategoryRequest) -> None:
        category = self.repository.get_by_id(request.id)

        if category is None:
            raise CategoryNotFound(f"Category with id {request.id} not found")

        self.repository.delete(category.id)